from fastapi import FastAPI, Request
import pickle
import numpy as np
import os

app = FastAPI()

# Load the pre-trained model
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()

    # You may customize this schema
    features = np.array(data["features"]).reshape(1, -1)

    # Get prediction
    probability = model.predict_proba(features)[0][1]
    prediction = int(probability > 0.5)

    return {
        "is_fraud": prediction,
        "fraud_probability": round(probability, 4)
    }
