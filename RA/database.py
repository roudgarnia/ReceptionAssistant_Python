import pyodbc
from .settings import Settings

def get_db_connection():
    connection_string = (
        f"DRIVER={Settings.DB_DRIVER};"
        f"SERVER={Settings.DB_SERVER};"
        f"DATABASE={Settings.DB_NAME};"
        f"UID={Settings.DB_USER};"
        f"PWD={Settings.DB_PASSWORD};"
    )
    return pyodbc.connect(connection_string)
