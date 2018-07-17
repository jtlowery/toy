import numpy as np
import pandas as pd
import pytest
from hypothesis import given, assume, example, seed
from hypothesis.extra.numpy import arrays
from hypothesis.strategies import integers, floats, composite, lists, one_of, text
from hypothesis.extra.pandas import data_frames, column, range_indexes, series

from toy.hypothesis.random_funcs import fibonacci, mean_absolute_error, error

seed(2018)


@given(integers(min_value=0, max_value=100))
@example(1)
@example(0)
def test_fibonacci(x):
    fib = fibonacci(x)
    if x >= 2:
        fib_less_1 = fibonacci(x - 1)
        fib_less_2 = fibonacci(x - 2)
        assert fib == fib_less_1 + fib_less_2
        assert fib >= fib_less_1
        assert fib_less_1 >= fib_less_2
    elif x == 1:
        assert fib == 1
    else:
        assert fib == 0

    assert isinstance(fib, int)


float_strategy = floats(
    min_value=1e-10, max_value=1e10, allow_nan=None, allow_infinity=None
)


@given(
    arrays(dtype=np.float64, shape=5, elements=float_strategy),
    arrays(dtype=np.float64, shape=5, elements=float_strategy),
)
def test_mae(y, y_hat):
    if np.isinf(y).any() or np.isinf(y_hat).any():
        with pytest.raises(ValueError):
            mae = mean_absolute_error(y, y_hat)
    else:
        mae = mean_absolute_error(y, y_hat)
        if np.isnan(y).any() or np.isnan(y_hat).any():
            assert np.isnan(mae)
        elif (y == y_hat).all():
            assert mae == 0.
        else:
            assert mae > 0.


@composite
def two_equal_size_series(draw):
    series_strategy = series(
        dtype=np.float64, elements=float_strategy, index=range_indexes(min_size=1)
    )
    s1 = draw(series_strategy)
    s2 = draw(series_strategy)
    assume(len(s1) == len(s2))
    return s1, s2


@given(two_equal_size_series())
def test_mae_series(two_series):
    y, y_hat = two_series
    if np.isinf(y).any() or np.isinf(y_hat).any():
        with pytest.raises(ValueError):
            mae = mean_absolute_error(y, y_hat)
    else:
        mae = mean_absolute_error(y, y_hat)
        if np.isnan(y).any() or np.isnan(y_hat).any():
            assert np.isnan(mae)
        elif (y == y_hat).all():
            assert mae == 0.
        else:
            assert mae > 0.


@composite
def build_error_df(draw):
    numeric_list_strat = lists(
        elements=one_of(
            integers(min_value=1e-10, max_value=1e10),
            floats(min_value=1e-10, max_value=1e10),
        ),
        min_size=1,
    )
    y = draw(numeric_list_strat)
    y_hat = draw(numeric_list_strat)
    assume(len(y) == len(y_hat))
    return pd.DataFrame(data={"y": y, "y_hat": y_hat})


@given(build_error_df())
def test_error(df):
    df = error(df)
    assert "error" in df.columns, "error column expected"
    zero_error = df["y"] == df["y_hat"]
    assert (df.loc[zero_error, "error"] == 0.).all(), "if y == y_hat, error should be 0"
    assert (
        df.loc[~zero_error, "error"] != 0.
    ).all(), "if y != y_hat, error should not be 0"


@given(
    data_frames(
        columns=[
            column(name="y", elements=float_strategy),
            column(name="y_hat", elements=float_strategy),
        ]
    )
)
def test_error_using_pd_extra(df):
    df = error(df)
    assert "error" in df.columns, "error column expected"
    zero_error = df["y"] == df["y_hat"]
    assert (df.loc[zero_error, "error"] == 0.).all(), "if y == y_hat, error should be 0"
    assert (
        df.loc[~zero_error, "error"] != 0.
    ).all(), "if y != y_hat, error should not be 0"
