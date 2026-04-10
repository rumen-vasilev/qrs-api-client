import os
import requests
import random
import string
from qrs_api_client.auth import AuthManager
import qrs_api_client.models as models
import json
import uuid
from datetime import datetime
from urllib.parse import urlparse, unquote


class QRSClient:
    """
    Client for interacting with the Qlik Repository Service (QRS) API.

    Provides methods for establishing a session and performing CRUD operations on QRS entities.
    """

    def __init__(self, server_name: str, server_port: int, auth_method: str, auth_manager: AuthManager = None, verify_ssl=True):
        """
        Initializes the QRSClient instance and establishes a session with the Qlik Sense Repository Service.

        Args:
            server_name (str): The hostname or domain name of the server.
            server_port (int): The port number of the server (e.g., 4242).
            auth_manager (AuthManager): An instance of AuthManager for handling authentication.
            auth_method (str): The authentication method to use (e.g., "ntlm" or "cert").
            verify_ssl (bool or str, optional): Boolean or path to a root.pem file for SSL verification.
        """
        self.xrf = ''.join(random.sample(string.ascii_letters + string.digits, 16))

        self.server = server_name + ":" + str(server_port) #+ "/qrs"
        self.auth_method = auth_method

        # Initialize authentication manager
        self.session = requests.session()  # Initialize session
        if auth_manager is None:
            auth_manager = AuthManager()
        self.session = auth_manager.get_auth(self.session, auth_method, verify_ssl)

    def _request(self, method: str, endpoint: str, **kwargs):
        """
        Executes an HTTP request to the QRS API.

        Args:
            method (str): HTTP method to use (e.g., "GET", "POST", "DELETE").
            endpoint (str): The API endpoint to call.
            **kwargs: Additional arguments to pass to the request (e.g., params, data).

        Returns:
            dict: JSON response as a dictionary or None if an error occurs.

        Raises:
            requests.exceptions.RequestException: If an error occurs during the API request.
        """
        if kwargs['params'] is None:
            query_params = f"?Xrfkey={self.xrf}"
        else:
            query_params = f"?Xrfkey={self.xrf}&{kwargs['params']}"

        # Remove params from kwargs so requests doesn't append them a second time
        kwargs.pop('params', None)

        # Construct the url
        url = "https://" + f"{self.server}{endpoint}{query_params}"
        print(f"Making request to: {url}")

        # Construct the headers
        headers = {"X-Qlik-Xrfkey": self.xrf, "Accept": "application/json",
                   "X-Qlik-User": "UserDirectory=INTERNAL;UserID=sa_repository",
                   "Content-Type": "application/json", "Connection": "Keep-Alive"}
        if self.auth_method == "ntlm":
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
            headers.pop("X-Qlik-User")
            # self.headers = {"X-Qlik-Xrfkey": self.xrf, "User-Agent": "Windows"}

        # Merge the headers passed from another method
        kwargs['headers'] = headers | kwargs['headers']

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            return None

    def get(self, endpoint: str, params: str = None, headers: dict = None) -> dict:
        """
        Executes a GET request to the QRS API.

        Args:
            endpoint (str): The API endpoint to call.
            params (str, optional): Query parameters to include in the request.
            headers (dict, optional): Additional header parameters.

        Returns:
            dict: JSON response as a dictionary or None if an error occurs.
        """
        if headers is None:
            headers = {}
        response = self._request(method="GET", endpoint=endpoint, params=params, headers=headers)
        if response is None:
            return None
        return response.json()

    def post(self, endpoint: str, params: str = None, headers: dict = None, data=None) -> dict:
        """
        Executes a POST request to the QRS API.

        Args:
            endpoint (str): The API endpoint to call.
            params (str, optional): Query parameters to include in the request.
            headers (dict, optional): Additional header parameters.
            data (dict or str, optional): The JSON payload to include in the request body.

        Returns:
            dict: JSON response as a dictionary or None if an error occurs.
        """
        if headers is None:
            headers = {}
        response = self._request(method="POST", endpoint=endpoint, params=params, headers=headers, data=data)
        if response is None:
            return None
        return response.json()

    def put(self, endpoint: str, params: str = None, headers: dict = None, data=None) -> dict:
        """
        Executes a PUT request to the QRS API.

        Args:
            endpoint (str): The API endpoint to call.
            params (str, optional): Query parameters to include in the request.
            headers (dict, optional): Additional header parameters.
            data (dict or str, optional): The JSON payload to include in the request body.

        Returns:
            dict: JSON response as a dictionary or None if an error occurs.
        """
        if headers is None:
            headers = {}
        response = self._request(method="PUT", endpoint=endpoint, params=params, headers=headers, data=data)
        if response is None:
            return None
        return response.json()

    def delete(self, endpoint: str, params: str = None) -> dict:
        """
        Executes a DELETE request to the QRS API.

        Args:
            endpoint (str): The API endpoint to call.
            params (str, optional): Query parameters to include in the request.

        Returns:
            dict: JSON response as a dictionary or None if an error occurs.
        """
        response = self._request(method="DELETE", endpoint=endpoint, params=params, headers={})
        if response is None:
            return None
        return response.json()

    def app_export(self, app_id: uuid.UUID, file_path: str, file_name: str = None, skip_data: bool = False):
        """
        Exports an app in a two-step process using POST and GET methods.

        Step 1: POST to /qrs/app/{id}/export/{token} to trigger the export.
                The API returns JSON with a 'downloadPath' field.
        Step 2: GET the downloadPath to download the binary .qvf file.

        Args:
            app_id (UUID): The ID of the app to be exported.
            file_path (str): The directory path where the exported app should be stored.
            file_name (str, optional): File name for the exported app (e.g., "MyApp.qvf"). Falls kein Wert übergeben
            wurde, wird der ursprüngliche Name der Datei genommen.

        Returns:
            str: Success message with file name and path, or None if an error occurs.
        """
        ################################################################################################################
        # Step 1: Trigger the export on the Sense Enterprise Server.
        ################################################################################################################
        export_token = str(uuid.uuid4())
        path = '/qrs/app/{0}/export/{1}'.format(app_id, export_token)
        # query = 'skipData={0}'.format(str(skip_data).lower())
        query = 'skipData={0}'.format(skip_data)
        data = self.post(endpoint=path, params=query)
        # data = self._request(method="GET", endpoint=path, params=query, headers={})
        if data is None:
            print("Export request failed.")
            return None

        ################################################################################################################
        # Step 2: Download the .qvf file.
        ################################################################################################################
        download_path = data.get('downloadPath', '')
        parsed = urlparse(download_path)
        path_part = parsed.path
        query_part = parsed.query
        if file_name is None:
            # Extract file name
            file_name = os.path.basename(path_part)
            # Decode URL-Encoding
            file_name = unquote(file_name)

        # Complete header for the download request
        headers = {"Content-Type": "application/vnd.qlik.sense.app"}

        try:
            response = self._request(method="GET", endpoint=path_part, params=query_part, headers=headers, stream=True)
            with open(file_path + "/" + file_name, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            return 'Application: {0} written to {1}'.format(file_name, file_path)

        except requests.exceptions.RequestException as e:
            print(f"Download error: {e}")
            return None

    def app_upload(self, app_name: str, file_name: str):
        """
        Executes a POST request to the QRS API.

        Args:
            app_name (str): The name of the app after upload.
            file_name (str): The path to the file.

        Returns:
            dict: JSON response as a dictionary.
        """
        headers = {"Content-Type": "application/vnd.qlik.sense.app"}
        with open(file_name, 'rb') as payload:
            return self.post(endpoint="/qrs/app/upload", params="name={0}".format(app_name), headers=headers, data=payload)

    def app_upload_replace(self, target_app_id: uuid.UUID, file_name: str):
        """
        Executes a POST request to the QRS API.

        Args:
            target_app_id (UUID): The ID of the app to be replaced.
            file_name (str): The path to the file.

        Returns:
            dict: JSON response as a dictionary.
        """
        headers = {"Content-Type": "application/vnd.qlik.sense.app"}
        with open(file_name, 'rb') as payload:
            return self.post(endpoint="/qrs/app/upload/replace", params="targetappid={0}".format(target_app_id),
                             headers=headers, data=payload)

    def reloadtask_create(self, app_id, task_name, custom_properties=None, tags: list = None,
                          created_date: datetime = None, modified_date: datetime = None,
                          modified_by_user_name: str = None, schema_events: list = None, composite_events: list = None,
                          schema_path: str = None, privileges: list = None, task_type: int = None, enabled: bool = None,
                          task_session_timeout: int = None, max_retries: int = None, is_manually_triggered: bool = None,
                          operational=None, is_partial_reload: bool = None, time_to_live: int = None,
                          preload_nodes=None) -> dict:
        """
        Creates a reload task for a specified app.

        Args:
            app_id (str): The ID of the app for which the task is created.
            task_name (str): The name of the reload task to create.
            custom_properties (dict, optional): Dictionary of custom property IDs and their values.
            tags (list, optional): List of tag IDs to associate with the task.
            schema_events (list, optional): List of schema events to schedule the task.
            composite_events (list, optional): List of composite events to schedule the task.
            schema_path (str, optional): Schema path.
            privileges (list, optional): Privileges.
            task_type (int, optional): Task type. Default value is 0.
            enabled (bool, optional): True, if the task is active. Default value is True.

        Returns:
            dict: JSON response from the API or None if an error occurs.
        """
        # # Initialize mutable default arguments
        # if privileges is None:
        #     privileges = []

        # Create app reference
        app_condensed = models.app_condensed(_id=app_id)

        # Prepare custom properties
        custom_property_list = []
        if custom_properties is not None:
            for custom_property_id, custom_property_values in custom_properties.items():
                custom_property_definition_condensed = models.custom_property_definition_condensed(_id=custom_property_id)
                for value in custom_property_values:
                    custom_property_value = models.custom_property_value(value=value,
                                                                         definition=custom_property_definition_condensed)
                    custom_property_list.append(custom_property_value)

        # Prepare tags
        tag_list = []
        if tags is not None:
            for tag in tags:
                tag_condensed = models.tag_condensed(_id=tag)
                tag_list.append(tag_condensed)

        # Construct reload task
        reload_task = models.reload_task(custom_properties=custom_property_list, name=task_name, tags=tag_list,
                                         app=app_condensed, created_date=created_date, modified_date=modified_date,
                                         modified_by_user_name=modified_by_user_name, schema_path=schema_path,
                                         privileges=privileges, task_type=task_type, enabled=enabled,
                                         task_session_timeout=task_session_timeout, max_retries=max_retries,
                                         is_manually_triggered=is_manually_triggered, operational=operational,
                                         is_partial_reload=is_partial_reload, time_to_live=time_to_live,
                                         preload_nodes=preload_nodes)

        # Construct reload task bundle
        reload_task_bundle = models.reload_task_bundle(task=reload_task, composite_events=composite_events,
                                                       schema_events=schema_events)

        # Serialize payload to JSON
        payload = json.dumps(reload_task_bundle)

        # Execute API call
        return self.post(endpoint="/qrs/reloadtask/create", data=payload)