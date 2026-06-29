from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.product import Product
from app.models.transaction import (
    Transaction,
    TransactionDetail
)

from app.ml_core.preprocessing import (
    prepare_prophet_dataframe
)

from app.ml_core.forecasting import (
    generate_forecast
)
class ForecastService:

    @staticmethod
    def forecast_product(
        db: Session,
        product_id: int
    ):

        product = (
            db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

        if not product:
            raise ValueError(
                "Produk tidak ditemukan"
            )

        sales = (
            db.query(
                func.date(Transaction.tanggal).label("ds"),
                func.sum(
                    TransactionDetail.jumlah
                ).label("y")
            )
            .join(
                Transaction,
                Transaction.id ==
                TransactionDetail.transaction_id
            )
            .filter(
                TransactionDetail.product_id
                == product_id
            )
            .group_by(
                func.date(Transaction.tanggal)
            )
            .order_by(
                func.date(Transaction.tanggal)
            )
            .all()
        )

        data = []

        for row in sales:
            data.append({
                "ds": row.ds,
                "y": row.y
            })

        df = prepare_prophet_dataframe(
            data
        )

        forecast = generate_forecast(
            df,
            90
        )

        if forecast is None:
            return None

        forecast_30 = int(
            forecast.tail(30)["yhat"]
            .clip(lower=0)
            .sum()
        )

        forecast_60 = int(
            forecast.tail(60)["yhat"]
            .clip(lower=0)
            .sum()
        )

        forecast_90 = int(
            forecast.tail(90)["yhat"]
            .clip(lower=0)
            .sum()
        )

        recommended_order = max(
            0,
            forecast_30 -
            product.stok_saat_ini
        )

        # Format ds columns to string for JSON serialization
        df_json = df.copy()
        df_json['ds'] = df_json['ds'].dt.strftime('%Y-%m-%d')
        historical_list = df_json.to_dict('records')

        forecast_json = forecast.copy()
        forecast_json['ds'] = forecast_json['ds'].dt.strftime('%Y-%m-%d')
        forecast_json['yhat'] = forecast_json['yhat'].clip(lower=0)
        forecast_json['yhat_lower'] = forecast_json['yhat_lower'].clip(lower=0)
        forecast_json['yhat_upper'] = forecast_json['yhat_upper'].clip(lower=0)
        forecast_list = forecast_json[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict('records')

        return {
            "product_id": product.id,
            "product_name": product.nama_produk,
            "current_stock": product.stok_saat_ini,
            "forecast_30_days": forecast_30,
            "forecast_60_days": forecast_60,
            "forecast_90_days": forecast_90,
            "recommended_order": recommended_order,
            "historical_data": historical_list,
            "forecast_data": forecast_list
        }

    @staticmethod
    def forecast_all_products(db: Session):

        products = db.query(Product).all()

        results = []

        for product in products:

            sales = (
                db.query(
                    func.date(Transaction.tanggal).label("ds"),
                    func.sum(
                        TransactionDetail.jumlah
                    ).label("y")
                )
                .join(
                    Transaction,
                    Transaction.id ==
                    TransactionDetail.transaction_id
                )
                .filter(
                    TransactionDetail.product_id ==
                    product.id
                )
                .group_by(
                    func.date(Transaction.tanggal)
                )
                .order_by(
                    func.date(Transaction.tanggal)
                )
                .all()
            )

            data = [
                {
                    "ds": row.ds,
                    "y": row.y
                }
                for row in sales
            ]

            df = prepare_prophet_dataframe(data)

            # Skip jika data terlalu sedikit
            if len(df) < 2:
                continue

            forecast = generate_forecast(df, 30)

            if forecast is None:
                continue

            forecast_30 = int(
                forecast.tail(30)["yhat"]
                .clip(lower=0)
                .sum()
            )

            recommended_order = max(
                0,
                forecast_30 - product.stok_saat_ini
            )

            results.append({
                "product_id": product.id,
                "product_name": product.nama_produk,
                "category": product.kategori,
                "current_stock": product.stok_saat_ini,
                "minimum_stock": product.stok_minimum,
                "forecast_30_days": forecast_30,
                "recommended_order": recommended_order,
                "status": (
                    "KRITIS"
                    if product.stok_saat_ini <
                    product.stok_minimum
                    else "AMAN"
                )
            })

        results.sort(
            key=lambda x:
            x["recommended_order"],
            reverse=True
        )

        return results
