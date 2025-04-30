# ml/train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the generated data
df = pd.read_csv('transactions.csv')

# For simplicity: use only "amount" for now
X = df[['amount']]
y = df['is_fraud']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

model = RandomForestClassifier()
model.fit(X_train, y_train)

joblib.dump(model, 'model.pkl')
print("✅ model.pkl saved.")
