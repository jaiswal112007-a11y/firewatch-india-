import requests
import pandas as pd
from io import StringIO
from dotenv import load_dotenv
import os

env_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(dotenv_path=env_path)
MAP_KEY = "2236028ccafa2ccabfd125e00ca4651d"

def fetch_hotspots(days=5):
    url = (
        f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
        f"{MAP_KEY}/VIIRS_SNPP_NRT/"
        f"68,8,92,35/"
        f"{days}"
    )

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        df = pd.read_csv(StringIO(response.text))

        # Sirf India ke andar filter karo
        df = df[
            (df['latitude'] >= 10) & (df['latitude'] <= 35) &
            (df['longitude'] >= 72) & (df['longitude'] <= 92)
        ]

        # Remove low confidence detections
        df = df[df['confidence'] != 'low']

        # Keep only required columns
        df = df[[
            'latitude',
            'longitude',
            'bright_ti4',
            'frp',
            'confidence',
            'satellite',
            'instrument',
            'acq_date',
            'acq_time'
        ]]

        df.rename(columns={'bright_ti4': 'brightness'}, inplace=True)

        print(f"{len(df)} hotspots fetched from FIRMS")
        return df

    except Exception as e:
        print(f"FIRMS fetch error: {e}")
        return pd.DataFrame()