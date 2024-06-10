"""File housing user flows
"""
# ======== standard imports ========
from dataclasses import dataclass
from datetime import datetime
# ==================================

# ======= third party imports ======
# ==================================

# ========= program imports ========
from joe.model.base import JourneyObject
from joe.model.other import Mission
# ==================================


# TODO: Define what this will mutate into in the future
@dataclass
class Simulation(JourneyObject):
    ''' Simulations define simulation runs of a Mission '''
    mission: Mission
    status: str
    engine: str
    simulation_payload: str
    start_time: datetime
    update_time: datetime
    finish_time: datetime
    results: dict

    attribute_doc_strings = {
        "mission": "Mission for this Simulation",
        "status": "Simulation status: None, STARTED, RUNNING, COMPLETED",
        "engine": "Preliminary (PMD) or Advanced Mission-Design (AMD)",
        "simulation_payload": "JSON Payload for Mission-Design",
        "start_time": "Timestamp of starting time",
        "update_time": "Timestamp of the last update to the simulation",
        "finish_time": "Timestamp of simulation completion",
        "results": "JSON of simulation result object"
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "mission": Mission.example,
        "status": "Complete",
        "engine": "PMD",
        "simulation_payload": '{"foo": "bar"}',
        "start_time": "2024-04-04T20:49:02",
        "update_time": "2024-04-04T20:49:02",
        "finish_time": "2024-04-04T20:49:02",
        "results": {}
    }
