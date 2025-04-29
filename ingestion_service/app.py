# app.py
from fastapi import FastAPI, Request
import boto3
import json
import os

app = FastAPI()

kinesis_stream_name = os.getenv("KINESIS_STREAM_NAME")

kinesis_client = boto3.client("kinesis", region_name="eu-west-1")

@app.post("/transactions")
async def ingest_transaction(request: Request):
    data = await request.json()
    response = kinesis_client.put_record(
        StreamName=kinesis_stream_name,
        Data=json.dumps(data),
        PartitionKey="transaction"
    )
    return {"message": "Transaction received", "response": response}
