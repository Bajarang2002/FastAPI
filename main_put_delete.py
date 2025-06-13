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
        
class Patient_update(BaseModel):
    name : Annotated[str,Field(...,description="Name of the patient")]
    age :Annotated[int,Field(...,description="Age of the patient")]
    city :Annotated[str,Field(...,description= "City where patients belong")]
    gender :Annotated[Literal['male','female','other'],Field(...,description=" Selelct your gender")]
    height : Annotated[float,Field(...,gt = 0,description= "height in meters")]
    weight : Annotated[float,Field(...,gt=0,description="weight in kgs")]


def load_data():
    with open ('patients.json','r') as f:
        data = json.load(f)
    return data
def save_data(data):
    with open ('patients.json','w') as f:
        json.dump(data,f)


@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patients(patient_id: str = Path(..., description="Valid patient ID to display", example="P001")):
    #load data
    data = load_data() 
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code= 404, detail = "Patient not found")
    
    

@app.put("/update_data/{patient_id}")
def update_data(patient_id:str, patient_updated :Patient_update):
    #load data

    data = load_data()

    # check data exist or not
    if patient_id not in data :
        raise HTTPException(status_code=404,detail="Patient not found")
    
    existing_patient_info = data[patient_id]
    updated_patient_info = patient_updated.model_dump(exclude_unset = True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)

    patient_pydantic_obj.model_dump(exclude='id')

    data[patient_id] = existing_patient_info
    save_data(data)

    return JSONResponse(status_code=201,content="Succesfully update_data")


@app.delete("/delete/{patient_id}")
def delete_data(patient_id: str):
    # Load data
    data = load_data()

    #Check patient exist or not
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=404, content={"Data Delected successfuly"})









