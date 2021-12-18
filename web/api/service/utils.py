from datetime import datetime, timedelta
from typing import Any

import numpy as np
from numpy import ndarray


def get_master_timestamps(start_date: datetime, finish_date: datetime, delta_time: timedelta) -> ndarray:
    master_timestamps: ndarray = np.array([int(start_date.timestamp())])

    while start_date <= finish_date:
        start_date += delta_time
        if start_date > finish_date:
            break
        master_timestamps = np.append(master_timestamps, int(start_date.timestamp()))

    return master_timestamps


def get_concurrence(master_timestamps: ndarray, devs: ndarray) -> ndarray:

    status_matrix: ndarray = np.array([[False for _ in range(len(master_timestamps))] for _ in range(len(devs))])

    for i, d in enumerate(devs):
        for j, _ in enumerate(master_timestamps):
            for t in d.timestamps:
                if j == len(master_timestamps) - 1:
                    continue
                if master_timestamps[j] <= t.timestamp < master_timestamps[j + 1]:
                    status_matrix[i][j] += 1

    active_master: ndarray = np.array([0 for _ in range(len(master_timestamps))])

    for i, _ in enumerate(active_master):
        for d in status_matrix:
            if d[i]:
                active_master[i] += 1

    return active_master
