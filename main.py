from fastapi import FastAPI
from typing import Optional
import requests

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
    return get_running_info(lineName[lineCode])

def get_running_info(lineName):
    url = 'https://api-public.odpt.org/api/v4/odpt:Train?odpt:operator=odpt.Operator:Toei'
    response = requests.get(url)
    data = response.json()
    return data
