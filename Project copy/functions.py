#Error Fix for Matplotlib using the MacOS GUI backend
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.pyplot as plt 
from flask import flash, session
import pandas as pd
from module_06_07 import prepare_weather_df
from module_01 import read_csv_file

def datasetValid(df):
    '''
        Function to check if dataset is valid, if valid return a tuple (True, None), 
        if missing values, return a tuple (False, {missing values} )
    '''
    requiredCols = {
        'Location', 'MinTemp', 'MaxTemp', 'Rainfall', 'Humidity9am', 
        'Humidity3pm', 'Temp9am', 'Temp3pm', 'Pressure9am', 'Cloud9am', 'RainToday'
        }
    missing = requiredCols - set(df.columns)
    return (len(missing) == 0, missing)

def import_weather_data(file_path, db, User):
    raw_df = read_csv_file(file_path)
    ok, missing = datasetValid(raw_df)

    if not ok:
        flash(f"Missing columns: {', '.join(sorted(missing))}", "error")
        return False

    clean_df = prepare_weather_df(raw_df)

    db.session.query(User).delete()

    for _, row in clean_df.iterrows():
        record = User(
            location=row['Location'],
            min_temp=row['MinTemp'],
            max_temp=row['MaxTemp'],
            rainfall=row['Rainfall'],
            humidity_9am=row['Humidity9am'],
            humidity_3pm=row['Humidity3pm'],
            temp_9am=row['Temp9am'],
            temp_3pm=row['Temp3pm'],
            pressure_9am=row['Pressure9am'],
            cloud_9am=row['Cloud9am'],
            rain=row['RainToday']
        )
        db.session.add(record)

    return True
    
def convert_city_df(city, User) -> pd.DataFrame:
    rows = User.query.filter(User.location == city).all()

    if not rows:
        return pd.DataFrame(columns=[
            "Location","MinTemp","MaxTemp","Rainfall","Humidity9am","Humidity3pm",
            "Temp9am","Temp3pm","Pressure9am","Cloud9am","RainToday"
        ])

    return pd.DataFrame([{
        "Location": r.location,
        "MinTemp": r.min_temp,
        "MaxTemp": r.max_temp,
        "Rainfall": r.rainfall,
        "Humidity9am": r.humidity_9am,
        "Humidity3pm": r.humidity_3pm,
        "Temp9am": r.temp_9am,
        "Temp3pm": r.temp_3pm,
        "Pressure9am": r.pressure_9am,
        "Cloud9am": r.cloud_9am,
        "RainToday": r.rain
    } for r in rows])

#________HELPERS________
def _safe_city(city: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("_", "-") else "_" for ch in city.strip())

def _img_dir() -> Path:
    p = Path("static/img")
    p.mkdir(parents=True, exist_ok=True)
    return p


#________TEMPERATURE________
def temperature_trends(city_df: pd.DataFrame, city: str):
    '''
        Creates Temperature trends from filtered dataset.
        example: Cobar Temperaturess: 
        - Average Range: 12.9°C to 25.3°C 
        - Mean Conditions: 17.7°C at 9am, 24.0°C at 3pm 
        - Typical Daily Spread: ~12.4°C 
        - Record High: 45.4°C
    '''
    if city_df.empty:
        return f"No data found for {city}.", []

    out_path = _img_dir()
    safe = _safe_city(city)

    # Summary metrics
    avg_min = city_df["MinTemp"].mean()
    avg_max = city_df["MaxTemp"].mean()
    avg_9 = city_df["Temp9am"].mean()
    avg_3 = city_df["Temp3pm"].mean()
    avg_range = (city_df["MaxTemp"] - city_df["MinTemp"]).mean()
    max_seen = city_df["MaxTemp"].max()

    summary = (
    f"{city.title()} Temperaturess:\n"
    f"- Average Range: {avg_min:.1f}°C to {avg_max:.1f}°C\n"
    f"- Mean Conditions: {avg_9:.1f}°C at 9am, {avg_3:.1f}°C at 3pm\n"
    f"- Typical Daily Spread: ~{avg_range:.1f}°C\n"
    f"- Record High: {max_seen:.1f}°C"
)

    # Chart 1: MaxTemp histogram
    f1 = out_path / f"temp_max_hist_{safe}.png"
    plt.figure()
    plt.hist(city_df["MaxTemp"].dropna(), bins=30)
    plt.title(f"Maximum Temperature Distribution - {city}")
    plt.xlabel("MaxTemp")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(f1, dpi=150)
    plt.close()

    # Chart 2: Temp range histogram
    temp_range = (city_df["MaxTemp"] - city_df["MinTemp"]).dropna()
    f2 = out_path / f"temp_range_hist_{safe}.png"
    plt.figure()
    plt.hist(temp_range, bins=30)
    plt.title(f"Daily Temperature Range (Max-Min) - {city}")
    plt.xlabel("Temp Range")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(f2, dpi=150)
    plt.close()

    charts = [f"/static/img/{f1.name}", f"/static/img/{f2.name}"]
    return summary, charts

#________RAINFALL________
def rainfall_patterns(city_df: pd.DataFrame, city: str):
    if city_df.empty:
        return f"No data found for {city}.", []

    out_path = _img_dir()
    safe = _safe_city(city)

    # Summary metrics
    rain_rate = city_df["RainToday"].mean() * 100.0  # True=1, False=0
    total_rain = city_df["Rainfall"].fillna(0).sum()
    rainy = city_df[city_df["RainToday"] == True]
    avg_rain_rainy = rainy["Rainfall"].mean() if not rainy.empty else 0.0
    max_rain = city_df["Rainfall"].max()

    summary = (
    f"In {city}, it rains on {rain_rate:.1f}% of days. "
    f"The total recorded rainfall is {total_rain:.1f} mm. "
    f"On days when it rains, the average is {avg_rain_rainy:.1f} mm, "
    f"with a recorded maximum of {max_rain:.1f} mm in a single day."
    )

    # Chart 1: RainToday counts
    true_count = int(city_df["RainToday"].sum())
    false_count = int((~city_df["RainToday"]).sum())
    f1 = out_path / f"rain_today_counts_{safe}.png"
    plt.figure()
    plt.bar(["No Rain", "Rain"], [false_count, true_count])
    plt.title(f"Raining Day Counts - {city}")
    plt.xlabel("Class")
    plt.ylabel("Days")
    plt.tight_layout()
    plt.savefig(f1, dpi=150)
    plt.close()

    # Chart 2: Rainfall histogram (prefer >0 so it's not mostly zeros)
    rain_pos = city_df.loc[city_df["Rainfall"] > 0, "Rainfall"].dropna()
    data = rain_pos if not rain_pos.empty else city_df["Rainfall"].dropna()
    f2 = out_path / f"rainfall_hist_{safe}.png"
    plt.figure()
    plt.hist(data, bins=30)
    plt.title(f"Rainfall Distribution - {city}")
    plt.xlabel("Rainfall")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(f2, dpi=150)
    plt.close()

    charts = [f"/static/img/{f1.name}", f"/static/img/{f2.name}"]
    return summary, charts

#________EXTREME________
def extreme_indicators(city_df: pd.DataFrame, city: str, hot_thresh=35, heavy_rain_thresh=10, humid_thresh=90):
    if city_df.empty:
        return f"No data found for {city}.", []

    out_path = _img_dir()
    safe = _safe_city(city)

    # Counts + peaks
    hot_days = int((city_df["MaxTemp"] >= hot_thresh).sum())
    heavy_days = int((city_df["Rainfall"] >= heavy_rain_thresh).sum())
    humid_days = int((city_df["Humidity9am"] >= humid_thresh).sum())
    max_temp = float(city_df["MaxTemp"].max())
    max_rain = float(city_df["Rainfall"].max())

    summary = (
    f"{city.title()} Extremes:\n"
    f"- Hot days (MaxTemp ≥ {hot_thresh}°C): {hot_days}\n"
    f"- Heavy rain days (Rainfall ≥ {heavy_rain_thresh} mm): {heavy_days}\n"
    f"- High humidity mornings (Humidity9am ≥ {humid_thresh}%): {humid_days}\n"
    f"- Peak MaxTemp: {max_temp:.1f}°C, Peak Rainfall: {max_rain:.1f} mm"
    )

    # Chart 1: Hot days vs normal
    f1 = out_path / f"extreme_hot_{safe}.png"
    plt.figure()
    plt.bar(["Normal", "Hot"], [len(city_df) - hot_days, hot_days])
    plt.title(f"Hot Days (Maximum Temperature ≥ {hot_thresh}) - {city}")
    plt.ylabel("Days")
    plt.tight_layout()
    plt.savefig(f1, dpi=150)
    plt.close()

    # Chart 2: Heavy rain days vs normal
    f2 = out_path / f"extreme_heavy_rain_{safe}.png"
    plt.figure()
    plt.bar(["Normal", "Heavy Rain"], [len(city_df) - heavy_days, heavy_days])
    plt.title(f"Heavy Rain Days (Rainfall ≥ {heavy_rain_thresh}) - {city}")
    plt.ylabel("Days")
    plt.tight_layout()
    plt.savefig(f2, dpi=150)
    plt.close()

    charts = [f"/static/img/{f1.name}", f"/static/img/{f2.name}"]
    return summary, charts