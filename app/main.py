from fastapi import FastAPI
from starlette.responses import JSONResponse
from fastapi.responses import HTMLResponse
from joblib import load
import pandas as pd
import os
import numpy as np
from  my_krml_24587139.models.modelling import generate_features, time_series_forecast_generate_data
from  my_krml_24587139.data.sets import create_date_features


app = FastAPI()

print(os.getcwd())
xgb_pipe = load('../models/predictive/xgb_pipe.joblib')
prophet_m = load('../models/forecasting/prophet.joblib')

@app.get("/", response_class=HTMLResponse)
def read_root():
    brief_description = '''
    Objectives:
    - Predictive model to predict sales revenue 
    - Forecasting model to forecast national sales revenue for the next 7 days 

    List of endpoints:
    - /health : Returns a welcome message
    - /sales/stores/items: input item_id, store_id and date - returns the respective predicted sales revenue 
    - /sales/national: input parameter date - returns the forecasted toatl sales revenue for the next 7 days
    
    '''
    # Replace newline characters with <br> tags
    formatted_description = brief_description.replace('\n', '<br>\n')
    return formatted_description

@app.get('/health', status_code=200)
def healthcheck():
    return 'The API is ready to go!'

@app.get("/sales/stores/items")
def predict(item_id: str, store_id: str, date: str):
    calendar_events = pd.read_csv('../data/raw/calendar_events.csv')
    calendar = pd.read_csv('../data/raw/calendar.csv')
    # Joining the calendar and calendar_events data sets
    merged_calendar = calendar.merge(calendar_events, how='left', on='date')
    data_obs = generate_features(item_id=item_id,
                             store_id=store_id,
                             date=date,
                             calendar_events_df=merged_calendar)
    
    data_obs_features = create_date_features(df=data_obs) 
    pred = xgb_pipe.predict(data_obs_features)
    return JSONResponse({'prediction': np.float64(pred[0])})

@app.get("/sales/national")
def forecast(date: str):
    data_obs = time_series_forecast_generate_data(date=date)
    pred = prophet_m.predict(data_obs)
    print(type(pred))
    print(pred)
    return JSONResponse(dict(zip(pred['ds'].dt.strftime('%Y-%m-%d'), 
                                 pred['yhat'])))