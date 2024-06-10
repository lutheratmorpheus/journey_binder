"""File housing classes for simulation via numerical computation
"""
# ======== standard imports ========
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
# ==================================

# ======= third party imports ======
import numpy as np
# ==================================

# ========= program imports ========
from joe.model.base import JourneyObject
from joe.model.other import Mission
# ==================================

@dataclass
class Propagator(JourneyObject):
    ''' Propagators describe how to computationally integrate an initial value problem '''

    class Algorithm(Enum):
        """ Model for integration algorithm """
        RK45 = "RK45"
        DOP853 = "DOP853"

    class AveragingMethod(Enum):
        """ Strategy for differential equation smoothing """
        DSST = "DSST"
        #ORBITAL = "ORBITAL"
        NONE = "None"

    algorithm: Algorithm = Algorithm.DOP853
    averaging: AveragingMethod = AveragingMethod.NONE
    min_step: Optional[float] = None
    max_step: Optional[float] = None
    first_step: Optional[float] = None
    tolerances: tuple[float, Optional[float]] = (0.001, None)

    attribute_doc_strings = {
        "algorithm": "Integration routine",
        "averaging": "Differential equation smoothing technique",
        "min_step": "Minimum step size [seconds]",
        "max_step": "Maximum step size [seconds]",
        "first_step": "Size of first step taken [seconds]",
        "tolerances": "Either position tolerance [m] or (absolute tolerance, relative tolerance) [unitless]"
    }

    def validate_steps(self):
        local_min_step = 0 if self.min_step is None else self.min_step
        local_max_step = np.inf if self.max_step is None else self.max_step
        assert (
            self.min_step is None 
            or 0 <= self.min_step <= local_max_step
        )
        assert (
            self.max_step is None 
            or local_min_step <= self.max_step
        )
        assert (
            self.first_step is None
            or local_min_step <= self.first_step <= local_max_step
        )

    def validate_tolerances(self):
        assert self.tolerances[0] > 0
        assert self.tolerances[1] is None or self.tolerances[1] > 0


    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        
        "algorithm": "DOP853",
        "averaging": "None",
        "min_step": 1e-3,
        "max_step": None,
        "first_step": 60.0,
        "tolerances": (0.001, None)
    }

@dataclass
class Status(JourneyObject):
    ''' Status objects describe the state of computation '''

    class State(Enum):
        """ Model for integration algorithm """
        SUCCESS = "success"
        TERMINATED = "terminated"
        RUNNING = "running"
        FAILED = "failed"

    percentage_completion: float
    computation_state: State
    message: str
    information: dict

    attribute_doc_strings = {
        "percentage_completion": "Percentage of the computation which is complete",
        "computation_state": "Current state of computation",
        "message": "Any message",
        "information": "Additional information"
    }

    def validate_percentage(self):
        assert 0 <= self.percentage_completion <= 1

    example = {
        "id": "449465be-5533-40ad-9e85-bfa95b0ee39a",
        "creation_date": "2024-04-04T20:49:02",
        "update_date": "2024-04-04T20:49:02",
        "percentage_completion": 0.5,
        "computation_state": "running",
        "message": "",
        "information": {'steps_taken':4} 
    }


