"""
Test02
"""

from time import time
import requests
import ads

# Impostazioni iniziali
BASE_URL = "https://modeldeployment.eu-frankfurt-1.oci.customer-oci.com"
ENDPOINT = f"{BASE_URL}/ocid1.datasciencemodeldeployment.oc1.eu-frankfurt-1.amaaaaaa2xxap7yagq4z62toy5toj6fijrzi6deswanqy2l3yik7mmifix2a/predict"


# in secs
TIMEOUT = 60


def create_payload(request: list):
    """Crea il payload JSON per la richiesta al modello."""
    return {"model": "odsc-llm", "input": request}


def send_request(endpoint, payload, auth):
    """Invia la richiesta POST all'endpoint specificato."""
    try:
        response = requests.post(endpoint, json=payload, auth=auth, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error in model invocation: {e}")


# Programma principale
if __name__ == "__main__":

    # Auth
    ads.set_auth(auth="api_key", oci_config_location="~/.oci/config", profile="DEFAULT")
    auth = ads.common.auth.default_signer()["signer"]

    t_start = time()

    try:
        REQUEST = [
            "Hello, I am a car repair expert. I will help you to identify the parts to replace in the car.",
            "Hello, I am a car repair expert.",
        ]
        payload = create_payload(REQUEST)

        response = send_request(ENDPOINT, payload, auth)

        t_elapsed = round(time() - t_start, 1)

        print("\nRequest completed in:", t_elapsed, "sec.")
        print("")
        print("Request: ", REQUEST)
        print("")
        print("Response:")
        print(response["data"])
        print("")

    except Exception as e:
        print(f"{e}")
