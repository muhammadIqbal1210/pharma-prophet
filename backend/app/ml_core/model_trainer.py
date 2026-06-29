from prophet import Prophet

def run_forecast(df, days=90):

    model = Prophet()

    model.fit(df)

    future = model.make_future_dataframe(
        periods=days
    )

    forecast = model.predict(future)

    return forecast