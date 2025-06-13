

from fastapi import FastAPI,Path,HTTPException,Query
from pydantic import BaseModel,Field,computed_field
from fastapi.responses import JSONResponse
from typing import List, Dict, Literal,Annotated
import json


app = FastAPI()


class Patient(BaseModel):
    id :str
    name : Annotated[str,Field(...,description="Name of the patient")]
    age :Annotated[int,Field(...,description="Age of the patient")]
    city :Annotated[str,Field(...,description= "City where patients belong")]
    gender :Annotated[Literal['male','female','other'],Field(...,description=" Selelct your gender")]
    height : Annotated[float,Field(...,gt = 0,description= "height in meters")]
    weight : Annotated[float,Field(...,gt=0,description="weight in kgs")]


    @computed_field
    @property
    def bmi(self)-> float:
        bmi =round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self)-> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        else:
            return "Overweight"


def load_data():
    with open ('patients.json','r') as f:
        data = json.load(f)
    return data
def save_data(data):
    with open ('patients.json','w') as f:
        json.dump(data,f)
    


@app.get("/")
def read_root():
    return {"Message": " Welcome to Hospital patient record management"}


@app.get("/about")
def about():
    return {"Message": " Website ensure, maintain  the patients record"}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patients(patient_id: str = Path(..., description="Valid patient ID to display", example="P001")):
    data = load_data() 

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code= 404, detail = "Patient not found")

@app.get('/sort')
def sort_patients(sort_by :str= Query(...,description= " Sort the data for age, height, wright, bmi"),order: str = Query('asc', description="Order in between ['asc','desc']")):
    valid_fields = ['age','height','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=404, detail=" Invalid field select from {valid_fields}" )
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=404, detail = "Invalid order select between asc and desc")
    
    data = load_data()
    sort_order = True if order =='desc' else False
    sorted_data  = sorted(data.values(),key= lambda x:x.get(sort_by,0),reverse = sort_order  ) 
    return sorted_data


@app.post('/create')
def create(patient:Patient):

    # load data
    data = load_data()

    # Make sure that data already present or not
    if patient.id in data:
        raise HTTPException(status_code=404,detail="Patient already exist")
    
    # Add new patient to the database 

    data[patient.id] = patient.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(status_code=201,content={"message":"successfully return the response"})









    