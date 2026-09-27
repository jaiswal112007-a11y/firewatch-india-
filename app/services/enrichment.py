import pandas as pd

# Known Indian Industrial Zones
INDIAN_INDUSTRIAL_ZONES = [
    # Gujarat — Oil refineries
    (22.3, 69.5, 50, 'Oil Refinery'),       # Jamnagar
    (21.6, 72.9, 30, 'Industrial'),          # Surat
    (22.8, 72.1, 25, 'Industrial'),          # Vadodara
    (23.0, 72.5, 20, 'Industrial'),          # Ahmedabad

    # Jharkhand/Odisha — Steel & Mining
    (22.8, 86.2, 40, 'Steel Plant'),         # Jamshedpur
    (22.0, 85.8, 30, 'Steel Plant'),         # Rourkela
    (23.8, 86.4, 25, 'Coal Mine'),           # Dhanbad
    (23.75, 86.42, 20, 'Coal Mine'),         # Jharia

    # Assam — Oil fields
    (27.47, 95.35, 40, 'Oil Field'),         # Baghjan
    (27.1, 93.6, 30, 'Oil Field'),           # Digboi
    (26.7, 94.2, 25, 'Oil Field'),           # Duliajan

    # Andhra Pradesh
    (17.68, 83.29, 25, 'Oil Refinery'),      # Vizag refinery
    (17.4, 78.5, 20, 'Industrial'),          # Hyderabad industrial

    # Maharashtra
    (19.0, 73.0, 30, 'Industrial'),          # Thane/Navi Mumbai
    (18.6, 73.8, 20, 'Industrial'),          # Pune industrial

    # Punjab/Haryana — Agricultural zones
    (30.9, 75.8, 80, 'Agricultural'),        # Punjab
    (29.0, 76.0, 80, 'Agricultural'),        # Haryana

    # West Bengal
    (22.6, 88.4, 30, 'Industrial'),          # Kolkata industrial
    (23.7, 86.9, 25, 'Steel Plant'),         # Burnpur steel

    # Madhya Pradesh
    (22.0, 79.0, 30, 'Industrial'),          # Jabalpur
    (23.2, 77.4, 25, 'Industrial'),          # Bhopal industrial

    # Tamil Nadu
    (13.1, 80.3, 25, 'Industrial'),          # Chennai industrial
    (10.9, 78.7, 20, 'Industrial'),          # Trichy
]


def is_industrial_zone(lat, lon):
    """Check if location is near a known Indian industrial zone"""
    for zone_lat, zone_lon, radius_km, zone_type in INDIAN_INDUSTRIAL_ZONES:
        dist = ((lat - zone_lat)**2 + (lon - zone_lon)**2)**0.5 * 111
        if dist < radius_km:
            return 1, zone_type
    return 0, 'Non-Industrial'


def check_persistence(lat, lon, df_history):
    """Check if same spot appeared multiple times"""
    nearby = df_history[
        (abs(df_history['latitude'] - lat) < 0.05) &
        (abs(df_history['longitude'] - lon) < 0.05)
    ]
    return len(nearby)


def enrich_hotspots(df, df_history=pd.DataFrame()):
    """Enrich hotspots with industrial zone data"""
    print(f"Enriching {len(df)} hotspots...")

    enriched = []
    for _, row in df.iterrows():
        lat = row['latitude']
        lon = row['longitude']

        # Check industrial zone
        industrial_nearby, zone_type = is_industrial_zone(lat, lon)

        # Check persistence
        persistence = check_persistence(lat, lon, df_history) \
                      if not df_history.empty else 0

        enriched.append({
            **row.to_dict(),
            'industrial_nearby': industrial_nearby,
            'land_cover': zone_type,
            'persistence_count': persistence,
            'is_chronic': 'yes' if persistence >= 3 else 'no'
        })

    print(f"Enrichment done — {sum(1 for e in enriched if e['industrial_nearby'] == 1)} industrial zones found")
    return pd.DataFrame(enriched)