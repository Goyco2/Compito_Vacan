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
Regioni = geopandas.read_file('/workspace/Compito_Vacanze/Reg01012021_g_WGS84.zip')
geometry = [Point(xy) for xy in zip(Giudizio.longitude, Giudizio.latitude)]
Giudizio = Giudizio.drop(['longitude', 'latitude'], axis=1)
gGiudizio = GeoDataFrame(Giudizio, crs="EPSG:4326", geometry=geometry)
Province = geopandas.read_file('/workspace/Compito_Vacanze/ProvCM01012021_g.zip')

@app.route('/', methods=['GET'])
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
        return redirect(url_for("esercizio5"))
    elif scelta == "es6":
        return redirect(url_for("Sesercizio6"))
    elif scelta == "es7":
        return redirect(url_for("Sesercizio7"))    
    else:
        return redirect(url_for("esercizio8"))


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
    global giud, giud_Lomb
    giud = Regioni[Regioni.DEN_REG == 'Lombardia']
    giud_Lomb = gGiudizio[gGiudizio.intersects(giud.geometry.squeeze())]   # ? non rislutano punti in lobardia anche se ci sono
    return render_template("risultato4.html",risultato4 = giud_Lomb.to_html())   

@app.route("/mappaLombardia.png", methods=["GET"])
def mappaLombardia():
    fig, ax = plt.subplots(figsize = (12,8))

    giud_Lomb.to_crs(epsg=3857).plot(ax=ax, pointcolor='k')
    giud.to_crs(epsg=3857).plot(ax=ax, edgecolor="k", facecolor='None')
    contextily.add_basemap(ax=ax)   

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

    
 
@app.route('/esercizio5', methods=['GET'])
def esercizio5():
    global giud, giud_Lomb, popup
    giud = Regioni[Regioni.DEN_REG == 'Lombardia']
    giud_Lomb = gGiudizio[gGiudizio.contains(giud.geometry.squeeze())]
    for index, row in gGiudizio.iterrows():
        IFrame = folium.IFrame(str(row.loc['giudizio']))
        popup = folium.Popup(IFrame, min_width=210, max_width=210)
        return render_template("risultato5.html",risultato5 = giud_Lomb.to_html())   



@app.route("/mappaLombardia2.png", methods=["GET"])
def mappaLombardia2():
    fig, ax = plt.subplots(figsize = (12,8))

    giud_Lomb.to_crs(epsg=3857).plot(ax=ax, pointcolor='k',popup=popup)
    giud.to_crs(epsg=3857).plot(ax=ax, edgecolor="k", facecolor='None')
    contextily.add_basemap(ax=ax)   

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/Sesercizio6', methods = ["GET"])
def Sesercizio6():
    return render_template("esercizio6.html")

@app.route('/esercizio6', methods = ["GET"])
def esercizio6():
    global giud_Rich, giudizioR
    inp = request.args["Input"]
    regione_richiesta = list(Regioni["DEN_REG"])
    if inp in regione_richiesta:
        giudizioR = Regioni[Regioni.DEN_REG == inp]
        giud_Rich = gGiudizio[gGiudizio.intersects(giudizioR.geometry.squeeze())]
        return render_template("risultato6.html",risultato6 = giud_Rich.to_html())   
    else:
        return render_template('errore.html')


@app.route("/mappaRichiesta.png", methods=["GET"])
def mappaRichiesta():
    global giud_Rich, giudizioR

    fig, ax = plt.subplots(figsize = (12,8))

    giud_Rich.to_crs(epsg=3857).plot(ax=ax, pointcolor='k')
    giudizioR.to_crs(epsg=3857).plot(ax=ax, edgecolor="k", facecolor='None')
    contextily.add_basemap(ax=ax)   

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/Sesercizio7', methods = ["GET"])
def Sesercizio7():
    return render_template("esercizio7.html")        #non trovo un datasets di tutti  i laghi italiani

@app.route('/esercizio7', methods = ["GET"])
def esercizio7():
    lago = request.args["lago"]

    return render_template('risultato7.html')

@app.route('/esercizio8', methods = ["GET"])
def esercizio8():
    global giudB, prov
    prov = Province[['DEN_PROV','geometry']]
    giudB = gGiudizio[gGiudizio.contains(prov.geometry.squeeze())]



    return render_template('risultato8.html')

@app.route("/mappaProv.png", methods=["GET"])
def mappaProv():
    fig, ax = plt.subplots(figsize = (12,8))

    giudB.to_crs(epsg=3857).plot(ax=ax, column = 'giudizio', edgecolor = 'k', legend = True, figsize=(10,10),cmap='Reds', alpha = 0.6)
    contextily.add_basemap(ax=ax)   

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)