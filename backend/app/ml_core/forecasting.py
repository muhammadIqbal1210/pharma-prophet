from prophet import Prophet

def generate_forecast(df, days=90):
    if len(df) < 2:
        return None

    model = Prophet(
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=True
    )

    model.fit(df)
    future = model.make_future_dataframe(
        periods=days
    )
    forecast = model.predict(future)
    return forecast