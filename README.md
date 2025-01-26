Financial Data QA Bot
This repository contains the implementation of a Financial Data QA Bot that processes Profit & Loss (P&L) statements in PDF format, embeds extracted data into Pinecone for efficient retrieval, and answers financial queries using the Gemini Generative AI API.

Features
PDF Data Extraction: Extracts tables and text from uploaded PDFs using camelot and pdfplumber.
Embeddings: Converts extracted data into vector embeddings using SentenceTransformer.
Pinecone Storage: Stores vector embeddings in Pinecone for similarity-based search and retrieval.
Generative QA: Queries the Gemini Generative AI API to generate context-aware answers to user questions.
Streamlit Interface: A user-friendly Streamlit app for uploading PDFs, asking financial questions, and retrieving results.
Prerequisites
Ensure the following tools and APIs are set up:

Python 3.8+
Pinecone API Key (create one at pinecone.io)
Gemini Generative AI API Key (create one at Google Generative AI)
Streamlit installed locally for running the application.
Installation
Clone the Repository

bash
Copy
Edit
git clone https://github.com/your-username/financial-qa-bot.git
cd financial-qa-bot
Install Dependencies Install all required Python libraries:

bash
Copy
Edit
pip install -r requirements.txt
Set API Keys Update the following placeholders in the main.py file with your API keys:

Your_pinecone_api
Your_Api_Key
Run the Streamlit App

bash
Copy
Edit
streamlit run main.py
Deployment
Deploy Locally
Run the Application Locally:

bash
Copy
Edit
streamlit run main.py
Visit the URL (e.g., http://localhost:8501) to interact with the app.

Test the Bot:

Upload a sample P&L PDF.
Ask questions like:
"What is the net income for Q4 2024?"
"How do the operating expenses compare between Q2 2023 and Q3 2023?"
Deploy on a Server (e.g., AWS/Google Cloud/Heroku)
Set up a Python Environment:

Use a virtual environment (e.g., venv or conda) on your server.
Install dependencies using pip install -r requirements.txt.
Expose Streamlit App:

Open the port where Streamlit is running (8501 by default).
Use a reverse proxy (e.g., Nginx) or cloud deployment tools for external access.
Dockerize the Application (Optional):

Create a Dockerfile to containerize the app:
dockerfile
Copy
Edit
FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
Build and run the Docker container:
bash
Copy
Edit
docker build -t financial-qa-bot .
docker run -p 8501:8501 financial-qa-bot
Cloud Deployment:

AWS EC2: Deploy the app on an EC2 instance and open port 8501.
Google Cloud Run: Upload your container image for serverless deployment.
Heroku: Use streamlit buildpacks for Heroku deployment.
Directory Structure
plaintext
Copy
Edit
financial-qa-bot/
├── main.py                  # Streamlit app entry point
├── extract_pnl_data.py      # PDF extraction functions
├── embed_pnl_data.py        # Pinecone embedding storage
├── rag_qa.py                # Retrieval and QA functions
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
Key Python Libraries Used
Streamlit: For building the user interface.
Pinecone: For vector database and embedding storage.
Sentence Transformers: For generating vector embeddings.
Camelot: For extracting structured tables from PDFs.
PDFPlumber: For extracting unstructured text from PDFs.
Google Generative AI (Gemini): For generating query responses.
Example Queries
Revenue Query:

Question: "What is the revenue for the latest quarter?"
Response: Data from the table or text containing "Revenue".
Expense Comparison:

Question: "How do the operating expenses for Q2 2023 compare to Q3 2023?"
Response: A detailed comparison from the extracted financial data.
Net Income Change:

Question: "How has net income changed year-over-year?"
Response: Summarized year-over-year net income details.
Future Enhancements
Add multi-language support for global financial documents.
Enhance data visualization using matplotlib or plotly.
Support other document types (e.g., Word, Excel).
License
This project is licensed under the MIT License. See the LICENSE file for details.
