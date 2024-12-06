import requests
import random
import string
from qrs_api_client.auth import AuthManager
import qrs_api_client.models as models
import json


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

        self.server = server_name + ":" + str(server_port) + "/qrs"
        self.headers = {"X-Qlik-XrfKey": self.xrf, "Accept": "application/json",
                        "X-Qlik-User": "UserDirectory=INTERNAL;UserID=sa_repository",
                        "Content-Type": "application/json"}

        # Initialize authentication manager
        self.session = requests.session()  # Initialize session
        if auth_manager is None:
            auth_manager = AuthManager()
        self.session = auth_manager.get_auth(self.session, auth_method, verify_ssl)

        if auth_method == "ntlm":
            self.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
            self.headers.pop("X-Qlik-User")
            # self.headers = {"X-Qlik-XrfKey": self.xrf, "User-Agent": "Windows"}

    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
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
        url = "https://" + f"{self.server}/{endpoint}?xrfkey={self.xrf}"
        print(f"Making request to: {url}")

        try:
            response = self.session.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            return None

    def get(self, endpoint: str, params=None) -> dict:
        """
        Executes a GET request to the QRS API.

        Args:
            endpoint (str): The API endpoint to call.
            params (dict, optional): Query parameters to include in the request.

        Returns:
            dict: JSON response as a dictionary or None if an error occurs.
        """
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, data=None) -> dict:
        """
        Executes a POST request to the QRS API.

        Args:
            endpoint (str): The API endpoint to call.
            data (dict or str, optional): The JSON payload to include in the request body.

        Returns:
            dict: JSON response as a dictionary or None if an error occurs.
        """
        return self._request("POST", endpoint, data=data)

    def delete(self, endpoint: str) -> dict:
        """
        Executes a DELETE request to the QRS API.

        Args:
            endpoint (str): The API endpoint to call.

        Returns:
            dict: JSON response as a dictionary or None if an error occurs.
        """
        return self._request("DELETE", endpoint)

    def create_reload_task(self, app_id, task_name, custom_properties=None, tags: list = None,
                           schema_events: list = None, composite_events: list = None) -> dict:
        """
        Creates a reload task for a specified app.

        Args:
            app_id (str): The ID of the app for which the task is created.
            task_name (str): The name of the reload task to create.
            custom_properties (dict, optional): Dictionary of custom property IDs and their values.
            tags (list, optional): List of tag IDs to associate with the task.
            schema_events (list, optional): List of schema events to schedule the task.
            composite_events (list, optional): List of composite events to schedule the task.

        Returns:
            dict: JSON response from the API or None if an error occurs.
        """

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
                                         app=app_condensed)

        # Construct reload task bundle
        reload_task_bundle = models.reload_task_bundle(task=reload_task, composite_events=composite_events,
                                                       schema_events=schema_events)

        # Serialize payload to JSON
        payload = json.dumps(reload_task_bundle)

        # Execute API call
        return self.post("reloadtask/create", data=payload)
