from fastapi import FastAPI,Path,HTTPException,Query
import json


app = FastAPI()


def load_data():
    with open ('patients.json','r') as f:
        data = json.load(f)
    return data


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







    