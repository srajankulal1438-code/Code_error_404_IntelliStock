from prophet import Prophet
import pandas as pd

def forecast_sales(data):
    df = data.rename(columns={'date': 'ds', 'sales': 'y'})
    df['ds'] = pd.to_datetime(df['ds'])

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=7)
    forecast = model.predict(future)

    return forecast[['ds', 'yhat']]