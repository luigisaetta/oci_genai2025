"""
Test the Langchain wrapper for Embeddings
"""

from time import time
import numpy as np
from oci_aqua_embeddings import OCIAquaEmbeddings

# TODO move in a config file
BASE_URL = "https://modeldeployment.eu-frankfurt-1.oci.customer-oci.com"
ENDPOINT = f"{BASE_URL}/ocid1.datasciencemodeldeployment.oc1.eu-frankfurt-1.amaaaaaa2xxap7yagq4z62toy5toj6fijrzi6deswanqy2l3yik7mmifix2a/predict"

time_start = time()

embed_model = OCIAquaEmbeddings(endpoint=ENDPOINT)

texts = ["Hello world", "Ciao mondo"]

vet_embed = embed_model.embed_documents(texts)
np_embed = np.array(vet_embed)
time_elapsed = time() - time_start

print("")
print("Vector embeddings shape:", np_embed.shape)
print("Time elapsed (sec.):", round(time_elapsed, 1))
print("")
