import pandas as pd
from prophet import Prophet

def run_prophet_forecast(data):
    # Ubah data dari DB menjadi DataFrame Pandas
    df = pd.DataFrame(data)
    
    # Cara melihat data training di terminal/console
    print("--- DATA TRAINING YANG DITERIMA ---")
    print(df.head()) # Melihat 5 data teratas
    print(df.tail()) # Melihat 5 data terbawah
    # Inisialisasi Prophet dengan parameter yang optimal
    model = Prophet(
        yearly_seasonality=True, 
        weekly_seasonality=True,
        daily_seasonality=False
    )
    
    # Tambahkan hari libur Indonesia untuk akurasi lebih tinggi
    model.add_country_holidays(country_name='ID')
    
    # Proses Training
    model.fit(df)
    
    # Prediksi untuk 30 hari ke depan
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    
    # Ambil kolom esensial saja (Tanggal, Prediksi, Batas Bawah, Batas Atas)
    result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30)
    return result.to_dict('records')