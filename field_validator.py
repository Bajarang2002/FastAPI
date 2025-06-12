from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator
from typing import List, Dict,Optional,Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr
    linkedln_url : AnyUrl
    age: int
    weight: float
    height: float
    married: bool
    allergies: List[str]
    contact_detail: Dict[str, str]



@field_validator('email')         # Use this to validate particular one field
@classmethod
def validate_field(cls,value):
    valid_domain=['hdfc.com',"sbi.com"]
    #abc@gmail.com
    domain_name = value.split("@") [-1]

    if domain_name not in valid_domain:
        raise ValueError("Plase provide valid domain name")
    return value   

@field_validator('name')  
@classmethod
def validate_name(cls,value):
     return value.upper()     


@model_validator(mode = 'after')                     # the mode indicate type corrosion
def show_emergency_number(cls,model):
    if model.age> 60 & 'emergency' not in model.contact_detail :
        raise ValueError("older than 60 must have emrgency number")
    return model




def update_data(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.weight)
    print(patient.married)

    print("data updated")

patient_info = {
    'name': 'Pavan',
    'email': 'abc@gmail.com',
    'age' : 100,
    'linkedln_url': 'https://www.linkedin.com/in/bajarang-dhamanekar/',
    'height': 1.7,
    'weight': 70,
    'married': True,
    'allergies': ['Fungal Infection', 'fever'],
    'contact_detail': {"phone_no": "7218761130","emergency":"123456"}
}


patient1 = Patient(**patient_info)
update_data(patient1)




 

