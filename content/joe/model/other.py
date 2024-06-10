"""File housing exclusively stuff related to Companies and Products.
This should be better specified in the future.
"""
# ======== standard imports ========
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
# ==================================

# ======= third party imports ======
# ==================================

# ========= program imports ========
from joe.model.base import JourneyObject
# ==================================


@dataclass
class Company(JourneyObject):
    ''' Company organizes product, missions, and users and are the basis for permissions

        Example: {"name": "FubaruToMoon"}'''
    name: str

    attribute_doc_strings = {
        "name": "Name of Company"
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "name": "FubaruToTheMoon"
    }


@dataclass
class Product(JourneyObject):
    ''' Products satellite components manufactured by Companies

        Example: '''
    class ProductType(Enum):
        PROPULSION = "Propulsion"
        ADCS = "ADCS"
        BATTERY = "Battery"
        SOLARPANEL = "Solar Panel"
        TRANSMITTER = "Transmitter"
        RECEIVER = "Receiver"
        ANTENNA = "Antenna"

    manufactured_by: Company
    product_type: ProductType
    specification: dict

    attribute_doc_strings = {
        "manufactured_by": "The Company that manufactures the Product",
        "product_type": "The high-level type of Satellite Product",
        "specification": "This is a JSON definition of all product specs. The exact structure will depend on the product"
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "manufactured_by": Company.example,
        "product_type": "Propulsion",
        "specification": {"isp": 5}
    }


@dataclass
class ProductAssociation(JourneyObject):
    ''' Product Associations describe interactions between sets of products '''
    status: str
    notes: str

    attribute_doc_strings = {
        "status": "Type of Association",
        "notes": "Comments on Association"
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "status": "WorkingSuperWell",
        "notes": "JustNotActuallyWorking"
    }


@dataclass
class AssociatedProduct(JourneyObject):
    ''' Associated Products defines the relationship between a ProductAssociation record and an Product '''
    product: Product
    association: ProductAssociation

    attribute_doc_strings = {
        "product": "Product in Association",
        "association": "Association with Product"
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "product": Product.example,
        "association": ProductAssociation.example
    }


@dataclass
class Mission(JourneyObject):
    ''' Missions define Constellations '''
    created_by: Company
    name: str
    launch_date: datetime
    amd_enabled: bool

    attribute_doc_strings = {
        "created_by": "Company that created the Mission",
        "name": "Name of Mission",
        "launch_date": "Mission launch date in ISO 8601 format",
        "amd_enabled": "Flag for making mission available in AMD"
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "created_by": Company.example,
        "name": "MyMissionToMars",
        "launch_date": "2027-04-04T20:49:02",
        "amd_enabled": True
    }


@dataclass
class RequestForInformation(JourneyObject):
    ''' Requests for Information track a User's request for more details on a product '''
    created_by: Company
    mission: Mission
    request: str

    attribute_doc_strings = {
        "created_by": "Company who submitted RFI",
        "mission": "Mission the RFI was submitted from",
        "request": "Contents of the RFI"
    }

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "created_by": Company.example,
        "mission": Mission.example,
        "request": "HALP"
    }
