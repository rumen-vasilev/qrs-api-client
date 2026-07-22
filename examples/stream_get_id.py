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

stream_name = "<stream_name>"

# Looks up the IDs of all streams with this name
result = client.stream_get_id(stream_name=stream_name)

if result:
    print(f"Found {len(result)} stream(s) named '{stream_name}':")
    for stream_id in result:
        print(" -", stream_id)
else:
    print(f"No stream named '{stream_name}' found.")
