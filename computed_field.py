from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator,computed_field
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

@computed_field()
@property
def bmi(self) -> float:
    bmi = round(self.weight/(self.height**2),2)
    return bmi



def update_data(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print("bmi",patient.bmi())
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




 

