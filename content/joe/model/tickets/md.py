"""File housing tickets used for requesting calculation
"""
# ======== standard imports ========
from dataclasses import dataclass
from datetime import datetime
# ==================================

# ======= third party imports ======
# ==================================

# ========= program imports ========
from joe.model.base import JourneyObject
from joe.model.astro import *
from joe.model.numerical import *
# ==================================


@dataclass
class PropagationTicket(JourneyObject):
    ''' A request for a propagation computation from Mission-Design '''
    # Required
    # Core
    start_time: datetime
    initial_orbit: Orbit
    maneuver: Maneuver
    physics: Physics

    # Objective
    groundstations: list[GroundStation]
    targets: list[Target]

    # Propagation
    propagator: Propagator
    status: Status

    # Satellite
    satellite: Satellite
    bus: Bus

    # Optionals

    # Physics
    attitude: Optional[Attitude] = None

    # Satellite
    propulsion: Optional[Propulsion] = None
    solarpanel: Optional[SolarPanel] = None
    battery: Optional[Battery] = None
    powerbudget: Optional[PowerBudget] = None
    payload: Optional[Payload] = None

    attribute_doc_strings = {
        "start_time": "Timestamp of when to start propagation",
        "initial_orbit": "Starting Orbit for propagation",
        "maneuver": "Maneuver to propagate",
        "physics": "Definition of physic models",
        "groundstations": "Groundstations to simulate connecting to",
        "targets": "Targets to simulate capturing",
        "propagator": "Propagator to use",
        "status": "Status of simulation",
        "satellite": "Satellite to propagate",
        "bus": "Satellite bus",
        "attitude": "Satellite attitude",
        "propulsion": "Satellite propulsion system",
        "solarpanel": "Satellite solar panels",
        "battery": "Satellite battery",
        "powerbudget": "Satellite power budget",
        "payload": "Satellite payload"
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "start_time": "2024-04-04T20:49:02",
        "initial_orbit": Orbit.example,
        "maneuver": Maneuver.example,
        "physics": Physics.example,
        "attitude": Attitude.example,

        "satellite": Satellite.example,
        "bus": Bus.example,
        "propulsion": Propulsion.example,
        "solarpanel": SolarPanel.example,
        "battery": Battery.example,
        "powerbudget": PowerBudget.example,
        "payload": Payload.example,

        "groundstations": [GroundStation.example],
        "targets": [Target.example],

        "propagator": Propagator.example,
        "status": Status.example
    }


@dataclass
class MultiManeuverTicket(JourneyObject):
    ''' A request for multiple maneuvers to be propagated in Mission-Design '''
    # Core
    start_time: datetime
    initial_orbit: Orbit
    maneuvers: list[Maneuver]
    physics: Physics

    # Objective
    groundstations: list[GroundStation]
    targets: list[Target]

    # Propagation
    propagator: Propagator
    status: Status

    # Satellite
    satellite: Satellite
    bus: Bus
    propulsion: Optional[Propulsion] = None
    solarpanel: Optional[SolarPanel] = None
    battery: Optional[Battery] = None
    powerbudget: Optional[PowerBudget] = None
    payload: Optional[Payload] = None

    attribute_doc_strings = {
        "start_time": "Timestamp of when to start propagation",
        "initial_orbit": "Starting Orbit for propagation",
        "maneuvers": "Maneuver to propagate",
        "physics": "Definition of physic models",
        "groundstations": "Groundstations to simulate connecting to",
        "targets": "Targets to simulate capturing",
        "propagator": "Propagator to use",
        "status": "Status of simulation",
        "satellite": "Satellite to propagate",
        "bus": "Satellite bus",
        "propulsion": "Satellite propulsion system",
        "solarpanel": "Satellite solar panels",
        "battery": "Satellite battery",
        "powerbudget": "Satellite power budget",
        "payload": "Satellite payload"
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "start_time": "2024-04-04T20:49:02",
        "initial_orbit": Orbit.example,
        "maneuvers": [Maneuver.example, Maneuver.example],
        "physics": Physics.example,

        "satellite": Satellite.example,
        "bus": Bus.example,
        "propulsion": Propulsion.example,
        "solarpanel": SolarPanel.example,
        "battery": Battery.example,
        "powerbudget": PowerBudget.example,
        "payload": Payload.example,

        "groundstations": [GroundStation.example],
        "targets": [Target.example],

        "propagator": Propagator.example,
        "status": Status.example
    }


@dataclass
class PropagationResult(JourneyObject):
    ''' A result of a propagation computation from Mission-Design '''

    timestamps: list[datetime]
    orbits: list[Orbit]
    masses: list[float]
    attitudes: list[Attitude]
    lighting_ratios: list[float]
    thrust_directions: list[list[float]]
    thrust_magnitudes: list[float]
    delta_v: list[float]
    total_impulse: list[float]
    groundstation_events: list[dict]
    target_events: list[dict]

    attribute_doc_strings = {
        "timestamps": "Times at which all other fields occured",
        "orbits": "",
        "masses": "",
        "attitudes": "",
        "lighting_ratios": "",
        "thrust_directions": "",
        "thrust_magnitudes": "",
        "delta_v": "",
        "total_impulse": "",
        "groundstation_events": "",
        "target_events": ""
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "timestamps": ["2024-04-04T20:49:02"],
        "orbits": [Orbit.example],
        "masses": [7.98],
        "attitudes": [Attitude.example],
        "lighting_ratios": [1.0],
        "thrust_directions": [[1.0, 0.0, 0.0]],
        "thrust_magnitudes": [1.0],
        "delta_v": [1.0],
        "total_impulse": [1.0],
        "groundstation_events": [{}],
        "target_events": [{}]
    }

    def __len__(self):
        return len(self.timestamps)
