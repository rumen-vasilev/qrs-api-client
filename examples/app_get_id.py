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

# Looks up the IDs of all apps with this name
result = client.app_get_id(app_name=app_name)

if result:
    print(f"Found {len(result)} app(s) named '{app_name}':")
    for app_id in result:
        print(" -", app_id)
else:
    print(f"No app named '{app_name}' found.")

# Optional: restrict the search to a specific stream by name
# result = client.app_get_id(app_name=app_name, stream_name="<stream_name>")
# print(result)
