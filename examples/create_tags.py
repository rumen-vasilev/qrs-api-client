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

tags=["<tag1>", "<tag2>", "<tag3>"]

# Calls the API
result = client.create_tags(names=tags)

if result:
    print("Tags created:", result)
else:
    print("API request error.")
