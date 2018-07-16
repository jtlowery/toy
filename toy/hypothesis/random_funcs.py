from functools import lru_cache

import numpy as np


@lru_cache(maxsize=128, typed=False)
def fibonacci(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def mean_absolute_error(y, y_hat):
    inf_present = np.isinf(y).any() or np.isinf(y_hat).any()
    if inf_present:
        raise ValueError('inf values present in inputs')
    abs_error = np.abs(y - y_hat)
    mae = abs_error.mean()
    return mae


def error(df):
    df['error'] = df['y'] - df['y_hat']
    return df
