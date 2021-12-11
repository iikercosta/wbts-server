from datetime import datetime, date, timedelta
from typing import List

import numpy as np
from numpy import ndarray

from web.api.model.models import Device


def get_master_timestamps(start_date: datetime, finish_date: datetime, delta_time: timedelta) -> ndarray:
    master_timestamps: ndarray = np.array([int(start_date.timestamp())])

    while start_date <= finish_date:
        start_date += delta_time
        if start_date > finish_date:
            break
        master_timestamps = np.append(master_timestamps, int(start_date.timestamp()))

    return master_timestamps


def get_status_matrix(master_timestamps: ndarray, devs: ndarray) -> ndarray:

    status_matrix = np.array([[False for _ in range(len(master_timestamps))] for _ in range(len(devs))])

    for i, d in enumerate(devs):
        for j, m in enumerate(master_timestamps):
            for t in d.timestamps:
                try:
                    if master_timestamps[j] <= t.timestamp < master_timestamps[j + 1]:
                        status_matrix[i][j] = True
                except IndexError:
                    pass

    return status_matrix


def master_count(master_timestamps: ndarray, status_matrix: ndarray) -> ndarray:
    active_master: ndarray = np.array([0 for _ in range(len(master_timestamps))])

    for i, _ in enumerate(active_master):
        for d in status_matrix:
            if d[i]:
                active_master[i] += 1

    return active_master
