"""
Langchain wrapper for an Embeddings model deployed in Aqua
"""

import requests
from tqdm import tqdm

# we're using OCI ads to setup security and signing of requests
from ads import set_auth
from ads.common.auth import default_signer
from langchain.embeddings.base import Embeddings


# in secs
TIMEOUT = 60
# max limit of rows to process in a single batch
# consider that max_token is 32K
MAX_ROWS = 20


class OCIAquaEmbeddings(Embeddings):
    """
    Wrap an embedding model deployed in OCI Aqua in LangChain
    """

    def __init__(self, endpoint: str, **kwargs):
        """
        Initialize the embedding model.
        :param endpoint: the model deployment endpoint.
        :param kwargs: Additional parameters for the model initialization.
        """
        # Auth
        set_auth(auth="api_key", oci_config_location="~/.oci/config", profile="DEFAULT")
        self.auth = default_signer()["signer"]

        self.endpoint = endpoint
        self.kwargs = kwargs

    def create_payload(self, texts: list):
        """
        Create JSON payload to invoke the model.

        :param texts: List of texts to embed.
        :return: JSON payload.
        """
        return {"model": "odsc-llm", "input": texts}

    def send_request(self, endpoint, payload, auth):
        """
        send a POST request to the model deployment.

        :param endpoint: the model deployment endpoint.
        :param payload: the JSON payload to send.
        :param auth: the authentication object.
        :return: the response from the model.
        """
        try:
            response = requests.post(endpoint, json=payload, auth=auth, timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error in model invocation: {e}") from e

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """
        Embed a list of documents into vectors.
        :param texts: List of texts to embed.
        :return: List of embedding vectors.
        """

        # Call the embedding model and return embeddings
        def batchify(data, batch_size):
            """Yield successive batches from the data."""
            for i in range(0, len(data), batch_size):
                yield data[i : i + batch_size]

        embeddings = []

        if len(texts) > MAX_ROWS:
            # process in batches
            batches = list(batchify(texts, MAX_ROWS))
            # tqdm for progress bar
            with tqdm(total=len(batches), desc="Processing batches...") as pbar:
                for batch in batches:
                    payload = self.create_payload(batch)
                    # call the m. deployment
                    response = self.send_request(self.endpoint, payload, self.auth)
                    embeddings.extend([item["embedding"] for item in response["data"]])
                    pbar.update(1)
        else:
            # single call
            payload = self.create_payload(texts)
            response = self.send_request(self.endpoint, payload, self.auth)
            embeddings = [item["embedding"] for item in response["data"]]

        return embeddings

    def embed_query(self, text: str) -> list[float]:
        """
        Embed a single query into a vector.
        :param text: The query to embed.
        :return: The embedding vector.
        """
        # Call the embedding model and return the query embedding
        # just for now
        return self.embed_documents([text])[0]
