from fastapi import FastAPI
from typing import Optional

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
    return lineName[lineCode]