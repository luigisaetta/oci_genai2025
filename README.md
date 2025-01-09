# OCI Generative AI 2025
This repository will contains  a set of examples and prototypes for new things we can do with LLM

## Configuration
Create a file config.py starting from the template provided.
You need to put your COMPATMENT OCID.

## Security
For the security, you need to have all the right policies in place.

if AUTH = "API_KEY" create a key-pair and put in $HOME/.oci

if you want to user RESOURCE_PRINCIPAL then you need to create a Dynamic Groupt and authorize it.
(For example, if you want to run the code in a Data Science Notebook Session)

Refer to the OCI Security Documentation for details.

