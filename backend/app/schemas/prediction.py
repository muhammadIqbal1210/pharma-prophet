from pydantic import BaseModel


class PredictionResponse(BaseModel):

    product_id: int
    product_name: str
    current_stock: int

    forecast_30_days: int
    forecast_60_days: int
    forecast_90_days: int

    recommended_order: int