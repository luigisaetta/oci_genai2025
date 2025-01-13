"""
Invoke the OCI GenAI language model with a multimodal input (text and image) and print the response.
The model used is the "meta.llama-3.2-90b-vision-instruct" model.

Author: L. Saetta
Last update: 2025-10-06
"""

import base64
from langchain_core.messages import HumanMessage
from langchain_community.chat_models import ChatOCIGenAI

from config import (
    # here MODEL_ID must be: "meta.llama-3.2-90b-vision-instruct"
    MODEL_ID,
    AUTH,
    SERVICE_ENDPOINT,
    MAX_TOKENS,
    TEMPERATURE,
    COMPARTMENT_ID,
)


def encode_image(image_path):
    """
    Encode the image in BASE64 format.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_llm():
    """
    Initialize and return an instance of ChatOCIGenAI with the specified configuration.

    Returns:
        ChatOCIGenAI: An instance of the OCI GenAI language model.
    """
    _llm = ChatOCIGenAI(
        auth_type=AUTH,
        model_id=MODEL_ID,
        service_endpoint=SERVICE_ENDPOINT,
        compartment_id=COMPARTMENT_ID,
        is_stream=True,
        model_kwargs={"temperature": TEMPERATURE, "max_tokens": MAX_TOKENS},
    )
    return _llm


def print_stream(_ai_response):
    """
    Helper function to print streaming responses from the AI model.

    Args:
        ai_response (generator): A generator yielding chunks of the AI response.

    Returns:
        str: The complete response as a single string.
    """
    all_chunks = ""

    for chunk in _ai_response:
        print(chunk.content, end="", flush=True)
        all_chunks += chunk.content

    # return the entire result to be stored in history
    return all_chunks


#
# Main
#
DO_STREAM = True
IMG_FILE_NAME = "IMG01.jpg"

llm = get_llm()

base64_image = encode_image(IMG_FILE_NAME)

# this way the format the user request
# the same as the one the model expects
# we could also add a System Message at the beginning
QUESTION = "Create a detailed description of the content of this image."
messages = [
    HumanMessage(
        content=[
            {"type": "text", "text": QUESTION},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
            },
        ],
    )
]

# first we print the request
print("")
print(f"{QUESTION}:")
print("")

if DO_STREAM:
    ai_response = llm.stream(input=messages)

    all_text = print_stream(ai_response)
else:
    ai_response = llm.invoke(input=messages)

    print(ai_response.content)

print("")
print("")