import uvicorn
from fastapi import FastAPI
from routers.bitcoin import bitcoin_router

app = FastAPI()

app.include_router(bitcoin_router, prefix="/bitcoin")

if __name__ == "__main__":
    uvicorn.run("serve:app", host="127.0.0.1", port=5000, reload=True)