from fastapi import FastAPI,BackgroundTasks
from db_wrapper import create_connection,close_connection,read_document,read_all
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
from constants import stations
from core.helpers import filter_data
from core.models import train_input,date_input
import json
origins = [
    "https://train-finder-frontend-cjaz.vercel.app/",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def health_check():
    return {"message": "api running fine"}

@app.get("/get-all-dates")
def get_train_data():
    client = create_connection()
    result = read_all(client=client)
    all_dates = []
    for val in result:
        keys = [key for key in val.keys() if key not in ['_id','correlation_id']]
        print(val[keys[1]])
        date = {f"{keys[0]}, updated_at:{val[keys[1]]}"}
        all_dates.extend(date)
    close_connection(client=client)
    return all_dates

@app.post("/get-all-trains")
def get_trains(date: date_input):
    print(date.date)
    result = []
    client = create_connection()
    result = read_document(client,date.date)
    if result:
        mydata = result[date.date]
        result = [keys for keys in mydata]
    close_connection(client=client)
    
    # return result
    return result


@app.post("/get-train-avl")
def get_train_data(data: train_input,background_tasks: BackgroundTasks):
    
    train_number= data.train_number
    date = data.date
    from_station = data.from_station
    to_station = data.to_station
    filtered_data = []
    client = create_connection()
    result = read_document(client,date)
    if result:
        mydata = result[date]
        filtered_data= filter_data(train_number,mydata,from_station,to_station,background_tasks)
    else:
        filtered_data = {train_number: "Data not available for current date. Scrape"}
    close_connection(client=client)
    
    return filtered_data


