import osmnx as ox
import pandas as pd
from shapely.geometry import Point
import warnings
warnings.filterwarnings('ignore')

def get_nearby_industrial(lat, lon, dist=2000):
    """Check if industrial area exists within 2km"""
    try:
        tags = {'landuse': ['industrial', 'commercial'],
                'man_made': ['works', 'petroleum_well', 'chimney'],
                'industry': True}
        
        gdf = ox.features_from_point((lat, lon), tags=tags, dist=dist)
        return 1 if len(gdf) > 0 else 0
    
    except Exception:
        return 0


def get_land_cover(lat, lon, dist=500):
    """Get surrounding land type from OSM"""
    try:
        tags = {'landuse': True, 'natural': True}
        gdf = ox.features_from_point((lat, lon), tags=tags, dist=dist)
        
        if len(gdf) == 0:
            return 'unknown'
        
        if 'landuse' in gdf.columns:
            landuse = gdf['landuse'].dropna()
            if len(landuse) > 0:
                return landuse.mode()[0]
        
        return 'unknown'
    
    except Exception:
        return 'unknown'


def check_persistence(lat, lon, df_history):
    """Check if same spot appeared multiple times — chronic source"""
    nearby = df_history[
        (abs(df_history['latitude'] - lat) < 0.05) &
        (abs(df_history['longitude'] - lon) < 0.05)
    ]
    return len(nearby)


def enrich_hotspots(df, df_history=pd.DataFrame()):
    """Add all 5 signals to each hotspot"""
    print("Enriching hotspots with OSM data...")
    
    enriched = []
    for _, row in df.iterrows():
        lat = row['latitude']
        lon = row['longitude']
        
        # Signal 1 — Industrial nearby (OSM)
        industrial_nearby = get_nearby_industrial(lat, lon)
        
        # Signal 2 — Land cover type
        land_cover = get_land_cover(lat, lon)
        
        # Signal 3 — Persistence count
        persistence = check_persistence(lat, lon, df_history) \
                      if not df_history.empty else 0
        
        # Signal 4 — FRP intensity (already in df)
        # Signal 5 — Brightness temperature (already in df)
        
        enriched.append({
            **row.to_dict(),
            'industrial_nearby': industrial_nearby,
            'land_cover': land_cover,
            'persistence_count': persistence,
            'is_chronic': 'yes' if persistence >= 3 else 'no'
        })
    
    return pd.DataFrame(enriched)