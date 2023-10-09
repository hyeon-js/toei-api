from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/")
def init(lineCode: Optional[str] = None):
    return lineCode