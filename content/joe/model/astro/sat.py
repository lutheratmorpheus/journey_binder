"""File housing classes for Satellites and their components
"""
# ======== standard imports ========
from dataclasses import dataclass
from enum import Enum
import math
# ==================================

# ======= third party imports ======
# ==================================

# ========= program imports ========
from joe.model.base import JourneyObject
from joe.model.other import Mission
# ==================================


@dataclass
class Satellite(JourneyObject):
    ''' Satellite's are individual, dynamic bodies in an Orbit '''
    mission: Mission
    name: str

    attribute_doc_strings = {
        "mission": "Mission utilizing Satellite",
        "name": "Name of Satellite"
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "mission": Mission.example,
        "name": "Satellite7",
    }


@dataclass
class Bus(JourneyObject):
    ''' A Bus defines the physical structure of a Satellite '''
    satellite: Satellite

    size: str
    length: float
    width: float
    height: float
    mass: float
    drag: float = 2.2
    reflectivity: float = 0.9

    @staticmethod
    def get_dimensions_from_u(u: int) -> tuple:
        supported_satellites = {
            1: (0.1, 0.1, 0.1),
            2: (0.2, 0.1, 0.1),
            3: (0.3, 0.1, 0.1),
            6: (0.3, 0.2, 0.1),
            12: (0.3, 0.2, 0.2),
            16: (0.4, 0.2, 0.2),
            27: (0.3, 0.3, 0.3)
        }
        try:
            return supported_satellites[u]
        except KeyError:
            raise Exception(f"Unsupported satellite unit: {u}")

    @staticmethod
    def increase_units_by_ten(dimensions: list[int]) -> tuple:
        return (d * 10 for d in dimensions)

    @property
    def dimensions(self):
        return (self.length, self.width, self.height)

    @property
    def dimensions_in_centimeters(self):
        return self.increase_units_by_ten(self.dimensions)

    @property
    def estimate_mass_from_volume(self) -> float:
        cubic_centimeters = math.prod(self.dimensions_in_centimeters)
        return 1.33 * cubic_centimeters / 1000

    attribute_doc_strings = {
        "satellite": "Satellite utilizing Bus",
        "size": "Size of Satellite in satellite-units",
        "length": "Length of satellite in meters",
        "width": "Width of satellite in meters",
        "height": "Height of satellite in meters",
        "drag": "Drag coefficient of satellite in ???",
        "reflectivity": "Reflectivity of satellite in ???",
        "mass": "Mass of satellite in kilograms"
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "satellite": Satellite.example,
        "size": "6U",
        "length": 0.3,
        "width": 0.2,
        "height": 0.1,
        "drag": 0.4,
        "reflectivity": 0.01,
        "mass": 5.0
    }

    BUS_TEMPLATES = {
        '1U': {
            'size': '1U',
            'width': 10.0,
            'height': 10.0,
            'length': 10.0,
            'mass': 1.0,
            "reflectivity": 1.40,
            "drag": 2.50},
        '2U': {
            'size': '2U',
            'width': 10.0,
            'height': 20.0,
            'length': 10.0,
            'mass': 2.0,
            "drag": 2.50,
            "reflectivity": 1.40},
        '3U': {
            'size': '3U',
            'width': 10.0,
            'height': 30.0,
            'length': 10.0,
            "mass": 2.50,
            "drag": 1.40,
            'reflectivity': 4.0},
        '6U': {
            'size': '6U',
            'width': 10.0,
            'height': 30.0,
            'length': 20.0,
            "mass": 2.50,
            "drag": 1.40,
            'reflectivity': 6.0},
        '12U': {
            'size': '12U',
            'width': 20.0,
            'height': 30.0,
            'length': 20.0,
            "mass": 2.50,
            "drag": 1.40,
            'reflectivity': 12.0},
        '16U': {
            'size': '16U',
            'width': 20.0,
            'height': 40.0,
            'length': 20.0,
            "mass": 2.50,
            "drag": 1.40,
            'reflectivity': 24.0},
        '27U': {
            'size': '27U',
            'width': 30.0,
            'height': 30.0,
            'length': 30.0,
            "mass": 2.50,
            "drag": 1.40,
            'reflectivity': 32.0}
    }


@dataclass
class Propulsion(JourneyObject):
    ''' Propulsion defines the thrusting capabilities of a Satellite '''

    class PropulsionType(Enum):
        """ Model for Gravity """
        HYDRAZINE = "Hydrazine"
        HPGP = "HPGP"
        IONTHRUSTER = "Ion Thruster"
        HALLEFFECT = "Hall Effect"
        CUSTOM = "Custom"

    satellite: Satellite
    type: PropulsionType
    prop_mass: float
    isp: list[float]
    thrust: list[float]

    attribute_doc_strings = {
        "satellite": "",
        "type": "",
        "prop_mass": "Propellent Mass in kilograms",
        "isp": "Array of Specific Impulse (ISP) values of thruster in meters / second",
        "thrust": "Array of Thrust values in newtons"
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "satellite": Satellite.example,
        "prop_mass": 4.2,
        "isp": [45.2],
        "thrust": [31.4],
        "type": "Ion Thruster"
    }


@dataclass
class Payload(JourneyObject):
    ''' Payloads describe imaging capabilites of Satellites '''

    satellite: Satellite
    fov_cross: float
    fov_along: float

    def validate_positive_values(self):
        for attr in ['fov_cross', 'fov_along']:
            self.check_bound(attr, getattr(self, attr), min_bound=0)

    attribute_doc_strings = {
        "satellite": "Satellite with this solar panel",
        "fov_cross": "Field of View in perpendicular direction to groundtrack motion (deg)",
        "fov_along": "Field of View in parallel direction to groundtrack motion (deg)",
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "satellite": Satellite.example,
        "fov_cross": 45.0,
        "fov_along": 45.0,
    }


@dataclass
class SolarPanel(JourneyObject):
    ''' Solar Panels define the power generation devices a Satellite has '''

    class MountConfiguration:
        BODY = "Body"
        LATERAL = "Lateral"

    satellite: Satellite
    mount_type: str
    cell_efficiency: float
    surface_area: float
    voltage: float

    def validate_positive_values(self):
        for attr in ['voltage', 'surface_area', 'cell_efficiency']:
            self.check_bound(attr, getattr(self, attr), min_bound=0)

    attribute_doc_strings = {
        "satellite": "Satellite with this solar panel",
        "mount_type": "Mounting configuration for solar panel",
        "cell_efficiency": "Power conversion efficiency for solar panel as a percentage",
        "surface_area": "Surface area of solar panel in square meters",
        "voltage": "Supply voltage from solar panel in volts"
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "satellite": Satellite.example,
        "mount_type": "Body",
        "cell_efficiency": 32.4,
        "surface_area": 11.2,
        "voltage": 5.2
    }


@dataclass
class Battery(JourneyObject):
    ''' Batterys define the power storage devices a Satellite has '''
    satellite: Satellite

    voltage: float
    capacity: float
    maximum_discharge_rate: float
    recommended_discharge_rate: float

    def validate_positive_values(self):
        for attr in ['voltage', 'capacity', 'maximum_discharge_rate', 'recommended_discharge_rate']:
            self.check_bound(attr, getattr(self, attr), min_bound=0)

    attribute_doc_strings = {
        "satellite": "Satellite containing battery",
        "voltage": "Supply voltage from battery in volts",
        "capacity": "Energy capacity of battery in watt-hours",
        "maximum_discharge_rate": "Maximum discharge rate for battery in amperes",
        "recommended_discharge_rate": "Recommended discharge rate for battery in amperes"
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "satellite": Satellite.example,
        "voltage": 5.1,
        "capacity": 21000.0,
        "maximum_discharge_rate": 100.0,
        "recommended_discharge_rate": 20.0
    }


@dataclass
class PowerBudget(JourneyObject):
    ''' Power Budgets define how power is consumed across a Satellite during a Simulation '''
    satellite: Satellite
    budget: dict

    attribute_doc_strings = {
        "satellite": "Satellite with this Power Budget",
        "budget": "Definition of satellite power budget"
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "satellite": Satellite.example,
        "budget": {"active_power_draw": 5}
    }
