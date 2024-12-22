from qrs_api_client.client import QRSClient
from dotenv import load_dotenv
import os

# Loads environment variables from .env file.
load_dotenv()

# Authenticates on the enterprise server (Cert paths are called from the .env file)
client = QRSClient(server_name=os.getenv("SERVER_NAME"), server_port=os.getenv("SERVER_PORT"),
                   auth_method="certificate", verify_ssl=True)

# Calls the API
app_replace = client.app_upload_replace(target_app_id="<target_app_id>", file_name="<path_to_certificates>/<file_name>.qvf")

if app_replace:
    print("App replaced:", app_replace)
else:
    print("API request error.")
