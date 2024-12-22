import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI  # Fixed import for ChatOpenAI

# Step 1: Load Documents
loader = DirectoryLoader(
    "extracted_tools/",  # Directory containing your text files
    glob="**/*.txt",  # Glob pattern to match files
    show_progress=True,  # Show progress while loading documents
    use_multithreading=True,  # Use multithreading for faster loading
    loader_cls=TextLoader  # Use TextLoader as the default loader for files
)
docs = loader.load()

print(f"Loaded {len(docs)} documents.")

# Step 2: Split Text into Chunks for Better Processing
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Size of each chunk
    chunk_overlap=100  # Overlap between chunks
)
split_docs = text_splitter.split_documents(docs)  # Split the documents into smaller chunks

print(f"Split {len(docs)} documents into {len(split_docs)} chunks.")

# Step 3: Embed the Documents
# Embeddings will allow the documents to be searched effectively in a vector space
embedding_model = OpenAIEmbeddings()  # Replace with your embedding model (e.g., OpenAI, HuggingFace)
docsearch = FAISS.from_documents(split_docs, embedding_model)  # Store document chunks in a FAISS vector store

print("Documents embedded and stored in FAISS vector store.")

# Step 4: Create a Retriever
retriever = docsearch.as_retriever()  # Convert the FAISS vector store into a retriever

print("Retriever created.")

# Step 5: Initialize Language Model and Build Retrieval-Augmented QA Chain
# Using the updated version of ChatOpenAI with langchain-openai package
chat_model = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="google/gemini-pro-1.5"
)
qa_chain = RetrievalQA.from_chain_type(llm=chat_model, retriever=retriever)

print("QA Chain initialized.")

# Step 6: Query the System
query = "Based on the extracted documents from the directory, please summarize the purpose of all the tools described"
result = qa_chain.invoke({'query': query})  # Use the correct key "query"
print(result['output'])  # Print the generated answer