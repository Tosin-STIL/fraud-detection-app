from fastapi import FastAPI, Request
from datetime import datetime
import json
import os

app = FastAPI()

LOG_FILE = os.getenv("ACTION_LOG_FILE", "action_log.jsonl")

@app.post("/action")
async def handle_action(request: Request):
    data = await request.json()

    transaction_id = data.get("transaction_id")
    is_fraud = data.get("is_fraud")
    probability = data.get("fraud_probability")

    action = "block_transaction" if is_fraud else "allow_transaction"

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "transaction_id": transaction_id,
        "action": action,
        "fraud_score": probability,
    }

    # Append to local log file
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    return {
        "message": f"Action taken: {action}",
        "log": log_entry
    }
