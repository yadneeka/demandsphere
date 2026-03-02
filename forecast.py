import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
import math

def generate_forecast(daily_data, steps=7):
    if not daily_data:
        return {"error": "Not enough data"}

    df = pd.DataFrame(daily_data)
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    df = df.set_index('sale_date')
    df = df.sort_index()

    series = df['total_quantity']

    if len(series) < 5:
        return {"error": "Need at least 5 days of data for forecasting"}

    try:
        model = ARIMA(series, order=(1,0,1))
        model_fit = model.fit()

        forecast_values = model_fit.forecast(steps=steps)

        # Cap extreme growth
        last_value = series.iloc[-1]
        forecast_values = np.clip(forecast_values, 0, last_value * 1.5)

        forecast_dates = pd.date_range(
            start=series.index[-1],
            periods=steps + 1,
            freq='D'
        )[1:]

        buffer_percentage = 0.10  # 10% safety buffer

        result = [
    {
        "date": str(date.date()),
        "predicted_quantity": math.ceil(float(value)),
        "recommended_stock": math.ceil(float(value) * (1 + buffer_percentage))
    }
    for date, value in zip(forecast_dates, forecast_values)
]
        return result

    except Exception as e:
        return {"error": f"Forecast failed: {str(e)}"}
