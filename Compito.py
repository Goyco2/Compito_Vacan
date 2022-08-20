from flask import Flask, render_template, request, send_file, make_response, url_for, Response, redirect
app = Flask(__name__)
import io
import geopandas
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
        return redirect(url_for(""))
    elif scelta == "es4":
        return redirect(url_for(""))
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
    Giudizio['localita'] = (giud_luog['localita'] / Giudizio['localitaSum'])*100
    print(Giudizio['localita'])


    return render_template("risultato2.html",risultato2 = Giudizio[['giudizio','localita']].head(3).to_html())

    
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)