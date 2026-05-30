# Invoice Payment Delay Prediction Service

This service provides an API to predict invoice payment delays and aging buckets.

## Getting Started

### Prerequisites
- Python 3.8+
- Dependencies listed in `requirements.txt`

### Running the API
```bash
uvicorn src.main.api.app:app --reload
```

## API Endpoints

### 1. Root Endpoint
Checks if the API is running.

**Request:**
```bash
curl -X GET http://localhost:8000/
```

### 2. Predict Delay
Predicts the payment delay for a given invoice.

**Request:**
```bash
curl -X POST http://localhost:8000/predict \
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
