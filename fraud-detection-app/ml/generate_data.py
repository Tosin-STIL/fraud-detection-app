# ml/generate_data.py

from faker import Faker
import pandas as pd
import random

fake = Faker()

def create_transactions(n=10000):
    transactions = []
    for _ in range(n):
        transactions.append({
            'amount': round(random.uniform(10, 5000), 2),
            'device_id': fake.uuid4(),
            'location': fake.city(),
            'is_fraud': random.choices([0, 1], weights=[0.98, 0.02])[0]
        })
    return pd.DataFrame(transactions)

df = create_transactions()
df.to_csv('transactions.csv', index=False)
print("✅ transactions.csv generated.")
