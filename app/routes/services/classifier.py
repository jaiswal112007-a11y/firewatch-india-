import joblib
import pandas as pd
import numpy as np
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../ml/model.pkl')

# Fire type labels
FIRE_TYPES = {
    0: 'Industrial Fire',
    1: 'Wildfire',
    2: 'Agricultural Burning',
    3: 'Gas Flare'
}

def load_model():
    """Load XGBoost model from disk"""
    try:
        model = joblib.load(MODEL_PATH)
        print("Model loaded successfully")
        return model
    except Exception:
        print("Model not found — using rule based fallback")
        return None


def rule_based_classify(row):
    """Fallback classification when model not available"""
    if row['industrial_nearby'] == 1 and row['frp'] > 50:
        return 'Industrial Fire', 0.75

    if row['industrial_nearby'] == 1 and row['persistence_count'] >= 3:
        return 'Gas Flare', 0.70

    if row['land_cover'] in ['farmland', 'meadow', 'grass']:
        return 'Agricultural Burning', 0.72

    if row['land_cover'] in ['forest', 'wood', 'scrub']:
        return 'Wildfire', 0.78

    return 'Industrial Fire', 0.55


def classify_hotspots(df):
    """Classify each hotspot — model if available, else rule based"""
    model = load_model()

    features = ['frp', 'brightness', 'industrial_nearby', 'persistence_count']

    results = []
    for _, row in df.iterrows():
        try:
            if model is not None:
                X = pd.DataFrame([row[features]])
                pred = model.predict(X)[0]
                proba = model.predict_proba(X)[0]
                fire_type = FIRE_TYPES[pred]
                confidence_score = round(float(np.max(proba)), 2)
            else:
                fire_type, confidence_score = rule_based_classify(row)

        except Exception:
            fire_type, confidence_score = rule_based_classify(row)

        results.append({
            **row.to_dict(),
            'fire_type': fire_type,
            'confidence_score': confidence_score
        })

    return pd.DataFrame(results)