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

schema_path = "<schema_path>"

# Calls the API
result = client.get_enum(schema_path=schema_path)

if result:
    print("Result:", result)
else:
    print("API request error.")
