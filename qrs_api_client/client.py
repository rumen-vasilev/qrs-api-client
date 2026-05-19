"""
QRS API Client for Qlik Sense Enterprise.
"""
import os
import random
import string
import json
import time
import uuid
import logging
from datetime import datetime
from urllib.parse import urlparse, unquote

import requests

from qrs_api_client.auth import AuthManager
import qrs_api_client.models as models


logger = logging.getLogger(__name__)


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
                      params should be a dict (e.g., {"skipData": "false"}) or None.

        Returns:
            requests.Response: Response object or None if an error occurs.
        """
        # Build query parameters — Xrfkey is always required
        params = kwargs.get('params') or {}
        params['Xrfkey'] = self.xrf
        kwargs['params'] = params

        # Construct the url
        url = f"https://{self.server}{endpoint}"

        # Construct the headers
        headers = {"X-Qlik-Xrfkey": self.xrf, "Accept": "application/json",
                   "X-Qlik-User": "UserDirectory=INTERNAL;UserID=sa_repository",
                   "Content-Type": "application/json", "Connection": "Keep-Alive"}
        if self.auth_method == "ntlm":
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
            headers.pop("X-Qlik-User")

        # Merge the headers passed from another method
        kwargs['headers'] = headers | kwargs.get('headers', {})

        logger.debug("QRS request: %s %s params=%s", method, url, params)

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error("QRS request failed: %s", e)
            return None


    # ---------------------------------------------------------------------------------------------------------------- #
    # Generic HTTP methods                                                                                             #
    # ---------------------------------------------------------------------------------------------------------------- #

    def get(self, endpoint: str, params: dict = None, headers: dict = None) -> dict:
        """
        Executes a GET request to the QRS API.

        Args:
            endpoint (str): The API endpoint to call.
            params (dict, optional): Query parameters as key-value pairs.
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

    def post(self, endpoint: str, params: dict = None, headers: dict = None, data=None):
        """
        Executes a POST request to the QRS API.

        Args:
            endpoint (str): The API endpoint to call.
            params (dict, optional): Query parameters as key-value pairs.
            headers (dict, optional): Additional header parameters.
            data (dict or str, optional): The JSON payload to include in the request body.

        Returns:
            dict: JSON response as a dictionary or None if an error occurs.
        """
        if headers is None:
            headers = {}
        response = self._request(method="POST", endpoint=endpoint, params=params, headers=headers, data=data)
        if isinstance(response, requests.Response):
            print("IF:",response)
            return response.json()
        else:
            print("ELSE:", response)
            return response


    def put(self, endpoint: str, params: dict = None, headers: dict = None, data=None):
        """
        Executes a PUT request to the QRS API.

        Args:
            endpoint (str): The API endpoint to call.
            params (dict, optional): Query parameters as key-value pairs.
            headers (dict, optional):
            data:
            payload:

        Returns:
            dict: JSON response as a dictionary or None if an error occurs.
        """
        if headers is None:
            headers = {}
        response = self._request(method="PUT", endpoint=endpoint, params=params, headers=headers, data=data)
        return response

    def delete(self, endpoint: str, params: dict = None) -> dict:
        """
        Executes a DELETE request to the QRS API.

        Args:
            endpoint (str): The API endpoint to call.
            params (dict, optional): Query parameters as key-value pairs.

        Returns:
            dict: JSON response as a dictionary or None if an error occurs.
        """
        response = self._request(method="DELETE", endpoint=endpoint, params=params, headers={})
        if response is None:
            return None
        return response.json()


    # ---------------------------------------------------------------------------------------------------------------- #
    # Server-side enum lookups                                                                                         #
    # ---------------------------------------------------------------------------------------------------------------- #

    def get_enum(self, schema_path: str) -> list[str] | None:
        """
        Retrieves the list of values for the enum that is used at a given
        Qlik Sense schema path.

        Each Qlik object property whose type is an enum (e.g.
        ExecutionResult.Status, ReloadTask.TaskType, App.AvailabilityStatus)
        is associated with exactly one enum definition. This method fetches
        the full enum table from /qrs/about/api/enums and looks up the
        values for the property identified by the given schema path.

        The returned list mirrors the raw server format - each entry is a
        string of the form "<int>: <name>" (e.g. "7: FinishedSuccess").

        Args:
            schema_path (str): The schema path of the property whose enum
                values should be returned (e.g. "ExecutionResult.Status",
                "ReloadTask.TaskType", "App.AvailabilityStatus").

        Returns:
            list[str]: The list of enum value strings (e.g.
                ["0: NeverStarted", "1: Triggered", ...]), or None if the
                schema path is not associated with any enum on the server.

        Examples:
            >>> client.get_enum("ExecutionResult.Status")
            ['0: NeverStarted', '1: Triggered', ..., '14: DistributionRunning']

            >>> client.get_enum("ReloadTask.TaskType")
            ['0: Reload', '1: ExternalProgram', '2: UserSync',
             '3: Distribute', '4: Preload']
        """
        raw = self.get(endpoint="/qrs/about/api/enums")
        if raw is None:
            logger.error("Failed to fetch enum definitions from "
                         "/qrs/about/api/enums.")
            return None

        # The server response is keyed by enum name (e.g. "TaskTypeEnum");
        # we walk all definitions and return the values of the one whose
        # "usages" list contains the requested schema path. A single enum
        # may be referenced by multiple schema paths (e.g. EventTypeEnum is
        # used by CompositeEvent.EventType, IEvent.EventType and
        # SchemaEvent.EventType).
        for definition in raw.values():
            if schema_path.lower() in [u.lower() for u in definition.get("usages", [])]:
                return definition.get("values", [])

        logger.error("No enum is defined for schema path \"%s\". "
                     "Use a valid schema path such as "
                     "\"ExecutionResult.Status\".", schema_path)
        return None


    # ---------------------------------------------------------------------------------------------------------------- #
    # High-level convenience methods                                                                                   #
    # ---------------------------------------------------------------------------------------------------------------- #

    def app_get_custom_properties(self, app_id: uuid.UUID) -> list:
        """
        Exports the custom properties of certain app as JSON.

        Args:
            app_id (UUID): The ID of the app.

        Returns:
            list: JSON response as a list.
        """
        result = self.get(endpoint=f"/qrs/app/{app_id}")
        custom_properties = result["customProperties"]
        return custom_properties


    def app_set_custom_properties(self, app_id: uuid.UUID, custom_properties: dict):
        """
        Inserts custom properties into an app.

        Args:
            app_id (UUID): The ID of the app.
            custom_properties (dict): Custom property with name and values to be inserted. The values have a 'list' as data type.

        Returns:
            list: JSON response as a list.
        """
        # Get app JSON structure
        app = self.get(endpoint=f"/qrs/app/{app_id}")
        # Create a list with custom properties, which were assigned to the app
        app_cps = []
        for app_cp in app["customProperties"]:
            app_cps.append(app_cp["definition"]["id"] + "_" + app_cp["value"])

        for name, values in custom_properties.items():
            for value in values:
                # Create filter string
                _filter = {"filter": f"objectTypes eq 'App' and name eq '{name}' and choiceValues eq '{value}'"}
                try:
                    # Get the custom property definition
                    cp = self.get(endpoint=f"/qrs/custompropertydefinition/full", params=_filter)[0]
                except IndexError:
                    logger.error("Custom property name or value you try to import does not exist in Qlik Sense! "
                                 "You should create it first in the QMC.: %s", IndexError)
                    continue
                # Get ID of the custom property
                def_id = cp["id"]
                # Build custom property definition structure
                custom_property_definition_condensed = models.custom_property_definition_condensed(_id=def_id)
                # Build custom property structure
                custom_property_value = models.custom_property_value(value=value, definition=custom_property_definition_condensed)
                # Check if a custom property was assigned to the app
                if custom_property_value["definition"]["id"] + "_" + custom_property_value["value"] not in app_cps:
                    # Insert custom property to the app
                    app["customProperties"].append(custom_property_value)

        return self.put(endpoint=f"/qrs/app/{app_id}", data=json.dumps(app))


    def app_get_tags(self, app_id: uuid.UUID, tags: list):
        """
        Exports the tags of certain app as JSON.

        Args:
            app_id (UUID): The ID of the app.
            tags (list): List with tags to be imported.

        Returns:
            list: JSON response as a list.
        """
        result = self.get(endpoint=f"/qrs/app/{app_id}")
        tags = result["tags"]
        return tags


    def app_set_tags(self, app_id: uuid.UUID, tags: list):
        """
        Inserts tags into an app.

        Args:
            app_id (UUID): The ID of the app.
            tags (list): The tags of the app.

        Returns:
            list: JSON response as a list.
        """
        # Get app JSON structure
        app = self.get(endpoint=f"/qrs/app/{app_id}")

        for name in tags:
            # Create filter string
            _filter = {"filter": f"name eq '{name}'"}
            try:
                # Get the custom property definition
                tag = self.get(endpoint=f"/qrs/tag/full", params=_filter)[0]
            except IndexError:
                logger.error("The tag you try to import does not exist in Qlik Sense! "
                             "You should create it first in the QMC.: %s", IndexError)
                continue
            # Get ID of the tag
            def_id = tag["id"]
            # Build tag definition structure
            tag_condensed = models.tag_condensed(_id=def_id, name=name)
            # Insert custom property to the app
            app["tags"].append(tag_condensed)
        return self.put(endpoint=f"/qrs/app/{app_id}", data=json.dumps(app))


    def app_get_owner(self, app_id: uuid.UUID) -> dict:
        """
        Exports the owner of certain app as JSON.

        Args:
            app_id (UUID): The ID of the app.

        Returns:
            list: JSON response as a dict.
        """
        result = self.get(endpoint=f"/qrs/app/{app_id}")
        owner = result["owner"]
        return owner


    def app_change_owner(self, app_id: uuid.UUID, user_directory: str, user_id: str) -> dict:
        """
        Changes the owner of certain app.

        Args:
            app_id (UUID): The ID of the app.
            user_directory (str): The user directory of the new owner.
            user_id (str): The user id of the new owner.

        Returns:
            list: JSON response as a dict.
        """
        # Create filter string
        _filter = {"filter": f"userDirectory eq '{user_directory}' and userId eq '{user_id}'"}
        # Get the new owner
        owner = self.get(endpoint="/qrs/user", params=_filter)[0]
        # Get app JSON structure
        app = self.get(endpoint=f"/qrs/app/{app_id}")
        # Replace the old owner with the new owner in the app JSON structure
        app["owner"] = owner
        return self.put(endpoint=f"/qrs/app/{app_id}", data=json.dumps(app))


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
            skip_data:

        Returns:
            str: Success message with file name and path, or None if an error occurs.
        """
        ################################################################################################################
        # Step 1: Trigger the export on the Sense Enterprise Server.
        ################################################################################################################
        export_token = str(uuid.uuid4())
        path = '/qrs/app/{0}/export/{1}'.format(app_id, export_token)
        query = {"skipData": skip_data}
        data = self.post(endpoint=path, params=query)
        # data = self._request(method="GET", endpoint=path, params=query, headers={})
        if data is None:
            logger.error("Export request failed for app %s", app_id)
            return None

        ################################################################################################################
        # Step 2: Download the .qvf file.
        ################################################################################################################
        download_path = data.get('downloadPath', '')
        parsed = urlparse(download_path)
        path_part = parsed.path
        query_dict = dict(pair.split('=', 1) for pair in parsed.query.split('&') if '=' in pair) if parsed.query else {}
        if file_name is None:
            # Extract file name
            file_name = os.path.basename(path_part)
            # Decode URL-Encoding
            file_name = unquote(file_name)

        # Complete header for the download request
        headers = {"Content-Type": "application/vnd.qlik.sense.app"}

        try:
            response = self._request(method="GET", endpoint=path_part, params=query_dict, headers=headers, stream=True)
            with open(file_path + "/" + file_name, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            return 'Application: {0} written to {1}'.format(file_name, file_path)

        except requests.exceptions.RequestException as e:
            logger.error("Download error: %s", e)
            return None

    def app_upload(self, app_name: str, file_name: str, keep_data: bool = True, exclude_connections: bool = False):
        """
        Executes a POST request to the QRS API.

        Args:
            app_name (str): The name of the app after upload.
            file_name (str): The path to the file.
            exclude_connections (bool, optional): If set to true and the uploaded .qvf file contains any data connections, they will not be imported to the system. The default value is false.
            keep_data (bool, optional): If set to false and the uploaded .qvf file contains app data, the data will be silently discarded. The default value is true.

        Returns:
            dict: JSON response as a dictionary.
        """
        headers = {"Content-Type": "application/vnd.qlik.sense.app"}
        with open(file_name, 'rb') as payload:
            return self.post(endpoint="/qrs/app/upload", params={"name": app_name, "keepdata": keep_data, "excludeconnections": exclude_connections}, headers=headers, data=payload)

    def app_upload_replace(self, target_app_id: uuid.UUID, file_name: str, keep_data: bool = True):
        """
        Executes a POST request to the QRS API.

        Args:
            target_app_id (UUID): The ID of the app to be replaced.
            file_name (str): The path to the file.
            keep_data (bool, optional): If set to false and the uploaded .qvf file contains app data, the data will be silently discarded. The default value is true.

        Returns:
            dict: JSON response as a dictionary.
        """
        headers = {"Content-Type": "application/vnd.qlik.sense.app"}
        with open(file_name, 'rb') as payload:
            return self.post(endpoint="/qrs/app/upload/replace", params={"targetappid": str(target_app_id), "keepdata": keep_data},
                             headers=headers, data=payload)


    def app_reload(self, id: uuid.UUID, poll_interval: float = 5.0) -> dict:
        """
        Triggers a reload, identified by either a reload task ID or an app
        ID, and waits for it to complete. Mimics the QMC's "Reload now"
        functionality.

        The given ID is resolved in two steps:
            1. The method first checks whether a reload task with that ID
               exists. If so, the task is reused as-is (the method does
               not create or modify anything). Only reload tasks (taskType
               0) are accepted; tasks of other types are rejected.
            2. If no reload task with that ID exists, the ID is treated as
               an app ID. The method then looks for an existing reload
               task named "Manually triggered reload of <app_name>" for
               that app, creating one via reloadtask_create() if needed
               (with no schema events, only manually triggerable).

        Once a reload task has been resolved, the task is started via
        POST /qrs/task/{id}/start/synchronous. The server returns an
        execution session GUID. An empty GUID (00000000-...) means the
        task could not be started (disabled, no scheduler available, app
        not available).

        The execution session is then polled via
        GET /qrs/executionsession/{id} until it returns 404 Not Found -
        per Qlik's documentation this indicates the task has finished and
        the execution session entity has been deleted from the database.

        Finally, the execution result is fetched via
        GET /qrs/executionresult?filter=executionID eq <session_id>
        to determine the final status, duration and details.

        Args:
            id (UUID): Either the ID of a reload task to start, or the ID
                of an app to reload (resolved in that order).
            poll_interval (float, optional): Interval in seconds between
                status checks. Default value is 5.0.

        Returns:
            dict: A result dictionary with the following keys:
                - "success" (bool): True if the reload completed successfully
                  (status FinishedSuccess), False otherwise.
                - "task" (dict): The reload task object that was used.
                Returns None if the ID could not be resolved to either a
                reload task or an app, the task could not be created or
                started, or no execution result was found afterwards.
        """
        # Rebind to a local name so we don't shadow Python's built-in id()
        # inside the method body.
        _id = id

        _EMPTY_GUID = "00000000-0000-0000-0000-000000000000"
        _TASK_TYPE_RELOAD = 0

        # ------------------------------------------------------------------
        # Resolve the given ID to a reload task
        # ------------------------------------------------------------------

        # Step 1: try to interpret the ID as a reload task ID.
        task = self.get(endpoint=f"/qrs/reloadtask/{_id}")
        if task:
            task_type = task.get("taskType")
            if task_type != _TASK_TYPE_RELOAD:
                logger.error("Task with ID \"%s\" exists but is not a reload "
                             "task (taskType=%s).", _id, task_type)
                return None
            logger.info("Using existing reload task \"%s\" (ID: %s).",
                        task.get("name", _id), task["id"])
        else:
            # Step 2: not a task ID - try to interpret it as an app ID.
            app = self.get(endpoint=f"/qrs/app/{_id}")
            if not app:
                logger.error("No reload task or app with ID \"%s\" exists!", _id)
                return None

            app_id = _id
            app_name = app.get("name", str(app_id))
            task_name = f"Manually triggered reload of {app_name}"

            # Look for an existing reload task with the conventional name
            # for this app
            existing_tasks = self.get(
                endpoint="/qrs/reloadtask/full",
                params={"filter": f"app.id eq {app_id} and name eq '{task_name}'"},
            )

            if existing_tasks:
                task = existing_tasks[0]
                logger.info("Reusing existing reload task \"%s\" (ID: %s) "
                            "for app \"%s\".",
                            task_name, task["id"], app_name)
            else:
                logger.info("Creating reload task \"%s\" for app \"%s\".",
                            task_name, app_name)
                created_task = self.reloadtask_create(
                    app_id=str(app_id),
                    task_name=task_name,
                    task_type=_TASK_TYPE_RELOAD,
                    enabled=True,
                    is_manually_triggered=True,
                )
                if not created_task:
                    logger.error("Failed to create reload task for app \"%s\"!",
                                 app_name)
                    return None

                # Re-fetch the new task by name to get its ID
                task = self.get(
                    endpoint="/qrs/reloadtask/full",
                    params={"filter": f"app.id eq {app_id} and name eq '{task_name}'"},
                )[0]

        # ------------------------------------------------------------------
        # Start the task and wait for the execution session to finish
        # ------------------------------------------------------------------

        task_id = uuid.UUID(task["id"])
        task_name = task.get("name", str(task_id))

        # Start the task synchronously - the server returns an execution
        # session GUID as soon as the task has been picked up by the scheduler.
        logger.info("Starting reload task \"%s\" (ID: %s).", task_name, task_id)
        start_response = self.post(endpoint=f"/qrs/task/{task_id}/start/synchronous")
        if start_response is None:
            logger.error("Failed to start reload task \"%s\"!", task_name)
            return None

        # Get the session id
        session_id = start_response.get("value")
        if not session_id or session_id == _EMPTY_GUID:
            logger.error("Reload task \"%s\" could not be started: the server "
                         "returned an empty session ID. The task may be disabled, "
                         "no scheduler is available or the app is unavailable.",
                         task_name)
            return None

        logger.info("Reload task \"%s\" started with execution session ID %s.",
                    task_name, session_id)

        # Poll GET /qrs/executionsession/{id} until it returns 404 Not Found.
        # Per Qlik's documentation, 404 indicates the task has finished and
        # the execution session entity has been deleted from the database.
        # self.get returns None on any non-2xx response (including 404), so
        # we treat a None response as "task finished".
        start_time = time.monotonic()
        while True:
            elapsed = time.monotonic() - start_time

            time.sleep(poll_interval)

            session = self.get(endpoint=f"/qrs/executionsession/{session_id}")
            if session is None:
                # 404 from the server: task is finished. If the very first poll
                # already returns None, the task simply finished before we got
                # a chance to observe it - this is normal for very short reloads.
                logger.info("Execution session %s no longer exists - reload "
                            "task \"%s\" has finished.", session_id, task_name)
                break

            logger.debug("Reload task \"%s\" still in progress (elapsed: %.0fs)",
                         task_name, elapsed)

        # Fetch the final execution result for this session. With task retries
        # configured there can be more than one result - we take the newest.
        results = self.get(
            endpoint="/qrs/executionresult/full",
            params={
                "filter": f"executionID eq {session_id}",
                "orderby": "startTime desc",
            },
        )
        if not results:
            logger.error("Reload task \"%s\" finished but no execution result "
                         "was found for session %s.", task_name, session_id)
            return None

        latest = results[0]
        status = latest.get("status")
        # success = status == self.get_enum("TaskExecutionStatus", "FinishedSuccess")
        success = status == 7

        if success:
            logger.info("Reload task \"%s\" finished successfully "
                        "(duration: %s ms).", task_name, latest.get("duration"))
        else:
            logger.error("Reload task \"%s\" finished with status %s "
                         "(duration: %s ms).",
                         task_name, status, latest.get("duration"))

        return {
            "success": success,
            "task": task,
        }


    def reloadtask_create(self, app_id, task_name, custom_properties=None, tags: list = None,
                          created_date: datetime = None, modified_date: datetime = None,
                          modified_by_user_name: str = None, schema_events: list = None, composite_events: list = None,
                          schema_path: str = None, privileges: list = None, task_type: int = None, enabled: bool = None,
                          task_session_timeout: int = None, max_retries: int = None, is_manually_triggered: bool = None,
                          operational=None, is_partial_reload: bool = None, time_to_live: int = None,
                          preload_nodes=None):
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


    # def create_tag(self, name: str):
    #
    #     tags = self.get(endpoint="/qrs/tag")
    #
    #     if not any(item["name"].lower() == name.lower() for item in tags):
    #         # Construct tag structure
    #         tag = models.tag(name=name)
    #         # Serialize payload to JSON
    #         payload = json.dumps(tag)
    #         # Execute API call
    #         return self.post(endpoint="/qrs/tag", data=payload)
    #     logger.error("The tag \"%s\" already exists!", name)
    #     return None

    def create_tag(self, name: str):
        """
        Creates a single tag via the Qlik Repository Service.

        Retrieves all existing tags first and checks case-insensitively whether
        a tag with the given name already exists. If not, a new tag is created
        via the POST /qrs/tag endpoint.

        Args:
            name (str): The name of the tag to create. Comparison with existing
                tags is case-insensitive.

        Returns:
            dict: JSON response from the API containing the created tag, or
                None if a tag with the given name already exists.
        """
        # Call existing tags
        existing_tags = self.get(endpoint="/qrs/tag")
        # Get names of existing tags
        existing_names = {item["name"].lower() for item in existing_tags}

        # Check, if a tag already exists
        if name.lower() in existing_names:
            logger.error("The tag \"%s\" already exists!", name)
            return None
        # Construct tag structure
        tag = models.tag(name=name)
        # Serialize payload to JSON
        payload = json.dumps(tag)
        # Execute API call to /tag endpoint
        return self.post(endpoint="/qrs/tag", data=payload)

    def create_tags(self, names: list[str]):
        """
        Creates multiple tags in a single API call.

        Uses the bulk endpoint POST /qrs/tag/many to create several tags at once.
        Before sending the request, both already existing tags and duplicates
        within the input list are filtered out (case-insensitive). If no tags
        remain after filtering, no request is sent.

        Args:
            names (list[str]): List of tag names to create. Already existing
                names and duplicates within the list are skipped and logged
                as errors.

        Returns:
            list[dict]: JSON response from the API containing the created tags,
                or None if no new tags remain to be created after filtering.
        """
        # Call existing tags
        existing_tags = self.get(endpoint="/qrs/tag")
        # Get names of existing tags
        existing_names = {item["name"].lower() for item in existing_tags}

        # Filter new tags and remove duplicates from input
        seen = set()
        new_tags = []
        for name in names:
            key = name.lower()
            if key in existing_names:
                logger.error("The tag \"%s\" already exists!", name)
                continue
            if key in seen:
                logger.error("The tag \"%s\" is duplicated in the input!", name)
                continue
            seen.add(key)
            new_tags.append(models.tag(name=name))

        if not new_tags:
            logger.warning("No new tags to create.")
            return None

        # Serialize payload to JSON
        payload = json.dumps(new_tags)
        # Execute API call to /tag/many endpoint
        return self.post(endpoint="/qrs/tag/many", data=payload)

    def create_custom_property(self, name: str, value_type: str = "Text",
                               choice_values: list[str] = None,
                               object_types: list[str] = None,
                               description: str = None):
        """
        Creates a single custom property definition via the Qlik Repository Service.

        Retrieves all existing custom property definitions first and checks
        case-insensitively whether a definition with the given name already
        exists. If not, a new custom property definition is created via the
        POST /qrs/custompropertydefinition endpoint.

        Args:
            name (str): The name of the custom property definition to create.
                Comparison with existing definitions is case-insensitive.
            value_type (str, optional): The type of value the property accepts
                (e.g. "Text"). Default value is "Text".
            choice_values (list[str], optional): Predefined choice values for
                the property. Only relevant when the property should be
                restricted to a fixed set of values.
            object_types (list[str], optional): List of object types the
                property can be applied to (e.g. ["App", "Stream"]).
            description (str, optional): A description of the custom property
                definition.

        Returns:
            dict: JSON response from the API containing the created custom
                property definition, or None if a definition with the given
                name already exists.
        """
        # Retrieve existing custom property definitions
        existing_properties = self.get(endpoint="/qrs/custompropertydefinition")
        existing_names = {item["name"].lower() for item in existing_properties}

        # Existence check
        if name.lower() in existing_names:
            logger.error("The custom property \"%s\" already exists!", name)
            return None

        # Construct custom property definition structure
        custom_property = models.custom_property_definition(
            name=name,
            value_type=value_type,
            choice_values=choice_values,
            object_types=object_types,
            description=description,
        )
        # Serialize payload to JSON
        payload = json.dumps(custom_property)
        # Execute API call
        return self.post(endpoint="/qrs/custompropertydefinition", data=payload)

    def create_custom_properties(self, properties: list[dict]):
        """
        Creates multiple custom property definitions in a single API call.

        Uses the bulk endpoint POST /qrs/custompropertydefinition/many to create
        several custom property definitions at once. Each entry in the input
        list is expected to be a custom property definition dict as produced by
        models.custom_property_definition(). Already existing definitions and
        duplicates within the input list are filtered out (case-insensitive,
        by name). If no definitions remain after filtering, no request is sent.

        Args:
            properties (list[dict]): List of custom property definition dicts
                (e.g. produced by models.custom_property_definition()) to be
                created. Already existing names and duplicates within the list
                are skipped and logged as errors.

        Returns:
            list[dict]: JSON response from the API containing the created
                custom property definitions, or None if no new definitions
                remain to be created after filtering.
        """
        # Retrieve existing custom property definitions once
        existing_properties = self.get(endpoint="/qrs/custompropertydefinition")
        existing_names = {item["name"].lower() for item in existing_properties}

        # Filter new definitions and remove duplicates within the input
        seen = set()
        new_properties = []
        for prop in properties:
            name = prop.get("name")
            if not name:
                logger.error("Skipping custom property without a name: %s", prop)
                continue

            key = name.lower()
            if key in existing_names:
                logger.error("The custom property \"%s\" already exists!", name)
                continue
            if key in seen:
                logger.error("The custom property \"%s\" is duplicated in the input!", name)
                continue
            seen.add(key)

            # Forward the prebuilt definition as-is
            new_properties.append(prop)

        if not new_properties:
            logger.warning("No new custom properties to create.")
            return None

        # Serialize payload as JSON array
        payload = json.dumps(new_properties)
        # Execute API call to the /many endpoint
        return self.post(endpoint="/qrs/custompropertydefinition/many", data=payload)
