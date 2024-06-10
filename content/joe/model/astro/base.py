"""File housing classes for Astrodynamics concepts
"""
# ======== standard imports ========
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
# ==================================

# ======= third party imports ======
# ==================================

# ========= program imports ========
from joe.model.base import JourneyObject
from joe.model.other import Mission
# ==================================

@dataclass
class Physics(JourneyObject):
    ''' Physics define the method of simulation for a Mission '''

    class GravityModel(Enum):
        """ Model for Gravity """
        EIGEN6S = "EIGEN-6S"
        GGM02C = "GGM02C"
        GGM03S = "GGM03S"
        GGM03C = "GGM03C"

    class AtmosphericModel(Enum):
        """ Model for Gravity """
        OFF = "Off"
        NRLMSISE00 = "NRLMSISE-00"
        JB2008 = "JB2008"
        HARRISPRIESTER = "Harris-Priester"

    class ThirdBodyModel(Enum):
        """ Third Body Model """
        NONE = "None"
        SUNMOON = "sunmoon"
        ALL = "all"

    mission: Mission
    start_time: datetime
    gravity_model: GravityModel
    atmospheric_model: AtmosphericModel
    third_body_model: ThirdBodyModel
    solar_radiation_model: bool
    harmonic_degree: int
    harmonic_order: int

    attribute_doc_strings = {
        "mission": "Mission utilizing these Physics settings",
        "start_time": "The starting date for a Simulation",
        "gravity_model": "Gravity Model to use in a Simulation",
        "atmospheric_model": "Atmospheric Drag Model to use in a Simulation",
        "third_body_model": "???",
        "solar_radiation_model": "Whether or not to use the Solar Radiation Model",
        "harmonic_degree": "???",
        "harmonic_order": "???"
    }

    def validate_gravity_model(self):
        assert self.gravity_model in self.GravityModel, f"Unrecognized Gravity Model: {self.gravity_model}"

    def validate_atmospheric_model(self):
        assert self.atmospheric_model in self.AtmosphericModel, f"Unrecognized Atmospheric Model {self.atmospheric_model}"

    def validate_third_body(self):
        assert self.third_body_model in self.ThirdBodyModel, f"Unrecognized Third Body Model {self.third_body_model}"

    def validate_harmonic_degree(self):
        assert 0 <= self.harmonic_degree <= 180

    def validate_harmonic_order(self):
        assert 0 <= self.harmonic_order <= 180

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "mission": Mission.example,
        "start_time": "2024-04-04T20:49:02",
        "gravity_model": "EIGEN-6S",
        "atmospheric_model": "NRLMSISE-00",
        "third_body_model": "all",
        "solar_radiation_model": True,
        "harmonic_degree": 0,
        "harmonic_order": 2
    }


@dataclass
class Target(JourneyObject):
    ''' Targets are locations a Satellite is attempting to observer during a Misison '''
    mission: Mission
    name: str
    latitude: float
    longitude: float
    minimum_elevation: float  # minimum degrees of elevation above the horizon for acquiring target
    altitude: float
    shapefile: Optional[str]

    attribute_doc_strings = {
        "mission": "Mission utilizing this Target",
        "name": "Name of target",
        "latitude": "Latitude of target in degrees",
        "longitude": "Longitude of target in degrees",
        "minimum_elevation": "Minimum elevation angle of target in degrees",
        "altitude": "Altitude of target in kilometers",
        "shapefile": "Polygon definition of a Target Area rather than a single (lat, lon) position"
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "mission": Mission.example,
        "name": "MyTarget6",
        "latitude": 20.3,
        "longitude": 33.5,
        "minimum_elevation": 65.0,
        "altitude": 12.5,
        "shapefile": None
    }


@dataclass
class GroundStation(JourneyObject):
    ''' Ground Stations are locations capable of transmitting to a Satellite '''
    mission: Mission
    name: str
    latitude: float
    longitude: float
    minimum_elevation: float
    altitude: float
    provider: str

    attribute_doc_strings = {
        "mission": "Mission utilizing this groundstation",
        "name": "Name of groundstation",
        "latitude": "Latitude of groundstation in degrees",
        "longitude": "Longitude of groundstation in degrees",
        "minimum_elevation": "Minimum elevation angle of groundstation in degrees",
        "altitude": "Altitude of groundstation in kilometers",
        "provider": "Provider of GroundStation"
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "mission": Mission.example,
        "name": "GroundStation5",
        "latitude": 20.3,
        "longitude": 33.5,
        "minimum_elevation": 65.0,
        "altitude": 12.5,
        "provider": "FSAT"
    }


@dataclass
class Orbit(JourneyObject):
    ''' Orbits define an orbital state for a body '''
    semi_major_axis: float | None
    eccentricity: float | None
    inclination: float | None
    argument_of_perigee: float | None
    raan: float | None
    true_anomaly: float | None

    def validate_eccentricity(self):
        assert self.eccentricity is None or 0 <= self.eccentricity <= 1, f"Invalid eccentricity value: {self.eccentricity}"

    def validate_inclination(self):
        assert self.inclination is None or 0 <= self.inclination <= 180, f"Invalid inclination value: {self.inclination}"

    def validate_true_anomaly(self):
        assert self.true_anomaly is None or 0 <= self.true_anomaly <= 360, f"Invalid true_anomaly value: {self.true_anomaly}"

    def validate_argument_of_perigee(self):
        assert self.argument_of_perigee is None or 0 <= self.argument_of_perigee <= 360, f"Invalid argument_of_perigee value: {self.argument_of_perigee}"

    @property
    def orbital_elements(self):
        return (self.semi_major_axis, self.eccentricity, self.inclination, self.argument_of_perigee, self.raan, self.true_anomaly)

    attribute_doc_strings = {
        "semi_major_axis": "Distance from the center of the Earth, in kilometers",
        "eccentricity": "Shape of orbit ellipse, between 0 (circular) and 1 (hyperbola)",
        "inclination": "Vertical tilt of orbit relative to equator, in degrees",
        "argument_of_perigee": "???, in degrees",
        "raan": "??? in degrees",
        "true_anomaly": "??? in degrees"
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "semi_major_axis": 7200.0,
        "eccentricity": 0.001,
        "inclination": 85.3,
        "argument_of_perigee": 6.29,
        "raan": 260.74,
        "true_anomaly": 0.0
    }

    ORBIT_TEMPLATES = {
        "LEO": {
            "semi_major_axis": 6778.137,
            "eccentricity": 0.0005703,
            "inclination": 51.6405,
            "argument_of_perigee": 6.2897,
            "raan": 260.7437,
            "true_anomaly": 0.0
        },
        "SSO-LEO": {
            "semi_major_axis": 7083.137,
            "eccentricity": 0,
            "inclination": 98.2,
            "argument_of_perigee": 0,
            "raan": 0,
            "true_anomaly": 0.0
        },
        "MEO": {
            "semi_major_axis": 9378.137,
            "eccentricity": 0.001,
            "inclination": 30,
            "argument_of_perigee": 0,
            "raan": 0,
            "true_anomaly": 0.0
        },
        "GEO": {
            "semi_major_axis": 7200.0,
            "eccentricity": 0.001,
            "inclination": 85.3,
            "argument_of_perigee": 6.29,
            "raan": 260.74,
            "true_anomaly": 0.0
        }
    }


@dataclass
class Attitude(JourneyObject):
    ''' The rotation between a reference frame and the satellite frame, as well as the spin of the satellite (axis and rotation rate) '''
    # frame: Enum but not necessary at the moment
    quaternions: list[float]
    spin: list[float]
    acceleration: list[float]

    #def validate_quaternions(self):
    #    assert len(self.quaternions) == 4, f"Invalid quaternions: {self.quaternions}"

    #def validate_spin(self):
    #    assert len(self.rotation_matrix) == 3, f"Invalid spin: {self.spin}"

    #def validate_acceleration(self):
    #    assert len(self.rotation_matrix) == 3, f"Invalid acceleration: {self.acceleration}"

    attribute_doc_strings = {
        "quaternions": "Quaterions",
        "spin": "Shape of orbit ellipse, between 0 (circular) and 1 (hyperbola)",
        "acceleration": "Acceleration of rotation",
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "quaternions": [0.0] * 4,  # Please don't actually use this
        "spin": [0.0] * 3,  # Please don't actually use this
        "acceleration": [0.0]  # Please don't actually use this
    }


@dataclass
class Maneuver(JourneyObject):
    ''' Maneuvers transition a Satellite from one Orbit to another '''
    class ManeuverType(Enum):
        ANALYTICAL = "analytical"
        MAINTENANCE = "maintenance"
        DRIFT = "drift"
        DEORBIT = "deorbit"
        PHASE = 'phase'

    mission: Mission
    maneuver_type: ManeuverType
    final_orbit: Orbit
    name: str
    optimize: bool
    duration: float
    sequence_number: int

    def maneuver_function(current_orbit: Orbit):
        """
        Given the current Satellite position, this function serves to
        produce the thrust in the satellite RTN frame.
        """
        raise NotImplementedError()

    def is_maneuver_manually_implemented(self):
        try:
            self.maneuver_function(Orbit(**Orbit.example))
            return True
        except NotImplementedError:
            return False

    attribute_doc_strings = {
        "mission": "",
        "maneuver_type": f"Maneuver classification, one of {ManeuverType._member_names_}",
        "final_orbit": "Target orbit at the conclusion of the maneuver",
        "name": "",
        "optimize": "",
        "duration": "Maximum duration of maneuver in days",
        "sequence_number": "Order of maneuver within the context of a mission"
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "mission": Mission.example,
        "maneuver_type": "deorbit",
        "final_orbit": Orbit.example,
        "name": "FubarToRabuf",
        "optimize": False,
        "duration": 15.0,
        "sequence_number": 1
    }
