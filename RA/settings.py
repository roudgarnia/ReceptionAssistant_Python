import os

class Settings:
    DB_DRIVER = os.getenv("DB_DRIVER", "{SQL Server}")
    DB_SERVER = os.getenv("DB_SERVER", "192.168.5.54")
    DB_NAME = os.getenv("DB_NAME", "ReceptionAssistant")
    DB_USER = os.getenv("DB_USER", "Erfan@Eslami")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Erfan@159357753951")

settings = Settings()
