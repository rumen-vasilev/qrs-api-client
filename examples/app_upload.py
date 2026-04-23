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

app_name = "<app_name>"
file=r"<file_path/file_name>"

# Calls the API
result = client.app_upload(app_name=app_name, file_name=file)

if result:
    print("App uploaded:", result)
else:
    print("API request error.")
