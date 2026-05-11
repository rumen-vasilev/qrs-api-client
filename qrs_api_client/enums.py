"""
Enumerations and constant values defined by the Qlik Sense Repository
Service (QRS) API. Centralized here so that client code can compare API
response fields against named values rather than magic numbers / strings.
"""
from enum import IntEnum


class ExecutionStatus(IntEnum):
    """
    Qlik Sense Repository Service execution result status codes.

    Used in the ExecutionResult schema (e.g. on /qrs/executionresult,
    /qrs/reloadtask/{id}/operational/lastExecutionResult) to indicate the
    progress and outcome of a task execution. See /qrs/about/api/enums on
    your QRS instance for the authoritative list.
    """
    NEVER_STARTED = 0
    TRIGGERED = 1
    STARTED = 2
    QUEUED = 3
    ABORT_INITIATED = 4
    ABORTING = 5
    ABORTED = 6
    FINISHED_SUCCESS = 7
    FINISHED_FAIL = 8
    SKIPPED = 9
    RETRY = 10
    ERROR = 11
    RESET = 12

    @classmethod
    def terminal_statuses(cls) -> frozenset:
        """
        Returns the set of statuses that indicate a finished execution
        (successful or not), i.e. the execution will no longer change state.
        """
        return frozenset({
            cls.ABORTED,
            cls.FINISHED_SUCCESS,
            cls.FINISHED_FAIL,
            cls.SKIPPED,
            cls.ERROR,
        })


# .NET DateTime.MinValue serialized to ISO 8601 - used by Qlik as a sentinel
# value for timestamp fields like stopTime/nextExecution when no value has
# been set yet.
DOTNET_MIN_DATETIME = "1753-01-01T00:00:00.000Z"
