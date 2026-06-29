from pydantic import BaseModel, ConfigDict
from typing import List

class PredictionRequest(BaseModel):
    days: int = 30  # Number of future days to forecast

    model_config = ConfigDict(from_attributes=True)
