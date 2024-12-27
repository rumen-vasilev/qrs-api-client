from qrs_api_client.client import QRSClient
import qrs_api_client.models as models
from dotenv import load_dotenv
import os

# Loads environment variables from .env file.
load_dotenv()

# Authenticates on the enterprise server (Cert paths are called from the .env file)
client = QRSClient(server_name=os.getenv("SERVER_NAME"), server_port=os.getenv("SERVER_PORT"),
                   auth_method="certificate", verify_ssl=True)


# Constructs the method parameters
tags = ["3917ffe9-4ded-4b7d-9eee-c9bad89f38b7", "4c6d23bb-21de-4bfc-9c94-7bbe0e795e4c"]
custom_properties = {"a917996a-c052-4ebb-b54b-a080c5e57517": ["1", "2"],
                     "d033b8e6-275d-4715-bb3b-d40082ac58c4": ["2", "5"]}

schema_event_1 = models.schema_event(increment_description="0 0 1 0", time_zone="Europe/Paris", increment_option=3,
                                     schema_filter_description=["* * - 0 1 * * *"], daylight_saving_time=0,
                                     name="Schema Event 1", start_date="2024-01-23T04:56:00.000Z",
                                     expiration_date="9999-01-01T00:00:00.000Z")
schema_event_2 = models.schema_event(increment_description="0 0 1 0", time_zone="Europe/Paris", increment_option=3,
                                     schema_filter_description=["* * - 0 1 * * *"], daylight_saving_time=0,
                                     name="Schema Event 2", start_date="2024-01-23T04:56:00.000Z",
                                     expiration_date="9999-01-01T00:00:00.000Z")
schema_events = [schema_event_1, schema_event_2]


reload_task_1_1 = models.reload_task(_id="4496ca4a-8725-482d-ba52-72e3b860c4e2")
reload_task_1_2 = models.reload_task(_id="784e63b0-7d4c-435b-96d1-423410e16301")
composite_event_rule_1_1 = models.composite_event_rule(rule_state=1, _reload_task=reload_task_1_1)
composite_event_rule_1_2 = models.composite_event_rule(rule_state=1, _reload_task=reload_task_1_2)
composite_event_rules_1 = [composite_event_rule_1_1, composite_event_rule_1_2]
composite_event_time_constraint_1 = models.composite_event_time_constraint(seconds=0, minutes=120, hours=0, days=0)
composite_event_1 = models.composite_event(name="Composite Event 1", event_type=1,
                                           composite_rules=composite_event_rules_1,
                                           time_constraint=composite_event_time_constraint_1)

reload_task_2_1 = models.reload_task(_id="4496ca4a-8725-482d-ba52-72e3b860c4e2")
reload_task_2_2 = models.reload_task(_id="784e63b0-7d4c-435b-96d1-423410e16301")
composite_event_rule_2_1 = models.composite_event_rule(rule_state=1, _reload_task=reload_task_2_1)
composite_event_rule_2_2 = models.composite_event_rule(rule_state=1, _reload_task=reload_task_2_2)
composite_event_rules_2 = [composite_event_rule_2_1, composite_event_rule_2_2]
composite_event_time_constraint_2 = models.composite_event_time_constraint(seconds=0, minutes=120, hours=0, days=0)
composite_event_2 = models.composite_event(name="Composite Event 2", event_type=1,
                                           composite_rules=composite_event_rules_1,
                                           time_constraint=composite_event_time_constraint_1)

composite_events = [composite_event_1, composite_event_2]

# Creating reload task
reloadtask_create = client.reloadtask_create(app_id="4cb45d72-1428-410b-a36d-208f9fdc59cb",
                                                    task_name="API generated reload task",
                                                    custom_properties=custom_properties, tags=tags,
                                                    composite_events=composite_events, schema_events=schema_events)

if reloadtask_create:
    print("Reload task created:", reloadtask_create)
else:
    print("API request error.")
