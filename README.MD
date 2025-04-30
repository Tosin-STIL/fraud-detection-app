# Fraud Detection Microservices Application

## Project Overview

This repository, **fraud-detection-app**, contains the full implementation of the microservices application layer for a real-time fraud detection system. It is the counterpart to the infrastructure code located in [`fraud-detection-infra`](https://github.com/Tosin-STIL/fraud-detection-infra). The application is composed of three FastAPI-based services:

- **Ingestion Service** – Receives transaction data and pushes it to Kinesis.
- **Fraud Detection Service** – Consumes from Kinesis and applies a machine learning model to determine fraud likelihood.
- **Action Service** – Responds to fraud events by logging, alerting, or simulating actions such as blocking accounts.

All services are containerized, deployed via ECS (Fargate), and orchestrated through a secure, automated CI/CD pipeline using GitHub Actions.

---

## Technologies Used

- **Python 3.11**
- **FastAPI**
- **Docker**
- **Amazon ECR & ECS (Fargate)**
- **Amazon Kinesis**
- **Amazon SNS**
- **Amazon RDS (PostgreSQL)**
- **GitHub Actions**
- **Scikit-Learn, Joblib, Faker, Pandas**

---

## Microservices Breakdown

### 1. Ingestion Service
- **Path**: `ingestion_service/`
- **Role**: Receives POST requests with transaction data and streams it to a Kinesis Data Stream.
- **Environment Variable**: `KINESIS_STREAM_NAME`
- **Key File**: `app.py`

### 2. Fraud Detection Service
- **Path**: `fraud_detection_service/`
- **Role**: Applies an ML model (trained offline) to determine fraud probability based on features.
- **Key Files**: `app.py`, `model.pkl`
- **ML Training Scripts**:
  - `ml/generate_data.py`: Generates synthetic transaction data
  - `ml/train_model.py`: Trains a RandomForest classifier

### 3. Action Service
- **Path**: `action_service/`
- **Role**: Logs fraud decisions and emits alerts via Amazon SNS or to local audit logs.
- **Environment Variable**: `ACTION_LOG_FILE`
- **Key File**: `app.py`

---

## Model Training & Inference

### Phase 1: Generate Training Data
```bash
cd ml/
pip install faker pandas
python generate_data.py
```
Output: `transactions.csv`

### Phase 2: Train Model
```bash
pip install scikit-learn joblib
python train_model.py
```
Output: `model.pkl` (used in `fraud_detection_service`)

---

## Local Testing

Each service can be run locally via:
```bash
cd <service_name>
pip install -r requirements.txt
uvicorn app:app --reload --port 8000  # change port per service
```

Example endpoints:
- Swagger UI: `http://127.0.0.1:8000/docs`
- Predict API: `POST /predict` with JSON body

---

## Docker Build & Push

Example steps for each service:

### Step 1: Build Docker Image
```bash
docker build -t ingestion-service:latest .
```

### Step 2: Tag for ECR
```bash
docker tag ingestion-service:latest \
590183956481.dkr.ecr.eu-west-1.amazonaws.com/fraud-detection-dev-ingestion-service:latest
```

### Step 3: Push to ECR
```bash
docker push \
590183956481.dkr.ecr.eu-west-1.amazonaws.com/fraud-detection-dev-ingestion-service:latest
```

Repeat for `fraud-detection-service` and `action-service` with appropriate tags.

---

## GitHub Actions CI/CD

Workflow: `.github/workflows/deploy.yml`

### Highlights
- Reusable workflow triggered per microservice
- Dynamically builds Docker images
- Pushes to ECR
- Registers new ECS task definition
- Updates ECS services via `update-service`

To trigger deployment:
- Go to GitHub Actions tab
- Select "Deploy to ECS"
- Input `ingestion_service`, `fraud_detection_service`, or `action_service`
- Click "Run workflow"

---

## CloudWatch Logs & Metrics

ECS task definitions emit logs to CloudWatch:
- `/ecs/fraud-detection-dev-<service>`

Enable Container Insights in ECS Cluster for metrics like CPU, memory, and task health.

---

## Fraud Alerting (SNS)

- SNS Topic: `fraud-alerts`
- Alerts sent by `action_service` for high-probability fraud events
- Subscribe via:
```bash
aws sns subscribe \
--topic-arn arn:aws:sns:eu-west-1:590183956481:fraud-alerts \
--protocol email \
--notification-endpoint your_email@example.com
```

---

## Recommendations

### ✅ Audit Logging to RDS
Store high-confidence fraud decisions:
```sql
CREATE TABLE audit_log (
  id SERIAL PRIMARY KEY,
  transaction_id VARCHAR,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR,
  details JSONB
);
```

### ✅ Use ECS Exec for Debugging
Use secure container access for troubleshooting:
```bash
aws ecs execute-command --cluster ... --task ... --container ... --interactive --command "sh"
```

### ✅ Store Secrets in SSM Parameter Store
Store credentials, keys, and sensitive configs securely:
```bash
aws ssm put-parameter --name "/fraud-detection/dev/db-password" --value "secret" --type SecureString
```

---

## Directory Structure (Simplified)

```
fraud-detection-app/
├── ingestion_service/
├── fraud_detection_service/
├── action_service/
├── ml/
│   ├── generate_data.py
│   └── train_model.py
└── .github/
    └── workflows/
        └── deploy.yml
```

---

## License

This project is open-source and licensed under the MIT License.

## Maintainer

**Oluwatosin Jegede**  
Cloud Solutions Architect | DevOps Engineer  
[GitHub](https://github.com/Tosin-STIL) | [LinkedIn](https://www.linkedin.com/in/oluwatosin-jegede/)

