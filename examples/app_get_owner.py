from qrs_api_client.client import QRSClient
from qrs_api_client.auth import AuthManager
import uuid


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
result = client.app_get_owner(app_id=app_id)

if result:
    print("Owner exported:", result)
else:
    print("API request error.")
