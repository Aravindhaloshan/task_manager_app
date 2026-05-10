import pandas as pd
import numpy as np


def generate_analytics(tasks):

    data = []

    for task in tasks:

        data.append({
            'status': task.status
        })

    if len(data) == 0:

        return {
            'total_tasks': 0,
            'completed_tasks': 0,
            'pending_tasks': 0,
            'completion_percentage': 0
        }

    df = pd.DataFrame(data)

    total_tasks = len(df)

    completed_tasks = np.sum(df['status'] == 'Completed')

    pending_tasks = np.sum(df['status'] == 'Pending')

    completion_percentage = round(
        (completed_tasks / total_tasks) * 100,
        2
    )

    return {
        'total_tasks': int(total_tasks),
        'completed_tasks': int(completed_tasks),
        'pending_tasks': int(pending_tasks),
        'completion_percentage': completion_percentage
    }
