from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import requests
import json

app = Dash(__name__)

gringos = pd.DataFrame()

#numero automovil
urlNumAuto='https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/6207123166/es/0700/true/BISE/2.0/80a99960-ce46-5bc8-e325-4f69c5b8e427?type=json'
rNumAuto = requests.get(urlNumAuto)

#gasto automovil
urlGastoAuto ='https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/6207123162/es/0700/true/BISE/2.0/80a99960-ce46-5bc8-e325-4f69c5b8e427?type=json'
rGastoAuto = requests.get(urlGastoAuto)

#numero avion
urlNumAvion = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/6207123163/es/0700/true/BISE/2.0/80a99960-ce46-5bc8-e325-4f69c5b8e427?type=json'
rNumAvion = requests.get(urlNumAvion)

#gasto avion
urlGastoAvion = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/6207123170/es/0700/true/BISE/2.0/80a99960-ce46-5bc8-e325-4f69c5b8e427?type=json'
rGastoAvion = requests.get(urlGastoAvion)

#numero crucero
urlNumCrucero = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/6207123181/es/0700/true/BISE/2.0/80a99960-ce46-5bc8-e325-4f69c5b8e427?type=json'
rNumCrucero = requests.get(urlNumCrucero)

#gasto crucero
urlGastoCrucero = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/6207123180/es/0700/true/BISE/2.0/80a99960-ce46-5bc8-e325-4f69c5b8e427?type=json'
rGastoCrucero = requests.get(urlGastoCrucero)

if rNumAuto.status_code==200:
    content= json.loads(rNumAuto.content)
    TNumAuto = float(content['Series'][0]['OBSERVATIONS'][0]['OBS_VALUE'])
    lastupdateAuto = content['Series'][0]['LASTUPDATE']

if rGastoAuto.status_code==200:
    content= json.loads(rGastoAuto.content)
    TGastoAuto = float(content['Series'][0]['OBSERVATIONS'][0]['OBS_VALUE'])

if rNumAvion.status_code==200:
    content= json.loads(rNumAvion.content)
    TNumAvion = float(content['Series'][0]['OBSERVATIONS'][0]['OBS_VALUE'])
    lastupdateAvion = content['Series'][0]['LASTUPDATE']

if rGastoAvion.status_code==200:
    content= json.loads(rGastoAvion.content)
    TGastoAvion = float(content['Series'][0]['OBSERVATIONS'][0]['OBS_VALUE'])

if rNumCrucero.status_code==200:
    content= json.loads(rNumCrucero.content)
    TNumCrucero = float(content['Series'][0]['OBSERVATIONS'][0]['OBS_VALUE'])
    lastupdateCrucero = content['Series'][0]['LASTUPDATE']

if rGastoCrucero.status_code==200:
    content= json.loads(rGastoCrucero.content)
    TGastoCrucero = float(content['Series'][0]['OBSERVATIONS'][0]['OBS_VALUE'])
    
elDictAuto ={ 'Name' : 'Automovil', 'ultimaActualizacion' : lastupdateAuto, 'NumeroTotal': TNumAuto, 'GastoTotal': TGastoAuto}
elDictAvion ={ 'Name' : 'Avion', 'ultimaActualizacion' : lastupdateAvion, 'NumeroTotal': TNumAvion, 'GastoTotal': TGastoAvion}
elDictCrucero ={ 'Name' : 'Crucero', 'ultimaActualizacion' : lastupdateCrucero, 'NumeroTotal': TNumCrucero, 'GastoTotal': TGastoCrucero}
automovil = pd.DataFrame([elDictAuto])
avion = pd.DataFrame([elDictAvion])
crucero = pd.DataFrame([elDictCrucero])

gringos = pd.concat([automovil,avion,crucero])

gringos['gastoIndividual'] = gringos['GastoTotal'] / gringos['NumeroTotal']

fig = px.bar(gringos, x="Name", y="NumeroTotal")

app.layout = html.Div(children=[
    html.H1(children='Jojuma BI'),

    html.Div(children='''
        Numero de viajeros, por forma de internación al pais, Fuente: INEGI 2023.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)