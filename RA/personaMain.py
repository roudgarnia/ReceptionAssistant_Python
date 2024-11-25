from fastapi import FastAPI
from ReceptionAssistant_Python.personaroutes import router

RA = FastAPI()

RA.include_router(router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(RA, host="0.0.0.0", port=8000)
