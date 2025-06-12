from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import List, Dict,Optional,Annotated,Strict

class Patient(BaseModel):
    name: str= Field(max_length=30)
    email: EmailStr
    linkedln_url : AnyUrl
    age: Annotated[int ,Field(gt=0,le=120)]# optional default for missing age
    weight: float
    height: float
    married: Optional[bool]
    allergies: Optional[List[str]]=None
    contact_detail: Dict[str, str]

def insert_data(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.weight)
    print(patient.married)
    print("data inserted")

def update_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.weight)
    print(patient.married)

    print("data updated")

patient_info = {
    "name": "Pavan",
    "email": "dhamanekarbajrang2002@gmail.com",
    "age" : "100",
    "linkedln_url": "https://www.linkedin.com/in/bajarang-dhamanekar/",
    "height": 1.7,
    "weight": 70,
    "married": True,
    "allergies": ["Fungal Infection", "fever"],
    "contact_detail": {"phone_no": "7218761130"}
}

patient1 = Patient(**patient_info)
update_data(patient1)



