"""
Test the Langchain wrapper for Embeddings

this one contains a complete process
    - load a PDF
    - split it into chunks
    - embed the chunks
    - load the embeddings into a vector store
"""

from time import time
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from oci_aqua_embeddings import OCIAquaEmbeddings

PDF_FILE = "alice_adventures_in_wonderland.pdf"
BASE_URL = "https://modeldeployment.eu-frankfurt-1.oci.customer-oci.com"
ENDPOINT = f"{BASE_URL}/ocid1.datasciencemodeldeployment.oc1.eu-frankfurt-1.amaaaaaa2xxap7yagq4z62toy5toj6fijrzi6deswanqy2l3yik7mmifix2a/predict"

time_start = time()

embed_model = OCIAquaEmbeddings(endpoint=ENDPOINT)

loader = PyPDFLoader(PDF_FILE)

# Load and parse the PDF
documents = loader.load()

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=3000,  # Specify the chunk size
    chunk_overlap=100,  # Specify overlap between chunks
)

chunks = text_splitter.split_documents(documents)
print("Loaded n. chunks: ", len(chunks))

print("Embedding and loading vector store...")
vectorstore = FAISS.from_documents(chunks, embed_model)

time_elapsed = time() - time_start

print("")
print("Time elapsed (sec.):", round(time_elapsed, 1))
print("")
