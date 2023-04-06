from tkinter import * 
from tkinter.messagebox import *
from tkinter import ttk

from classes.Graphique import Graphique
from classes.CRUD_produits import CRUD_produit
from classes.CRUD_categories import CRUD_categorie
from classes.Export import Export
from classes.connection import connexion

class Affichage:
    def __init__(self):
        conn=connexion()
        cursor=conn.cursor()
        self.__grid_dict = {"sticky": "ew"}
        #verifie l'existence de la database boutique
        stmt = "SHOW databases LIKE 'boutique'"
        cursor.execute(stmt)
        result = cursor.fetchone()

        if not result:
            #creer la database boutique si inexistante
            cursor.execute("CREATE database boutique")
        
        self.__crud_produit=CRUD_produit(conn)
        self.__crud_categorie=CRUD_categorie(conn)
        self.__export=Export(conn)
        
        self.__fenetre = Tk()
        self.__fenetre.state("zoomed")
        self.__fenetre.title("Gestion de stock")
        self.__fenetre.configure(bg='grey')
        
        #agencement de la frame par_produits
        self.affichage_par_produits()
        
    
    def affichage_par_produits(self):
        self.listes_nom_produits=[]
        self.clear_window()
        produits=self.__crud_produit.read_produits()
        frame_centrale=Frame(self.__fenetre, bg="grey")
        
        frame_graphique=Frame(frame_centrale)
        Graphique(frame_graphique,self.__crud_categorie)
        frame_test=Frame(frame_centrale,width=self.__fenetre.winfo_width())
        frame_frame=Frame(frame_centrale)
        main_frame=Frame(frame_frame, bg="grey")
        main_frame.grid(row=2, column=0, pady=(5, 0))
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_propagate(False)
        canvas = Canvas(main_frame, bg="grey")
        canvas.grid(row=0, column=0, sticky="news")
        
        vsb = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)
        
        info_frame=Frame(canvas,bg='grey')
        canvas.create_window((0, 0), window=info_frame, anchor='c')
        
        line=0
        for produit in produits:
            colone=0
            self.listes_nom_produits.append(produit[0])
            for info in produit:
                if info!=produit[5]:
                    label=Label(info_frame, font=("Arial", 20),text=info,bg='grey',fg=produit[5],borderwidth=1,relief="solid")
                    label.grid(row=line,column=colone, **self.__grid_dict)
                colone+=1
            line+=1
        
        info_frame.update_idletasks()
        first5rows_height = sum([label.winfo_height() for i in range(0, 7)])
        main_frame.config(width=self.__fenetre.winfo_width()-(self.__fenetre.winfo_width()-info_frame.winfo_width())+ vsb.winfo_width()*2
                          , height=first5rows_height)
        # Set the canvas scrolling region
        canvas.config(scrollregion=canvas.bbox("all"))
        frame_frame.pack()
        frame_centrale.pack()
        
        Button(frame_test, font=("Arial", 20),text="Ajouter produit", bg="red" , command= lambda:self.add_produit()).grid(row=line,column=0)
        Button(frame_test, font=("Arial", 20),text="Supprimer produit", bg="red" , command= lambda:self.choose_product(1)).grid(row=line,column=1)
        Button(frame_test, font=("Arial", 20),text="Modifier produit", bg="red" , command= lambda:self.choose_product(2)).grid(row=line,column=2)
        Button(frame_test, font=("Arial", 20),text="Afficher par categorie", bg="red" , command= lambda:self.affichage_par_categories()).grid(row=line,column=3)
        Button(frame_test, font=("Arial", 20),text="Exporter", bg="red" , command= lambda:self.__export.export()).grid(row=line,column=4)
        frame_test.pack()
        frame_graphique.pack()    
        
        
        self.__fenetre.mainloop()
    
    def add_produit(self):
        self.clear_window()
        entrys=[]
        produits=["Nom du produit","Description du produit","Prix du produit","Quantité du produit","ID categorie"]
        colone=0
        for info in produits:
            Label(self.__fenetre, font=("Arial", 20),text=info,bg='grey',fg='blue',borderwidth=1,relief="solid").grid(row=0,column=colone, **self.__grid_dict)
            entrys.append(Entry(self.__fenetre,font=("Arial", 20),borderwidth=1,relief="solid"))
            entrys[colone].grid(row=1,column=colone, **self.__grid_dict)
            colone+=1
        Button(self.__fenetre, font=("Arial", 20),text="Confirmer ajout", bg="red" , command= lambda:self.confirmer_ajout([entrys[0].get(),entrys[1].get(),entrys[2].get(),entrys[3].get(),entrys[4].get()],"produit")).grid(row=2,**self.__grid_dict)
    
    def modify_produit(self,nom):
        self.clear_window()
        entrys=[]
        produits=[]
        produits.append(["Nom du produit","Description du produit","Prix du produit","Quantité du produit","ID categorie"])
        produits.append(self.__crud_produit.read_one_produit(nom))
        count=0
        for info in produits[0]:
            Label(self.__fenetre, font=("Arial", 20),text=info,bg='grey',fg='blue',borderwidth=1,relief="solid").grid(row=0,column=count, **self.__grid_dict)
            count+=1
        count=-1
        for info in produits[1]:
            if count!=-1:
                text = StringVar()
                text.set(info)
                entrys.append(Entry(self.__fenetre,font=("Arial", 20),textvariable=text,borderwidth=1,relief="solid"))
                entrys[count].grid(row=1,column=count, **self.__grid_dict)
            count+=1
        Button(self.__fenetre, font=("Arial", 20),text="Confirmer modification", bg="red" , command= lambda:self.confirmer_modification([produits[1][0],entrys[0].get(),entrys[1].get(),entrys[2].get(),entrys[3].get(),entrys[4].get()],"produit")).grid(row=2,**self.__grid_dict)
    
    def confirmer_delete(self,nom,choice):
        if choice=="produit":
            self.__crud_produit.delete_produit(nom)
            self.affichage_par_produits()
        elif choice=="categorie":
            self.__crud_categorie.delete_categorie(nom)
            self.affichage_par_categories()
        
        
    def confirmer_ajout(self,info,choice):
        if choice=="produit":
            self.__crud_produit.create_produit(info)
            self.affichage_par_produits()
        elif choice=="categorie":
            self.__crud_categorie.create_categorie(info)
            self.affichage_par_categories()
        
    def confirmer_modification(self,info,choice):
        if choice=="produit":
            self.__crud_produit.update_produit(info)
            self.affichage_par_produits()
        elif choice=="categorie":
            self.__crud_categorie.update_categorie(info)
            self.affichage_par_categories()
        
    def clear_window(self):
        for widget in self.__fenetre.winfo_children():
            widget.destroy()
        
    def choose_product(self,action):
        self.clear_window()
        labelChoix = Label(self.__fenetre, text = "Veuillez faire un choix !", font=("Arial", 20))
        labelChoix.grid(row=0,**self.__grid_dict)
        # Création de la Combobox via la méthode ttk.Combobox()
        liste = ttk.Combobox(self.__fenetre, values=self.listes_nom_produits, font=("Arial", 20))     
        # Choisis l'élément qui s'affiche par défaut
        liste.current(0)
        liste.grid(row=1,**self.__grid_dict)
        if action==1:
            Button(self.__fenetre, font=("Arial", 20),text="Confirmer choix", bg="red" , command= lambda:self.confirmer_delete(liste.get(),"produit")).grid(row=2,**self.__grid_dict)
        elif action==2:
            Button(self.__fenetre, font=("Arial", 20),text="Confirmer choix", bg="red" , command= lambda:self.modify_produit(liste.get())).grid(row=2,**self.__grid_dict)
    
        
    def add_categorie(self):
        self.clear_window()
        Label(self.__fenetre, font=("Arial", 20),text="Nom de la categorie",bg='grey',borderwidth=1,relief="solid").grid(row=0,column=0, **self.__grid_dict)
        entry=Entry(self.__fenetre,font=("Arial", 20),borderwidth=1,relief="solid")
        entry.grid(row=1,column=0, **self.__grid_dict)
        Button(self.__fenetre, font=("Arial", 20),text="Confirmer ajout", bg="red" , command= lambda:self.confirmer_ajout([entry.get()],"categorie")).grid(row=2,**self.__grid_dict)

    def modify_categorie(self,nom):
        self.clear_window()
        categorie=self.__crud_categorie.read_one_categorie(nom)
        Label(self.__fenetre, font=("Arial", 20),text="Nom de la categorie",bg='grey',borderwidth=1,relief="solid").grid(row=0,column=0, **self.__grid_dict)
        text = StringVar()
        text.set(nom)
        entry=Entry(self.__fenetre,font=("Arial", 20),textvariable=text,borderwidth=1,relief="solid")
        entry.grid(row=1,column=0, **self.__grid_dict)
        Button(self.__fenetre, font=("Arial", 20),text="Confirmer modification", bg="red" , command= lambda:self.confirmer_modification([categorie[0],entry.get()],"categorie")).grid(row=2,**self.__grid_dict)

    def choose_categorie(self,action):
        self.clear_window()
        self.listes_nom_categories=[]
        self.listes_nom_categories=self.__crud_categorie.read_categorie_all()
        labelChoix = Label(self.__fenetre, text = "Veuillez faire un choix !", font=("Arial", 20))
        labelChoix.grid(row=0,**self.__grid_dict)
        # Création de la Combobox via la méthode ttk.Combobox()
        liste = ttk.Combobox(self.__fenetre, values=self.listes_nom_categories, font=("Arial", 20))     
        # Choisis l'élément qui s'affiche par défaut
        liste.current(0)
        liste.grid(row=1,**self.__grid_dict)
        if action==1:
            Button(self.__fenetre, font=("Arial", 20),text="Confirmer choix", bg="red" , command= lambda:self.confirmer_delete(liste.get(),"categorie")).grid(row=2,**self.__grid_dict)
        elif action==2:
            Button(self.__fenetre, font=("Arial", 20),text="Confirmer choix", bg="red" , command= lambda:self.modify_categorie(liste.get())).grid(row=2,**self.__grid_dict)
        elif action==3:
            Button(self.__fenetre, font=("Arial", 20),text="Confirmer choix", bg="red" , command= lambda:self.confirm_export_categorie(liste.get())).grid(row=2,**self.__grid_dict)

    def confirm_export_categorie(self,nom):
        self.__export.export_categorie(nom)
        self.affichage_par_categories()
    
         
    def affichage_par_categories(self):
        self.listes_nom_produits=[]
        self.clear_window()
        produits=self.__crud_categorie.read_categorie()
        frame_centrale=Frame(self.__fenetre, bg="grey")
        
        frame_graphique=Frame(frame_centrale)
        Graphique(frame_graphique,self.__crud_categorie)
        frame_test=Frame(frame_centrale,width=self.__fenetre.winfo_width())
        frame_frame=Frame(frame_centrale)
        main_frame=Frame(frame_frame, bg="grey")
        main_frame.grid(row=2, column=0, pady=(5, 0))
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_propagate(False)
        canvas = Canvas(main_frame, bg="grey")
        canvas.grid(row=0, column=0, sticky="news")
        
        vsb = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)
        
        info_frame=Frame(canvas,bg='grey')
        canvas.create_window((0, 0), window=info_frame, anchor='c')
        
        line=0
        for produit in produits:
            colone=0
            for info in produit:
                if info!=produit[len(produit)-1]:
                    label=Label(info_frame, font=("Arial", 20),text=info,bg='grey',fg=produit[len(produit)-1],borderwidth=1,relief="solid")
                    label.grid(row=line,column=colone, **self.__grid_dict)
                colone+=1
            line+=1
        
        info_frame.update_idletasks()
        first5rows_height = sum([label.winfo_height() for i in range(0, 7)])
        main_frame.config(width=self.__fenetre.winfo_width()-(self.__fenetre.winfo_width()-info_frame.winfo_width())+ vsb.winfo_width()*2
                          , height=first5rows_height)
        # Set the canvas scrolling region
        canvas.config(scrollregion=canvas.bbox("all"))
        frame_frame.pack()
        frame_centrale.pack()
        

        Button(frame_test, font=("Arial", 20),text="Ajouter categorie", bg="red" , command= lambda:self.add_categorie()).grid(row=line,column=0)
        Button(frame_test, font=("Arial", 20),text="Supprimer categorie", bg="red" , command= lambda:self.choose_categorie(1)).grid(row=line,column=1)
        Button(frame_test, font=("Arial", 20),text="Modifier categorie", bg="red" , command= lambda:self.choose_categorie(2)).grid(row=line,column=2)
        Button(frame_test, font=("Arial", 20),text="Afficher par produit", bg="red" , command= lambda:self.affichage_par_produits()).grid(row=line,column=3)
        Button(frame_test, font=("Arial", 20),text="Exporter une categorie", bg="red" , command= lambda:self.choose_categorie(3)).grid(row=line,column=4)
        frame_test.pack()
        frame_graphique.pack()    
        
        
        self.__fenetre.mainloop()