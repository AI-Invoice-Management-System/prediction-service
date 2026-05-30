from pydantic import BaseModel, Field

class InvoiceRequest(BaseModel):
    cust_number: str = Field(..., example="0200769623")
    cust_payment_terms: str = Field(..., example="NAH4")
    due_in_date: str = Field(..., example="2020-03-13")
    baseline_create_date: str = Field(..., example="2020-02-27")
    total_open_amount: float = Field(..., example=54273.28)

class PredictionResponse(BaseModel):
    predicted_delay_days: float
    predicted_clear_date: str
    aging_bucket: str
