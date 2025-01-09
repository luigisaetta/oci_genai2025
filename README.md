# OCI Generative AI 2025
This repository will contains  a set of examples and prototypes for **new things** we can do with LLM

## Features and demos
* Invoke a [multi-modal model in OCI](https://github.com/luigisaetta/oci_genai2025/blob/main/test_multimodal01.py) using Langchain.


## Configuration
Create a file **config.py** starting from the [template](https://github.com/luigisaetta/oci_genai2025/blob/main/config_template.py) provided.

You need to put your COMPARTMENT OCID.

## Security
For the security, you need to have all the right policies in place.

if AUTH = "API_KEY" create a key-pair and put in $HOME/.oci

if you want to user RESOURCE_PRINCIPAL then you need to create a Dynamic Group and authorize it.
(For example, if you want to run the code in a Data Science Notebook Session)

Refer to the OCI Security Documentation for details.

