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

@app.route('/', methods=['GET', 'POST'])
def scelta():
    return render_template("home.html")

@app.route('/selezione', methods=['GET'])
def selezione():
    scelta = request.args["scelta"]
    if scelta == "es1":
        return redirect(url_for("esercizio1"))
    elif scelta == "es2":
        return redirect(url_for(""))
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
    Giudizio= Giudizio['giudizio'].str.lower()
    print(Giudizio)
    giud_luog = Giudizio.groupby("giudizio")["localita"].count().reset_index()
    return render_template("risultato1.html",risultato = giud_luog.to_html())

    
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)