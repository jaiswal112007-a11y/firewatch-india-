import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

# Fire type labels
# 0 = Industrial Fire
# 1 = Wildfire
# 2 = Agricultural Burning
# 3 = Gas Flare

def create_synthetic_data():
    """Create rule based training data — no labeled dataset available"""
    np.random.seed(42)
    n = 1000

    data = []

    # Industrial Fire — high FRP, industrial nearby, low persistence
    for _ in range(250):
        data.append({
            'frp': np.random.uniform(50, 300),
            'brightness': np.random.uniform(320, 450),
            'industrial_nearby': 1,
            'persistence_count': np.random.randint(0, 3),
            'label': 0
        })

    # Wildfire — medium FRP, no industry, forest land
    for _ in range(250):
        data.append({
            'frp': np.random.uniform(10, 100),
            'brightness': np.random.uniform(300, 380),
            'industrial_nearby': 0,
            'persistence_count': np.random.randint(0, 2),
            'label': 1
        })

    # Agricultural Burning — low FRP, no industry, seasonal
    for _ in range(250):
        data.append({
            'frp': np.random.uniform(5, 50),
            'brightness': np.random.uniform(290, 340),
            'industrial_nearby': 0,
            'persistence_count': np.random.randint(0, 1),
            'label': 2
        })

    # Gas Flare — high FRP, industrial nearby, high persistence
    for _ in range(250):
        data.append({
            'frp': np.random.uniform(100, 500),
            'brightness': np.random.uniform(380, 500),
            'industrial_nearby': 1,
            'persistence_count': np.random.randint(3, 10),
            'label': 3
        })

    return pd.DataFrame(data)


def train_model():
    print("Creating synthetic training data...")
    df = create_synthetic_data()

    features = ['frp', 'brightness', 'industrial_nearby', 'persistence_count']
    X = df[features]
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training XGBoost model...")
    model = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=42,
        eval_metric='mlogloss'
    )

    model.fit(X_train, y_train)

    # Evaluation
    y_pred = model.predict(X_test)
    print("\nModel Performance:")
    print(classification_report(
        y_test, y_pred,
        target_names=[
            'Industrial Fire',
            'Wildfire',
            'Agricultural Burning',
            'Gas Flare'
        ]
    ))

    # Save model
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    joblib.dump(model, model_path)
    print(f"\nModel saved to {model_path}")


if __name__ == "__main__":
    train_model()