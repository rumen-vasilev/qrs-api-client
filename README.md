# qrs-api-client (Qlik Sense Repository API Client)
Python client for [Qlik Sense Repository Service API](https://help.qlik.com/en-US/sense-developer/November2024/Subsystems/RepositoryServiceAPI/Content/Sense_RepositoryServiceAPI/RepositoryServiceAPI-Introduction.htm).

Forked from [clintcarr/qrspy](https://github.com/clintcarr/qrspy)

## Requirements
* Python 3.6+
* requests>=2.32.3
* requests_ntlm>=1.2.0
* python-dotenv>=1.0.0

## Installation
```bash
pip install qrs-api-client
```

## Configuration
You can optionally put the authentication data into an .env file. Just create it in your project folder and initialize
the variables listed below.
```dotenv
CERT_PATH="qlik_certs/client.pem"
KEY_PATH="qlik_certs/client_key.pem"
ROOT_CERT_PATH="qlik_certs/root.pem"
SERVER_NAME="<server name>"
SERVER_PORT=4242
USER_ID="<DOMAIN>\\<user_id>"
PASSWORD="<insert password>"
```


## Connecting to Qlik Sense Enterprise Server using certificates
You need to export the Qlik Sense certificates in PEM format from the Qlik Sense Enterprise server to a local folder in 
order to authenticate on the server.

### Authentication without .env file
```python
from qrs_api_client.client import QRSClient
from qrs_api_client.auth import AuthManager

# Inserts certificates into the authentication manager
auth_manager = AuthManager(
    cert_path="<path_to_certificates>/client.pem",
    key_path="<path_to_certificates>/client_key.pem",
    root_cert_path="<path_to_certificates>/root.pem")

# Authenticates on the enterprise server
client = QRSClient(server_name="<server_name>", server_port=4242, auth_manager=auth_manager,
                   auth_method="certificate", verify_ssl=True)

# Calls the API
api_desc_post = client.get("about/api/description", "extended=false&method=POST")
if api_desc_post:
    print(api_desc_post)
else:
    print("API request error.")
```

### Authentication with .env file
```python
from qrs_api_client.client import QRSClient
from dotenv import load_dotenv
import os

# Loads environment variables from .env file.
load_dotenv()

# Authenticates on the enterprise server (Cert paths are called from the .env file)
client = QRSClient(server_name=os.getenv("SERVER_NAME"), server_port=os.getenv("SERVER_PORT"),
                   auth_method="certificate", verify_ssl=True)

# Calls the API
api_desc_post = client.get("about/api/description", "extended=false&method=POST")
if api_desc_post:
    print(api_desc_post)
else:
    print("API request error.")
```

## Connecting to Qlik Sense Enterprise Server using NTLM

### Authentication without .env file
```python
from qrs_api_client.client import QRSClient
from qrs_api_client.auth import AuthManager

# Inserts credentials into the authentication manager
auth_manager = AuthManager(user_id="<DOMAIN>\\<user_id>", password="<password>",
                           root_cert_path="<path_to_certificates>/root.pem")

# Authenticates on the enterprise server
client = QRSClient(server_name="<server_name>", server_port=443, auth_manager=auth_manager,
                   auth_method="ntlm", verify_ssl=False)

# Calls the API
api_desc_post = client.get("about/api/description", "extended=false&method=POST")
if api_desc_post:
    print(api_desc_post)
else:
    print("API request error.")
```

### Authentication with .env file
```python
from qrs_api_client.client import QRSClient

# Authenticates on the enterprise server
client = QRSClient(server_name="<server_name>", server_port=443, auth_method="ntlm", verify_ssl=False)

# Calls the API
api_desc_post = client.get("about/api/description", "extended=false&method=POST")
if api_desc_post:
    print(api_desc_post)
else:
    print("API request error.")
```

## Examples of usage
Please click on this [link](https://github.com/rumen-vasilev/qrs-api-client/tree/master/examples) to find examples of usage of this client.

## Documentation
Please click on this [link](https://rumen-vasilev.github.io/qrs-api-client/) for full API reference documentation.
