import streamlit as st
from extract_pnl_data import extract_all_data_from_pdf
from embed_pnl_data import embed_and_store_data
from rag_qa import query_pnl_data

def main():
    st.title("Financial Data QA Bot")

    # File upload section
    uploaded_file = st.file_uploader("Upload your P&L PDF", type="pdf")
    
    if uploaded_file is not None:
        try:
            # Extract data from uploaded PDF
            all_tables, all_text_data, financial_data = extract_all_data_from_pdf(uploaded_file)

            # Embed and store the data in Pinecone
            embed_and_store_data(uploaded_file)  # This should now work after fixing Pinecone authentication
            st.success("Data successfully embedded into Pinecone!")

        except Exception as e:
            # Handle any errors (including Pinecone issues)
            st.error(f"Error: {e}")

        # Query input section
        query = st.text_input("Ask a financial question ")

        if query:
            try:
                answer = query_pnl_data(query)  # Query Pinecone and generate an answer
                st.write("Answer:", answer)
            except Exception as e:
                st.error(f"Error querying Pinecone: {e}")

if __name__ == "__main__":
    main()
