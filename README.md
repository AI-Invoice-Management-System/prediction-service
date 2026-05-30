# Invoice Payment Delay Prediction Service

This service provides an API to predict invoice payment delays and aging buckets.

## Getting Started

### Prerequisites
- Python 3.11+ (recommended)
- Dependencies listed in `requirements.txt` (pinned for reproducibility)

### Running the API
```bash
uvicorn src.main.api.app:app --reload
```

### Running with Docker

1. **Build the Docker image:**
```bash
docker build -t prediction-service .
```

2. **Run the Docker container:**
```bash
docker run -p 9779:9779 prediction-service
```

### Running with Docker Compose

1. **Start the service:**
```bash
docker-compose up --build
```
The API will be available at `http://localhost:9779`.

## Logging

### Local Execution
Logs are printed directly to the terminal where you started the `uvicorn` or `python main.py` command.

### Docker Execution
To view logs for a running container:
```bash
docker logs <container_id_or_name>
```
To follow logs in real-time:
```bash
docker logs -f <container_id_or_name>
```

### Docker Compose Execution
To view logs for all services:
```bash
docker-compose logs
```
To follow logs for the prediction service:
```bash
docker-compose logs -f prediction-service
```

## API Endpoints

### 1. Root Endpoint
Checks if the API is running.

**Request:**
```bash
curl -X GET http://localhost:9779/
```

### 2. Predict Delay
Predicts the payment delay for a given invoice.

**Request:**
```bash
curl -X POST http://localhost:9779/predict \
     -H "Content-Type: application/json" \
     -d '{
           "cust_number": "0200769623",
           "cust_payment_terms": "NAH4",
           "due_in_date": "2020-03-13",
           "baseline_create_date": "2020-02-27",
           "total_open_amount": 54273.28
         }'
```

**Schema:**
- `cust_number`: Customer number (string)
- `cust_payment_terms`: Payment terms (string)
- `due_in_date`: Due date in YYYY-MM-DD format (string)
- `baseline_create_date`: Baseline creation date in YYYY-MM-DD format (string)
- `total_open_amount`: Total open amount (float)
