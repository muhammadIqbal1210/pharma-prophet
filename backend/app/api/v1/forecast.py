from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.session import (
    get_db
)

from app.services.forecast_service import (
    ForecastService
)

router = APIRouter(
    tags=["Forecast"]
)

@router.get("/all")
def forecast_all(
    db: Session = Depends(get_db)
):
    return ForecastService.forecast_all_products(
        db
    )

@router.get("/{product_id}")
def forecast_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    return ForecastService.forecast_product(
        db,
        product_id
    )