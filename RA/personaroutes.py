from fastapi import APIRouter, Query, HTTPException
from .services import (
    process_final_score,
    process_behavior_analysis,
    fetch_history,
    fetch_previous_visit_data
)
from .schemas import PredictionRequest
from .utils import modifyQ, umodifyQ, sortfunction, filter_dic
import numpy as np
import pandas as pd

router = APIRouter()


data_1402 = pd.read_excel('data/1402.xlsx')
product_score_data = pd.read_excel('data/product_Score.xlsx')

@router.get('/{bcod}')
async def predict(
    OwnerCode: int = Query(..., description="code namayandegi"),
    productID: int = Query(..., description="Product ID"),
    CompanyId: int = Query(..., description="Company ID"),
    year: int = Query(...),
    month: int = Query(...),
    defec: int = Query(...),
    time: int = Query(..., description="nobat?"),
    delivery: int = Query(...),
    fixall: int = Query(...),
    part: int = Query(...),
    pay: int = Query(...),
    cost: int = Query(...),
    reseptiontype: int = Query(...),
    age: int = Query(...),
    edu: int = Query(...),
    jobid: int = Query(200,description="job"),
    gen: int = Query(...),
    km: int = Query(...),
    Type_admission: int = Query(...),
    Vin: str = Query("na", description=""),
    phone: int = Query(0, description="")
):
    #owner data
    owner_data = data_1402[(data_1402['CompanyId'] == CompanyId) & (data_1402['OwnerCode'] == OwnerCode)]
    if not owner_data.empty:
        edraki = owner_data['Edraki'].values[0]
        amalkardi = owner_data['Amalkardi'].values[0]
        karayi = owner_data['Karayi'].values[0]
        talfigh = owner_data['Talfigh'].values[0]
    else:
        edraki = 765
        amalkardi = 887
        karayi = 831
        talfigh = 797

    #product score
    product_data = product_score_data[product_score_data['ProductId'] == productID]
    product_score = product_data['ProductScore'].values[0] if not product_data.empty else 748

    #Fetch previous visit data
    history_data = fetch_previous_visit_data(phone=phone, vin=Vin)
    if not history_data:
        raise HTTPException(status_code=404, detail="History data not found")
    PreviousSatisfactionScore = history_data["PreviousSatisfactionScore"]
    PreviousVisitStatus = history_data["PreviousVisitStatus"]
    AvgPreviousSatisfactionScore = history_data["AvgPreviousSatisfactionScore"]
    CountPreviousVisits = history_data["CountPreviousVisits"]



    #final score
    final_score = process_final_score(
        defec, time, km, delivery, fixall, part, pay, reseptiontype, age, edu, jobid, gen,PreviousSatisfactionScore, PreviousVisitStatus,
        AvgPreviousSatisfactionScore, CountPreviousVisits, Type_admission, cost, product_score, edraki, amalkardi, karayi, talfigh
    )


    #Calculate behavior analysis
    behaviorlys = process_behavior_analysis(
        defec, time, km, delivery, fixall, part, pay, reseptiontype, age, edu,jobid, gen, PreviousSatisfactionScore,
        PreviousVisitStatus,
        AvgPreviousSatisfactionScore, CountPreviousVisits, Type_admission, cost, product_score, talfigh, final_score
    )

    #print(behaviorlys.shape)



    #Sort n prepare output
    y2 = sortfunction(behaviorlys.reshape(1, -1)).reset_index(drop=True)
    output = pd.Series(y2['score'].values, index=y2['Q']).to_dict()
    #print(filter_dic(output))
    return filter_dic(output)

