import requests
import pandas as pd
from io import StringIO
from dotenv import load_dotenv
import os

load_dotenv()

MAP_KEY = os.getenv("FIRMS_MAP_KEY")

def fetch_hotspots(days=1):
    url = (
        f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
        f"{MAP_KEY}/VIIRS_SNPP_NRT/"
        f"60,5,100,40/"
        f"{days}"
    )

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        df = pd.read_csv(StringIO(response.text))

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