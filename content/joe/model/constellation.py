"""Data models/objects related to the constellation designer integration
"""
# ======== standard imports ========
from dataclasses import dataclass
from enum import Enum
# ==================================

# ======= third party imports ======
# ==================================

# ========= program imports ========
from joe.model.base import JourneyObject
# ==================================


@dataclass
class ConstellationDesign(JourneyObject):
    class ConstellationType(Enum):
        MOO = "Multi-Objective"
        GEO = "Geometric"

    type: ConstellationType
    number_of_planes: float | None
    inter_plane_spacing: float | None
    satellite_count: float | None
    elevation_angle: float | None
    desired_coverage_fold: float | None
    end_date_hours: float | None
    end_date_days: float | None
    spatial_coverage: float | None
    spatial_uniformity: float | None
    temporal_uniformity: float | None
    temporal_average_gap: float | None
    maximum_gap: float | None

    initial_orbit_type: str | None
    deployment_orbit_template: str | None

    semi_major_axis_value: float | None
    semi_major_axis_type: str | None
    eccentricity: float | None
    inclination: float | None
    argument_of_perigee: float | None
    raan: float | None
    true_anomaly: float | None

    attribute_doc_strings = {
        "type": "Type of Constellation Design, Multi-Objective or Geometric",
        "number_of_planes": "",
        "inter_plane_spacing": "",
        "satellite_count": "",
        "elevation_angle": "",
        "desired_coverage_fold": "",
        "end_date_hours": "",
        "end_date_days": "",
        "spatial_coverage": "",
        "spatial_uniformity": "",
        "temporal_uniformity": "",
        "temporal_average_gap": "",
        "maximum_gap": "",
        "initial_orbit_type": "",
        "deployment_orbit_template": "",
        "semi_major_axis_value": "",
        "semi_major_axis_type": "",
        "eccentricity": "",
        "inclination": "",
        "argument_of_perigee": "",
        "raan": "",
        "true_anomaly": ""
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "geo_type": "",
        "number_of_planes": 5,
        "inter_plane_spacing": 5,
        "satellite_count": 5,
        "elevation_angle": 5,
        "desired_coverage_fold": 5,
        "end_date_hours": 5,
        "end_date_days": 5,
        "spatial_coverage": 5,
        "spatial_uniformity": 5,
        "temporal_uniformity": 5,
        "temporal_average_gap": 5,
        "maximum_gap": 5,
        "initial_orbit_type": "LEO",
        "deployment_orbit_template": "MEO",
        "semi_major_axis_value": 7200,
        "semi_major_axis_type": "???",
        "eccentricity": 0.0005,
        "inclination": 57.4,
        "argument_of_perigee": 0,
        "raan": 0,
        "true_anomaly": 0
    }


@dataclass
class ConstellationTicket(JourneyObject):
    sim_start_time: str
    num_satellites: int
    spatial_coverage_weights: list
    temporal_coverage_weights: list

    attribute_doc_strings = {
        "sim_start_time": "",
        "num_satellites": "",
        "spatial_coverage_weights": "",
        "temporal_coverage_weights": ""
    }
    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "sim_start_time": "2024-04-04T20:49:02",
        "num_satellites": 5,
        "spatial_coverage_weights": '[7]',
        "temporal_coverage_weights": '[7]'
    }
