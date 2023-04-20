import tkinter as tk
import matplotlib

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

        

class Graphique:
    def __init__(self,fenetre,categorie):
        nombre_produits=[]
        nom_categorie = []
        for nom in categorie.get_categorie_all():
            nom_categorie.append(str(nom[0])+")\n"+nom[1])
            nombre_produits.append(categorie.count_produit_in_categorie(nom[1]))
        # create a figure
        figure = Figure(figsize=(len(nom_categorie), 5), dpi=100)
        figure.set_facecolor('grey')
        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, fenetre)
        # create axes
        axes = figure.add_subplot()
        # create the barchart
        axes.bar(nom_categorie, nombre_produits)
        axes.set_title('Nombre de produits par categorie')
        axes.set_ylabel('nombre de produits')

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)