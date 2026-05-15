# app/ml_core/model_trainer.py
import pandas as pd
from prophet import Prophet

def run_prophet_forecast(data):
    df = pd.DataFrame(data)
    df['ds'] = pd.to_datetime(df['ds'])
    
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
    model.add_country_holidays(country_name='ID')
    model.fit(df)
    
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30).to_dict('records')