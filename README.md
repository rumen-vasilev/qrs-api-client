# qrs-api-client (Qlik Sense Repository API Client)

Python client for [Qlik Sense Repository Service API](https://help.qlik.com/en-US/sense-developer/November2024/Subsystems/RepositoryServiceAPI/Content/Sense_RepositoryServiceAPI/RepositoryServiceAPI-Introduction.htm).

Forked from [clintcarr/qrspy](https://github.com/clintcarr/qrspy).

## Requirements

* Python 3.9+
* `requests >= 2.32.3`

Optional:
* `requests_ntlm >= 1.2.0` — only required for NTLM authentication

## Installation

```bash
# Minimal install (certificate authentication only)
pip install qrs-api-client

# With NTLM authentication support
pip install qrs-api-client[ntlm]
```

## Connecting using certificates

Export the Qlik Sense certificates in PEM format from the Qlik Sense Enterprise server to a local folder before running the code.

```python
from qrs_api_client import QRSClient, AuthManager

auth_manager = AuthManager(
    cert_path="<path_to_certificates>/client.pem",
    key_path="<path_to_certificates>/client_key.pem",
    root_cert_path="<path_to_certificates>/root.pem",
)

client = QRSClient(
    server_name="<server_name>",
    server_port=4242,
    auth_manager=auth_manager,
    auth_method="certificate",
    verify_ssl=True,
)

about = client.get("/qrs/about/api/description", {"extended": "false", "method": "POST"})
if about:
    print(about)
else:
    print("API request error.")
```

## Connecting using NTLM

Install with the `ntlm` extra: `pip install qrs-api-client[ntlm]`.

```python
from qrs_api_client import QRSClient, AuthManager

auth_manager = AuthManager(
    user_id="<DOMAIN>\\<user_id>",
    password="<password>",
    root_cert_path="<path_to_certificates>/root.pem",
)

client = QRSClient(
    server_name="<server_name>",
    server_port=443,
    auth_manager=auth_manager,
    auth_method="ntlm",
    verify_ssl=False,
)

about = client.get("/qrs/about/api/description", {"extended": "false", "method": "POST"})
print(about)
```

## Loading configuration from environment variables or .env files

`qrs-api-client` does not load any configuration automatically. This keeps it a clean, predictable library — you are in full control of where credentials come from.

A common pattern is to store credentials in environment variables or a `.env` file and load them in your own application code:

```bash
pip install python-dotenv
```

```dotenv
# .env in your project folder (add this to .gitignore!)
QLIK_CERT_PATH=/path/to/client.pem
QLIK_KEY_PATH=/path/to/client_key.pem
QLIK_ROOT_CERT_PATH=/path/to/root.pem
QLIK_SERVER_NAME=qliksense.example.com
QLIK_SERVER_PORT=4242
```

```python
import os
from dotenv import load_dotenv
from qrs_api_client import QRSClient, AuthManager

load_dotenv()

auth_manager = AuthManager(
    cert_path=os.environ["QLIK_CERT_PATH"],
    key_path=os.environ["QLIK_KEY_PATH"],
    root_cert_path=os.environ["QLIK_ROOT_CERT_PATH"],
)

client = QRSClient(
    server_name=os.environ["QLIK_SERVER_NAME"],
    server_port=int(os.environ["QLIK_SERVER_PORT"]),
    auth_manager=auth_manager,
    auth_method="certificate",
    verify_ssl=True,
)
```

Any other config source (Vault, AWS Secrets Manager, YAML files, command-line arguments) works the same way — just pass the values into `AuthManager()` and `QRSClient()`.

## Query parameters: dict or string

The HTTP methods accept `params` as a `dict`:

```python
client.get("/qrs/about", {"extended": "false"})
```

## Logging

The client uses the standard `logging` module under the name `qrs_api_client.client`. To see debug output:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Examples of usage

See the [examples folder](https://github.com/rumen-vasilev/qrs-api-client/tree/master/examples).

## Documentation

Full API reference: [https://rumen-vasilev.github.io/qrs-api-client/](https://rumen-vasilev.github.io/qrs-api-client/)

## License

MIT — see [LICENSE](LICENSE).
