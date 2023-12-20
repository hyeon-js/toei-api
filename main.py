from fastapi import FastAPI
from typing import Optional
import requests
from toei import Toei

app = FastAPI()

@app.get("/")
def init(lineCode: Optional[str] = None):
    if lineCode == None: return {}
    lineName = {
        'A': 'Asakusa',
        'I': 'Mita',
        'S': 'Shinjuku',
        'E': 'Oedo'
    }
    if not lineName.get(lineCode): return {}
    toei = Toei()
    return toei.get_running_info(lineName[lineCode])
