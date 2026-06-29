import pandas as pd

def prepare_prophet_dataframe(data):
    """
    Convert query result menjadi format Prophet

    ds = tanggal
    y  = jumlah penjualan
    """

    df = pd.DataFrame(data)
    if df.empty:
        return pd.DataFrame(columns=["ds", "y"])

    df["ds"] = pd.to_datetime(df["ds"])
    df["y"] = df["y"].astype(float)

    return df[["ds", "y"]]