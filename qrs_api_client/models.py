from datetime import datetime


def reload_task_bundle(schema_path: str = None, task=None, composite_events: list = None, schema_events: list = None):

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


def reload_task_condensed(_id=None, privileges: list = None, name: str = None, task_type: int = None,
                          enabled: bool = None, task_session_timeout: int = None, max_retries: int = None,
                          operational=None, time_to_live: int = None):

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


def reload_task(_id=None, created_date=None, modified_date=None, modified_by_user_name: str = None,
                schema_path: str = None, privileges: list = None, custom_properties: list = None, name: str = None,
                task_type: int = None, enabled: bool = None, task_session_timeout: int = None, max_retries: int = None,
                tags: list = None, app=None, is_manually_triggered: bool = None, operational=None,
                is_partial_reload: bool = None, time_to_live: int = None, preload_nodes=None):

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


def app_condensed(_id=None, privileges: list = None, name: str = None, app_id: str = None, publish_time=None,
                  published: bool = None, stream=None, saved_in_product_version: str = None, migration_hash: str = None,
                  availability_status=None):
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


def schema_event_condensed(_id=None, privileges: list = None, name: str = None, enabled: bool = None,
                           event_type: int = None, operational=None):
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


def schema_event(_id=None, created_date=None, modified_date=None, modified_by_user_name: str = None,
                 schema_path: str = None, privileges: list = None, name: str = None, enabled: bool = None,
                 event_type: int = None, _reload_task=None, user_sync_task=None, external_program_task=None,
                 time_zone: str = None, daylight_saving_time: int = None, start_date: datetime = None,
                 expiration_date=None, schema_filter_description: list = None, increment_description: str = None,
                 increment_option: int = None, operational=None):
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


def custom_property_value(_id=None, created_date=None, modified_date=None, modified_by_user_name: str = None,
                          schema_path: str = None, value: str = None, definition=None):
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


def custom_property_definition_condensed(_id=None, privileges: list = None, name: str = None, value_type: str = None,
                                         choice_values=None):
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


def tag_condensed(_id=None, privileges: list = None, name: str = None):
    _tag_condensed = {}

    if _id is not None:
        _tag_condensed["id"] = _id

    if privileges is not None:
        _tag_condensed["privileges"] = privileges

    if name is not None:
        _tag_condensed["name"] = name

    return _tag_condensed


def composite_event(_id=None, created_date=None, modified_date=None, modified_by_user_name: str = None,
                    schema_path: str = None, privileges: list = None, name: str = None, enabled: bool = None,
                    event_type: int = None, _reload_task=None, user_sync_task=None, external_program_task=None,
                    time_constraint=None, composite_rules: list = None, operational=None):
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


def composite_event_rule(_id=None, created_date=None, modified_date=None, modified_by_user_name: str = None,
                         schema_path: str = None, rule_state: int = None, _reload_task=None, user_sync_task=None,
                         external_program_task=None, operational=None):
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


def composite_event_time_constraint(_id=None, created_date=None, modified_date=None, modified_by_user_name: str = None,
                                    schema_path: str = None, days: int = None, hours: int = None, minutes: int = None,
                                    seconds: int = None):
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
