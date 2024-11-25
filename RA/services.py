import numpy as np
import pandas as pd
from .models import score_model, persona_model
from .utils import modifyQ, umodifyQ, calass
from .database import get_db_connection



def fetch_history(CompanyId, OwnerCode, Vin, phone):
    """Fetch history from database."""
    connection = get_db_connection()
    ####ADD PreviousSatisfactionScore, PreviousVisitStatus,AvgPreviousSatisfactionScore, CountPreviousVisits####
    #based on VIN and phone
    if Vin == 'na':
        query = f"SELECT CustomerId AS Id, OwnerCode AS OwnerCode, Phone, AcceptDate, VIN AS Shahsy, " \
                f"[1] AS Q1, [2] AS Q2,[8] AS Q8,[9]AS Q9, [12] AS Q12, [15] AS Q15, [26] AS Q26, [27] AS Q27, [28] AS Q28, [30] AS Q30, " \
                f"CAST(SUBSTRING(AcceptDate, 5, 2) AS INT) AS [month], CompanyId, [29] AS job, ProductId, [31] AS Score " \
                f"FROM dbo.Service WHERE Phone = {phone}"
    elif phone == 0:
        query = f"SELECT CustomerId AS Id, OwnerCode AS OwnerCode, Phone, AcceptDate, VIN AS Shahsy, " \
                f"[1] AS Q1, [2] AS Q2,[8] AS Q8,[9]AS Q9, [12] AS Q12, [15] AS Q15, [26] AS Q26, [27] AS Q27, [28] AS Q28, [30] AS Q30, " \
                f"CAST(SUBSTRING(AcceptDate, 5, 2) AS INT) AS [month], CompanyId, [29] AS job, ProductId, [31] AS Score " \
                f"FROM dbo.Service WHERE VIN = N'{Vin}'"
    else:
        query = f"SELECT CustomerId AS Id, OwnerCode AS OwnerCode, Phone, AcceptDate, VIN AS Shahsy, " \
                f"[1] AS Q1, [2] AS Q2,[8] AS Q8,[9]AS Q9, [12] AS Q12, [15] AS Q15, [26] AS Q26, [27] AS Q27, [28] AS Q28, [30] AS Q30, " \
                f"CAST(SUBSTRING(AcceptDate, 5, 2) AS INT) AS [month], CompanyId, [29] AS job, ProductId, [31] AS Score " \
                f"FROM dbo.Service WHERE VIN = N'{Vin}' AND Phone = {phone}"

    cursor = connection.cursor()


    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]


    df = pd.DataFrame.from_records(rows, columns=columns)

    #Modify req
    df['Q2'] = df['Q2'].apply(modifyQ)
    df['Q12'] = df['Q12'].apply(modifyQ)
    df['Q15'] = df['Q15'].apply(modifyQ)
    df['Q26'] = df['Q26'].apply(modifyQ)
    df['Q27'] = df['Q27'].apply(modifyQ)
    df['Q28'] = df['Q28'].apply(modifyQ)
    df['Q30'] = df['Q30'].apply(modifyQ)

    #print(df.columns)
    #print(df)
    connection.close()
    return df



def fetch_previous_visit_data(phone=None, vin=None):
    """Fetch processed historical visit data based on phone or VIN."""
    connection = get_db_connection()
    if phone != 0:
        where_clause = f"WHERE Phone = {phone}"
    elif phone == 0 and vin != "na":
        where_clause = f"WHERE VIN = N'{vin}'"
    #elif vin != "na" and phone != 0:
    #    where_clause = f"WHERE VIN = N'{vin}' AND Phone = {phone}"
    else:
        # If both are missing, will produce empty set or defaults
        return {
            "PreviousSatisfactionScore": 755,
            "PreviousVisitStatus": 0,
            "AvgPreviousSatisfactionScore": 755,
            "CountPreviousVisits": 0
        }

    query = f"""
    WITH ProcessedData AS (
        SELECT 
            [31] AS PreviousSatisfactionScore,
            CASE 
                WHEN [OwnerCode] = 2106 AND [CompanyId] = 34 THEN 3
                WHEN [CompanyId] = 34 THEN 2
                WHEN [CompanyId] <> 34 THEN 1
                ELSE 0 
            END AS PreviousVisitStatus,
            AVG([31]) OVER () AS AvgPreviousSatisfactionScore,
            COUNT(*) OVER () AS CountPreviousVisits,
            AcceptDate
        FROM dbo.Service
        {where_clause}
    )
    SELECT TOP 1 
        ISNULL(PreviousSatisfactionScore, 755) AS PreviousSatisfactionScore,
        ISNULL(PreviousVisitStatus, 0) AS PreviousVisitStatus,
        ISNULL(AvgPreviousSatisfactionScore, 755) AS AvgPreviousSatisfactionScore,
        ISNULL(CountPreviousVisits, 0) AS CountPreviousVisits
    FROM ProcessedData
    ORDER BY AcceptDate DESC
    OPTION (FAST 1);
    """

    cursor = connection.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    connection.close()

    if row:
        return {
            "PreviousSatisfactionScore": row.PreviousSatisfactionScore,
            "PreviousVisitStatus": row.PreviousVisitStatus,
            "AvgPreviousSatisfactionScore": row.AvgPreviousSatisfactionScore,
            "CountPreviousVisits": row.CountPreviousVisits
        }
    else:
        return {
            "PreviousSatisfactionScore": 755,
            "PreviousVisitStatus": 0,
            "AvgPreviousSatisfactionScore": 755,
            "CountPreviousVisits": 0
        }





def process_final_score(Q1,Q2,km,Q8,Q9,Q12,Q15,Q26,Q27,Q28, Q29,Q30,PreviousSatisfactionScore, PreviousVisitStatus,
        AvgPreviousSatisfactionScore, CountPreviousVisits, Type_admission, Paid, product_score, Edraki, Amalkardi, Karayi, Talfigh):
    #modifyQ
    Q2 = modifyQ(Q2)
    Q8 = modifyQ(Q8)
    Q9 = modifyQ(Q9)
    Q12 = modifyQ(Q12)
    Q15 = modifyQ(Q15)
    Q26 = modifyQ(Q26)
    Q27 = modifyQ(Q27)
    Q28 = modifyQ(Q28)
    Q30 = modifyQ(Q30)
    ##################Add bcodcluster#########
    # Prepare input
    X_test = np.array([[
        Q1, Q2, km, Q8, Q9, Q12, Q15, Q26, Q27, Q28,Q29, Q30, PreviousSatisfactionScore, PreviousVisitStatus,
        AvgPreviousSatisfactionScore, CountPreviousVisits, Type_admission, Paid,km, product_score, Edraki, Amalkardi, Karayi, Talfigh
    ]])

    #prediction
    final_score = score_model.predict(X_test)[0]

    # score_category = calass(final_score)

    return final_score


def process_behavior_analysis(Q1,Q2,km,Q8,Q9,Q12,Q15,Q26,Q27,Q28, Q29, Q30,PreviousSatisfactionScore, PreviousVisitStatus,
        AvgPreviousSatisfactionScore, CountPreviousVisits, Type_admission, Paid, product_score, Talfigh,final_score):
    # Prepare input
    X_test = np.array([[
        Q1, Q2, km, Q8, Q9, Q12, Q15, Q26, Q27, Q28, Q29, Q30, PreviousSatisfactionScore, PreviousVisitStatus,
        AvgPreviousSatisfactionScore, CountPreviousVisits, Type_admission, Paid, km, product_score, Talfigh,final_score
    ]])

    #prediction
    behavior_score = persona_model.predict(X_test)[0]


    return behavior_score
