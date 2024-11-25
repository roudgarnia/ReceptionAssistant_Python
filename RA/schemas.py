from pydantic import BaseModel

class PredictionRequest(BaseModel):
    OwnerCode: int
    productID: int
    CompanyId: int
    year: int
    month: int
    defec: int
    time: int
    delivery: int
    fixall: int
    part: int
    pay: int
    cost: int
    reseptiontype: int
    age: int
    edu: int
    jobid: int
    gen: int
    km: int
    Type_admission: int
    Vin: str = "na"
    phone: int = 0

class PredictionResponse(BaseModel):
    final_score: float
    behavior_score: dict
