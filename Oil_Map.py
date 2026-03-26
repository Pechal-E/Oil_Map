from bs4 import BeautifulSoup
import requests
import time
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import geopandas
import dash
from dash import dcc, html, Input, Output
import webbrowser
from threading import Timer

#app = dash.Dash(__name__)

#app.layout = html.Div([
#    dcc.Graph(id='live-map'),
    # Обновление каждый час
#    dcc.Interval(id='interval-component', interval=3600*1000, n_intervals=0)
#])

#@app.callback(Output('live-map', 'figure'),
#              Input('interval-component', 'n_intervals'))

 # url of the oil price
url = "https://oilprice.com/oil-price-charts/"

# method to get the price of oil
def get_price(url):
    
    # getting the request from url 
    data = requests.get(url)

    # converting the text 
    soup = BeautifulSoup(data.text, 'html.parser')

    benchmark = ('WTI-Crude','Brent-Crude','Murban-Crude','Mars','DME-Oman', 
    'Mexican-Basket','Indian-Basket','Urals-Brent','Western-Canadian-Select','Iran-Heavy',
    'Arab-Light','Kuwait-Export-Blend')

    price_oil = []

    for item in benchmark:

        # finding meta info for the current price
        price_oil_tag = soup.find("tr", attrs={'data-name': item}).find(class_='last_price')

        if  price_oil_tag:

            price_oil.append(price_oil_tag.get('data-price'))

        # returning the price
    return price_oil

price_oil = get_price(url)

data = {
    "Benchmarks":['WTI Crude','Brent Crude','Murban Crude','Mars','DME Oman', 
    'Mexican Basket','Indian Basket','Urals','Western Canadian Select','Iran Heavy','Arab Light','Kuwait Export Blend'],
    "Hubs":['Кушинг','Саллом-Во','Эль-Фуджайра','Порт-Фуршон','Салала', 
    'Тампико','Кандла','Новороссийск','Хардисти','Харк','Рас-Таннура','Шувайх'],
    "Latitude":[35.98, 60.45, 25.12, 29.14, 17.00, 
    22.22, 23.01, 44.72, 52.67, 29.25, 26.71, 29.35],
    "Longitude":[-96.77, -1.30, 56.35, -90.20, 54.06, 
    -97.86, 70.19,37.77,-111.30, 50.32, 50.07, 47.91],
    "Price":price_oil}




df = pd.DataFrame(data)
fig = go.Figure(go.Scattermap(
    lon = df.Longitude,
    lat = df.Latitude,
    mode ='markers',
        marker=go.scattermap.Marker(
            symbol="water",
            size=10
        ),
        #marker=dict(symbol="water", size=20),
    text = [f"<b>Марка:{x}</b><br>Хаб:{y}<br>Цена:{z} $" for x, y, z in zip(df.Benchmarks,df.Hubs,df.Price)],
    #hovertemplate=f"<b>{df.Benchmarks}</b><br>" +
    #              f"{df.Hubs}<br>" +
    #              f"{df.Price}<extra></extra>",
    hoverinfo ='text' 
        ))
    #fig = px.scatter_map(hubs,
    #                     lat="Latitude",
    #                      lon="Longitude",
    #                      hover_name="Hubs",
    #                      hover_data={"Latitude": False, "Longitude": False},
    #                      symbol="water",
    #                      zoom=1)

fig.update_layout(mapbox_style="open-street-map")
#fig.show(renderer='browser')
fig.write_html('Oil_map.html', auto_open=True)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Интерактивная карта на Dash"),
    dcc.Graph(figure=fig) # Вставка карты
])
    
#def open_browser():
#        webbrowser.open("http://127.0.0.1/:8050")
    
#if __name__ == '__main__':
# Запускаем открытие браузера через 1 секунду после запуска сервера
     #Timer(1, open_browser).start()
     #app.run(debug=True)
     #fig.show(renderer='browser')
     #print(price_oil)
     #fig.write_html('Oil_map.html', auto_open=True)

