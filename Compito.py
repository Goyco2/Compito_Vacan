from flask import Flask, render_template, request, send_file, make_response, url_for, Response, redirect
app = Flask(__name__)
import io
import geopandas
from geopandas import GeoDataFrame
from shapely.geometry import Point
import contextily
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random
import pandas as pd 
import folium
from folium.plugins import MousePosition
import numpy as np

Giudizio = pd.read_excel("/workspace/Compito_Vacanze/static/GdL_GV_2021.xlsx")
Giudizio['giudizio'] = Giudizio['giudizio'].str.lower()
Giudizio['giudizio'] = Giudizio['giudizio'].replace(['entro il limiti'],'entro i limiti')
regioni= geopandas.read_file('/workspace/Compito_Vacanze/static/Reg01012021_g-20220820T171732Z-001.zip')
geometry = [Point(xy) for xy in zip(Giudizio.longitudine, Giudizio.latitudine)]
Giudizio = Giudizio.drop(['longitudine', 'latitudine'], axis=1)
gGiudizio = GeoDataFrame(Giudizio, crs="EPSG:4326", geometry=geometry)

@app.route('/', methods=['GET', 'POST'])
def scelta():
    return render_template("home.html")

@app.route('/selezione', methods=['GET'])
def selezione():
    scelta = request.args["scelta"]
    if scelta == "es1":
        return redirect(url_for("esercizio1"))
    elif scelta == "es2":
        return redirect(url_for("esercizio2"))
    elif scelta == "es3":
        return redirect(url_for("esercizio3"))
    elif scelta == "es4":
        return redirect(url_for("esercizio4"))
    elif scelta == "es5":
        return redirect(url_for(""))
    elif scelta == "es6":
        return redirect(url_for(""))
    elif scelta == "es7":
        return redirect(url_for(""))    
    else:
        return redirect(url_for(""))

@app.route('/esercizio1', methods=['GET'])
def esercizio1():
    giud_luog = Giudizio.groupby("giudizio", as_index=False)["localita"].count()
    return render_template("risultato1.html",risultato = giud_luog.to_html())

@app.route('/esercizio2', methods=['GET'])
def esercizio2():
    giud_luog = Giudizio.groupby("giudizio", as_index=False)["localita"].count()
    Giudizio['localitaSum'] = Giudizio['localita'].count()
    Giudizio['localita%'] = (giud_luog['localita'] / Giudizio['localitaSum'])*100
    Giudizio2 = Giudizio[['localita%','giudizio']].copy()
    Giudizio1 = Giudizio2.dropna()
    return render_template("risultato2.html",risultato2 = Giudizio1[['giudizio','localita%']].to_html())

@app.route('/grafico', methods=['GET'])
def grafico():
    giud_luog = Giudizio.groupby("giudizio", as_index=False)["localita"].count()
    Giudizio['localitaSum'] = Giudizio['localita'].count()
    Giudizio['localita%'] = (giud_luog['localita'] / Giudizio['localitaSum'])*100
    Giudizio2 = Giudizio[['localita%','giudizio']].copy()
    Giudizio1 = Giudizio2.dropna()
    print(Giudizio1)
    

    fig = plt.figure()
    ax = plt.axes()
    ax.pie(Giudizio1['localita%'], labels = Giudizio1['giudizio'], autopct= '%1.2f%%')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/esercizio3', methods=['GET'])
def esercizio3():
    GiudizioSpiagge = Giudizio.loc[Giudizio['punto'].str.contains('Spiaggia | spiaggia', case= False)]
    GiudizioSpiagge = GiudizioSpiagge[['giudizio','punto']].copy()
    return render_template("risultato3.html",risultato3 = GiudizioSpiagge.to_html())

@app.route('/esercizio4', methods=['GET'])
def esercizio4():
    global Giud_Lombardia,GiudLomb
    giudInLom = Giudizio['giudizio']
    Giud_Lombardia = regioni[regioni.NIL.str.contains(giudInLom)]
    GiudLomb = Giudizio[Giudizio.within(Giud_Lombardia.geometry.squeeze())]
    return render_template("esercizio4.html", risultato4 = GiudLomb.to_html())
 


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)