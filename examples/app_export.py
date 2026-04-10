from qrs_api_client.client import QRSClient
from dotenv import load_dotenv
import os
import uuid

# Loads environment variables from .env file.
load_dotenv()

# Authenticates on the enterprise server (Cert paths are called from the .env file)
client = QRSClient(server_name=os.getenv("SERVER_NAME"), server_port=os.getenv("SERVER_PORT"),
                   auth_method="certificate", verify_ssl=False)

app_id = uuid.UUID("<app_id>")
file_path = r"<export_file_path>"
file_name="<export_file_name>.qvf"

# Calls the API
app_export = client.app_export(app_id=app_id, file_path=file_path, file_name=None, skip_data=False)

if app_export:
    print("App exported:", app_export)
else:
    print("API request error.")
