import pinecone
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# Initialize Pinecone using the new method
from pinecone import Pinecone, ServerlessSpec

# Replace your Pinecone API key
pc = Pinecone(api_key="Your_pinecone_api")

# Specify the index name
index_name = "pnl-data"

# Connect to Pinecone index (or create if not exists)
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  # Adjust to the dimension of your embeddings (384 for MiniLM-L6-v2)
        metric='cosine',  # You can change the metric depending on your use case
        spec=ServerlessSpec(
            cloud='aws',  # Choose cloud provider
            region='us-east-1'  # Select region
        )
    )

index = pc.Index(index_name)

# Initialize the model for embedding
embedder = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Configure the Gemini API
genai.configure(api_key="Your_Api_Key")
model = genai.GenerativeModel("gemini-1.5-flash")

def query_gemini_api(prompt):
    """
    Queries the Gemini API to generate a response for the given prompt.
    """
    response = model.generate_content(prompt)
    return response.text.strip()

def query_pnl_data(query):
    """
    Retrieve relevant rows from Pinecone and generate an answer using Gemini API.
    """
    # Embed the user's query
    query_embedding = embedder.encode([query])

    # Convert the query_embedding (which is a NumPy ndarray) to a list
    query_embedding_list = query_embedding[0].tolist()

    # Retrieve similar documents from Pinecone using keyword arguments
    result = index.query(vector=query_embedding_list, top_k=3, include_metadata=True)

    # Combine the text of the top results
    retrieved_text = "\n".join([match['metadata']['text'] for match in result['matches']])

    # Prepare prompt for Gemini API
    prompt = f"Answer the following financial question based on the provided data:\n\n{retrieved_text}\n\nQuestion: {query}\nAnswer:"
    
    # Get the answer from Gemini API
    answer = query_gemini_api(prompt)
    
    return answer
