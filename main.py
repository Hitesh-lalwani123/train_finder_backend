from fastapi import FastAPI,BackgroundTasks
from db_wrapper import create_connection,close_connection,read_document,read_all
app = FastAPI()
from constants import stations
from core.helpers import filter_data

@app.get("/")
def test():
    return {"message": "Hello from FastAPI!"}

@app.get("/get-all-dates")
def get_train_data():
    client = create_connection()
    result = read_all(client=client)
    all_dates = []
    for val in result:
        keys = [key for key in val.keys() if key != "_id"]
        all_dates.extend(keys)
    close_connection(client=client)
    return all_dates

# @app.get("/get-data")
# def get_train_data(date: str,background_tasks: BackgroundTasks):
#     client = create_connection()
#     result = read_document(client,date)
#     mydata = result[date]
#     filtered_data= filter_data(mydata,background_tasks)
#     close_connection(client=client)
    
#     return filtered_data



@app.get("/get-train-avl")
def get_train_data(train_number: str,date:str ,background_tasks: BackgroundTasks):
    client = create_connection()
    client = create_connection()
    result = read_document(client,date)
    mydata = result[date]
    filtered_data= filter_data(train_number,mydata,background_tasks)
    
    close_connection(client=client)
    
    return filtered_data


