from pydantic import BaseModel, validator

class train_input(BaseModel):
    train_number:str
    date:str
    from_station:str
    to_station:str

class date_input(BaseModel):
    date: str