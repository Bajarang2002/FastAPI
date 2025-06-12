from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator
from typing import List, Dict,Optional,Annotated


class Address(BaseModel):
    state :str
    city :str
    pin : int

class Patient(BaseModel):
    name :str
    age :int
    weight: float
    height : float
    address : Address


Address_dict = {"state":"Maharastra","city":"Pune","pin":416507}
address1 = Address(**Address_dict)

patient_info = { "name":"Askhay","age":21,"weight":70,"height":1.7,"address":address1}
patient1 = Patient(**patient_info)

print(patient1)
print(patient1.address.city)

print(patient1.address.pin)


temp = patient1.model_dump()
print(temp)
print(type(temp))

temp1 = patient1.model_dump(include=['age'])
print(temp1)
print(type(temp1))

temp2 = patient1.model_dump(exclude=['age','weight'])
print(temp2)
print(type(temp2))


temp3 = patient1.model_dump_json()
print(temp3)
print(type(temp3))

