import pickle
from pathlib import Path
from typing import List, Dict

# Directory where model pickle files are stored
MODEL_DIR = Path(__file__).resolve().parents[2] / "models"

def _find_model_path(product_name: str) -> Path:
    """Return the Path to the model file matching the given product name.
    The matching is case‑insensitive and looks for the product name (spaces replaced by underscores)
    inside the stem of the pickle filename.
    Raises FileNotFoundError if no model is found.
    """
    normalized = product_name.lower().replace(" ", "_")
    for file in MODEL_DIR.glob("*.pkl"):
        if normalized in file.stem.lower():
            return file
    raise FileNotFoundError(f"Model file for product '{product_name}' not found in {MODEL_DIR}")

def load_model(product_name: str):
    """Load and return the pickled Prophet model for the given product."""
    model_path = _find_model_path(product_name)
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model

def forecast(product_name: str, days: int = 30) -> List[Dict]:
    """Generate a forecast for *days* ahead using the stored Prophet model.
    Returns a list of dictionaries compatible with the ``Forecast`` Pydantic model.
    """
    model = load_model(product_name)
    future = model.make_future_dataframe(periods=days)
    prediction = model.predict(future)
    # Take only the future part (last ``days`` rows)
    future_records = prediction.tail(days)[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    # Convert to list of dicts, ensuring JSON‑serialisable types
    result = []
    for _, row in future_records.iterrows():
        result.append({
            "ds": row["ds"].strftime("%Y-%m-%d"),
            "yhat": float(row["yhat"]),
            "yhat_lower": float(row["yhat_lower"]),
            "yhat_upper": float(row["yhat_upper"]),
        })
    return result
