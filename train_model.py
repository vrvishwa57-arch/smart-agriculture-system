import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load data
data = pd.read_csv("crop_data.csv")

X = data.drop("label", axis=1)
y = data["label"]

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")

print("Model trained successfully!")