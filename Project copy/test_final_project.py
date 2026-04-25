# Run with pytest -q

import pandas as pd
import functions as f

def test_datasetValid_missing_columns():
    """
    Checks that datasetValid returns False and a set of missing columns
    when required columns are not present.
    """
    df = pd.DataFrame({
        "Location": ["Sydney"],
        "MinTemp": [10.0],
        # missing many columns on purpose
    })
    ok, missing = f.datasetValid(df)
    assert ok is False
    assert "MaxTemp" in missing
    assert "RainToday" in missing


def test_temperature_trends_output_shape():
    """
    Temperature_trends should return (summary, charts)
    where summary is a string and charts is a list of 2 paths.
    """
    df = pd.DataFrame({
        "Location": ["Sydney"] * 5,
        "MinTemp": [10, 11, 9, 12, 10],
        "MaxTemp": [25, 24, 26, 27, 23],
        "Temp9am": [15, 16, 14, 17, 15],
        "Temp3pm": [22, 21, 23, 24, 20],
        "Rainfall": [0, 2.0, 0, 5.0, 0],
        "Humidity9am": [70, 80, 75, 85, 60],
        "Humidity3pm": [50, 55, 45, 60, 40],
        "Pressure9am": [1012, 1010, 1011, 1009, 1013],
        "Cloud9am": [4, 6, 3, 7, 2],
        "RainToday": [False, True, False, True, False],
    })

    summary, charts = f.temperature_trends(df, "Sydney")
    assert isinstance(summary, str)
    assert len(summary) > 0
    assert isinstance(charts, list)
    assert len(charts) == 2
    assert all(isinstance(p, str) for p in charts)


def test_rainfall_patterns_math():
    """
    Logic test: RainToday mean (rate) and Rainfall sum should be consistent.
    We only check that summary is created and charts list is returned.
    """
    df = pd.DataFrame({
        "Location": ["Sydney"] * 4,
        "MinTemp": [10, 10, 10, 10],
        "MaxTemp": [20, 20, 20, 20],
        "Temp9am": [15, 15, 15, 15],
        "Temp3pm": [18, 18, 18, 18],
        "Rainfall": [0.0, 2.0, 0.0, 6.0],
        "Humidity9am": [70, 70, 70, 70],
        "Humidity3pm": [50, 50, 50, 50],
        "Pressure9am": [1012, 1012, 1012, 1012],
        "Cloud9am": [4, 4, 4, 4],
        "RainToday": [False, True, False, True],
    })

    summary, charts = f.rainfall_patterns(df, "Sydney")
    assert isinstance(summary, str)
    assert "Sydney" in summary
    assert isinstance(charts, list)
    assert len(charts) == 2