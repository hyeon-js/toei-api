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
    stns = [{"ko":"니시마고메","ja":"西馬込","en":"NishiMagome"},{"ko":"마고메","ja":"馬込","en":"Magome"},{"ko":"나카노부","ja":"中延","en":"Nakanobu"},{"ko":"토고시","ja":"戸越","en":"Togoshi"},{"ko":"고탄다","ja":"五反田","en":"Gotanda"},{"ko":"타카나와다이","ja":"高輪台","en":"Takanawadai"},{"ko":"센가쿠지","ja":"泉寺","en":"Sengakuji"},{"ko":"미타","ja":"三田","en":"Mita"},{"ko":"다이몬","ja":"大門","en":"Daimon"},{"ko":"신바시","ja":"新橋","en":"Shimbashi"},{"ko":"히가시긴자","ja":"東銀座","en":"HigashiGinza"},{"ko":"타카라초","ja":"宝町","en":"Takaracho"},{"ko":"니혼바시","ja":"日本橋","en":"Nihombashi"},{"ko":"닌교초","ja":"人形町","en":"Ningyocho"},{"ko":"히가시니혼바시","ja":"東日本橋","en":"HigashiNihombashi"},{"ko":"아사쿠사바시","ja":"浅草橋","en":"Asakusabashi"},{"ko":"쿠라마에","ja":"蔵前","en":"Kuramae"},{"ko":"아사쿠사","ja":"浅草","en":"Asakusa"},{"ko":"혼조아즈마바시","ja":"本所吾橋","en":"HonjoAzumabashi"},{"ko":"오시아게","ja":"押上","en":"Oshiage"}];
    data = []
    line = 'odpt.Railway:Toei.' + lineName
    for datum in response.json():
        if datum['odpt:railway'] == line :
            stn = datum['odpt:toStation']
            status = 'Approaching'
            if stn == None :
                stn = datum['odpt:fromStation']
                status = 'Arrived'
            owner = datum.get('odpt:trainOwner')
            if owner == None : owner = 'Toei'
            else : owner = owner.split('.')[-1].split(':')[-1]
            
            data.append({
                'no': datum['odpt:trainNumber'],
                'type': datum['odpt:trainType'].split('.')[-1],
                'owner': owner,
                'stn': stn.split('.')[-1],
                'status': status,
                'dir': datum['odpt:railDirection'].split('.')[-1].split(':')[-1]
            })
    return data

    # result = []
    # for i in range(0, len(stns)):
    #     datum = {}
    #     datum['stn'] = stns[i]
    #     for train in data:
    #         if train['stn'] == stns[i]['en']:
    #             if not 'up' in datum : datum['up'] = []
    #             datum['up'].append(train)
        
    #     result.append(datum)
    
    return result
