import camelot
import pdfplumber
import pandas as pd
import re
from tabulate import tabulate

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

# Function to save tables, text, and financial data to a text file
# Function to save tables, text, and financial data to a text file
def save_data_to_text_file(all_tables, all_text_data, financial_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:  # Set encoding to UTF-8
        # Save extracted tables data
        file.write("Extracted Tables Data:\n")
        for table in all_tables:
            file.write(f"\nData from Page {table['page']} (Table):\n")
            if table['table']:  # Check if there is valid table data
                try:
                    df = pd.DataFrame(table['table'][1:], columns=table['table'][0])  # Convert to DataFrame
                    file.write(tabulate(df, headers='keys', tablefmt='grid') + "\n")  # Save as grid formatted table
                except Exception as e:
                    file.write(f"Error processing table on Page {table['page']}: {e}\n")
            else:
                file.write("No valid data found in this table.\n")

        # Save extracted text data
        file.write("\n\nExtracted Text Data:\n")
        for page in all_text_data:
            file.write(f"--- Page {page['page']} ---\n")
            file.write(page['text'][:500] + "\n")  # Preview first 500 chars for readability

        # Save extracted financial data
        file.write("\n\nExtracted Financial Data:\n")
        for key, value in financial_data.items():
            file.write(f"{key}: {value}\n")


# Example usage
pdf_path = 'Sample Financial Statement.pdf'  # Replace with the actual path to your PDF
output_file = 'extracted_data.txt'  # The file where data will be saved

# Extract all tables, text, and financial data
all_tables, all_text_data, financial_data = extract_all_data_from_pdf(pdf_path)

# Save the extracted data into a text file
save_data_to_text_file(all_tables, all_text_data, financial_data, output_file)

print(f"Extracted data saved to {output_file}")
