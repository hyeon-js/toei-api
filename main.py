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
    stns = get_station_list(lineName)
    data = get_train_list(lineName)
    result = []
    for i in range(0, len(stns)):
        datum = {}
        datum['stn'] = stns[i]
        datum['up'] = []
        datum['down'] = []
        for train in data:
            if train['stn'] == stns[i]['en']:
                updn = 'down'
                if train['isUp'] : updn = 'up'
                datum[updn].append(train)
        result.append(datum)
    
    return result

def get_station_list(lineName):
    if lineName == 'Asakusa' : return [{"ko":"니시마고메","ja":"西馬込","en":"NishiMagome"},{"ko":"마고메","ja":"馬込","en":"Magome"},{"ko":"나카노부","ja":"中延","en":"Nakanobu"},{"ko":"토고시","ja":"戸越","en":"Togoshi"},{"ko":"고탄다","ja":"五反田","en":"Gotanda"},{"ko":"타카나와다이","ja":"高輪台","en":"Takanawadai"},{"ko":"센가쿠지","ja":"泉寺","en":"Sengakuji"},{"ko":"미타","ja":"三田","en":"Mita"},{"ko":"다이몬","ja":"大門","en":"Daimon"},{"ko":"신바시","ja":"新橋","en":"Shimbashi"},{"ko":"히가시긴자","ja":"東銀座","en":"HigashiGinza"},{"ko":"타카라초","ja":"宝町","en":"Takaracho"},{"ko":"니혼바시","ja":"日本橋","en":"Nihombashi"},{"ko":"닌교초","ja":"人形町","en":"Ningyocho"},{"ko":"히가시니혼바시","ja":"東日本橋","en":"HigashiNihombashi"},{"ko":"아사쿠사바시","ja":"浅草橋","en":"Asakusabashi"},{"ko":"쿠라마에","ja":"蔵前","en":"Kuramae"},{"ko":"아사쿠사","ja":"浅草","en":"Asakusa"},{"ko":"혼조아즈마바시","ja":"本所吾橋","en":"HonjoAzumabashi"},{"ko":"오시아게","ja":"押上","en":"Oshiage"}]
    if lineName == 'Mita' : return [{"ko":"메구로","ja":"目黒)","en":"Meguro"},{"ko":"시로카네다이","ja":"白金台)","en":"Shirokanedai"},{"ko":"시로카네타카나와","ja":"白金高輪)","en":"ShirokaneTakanawa"},{"ko":"미타","ja":"三田)","en":"Mita"},{"ko":"시바코엔","ja":"芝公園)","en":"Shibakoen"},{"ko":"오나리몬","ja":"御成門)","en":"Onarimon"},{"ko":"우치사이와이초","ja":"内幸町)","en":"Uchisaiwaicho"},{"ko":"히비야","ja":"日比谷)","en":"Hibiya"},{"ko":"오테마치","ja":"大手町)","en":"Otemachi"},{"ko":"진보초","ja":"神保町)","en":"Jimbocho"},{"ko":"스이도바시","ja":"水道橋)","en":"Suidobashi"},{"ko":"카스가","ja":"春日)","en":"Kasuga"},{"ko":"하쿠산","ja":"白山)","en":"Hakusan"},{"ko":"센고쿠","ja":"千石)","en":"Sengoku"},{"ko":"스가모","ja":"巣鴨)","en":"Sugamo"},{"ko":"니시스가모","ja":"西巣鴨)","en":"NishiSugamo"},{"ko":"신이타바시","ja":"新板橋)","en":"ShinItabashi"},{"ko":"이타바시쿠야쿠쇼마에","ja":"板橋区役所前)","en":"ItabashiKuyakushomae"},{"ko":"이타바시혼초","ja":"板橋本町)","en":"Itabashihoncho"},{"ko":"모토하스누마","ja":"本蓮沼)","en":"Motohasunuma"},{"ko":"시무라사카우에","ja":"志村坂上)","en":"ShimuraSakaue"},{"ko":"시무라산초메","ja":"志村三丁目)","en":"ShimuraSanchome"},{"ko":"하스네","ja":"蓮根)","en":"Hasune"},{"ko":"니시다이","ja":"西台)","en":"Nishidai"},{"ko":"타카시마다이라","ja":"高島平)","en":"Takashimadaira"},{"ko":"신타카시마다이라","ja":"新高島平)","en":"ShinTakashimadaira"},{"ko":"니시타카시마다이라","ja":"西高島平)","en":"NishiTakashimadaira"}];

def get_train_list(lineName):
    url = 'https://api-public.odpt.org/api/v4/odpt:Train?odpt:operator=odpt.Operator:Toei'
    response = requests.get(url)
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

            dir = datum['odpt:railDirection'].split('.')[-1].split(':')[-1]
            isUp = {
                'Asakusa': 'Southbound',
                'Mita': 'Southbound',
                'Shinjuku': 'Westbound',
                'Oedo': 'InnerLoop'
            }
            
            data.append({
                'no': datum['odpt:trainNumber'],
                'type': datum['odpt:trainType'].split('.')[-1],
                'owner': owner,
                'stn': stn.split('.')[-1],
                'status': status,
                'isUp': isUp[lineName] == dir
            })
    return data