from dataclasses import dataclass


@dataclass
class ElevatorColumns:
    ID: str = "id"
    CURRENT_FLOOR: str = "current_floor"
    DEMAND_FLOOR: str = "demand_floor"
    DESTINATION_FLOOR: str = "destination_floor"
    CALL_DATETIME: str = "call_datetime"
