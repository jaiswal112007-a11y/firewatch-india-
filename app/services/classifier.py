import joblib
import pandas as pd
import numpy as np
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../ml/model.pkl')

FIRE_TYPES = {
    0: 'Industrial Fire',
    1: 'Wildfire',
    2: 'Agricultural Burning',
    3: 'Gas Flare'
}

_model = None

def load_model():
    global _model
    if _model is not None:
        return _model
    try:
        _model = joblib.load(MODEL_PATH)
        print("Model loaded successfully")
        return _model
    except Exception as e:
        print(f"Model not found: {e}")
        return None


def rule_based_classify(row):
    frp = row.get('frp', 0) or 0
    industrial = row.get('industrial_nearby', 0) or 0
    persistence = row.get('persistence_count', 0) or 0
    land_cover = row.get('land_cover', 'unknown') or 'unknown'

    if industrial == 1 and frp > 50:
        return 'Industrial Fire', 0.75
    if industrial == 1 and persistence >= 3:
        return 'Gas Flare', 0.70
    if land_cover in ['farmland', 'meadow', 'grass']:
        return 'Agricultural Burning', 0.72
    if land_cover in ['forest', 'wood', 'scrub']:
        return 'Wildfire', 0.78
    if frp and frp > 100:
        return 'Industrial Fire', 0.65
    return 'Wildfire', 0.55


def classify_hotspots(df):
    model = load_model()
    features = ['frp', 'brightness', 'industrial_nearby', 'persistence_count']

    results = []
    for _, row in df.iterrows():
        try:
            row_dict = row.to_dict()
            
            if model is not None:
                feat_vals = [row_dict.get(f, 0) or 0 for f in features]
                X = pd.DataFrame([feat_vals], columns=features)
                pred = model.predict(X)[0]
                proba = model.predict_proba(X)[0]
                fire_type = FIRE_TYPES[int(pred)]
                confidence_score = round(float(np.max(proba)), 2)
            else:
                fire_type, confidence_score = rule_based_classify(row_dict)

        except Exception as e:
            print(f"Classification error: {e}")
            fire_type, confidence_score = rule_based_classify(row.to_dict())

        results.append({
            **row.to_dict(),
            'fire_type': fire_type,
            'confidence_score': confidence_score
        })

    return pd.DataFrame(results)