import os
import pinecone
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import pdfplumber
import camelot
import pandas as pd
from tabulate import tabulate
import re

# Initialize Pinecone using the new API
pc = Pinecone(api_key='Your_pinecone_api')

# Initialize the model for embedding
embedder = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Connect to Pinecone index (if not created, create one)
index_name = "pnl-data"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  # 384 for MiniLM-L6-v2 embeddings
        metric='cosine',  # Use cosine similarity for embeddings
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'  # Use the region that matches your setup
        )
    )

# Connect to the Pinecone index
index = pc.Index(index_name)

# Function to extract all data (tables and text) from the PDF using Camelot and pdfplumber
def extract_all_data_from_pdf(pdf_path):
    all_tables = []
    all_text_data = []
    financial_data = {}

    # Using pdfplumber to extract raw text
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            # Extracting text content from the page
            page_text = page.extract_text()
            all_text_data.append({
                'page': page_num + 1,
                'text': page_text
            })

            # Extract financial data using regex from the page text
            financial_data.update(extract_financial_data_from_text(page_text))

    # Using Camelot to extract tables
    tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')  # Use 'stream' for continuous tables, 'lattice' for structured ones
    for table in tables:
        cleaned_table = clean_table_data(table)
        if cleaned_table:
            all_tables.append({
                'page': table.page,
                'table': cleaned_table
            })

    return all_tables, all_text_data, financial_data

# Function to clean and structure table data
def clean_table_data(table):
    # Remove rows and columns that are completely empty
    cleaned_table = table.df.dropna(how='all', axis=0)  # Drop empty rows
    cleaned_table = cleaned_table.dropna(how='all', axis=1)  # Drop empty columns
    return cleaned_table.values.tolist() if not cleaned_table.empty else []

# Function to extract financial data using regex from page text
def extract_financial_data_from_text(text):
    patterns = {
        "Revenue": r"(Revenue|Sales)[\s\W]+([\d,]+(?:\.\d+)?)",
        "Net Income": r"(Net\s*Income|Profit)[\s\W]+([\d,]+(?:\.\d+)?)",
        "Gross Profit": r"(Gross\s*Profit)[\s\W]+([\d,]+(?:\.\d+)?)",
        "Operating Expenses": r"(Operating\s*Expenses)[\s\W]+([\d,]+(?:\.\d+)?)",
        "Total Assets": r"(Total\s*Assets)[\s\W]+([\d,]+(?:\.\d+)?)"
    }

    extracted_data = {}

    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            extracted_data[key] = match.group(2)

    return extracted_data

# Function to embed and store data in Pinecone
def embed_and_store_data(pdf_path):
    """
    Extracts P&L data from a PDF, embeds it, and stores it in Pinecone.
    """
    # Extract all data from the uploaded PDF (tables, text, and financial data)
    all_tables, all_text_data, financial_data = extract_all_data_from_pdf(pdf_path)
    
    # Process tables: Assuming you are using the first table for embedding (if there are multiple)
    if all_tables:
        pnl_df = pd.DataFrame(all_tables[0]['table'][1:], columns=all_tables[0]['table'][0])  # Convert first table to DataFrame
    else:
        pnl_df = pd.DataFrame()  # If no tables are found, create an empty DataFrame
    
    # Flatten the P&L table into rows and text
    data = pnl_df.to_dict(orient='records')
    texts = [f"{row}" for row in data]
    
    # Generate embeddings for each row of table data
    embeddings = embedder.encode(texts)
    
    # Store the embeddings for the table rows in Pinecone
    for i, embedding in enumerate(embeddings):
        index.upsert([(str(i), embedding, {"text": texts[i]})])
    
    # Extract and embed all text data from PDF (including non-table content)
    text_data = [page['text'] for page in all_text_data if page['text']]
    
    # Generate embeddings for each page of text
    text_embeddings = embedder.encode(text_data)
    
    # Store the embeddings for the text content in Pinecone
    for i, embedding in enumerate(text_embeddings):
        index.upsert([(f"text_{i}", embedding, {"text": text_data[i]})])

# Example usage:
pdf_path = 'Sample Financial Statement.pdf'  # Replace with actual path to the P&L PDF
embed_and_store_data(pdf_path)
print("Data embedded and stored in Pinecone.")
