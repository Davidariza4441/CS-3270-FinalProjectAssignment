import pandas as pd
import matplotlib.pyplot as plt
from functools import reduce
from typing import List
from pathlib import Path
import asyncio

REQUIRED_COLS = ["Location", "MinTemp", "MaxTemp", "Temp9am", "Temp3pm", "Rainfall", "Humidity9am", "Humidity3pm","Pressure9am", "Cloud9am", "RainToday"]
#Functions using async: filter_hot_days, total_rainfall, top_locations_by_avg_max_temp.
def prepare_weather_df(df) -> pd.DataFrame:
    '''
    Function to clean and standardize the DataFrame once.
    '''
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    clean = df[REQUIRED_COLS].copy()
    numeric_cols = ["MinTemp", "MaxTemp", "Temp9am", "Temp3pm", "Rainfall", "Humidity9am", "Humidity3pm", "Pressure9am", "Cloud9am"]
    for col in numeric_cols:
        clean[col] = pd.to_numeric(clean[col], errors="coerce")
    clean = clean.dropna(subset=REQUIRED_COLS)

    # Standarize Raintoday as Boolean
    clean['RainToday'] = clean['RainToday'].str.strip().str.lower().map({'yes': True, 'no': False})
    return clean

def add_derived(df) -> pd.DataFrame:
    '''
    Adds a few extra columns to help with analysis:
    temp_range, humidity_change, and is_rainy.
    '''
    out = df.copy()
    out["temp_range"] = out["MaxTemp"] - out["MinTemp"]
    out["humidity_change"] = out["Humidity3pm"] - out["Humidity9am"]
    out["is_rainy"] = out["Rainfall"] > 0
    return out

async def filter_hot_days(df, threshold=35) -> pd.DataFrame:
    '''
        Returns only the "hot" days.
        Uses filter + lambda.
    '''
    hot_records = list(filter(lambda r: float(r["MaxTemp"]) >= float(threshold), df.to_dict('records')))
    return pd.DataFrame(hot_records)

async def total_rainfall(df) -> float:
    '''
        Adds up all Rainfall values and returns the total.
        Uses reduce to meet the assignment requirement.
    '''
    rain_values = df["Rainfall"].tolist()
    if not rain_values:
        return 0.0
    return float(reduce(lambda acc, x: acc + float(x), rain_values, 0.0))

async def top_locations_by_avg_max_temp(df, top_n=10) -> pd.DataFrame:
    '''
        Finds the top N locations with the highest average MaxTemp.
        Uses map + lambda to compute averages per location.
    '''
    grouped = df.groupby("Location")["MaxTemp"]

    locations = list(grouped.groups.keys())
    # map + lambda to compute each location's average max temp
    averages = list(map(lambda loc: float(grouped.get_group(loc).mean()), locations))

    result = pd.DataFrame({"Location": locations, "avg_max_temp": averages})
    result = result.sort_values("avg_max_temp", ascending=False).head(int(top_n)).reset_index(drop=True)
    return result


async def make_plots(df, out_dir="static/img/") -> list[str]:
    '''
        Makes 3 charts (bar, histogram, scatter) and saves them as PNG files.
        Returns a list of the saved file paths.
    '''
    print("3 graphs are being created: \n-Top locations by avg max.\n-Histogram of rainfall distribution." \
    "\n-Scatter plot of MaxTemp vs Humidity3pm.\nProcess run in parallel. ")
    
    out_path = Path(out_dir)
    # This will now create static/img/ if it doesn't exist!
    out_path.mkdir(parents=True, exist_ok=True)

    saved_files: List[str] = []

    # 1) Bar: top locations by avg max temp
    top_df = await top_locations_by_avg_max_temp(df, top_n=10)
    plt.figure()
    plt.bar(top_df["Location"], top_df["avg_max_temp"])
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Location")
    plt.ylabel("Average Max Temperature")
    plt.title("Top 10 Locations by Average Max Temperature")
    bar_file = out_path / "top_locations_avg_max_temp.png"
    plt.tight_layout()
    plt.savefig(bar_file, dpi=150)
    plt.close()
    saved_files.append(str(bar_file))

    # 2) Histogram: rainfall distribution
    plt.figure()
    plt.hist(df["Rainfall"], bins=30)
    plt.xlabel("Rainfall")
    plt.ylabel("Frequency")
    plt.title("Rainfall Distribution")
    hist_file = out_path / "rainfall_distribution.png"
    plt.tight_layout()
    plt.savefig(hist_file, dpi=150)
    plt.close()
    saved_files.append(str(hist_file))

    # 3) Scatter: MaxTemp vs Humidity3pm
    plt.figure()
    plt.scatter(df["MaxTemp"], df["Humidity3pm"])
    plt.xlabel("Max Temperature")
    plt.ylabel("Humidity at 3pm")
    plt.title("MaxTemp vs Humidity3pm")
    scatter_file = out_path / "maxtemp_vs_humidity3pm.png"
    plt.tight_layout()
    plt.savefig(scatter_file, dpi=150)
    plt.close()
    saved_files.append(str(scatter_file))

    return saved_files