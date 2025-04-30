# generate_model.py

import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

# Dummy data (5 input features)
X = np.random.rand(1000, 5)
y = (X[:, 0] + X[:, 1] > 1).astype(int)  # Simple rule-based label

# Train a random forest classifier
model = RandomForestClassifier()
model.fit(X, y)

# Save the model to model.pkl
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ model.pkl created successfully.")
