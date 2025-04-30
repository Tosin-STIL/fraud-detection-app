from fastapi import FastAPI, Request
from datetime import datetime
import json
import os
import boto3
from botocore.exceptions import ClientError

app = FastAPI()

LOG_FILE = os.getenv("ACTION_LOG_FILE", "action_log.jsonl")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN", "arn:aws:sns:eu-west-1:590183956481:fraud-alerts")

# Initialize SNS client
sns_client = boto3.client("sns", region_name="eu-west-1")

def publish_alert(transaction_id, probability):
    message = f"🚨 Fraud detected!\nTransaction ID: {transaction_id}\nProbability: {probability}"
    try:
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="Fraud Alert"
        )
    except ClientError as e:
        print(f"[⚠️ SNS Error] Failed to publish alert: {e}")

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

    # Send alert if fraud detected
    if is_fraud:
        publish_alert(transaction_id, probability)

    return {
        "message": f"Action taken: {action}",
        "log": log_entry
    }
