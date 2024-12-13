from datetime import datetime
import uuid


def reload_task_bundle(schema_path: str = None, task=None, composite_events: list = None, schema_events: list = None):
    """Creates a dictionary representing a reload task bundle.

    Args:
        schema_path (str, optional): The path to the schema.
        task (dict, optional): The task data.
        composite_events (list, optional): A list of composite events.
        schema_events (list, optional): A list of schema events.

    Returns:
        dict: A dictionary containing the reload task bundle data.
    """
    _reload_task_bundle = {}

    if schema_path is not None:
        _reload_task_bundle["schemaPath"] = schema_path

    if task is None:
        _reload_task_bundle["task"] = {}
    else:
        _reload_task_bundle["task"] = task

    if composite_events is not None:
        _reload_task_bundle["compositeEvents"] = composite_events

    if schema_events is not None:
        _reload_task_bundle["schemaEvents"] = schema_events

    return _reload_task_bundle


def reload_task_condensed(_id: uuid.UUID = None, privileges: list = None, name: str = None, task_type: int = None,
                          enabled: bool = None, task_session_timeout: int = None, max_retries: int = None,
                          operational=None, time_to_live: int = None):
    """Creates a dictionary representing a condensed reload task.

    Args:
        _id (uuid.UUID, optional): The unique identifier of the task.
        privileges (list, optional): A list of privileges associated with the task.
        name (str, optional): The name of the task.
        task_type (int, optional): The type of task.
        enabled (bool, optional): Whether the task is enabled.
        task_session_timeout (int, optional): The task session timeout in seconds.
        max_retries (int, optional): The maximum number of retries allowed.
        operational (dict, optional): Operational details.
        time_to_live (int, optional): The time-to-live value for the task.

    Returns:
        dict: A dictionary containing the condensed reload task data.
    """
    _reload_task_condensed = {}

    if _id is not None:
        _reload_task_condensed["id"] = _id

    if privileges is not None:
        _reload_task_condensed["privileges"] = privileges

    if name is None:
        _reload_task_condensed["name"] = ""
    else:
        _reload_task_condensed["name"] = name

    if task_type is not None:
        _reload_task_condensed["taskType"] = task_type

    if enabled is not None:
        _reload_task_condensed["enabled"] = enabled

    if task_session_timeout is not None:
        _reload_task_condensed["taskSessionTimeout"] = task_session_timeout

    if max_retries is not None:
        _reload_task_condensed["maxRetries"] = max_retries

    if operational is not None:
        _reload_task_condensed["operational"] = operational

    if time_to_live is not None:
        _reload_task_condensed["timeToLive"] = time_to_live

    return _reload_task_condensed


def reload_task(_id: uuid.UUID = None, created_date: datetime = None, modified_date: datetime = None,
                modified_by_user_name: str = None, schema_path: str = None, privileges: list = None,
                custom_properties: list = None, name: str = None, task_type: int = None, enabled: bool = None,
                task_session_timeout: int = None, max_retries: int = None, tags: list = None, app=None,
                is_manually_triggered: bool = None, operational=None, is_partial_reload: bool = None,
                time_to_live: int = None, preload_nodes=None):
    """Creates a dictionary representing a reload task.

    Args:
        _id (uuid.UUID, optional): The unique identifier of the task.
        created_date (datetime, optional): The creation date of the task.
        modified_date (datetime, optional): The modification date of the task.
        modified_by_user_name (str, optional): The username of the person who modified the task.
        schema_path (str, optional): The path to the schema.
        privileges (list, optional): A list of privileges associated with the task.
        custom_properties (list, optional): Custom properties of the task.
        name (str, optional): The name of the task.
        task_type (int, optional): The type of task.
        enabled (bool, optional): Whether the task is enabled.
        task_session_timeout (int, optional): The task session timeout in seconds.
        max_retries (int, optional): The maximum number of retries allowed.
        tags (list, optional): A list of tags associated with the task.
        app (dict, optional): Application-specific data.
        is_manually_triggered (bool, optional): Whether the task is manually triggered.
        operational (dict, optional): Operational details.
        is_partial_reload (bool, optional): Whether the task supports partial reload.
        time_to_live (int, optional): The time-to-live value for the task.
        preload_nodes (list, optional): A list of preload nodes.

    Returns:
        dict: A dictionary containing the reload task data.
    """
    _reload_task = {}

    if _id is not None:
        _reload_task["id"] = _id

    if created_date is not None:
        _reload_task["createdDate"] = created_date

    if modified_date is not None:
        _reload_task["modifiedDate"] = modified_date

    if modified_by_user_name is not None:
        _reload_task["modifiedByUserName"] = modified_by_user_name

    if schema_path is not None:
        _reload_task["schemaPath"] = schema_path

    if privileges is not None:
        _reload_task["privileges"] = privileges

    if custom_properties is not None:
        _reload_task["customProperties"] = custom_properties

    if name is None:
        _reload_task["name"] = ""
    else:
        _reload_task["name"] = name

    if task_type is not None:
        _reload_task["taskType"] = task_type

    if enabled is not None:
        _reload_task["enabled"] = enabled

    if task_session_timeout is not None:
        _reload_task["taskSessionTimeout"] = task_session_timeout

    if max_retries is not None:
        _reload_task["maxRetries"] = max_retries

    if tags is not None:
        _reload_task["tags"] = tags

    if app is None:
        _reload_task["app"] = {}
    else:
        _reload_task["app"] = app

    if is_manually_triggered is not None:
        _reload_task["isManuallyTriggered"] = is_manually_triggered

    if operational is not None:
        _reload_task["operational"] = operational

    if is_partial_reload is not None:
        _reload_task["isPartialReload"] = is_partial_reload

    if time_to_live is not None:
        _reload_task["timeToLive"] = time_to_live

    if preload_nodes is not None:
        _reload_task["preloadNodes"] = preload_nodes

    return _reload_task


def app_condensed(_id: uuid.UUID = None, privileges: list = None, name: str = None, app_id: str = None,
                  publish_time: datetime = None, published: bool = None, stream=None,
                  saved_in_product_version: str = None, migration_hash: str = None, availability_status=None):
    """
    Creates a condensed representation of an application.

    Args:
        _id (uuid.UUID, optional): Unique identifier of the application.
        privileges (list, optional): List of privileges.
        name (str, optional): Name of the application.
        app_id (str, optional): Application ID.
        publish_time (datetime, optional): Publish time of the application.
        published (bool, optional): Whether the application is published.
        stream (optional): Stream information.
        saved_in_product_version (str, optional): Product version in which the application was saved.
        migration_hash (str, optional): Migration hash for version control.
        availability_status (optional): Availability status of the application.

    Returns:
        dict: Condensed application representation.
    """
    _app_condensed = {}

    if _id is not None:
        _app_condensed["id"] = _id

    if privileges is not None:
        _app_condensed["privileges"] = privileges

    if name is not None:
        _app_condensed["name"] = name

    if app_id is not None:
        _app_condensed["appId"] = app_id

    if publish_time is not None:
        _app_condensed["publishTime"] = publish_time

    if published is not None:
        _app_condensed["published"] = published

    if stream is not None:
        _app_condensed["stream"] = stream

    if saved_in_product_version is not None:
        _app_condensed["savedInProductVersion"] = saved_in_product_version

    if migration_hash is not None:
        _app_condensed["migrationHash"] = migration_hash

    if availability_status is not None:
        _app_condensed["availabilityStatus"] = availability_status

    return _app_condensed


def schema_event_condensed(_id: uuid.UUID = None, privileges: list = None, name: str = None, enabled: bool = None,
                           event_type: int = None, operational=None):
    """
    Creates a condensed representation of a schema event.

    Args:
        _id (uuid.UUID, optional): Unique identifier of the schema event.
        privileges (list, optional): List of privileges.
        name (str, optional): Name of the schema event.
        enabled (bool, optional): Whether the schema event is enabled.
        event_type (int, optional): Type of the event.
        operational (optional): Operational status or configuration.

    Returns:
        dict: Condensed schema event representation.
    """
    _schema_event_condensed = {}

    if _id is not None:
        _schema_event_condensed["id"] = _id

    if privileges is not None:
        _schema_event_condensed["privileges"] = privileges

    if name is None:
        _schema_event_condensed["name"] = ""
    else:
        _schema_event_condensed["name"] = name

    if enabled is not None:
        _schema_event_condensed["enabled"] = enabled

    if event_type is not None:
        _schema_event_condensed["eventType"] = event_type

    if operational is not None:
        _schema_event_condensed["operational"] = operational

    return _schema_event_condensed


def schema_event(_id: uuid.UUID = None, created_date: datetime = None, modified_date: datetime = None,
                 modified_by_user_name: str = None,
                 schema_path: str = None, privileges: list = None, name: str = None, enabled: bool = None,
                 event_type: int = None, _reload_task=None, user_sync_task=None, external_program_task=None,
                 time_zone: str = None, daylight_saving_time: int = None, start_date: datetime = None,
                 expiration_date: datetime = None, schema_filter_description: list = None,
                 increment_description: str = None, increment_option: int = None, operational=None):
    """
    Creates a detailed representation of a schema event.

    Args:
        _id (uuid.UUID, optional): Unique identifier of the schema event.
        created_date (datetime, optional): Creation date of the schema event.
        modified_date (datetime, optional): Last modification date of the schema event.
        modified_by_user_name (str, optional): Username of the person who modified the schema event.
        schema_path (str, optional): Schema path of the event.
        privileges (list, optional): List of privileges.
        name (str, optional): Name of the schema event.
        enabled (bool, optional): Whether the schema event is enabled.
        event_type (int, optional): Type of the schema event.
        _reload_task (optional): Reload task information.
        user_sync_task (optional): User synchronization task information.
        external_program_task (optional): External program task information.
        time_zone (str, optional): Time zone of the schema event.
        daylight_saving_time (int, optional): Daylight saving time offset.
        start_date (datetime, optional): Start date of the schema event.
        expiration_date (datetime, optional): Expiration date of the schema event.
        schema_filter_description (list, optional): Description of schema filters.
        increment_description (str, optional): Description of increments.
        increment_option (int, optional): Increment option.
        operational (optional): Operational status or configuration.

    Returns:
        dict: Detailed schema event representation.
    """
    _schema_event = {}

    if _id is not None:
        _schema_event["id"] = _id

    if created_date is not None:
        _schema_event["createdDate"] = created_date

    if modified_date is not None:
        _schema_event["modifiedDate"] = modified_date

    if modified_by_user_name is not None:
        _schema_event["modifiedByUserName"] = modified_by_user_name

    if schema_path is not None:
        _schema_event["schemaPath"] = schema_path

    if privileges is not None:
        _schema_event["privileges"] = privileges

    if name is None:
        _schema_event["name"] = ""
    else:
        _schema_event["name"] = name

    if enabled is not None:
        _schema_event["enabled"] = enabled

    if event_type is not None:
        _schema_event["eventType"] = event_type

    if _reload_task is not None:
        _schema_event["reloadTask"] = _reload_task

    if user_sync_task is not None:
        _schema_event["userSyncTask"] = user_sync_task

    if external_program_task is not None:
        _schema_event["externalProgramTask"] = external_program_task

    if time_zone is not None:
        _schema_event["timeZone"] = time_zone

    if daylight_saving_time is not None:
        _schema_event["daylightSavingTime"] = daylight_saving_time

    if start_date is not None:
        _schema_event["startDate"] = start_date

    if expiration_date is not None:
        _schema_event["expirationDate"] = expiration_date

    if schema_filter_description is not None:
        _schema_event["schemaFilterDescription"] = schema_filter_description

    if increment_description is not None:
        _schema_event["incrementDescription"] = increment_description

    if increment_option is not None:
        _schema_event["incrementOption"] = increment_option

    if operational is not None:
        _schema_event["operational"] = operational

    return _schema_event


def custom_property_value(_id: uuid.UUID = None, created_date: datetime = None, modified_date: datetime = None,
                          modified_by_user_name: str = None, schema_path: str = None, value: str = None,
                          definition=None):
    """
    Creates a dictionary representing a custom property value.

    Args:
        _id (uuid.UUID, optional): The unique identifier for the custom property value.
        created_date (datetime, optional): The date the property was created.
        modified_date (datetime, optional): The date the property was last modified.
        modified_by_user_name (str, optional): The username of the person who last modified the property.
        schema_path (str, optional): The schema path for the custom property.
        value (str, optional): The value of the custom property. Defaults to an empty string if not provided.
        definition (optional): The definition of the custom property.

    Returns:
        dict: A dictionary representing the custom property value.
    """
    _custom_property_value = {}

    if _id is not None:
        _custom_property_value["id"] = _id

    if created_date is not None:
        _custom_property_value["createdDate"] = created_date

    if modified_date is not None:
        _custom_property_value["modifiedDate"] = modified_date

    if modified_by_user_name is not None:
        _custom_property_value["modifiedByUserName"] = modified_by_user_name

    if schema_path is not None:
        _custom_property_value["schemaPath"] = schema_path

    if value is None:
        _custom_property_value["value"] = ""
    else:
        _custom_property_value["value"] = value

    if definition is None:
        _custom_property_value["definition"] = ""
    else:
        _custom_property_value["definition"] = definition

    return _custom_property_value


def custom_property_definition_condensed(_id: uuid.UUID = None, privileges: list = None, name: str = None,
                                         value_type: str = None, choice_values=None):
    """
    Creates a dictionary representing a condensed custom property definition.

    Args:
        _id (uuid.UUID, optional): The unique identifier for the property definition.
        privileges (list, optional): A list of privileges associated with the property.
        name (str, optional): The name of the property definition.
        value_type (str, optional): The type of value the property accepts.
        choice_values (optional): Possible values for the property.

    Returns:
        dict: A dictionary representing the custom property definition.
    """
    _custom_property_definition_condensed = {}

    if _id is not None:
        _custom_property_definition_condensed["id"] = _id

    if privileges is not None:
        _custom_property_definition_condensed["privileges"] = privileges

    if name is not None:
        _custom_property_definition_condensed["name"] = name

    if value_type is not None:
        _custom_property_definition_condensed["valueType"] = value_type

    if choice_values is not None:
        _custom_property_definition_condensed["choiceValues"] = choice_values

    return _custom_property_definition_condensed


def tag_condensed(_id: uuid.UUID = None, privileges: list = None, name: str = None):
    """
    Creates a dictionary representing a condensed tag.

    Args:
        _id (uuid.UUID, optional): The unique identifier for the tag.
        privileges (list, optional): A list of privileges associated with the tag.
        name (str, optional): The name of the tag.

    Returns:
        dict: A dictionary representing the tag.
    """
    _tag_condensed = {}

    if _id is not None:
        _tag_condensed["id"] = _id

    if privileges is not None:
        _tag_condensed["privileges"] = privileges

    if name is not None:
        _tag_condensed["name"] = name

    return _tag_condensed


def composite_event(_id: uuid.UUID = None, created_date: datetime = None, modified_date: datetime = None,
                    modified_by_user_name: str = None,
                    schema_path: str = None, privileges: list = None, name: str = None, enabled: bool = None,
                    event_type: int = None, _reload_task=None, user_sync_task=None, external_program_task=None,
                    time_constraint=None, composite_rules: list = None, operational=None):
    """
    Creates a dictionary representing a composite event.

    Args:
        _id (uuid.UUID, optional): The unique identifier for the event.
        created_date (datetime, optional): The date the event was created.
        modified_date (datetime, optional): The date the event was last modified.
        modified_by_user_name (str, optional): The username of the person who last modified the event.
        schema_path (str, optional): The schema path for the event.
        privileges (list, optional): A list of privileges associated with the event.
        name (str, optional): The name of the event. Defaults to an empty string if not provided.
        enabled (bool, optional): Whether the event is enabled.
        event_type (int, optional): The type of event.
        _reload_task (optional): The reload task associated with the event.
        user_sync_task (optional): The user synchronization task associated with the event.
        external_program_task (optional): The external program task associated with the event.
        time_constraint (optional): The time constraint for the event.
        composite_rules (list, optional): A list of composite rules for the event.
        operational (optional): Operational status of the event.

    Returns:
        dict: A dictionary representing the composite event.
    """
    _composite_event = {}

    if _id is not None:
        _composite_event["id"] = _id

    if created_date is not None:
        _composite_event["createdDate"] = created_date

    if modified_date is not None:
        _composite_event["modifiedDate"] = modified_date

    if modified_by_user_name is not None:
        _composite_event["modifiedByUserName"] = modified_by_user_name

    if schema_path is not None:
        _composite_event["schemaPath"] = schema_path

    if privileges is not None:
        _composite_event["privileges"] = privileges

    if name is None:
        _composite_event["name"] = ""
    else:
        _composite_event["name"] = name

    if enabled is not None:
        _composite_event["enabled"] = enabled

    if event_type is not None:
        _composite_event["eventType"] = event_type

    if _reload_task is not None:
        _composite_event["reloadTask"] = _reload_task

    if user_sync_task is not None:
        _composite_event["userSyncTask"] = user_sync_task

    if external_program_task is not None:
        _composite_event["externalProgramTask"] = external_program_task

    if time_constraint is not None:
        _composite_event["timeConstraint"] = time_constraint

    if composite_rules is not None:
        _composite_event["compositeRules"] = composite_rules

    if operational is not None:
        _composite_event["operational"] = operational

    return _composite_event


def composite_event_rule(_id: uuid.UUID = None, created_date: datetime = None, modified_date: datetime = None,
                         modified_by_user_name: str = None,
                         schema_path: str = None, rule_state: int = None, _reload_task=None, user_sync_task=None,
                         external_program_task=None, operational=None):
    """
    Creates a dictionary representing a composite event rule.

    Args:
        _id (uuid.UUID, optional): The unique identifier for the composite event rule.
        created_date (datetime, optional): The date the rule was created.
        modified_date (datetime, optional): The date the rule was last modified.
        modified_by_user_name (str, optional): The username of the person who last modified the rule.
        schema_path (str, optional): The schema path for the rule.
        rule_state (int, optional): The state of the rule.
        _reload_task (optional): The reload task associated with the rule.
        user_sync_task (optional): The user synchronization task associated with the rule.
        external_program_task (optional): The external program task associated with the rule.
        operational (optional): Operational status of the rule.

    Returns:
        dict: A dictionary representing the composite event rule.
    """
    _composite_event_rule = {}

    if _id is not None:
        _composite_event_rule["id"] = _id

    if created_date is not None:
        _composite_event_rule["createdDate"] = created_date

    if modified_date is not None:
        _composite_event_rule["modifiedDate"] = modified_date

    if modified_by_user_name is not None:
        _composite_event_rule["modifiedByUserName"] = modified_by_user_name

    if schema_path is not None:
        _composite_event_rule["schemaPath"] = schema_path

    if rule_state is not None:
        _composite_event_rule["ruleState"] = rule_state

    if _reload_task is not None:
        _composite_event_rule["reloadTask"] = _reload_task

    if user_sync_task is not None:
        _composite_event_rule["userSyncTask"] = user_sync_task

    if external_program_task is not None:
        _composite_event_rule["externalProgramTask"] = external_program_task

    if operational is not None:
        _composite_event_rule["operational"] = operational

    return _composite_event_rule


def composite_event_time_constraint(_id: uuid.UUID = None, created_date: datetime = None,
                                    modified_date: datetime = None, modified_by_user_name: str = None,
                                    schema_path: str = None, days: int = None, hours: int = None, minutes: int = None,
                                    seconds: int = None):
    """
    Creates a dictionary representing a time constraint for a composite event.

    Args:
        _id (uuid.UUID, optional): The unique identifier for the time constraint.
        created_date (datetime, optional): The date the time constraint was created.
        modified_date (datetime, optional): The date the time constraint was last modified.
        modified_by_user_name (str, optional): The username of the person who last modified the time constraint.
        schema_path (str, optional): The schema path for the time constraint.
        days (int, optional): The number of days in the time constraint.
        hours (int, optional): The number of hours in the time constraint.
        minutes (int, optional): The number of minutes in the time constraint.
        seconds (int, optional): The number of seconds in the time constraint.

    Returns:
        dict: A dictionary representing the composite event time constraint.
    """
    _composite_event_time_constraint = {}

    if _id is not None:
        _composite_event_time_constraint["id"] = _id

    if created_date is not None:
        _composite_event_time_constraint["createdDate"] = created_date

    if modified_date is not None:
        _composite_event_time_constraint["modifiedDate"] = modified_date

    if modified_by_user_name is not None:
        _composite_event_time_constraint["modifiedByUserName"] = modified_by_user_name

    if schema_path is not None:
        _composite_event_time_constraint["schemaPath"] = schema_path

    if days is not None:
        _composite_event_time_constraint["days"] = days

    if hours is not None:
        _composite_event_time_constraint["hours"] = hours

    if minutes is not None:
        _composite_event_time_constraint["minutes"] = minutes

    if seconds is not None:
        _composite_event_time_constraint["seconds"] = seconds

    return _composite_event_time_constraint
