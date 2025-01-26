# Financial Data QA Bot

This project allows you to upload financial statement PDFs, extract data (tables and text), and perform natural language querying using advanced embedding and retrieval techniques. The system integrates Pinecone for vector storage and Gemini AI for question answering.

## Features
- Extract financial data from PDFs (tables and text).
- Embed data using SentenceTransformer (`paraphrase-MiniLM-L6-v2`).
- Store embeddings in Pinecone.
- Perform natural language queries on the financial data.
- Use Gemini AI to provide accurate answers based on retrieved data.

## Requirements
Ensure the following are installed:

- Python 3.8+
- Streamlit
- SentenceTransformers
- Pinecone
- pdfplumber
- Camelot
- pandas
- tabulate

## Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Pinecone:**
   - Create an account at [Pinecone](https://www.pinecone.io/).
   - Retrieve your Pinecone API key and environment.
   - Replace `Your_pinecone_api` in the code with your actual Pinecone API key.

4. **Set Up Gemini AI:**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to generate your Gemini API key.
   - Replace `Your_Api_Key` in the code with your actual Gemini API key.

## Usage

### Running the Application
1. **Start the Streamlit App:**
   ```bash
   streamlit run app.py
   ```

2. **Upload a PDF:**
   - Upload your financial statement PDF through the app interface.

3. **Ask Questions:**
   - Enter financial questions, such as:
     - "What is the gross profit for the latest quarter?"
     - "What are the operating expenses?"
     - "What is the total revenue?"

4. **View Results:**
   - The app retrieves relevant data from Pinecone and generates an answer using Gemini AI.

## File Structure

```
.
├── app.py                  # Streamlit application entry point
├── extract_pnl_data.py     # PDF data extraction logic
├── embed_pnl_data.py       # Embedding and Pinecone storage logic
├── rag_qa.py               # Retrieval and Gemini API querying logic
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Deployment

1. **Local Deployment:**
   - Follow the "Running the Application" steps above.

2. **Cloud Deployment:**
   - Use platforms like AWS, Google Cloud, or Heroku to deploy your app.
   - Ensure environment variables for Pinecone and Gemini API keys are properly configured.

3. **Docker Deployment (Optional):**
   - Create a `Dockerfile` to containerize the application.
   - Build and run the Docker image:
     ```bash
     docker build -t financial-qa-bot .
     docker run -p 8501:8501 financial-qa-bot
     ```

## Examples of Queries
- "What is the net income for 2023?"
- "List the operating expenses for Q4."
- "Provide total assets reported."

## Troubleshooting
- Ensure API keys are correct and active.
- Check Pinecone and Gemini usage limits.
- Verify that the uploaded PDF has readable text and tables.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- [Streamlit](https://streamlit.io/)
- [SentenceTransformers](https://www.sbert.net/)
- [Pinecone](https://www.pinecone.io/)
- [Gemini AI](https://aistudio.google.com/app/apikey)

