"""File contianing basic functions to investigate expert model results
"""
# ======== standard imports ========
from datetime import datetime
from typing import Optional
# ==================================

# ======= third party imports ======
import numpy as np
import matplotlib.pyplot as plt
# ==================================

# ========= program imports ========
from joe.model.astro.base import Orbit
# ==================================

def plot_orbits_over_time(timestamps:list[datetime], orbits:list[Orbit]):
    total_seconds = [(ts - timestamps[0]).total_seconds() for ts in timestamps]
    total_days = [ts/(60*60*24) for ts in total_seconds]
    fig, axes = plt.subplots(2, 3, figsize = (15,8))
    axes[0, 0].plot(total_days, [o.semi_major_axis for o in orbits])
    axes[0, 0].set_title('Semi Major Axis')
    axes[0, 1].plot(total_days, [o.eccentricity for o in orbits])
    axes[0, 1].set_title('Eccentricity')
    axes[0, 2].plot(total_days, [o.inclination for o in orbits])
    axes[0, 2].set_title('Inclination')
    axes[1, 0].plot(total_days, [o.argument_of_perigee for o in orbits])
    axes[1, 0].set_title('Argument of Perigee')
    axes[1, 1].plot(total_days, [o.raan for o in orbits])
    axes[1, 1].set_title('RAAN')
    axes[1, 2].plot(total_days, [o.true_anomaly for o in orbits])
    axes[1, 2].set_title('True Anomaly')
    plt.show()

def plot_thrust_vectors_over_time(
        timestamps:list[datetime], 
        thrust_directions:list[list[float]], 
        thrust_magnitudes:list[float],
        delta_v:list[float],
        total_impulse:list[float],
        direction_labels:list[str] = ['Radial', 'Transverse', 'Normal'],
        thrust_max:Optional[float] = None
    ):
    total_seconds = [(ts - timestamps[0]).total_seconds() for ts in timestamps]
    total_days = [ts/(60*60*24) for ts in total_seconds]
    fig, axes = plt.subplots(2, 2, figsize = (15,8))
    thrust_directions = np.array(thrust_directions)
    thrust_magnitudes = np.array(thrust_magnitudes)
    axes[0, 0].plot(total_days, thrust_directions[:, 0], label = direction_labels[0])
    axes[0, 0].plot(total_days, thrust_directions[:, 1], label = direction_labels[1])
    axes[0, 0].plot(total_days, thrust_directions[:, 2], label = direction_labels[2])
    axes[0, 0].set_title('Thrust Direction')
    axes[0, 0].legend()
    axes[0, 1].plot(total_days, thrust_magnitudes, label = 'Magnitude [N]')
    if not thrust_max is None:
        axes[0, 1].plot(total_days, thrust_magnitudes/thrust_max, label = 'Percentage of Max Thrust')
    axes[0, 1].legend()
    axes[0, 1].set_title('Thrust Magnitude')

    axes[1, 0].plot(total_days, delta_v)
    axes[1, 0].set_title('Delta-V')

    axes[1, 1].plot(total_days, total_impulse)
    axes[1, 1].set_title('Total Impulse')
    plt.show()