import logging
import uuid

from qrs_api_client.client import QRSClient
from qrs_api_client.auth import AuthManager


# Configure logging — set level to DEBUG to also see the polling messages
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Optional: silence noisy libraries (urllib3 / requests warnings during polling)
logging.getLogger("urllib3").setLevel(logging.WARNING)


# Inserts certificates into the authentication manager
auth_manager = AuthManager(
    cert_path="<path_to_certificates>/client.pem",
    key_path="<path_to_certificates>/client_key.pem",
    root_cert_path="<path_to_certificates>/root.pem")

# Authenticates on the enterprise server
client = QRSClient(server_name="<server_name>", server_port=4242, auth_manager=auth_manager,
                   auth_method="certificate", verify_ssl=True)

app_id = uuid.UUID("<app_id>")

# Calls the API
result = client.app_reload(app_id=app_id, poll_interval=5.0)

if result:
    print("App reload started:", result)
else:
    print("API request error.")
