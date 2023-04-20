
class Produit:
    def __init__(self,conn):
        
        self.__conn=conn
        self.__database=conn.cursor()
        #verifie l'existence de la table produits
        self.__database.execute("SHOW TABLES LIKE 'produits'")
        result = self.__database.fetchone()
        
        if not result:
            #creer la table produits si inexistante et la remplie
            self.__database.execute("CREATE TABLE produits(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, nom varchar(255),description text, prix int, quantite int,id_categorie int,FOREIGN KEY (id_categorie) REFERENCES categories(Id) ON UPDATE CASCADE)")
            self.create_produit(['oeuf', 'Poule bio', 1,12,1])
            self.create_produit(['lait', 'Vache en plein air', 3,6,1])
            self.create_produit(['gateaux', 'Gout chocolat', 6,50,1])
            self.create_produit(['sucre', 'Sucre roux', 5,50,1])
            self.create_produit(['vin', 'production  local', 10,50,2])
            self.create_produit(['whisky', 'Grand brandy', 15,50,2])
            self.create_produit(['rhum', 'des îles', 1,12,2])
            self.create_produit(['courgette', 'bien verte', 3,6,3])
            self.create_produit(['poireaux', 'pas au menton', 6,50,3])
            self.create_produit(['carotte', 'approuvé par les lapins', 5,50,3])
            self.create_produit(['raisin', 'de France', 10,50,4])
            self.create_produit(['banane', 'de madagascar', 15,50,4])
            self.create_produit(['kiwi', 'pas le volatile', 1,12,4])
            self.create_produit(['fraise', 'bien rouge', 3,6,4])
            self.create_produit(['chaussette', 'de type socket', 6,50,5])
            self.create_produit(['chaussure', 'basket confortable', 5,50,5])
            self.create_produit(['jean', 'marque levis', 10,50,5])
            self.create_produit(['t-shirt', 'conton bio', 15,50,5])
        
            
    
    def delete_table(self):
        self.__database.execute("drop table produits")
    
    def delete_produit(self,nom):
        self.__database.execute(f"delete from produits where nom='{nom}'")
        self.__conn.commit()
        
    def create_produit(self,info):
        if "" in info :
            return "Veuillez remplir tout les champs"   
        try:
            self.__database.execute(f"insert into produits (nom,description,prix,quantite,id_categorie) values('{info[0]}','{info[1]}',{info[2]},{info[3]},{info[4]})")
        except:
            self.__database.execute("select id from categories")
            test=self.__database.fetchall()
            try:
                int(info[2])
                int(info[3])
            except:
                return "Les champs quantité et prix doivent être des nombres"
            else:
                return "Cette catégorie n'existe pas"
        else:
            self.__conn.commit()
        
    def get_produits(self):
        liste_produits=[["Nom du produit","Description du produit","Prix du produit","Quantité du produit","ID categorie","blue"]]
        self.__database.execute("SELECT nom,description,prix,quantite,id_categorie FROM produits")
        produits=self.__database.fetchall()
        for produit in produits:
            liste_produits.append([produit[0],produit[1],produit[2],produit[3],produit[4],"black"])
        return liste_produits
    
    
    def get_one_produit(self,nom):
        self.__database.execute(f"SELECT id,nom,description,prix,quantite,id_categorie FROM produits where nom='{nom}'")
        produit=self.__database.fetchone()
        return produit
    
    def get_column(self,column):
        self.__database.execute(f"SELECT {column} FROM produits")
        resultat=self.__database.fetchall()
        print(resultat)
        
    def set_produit(self,info):
        if "" in info :
            return "Veuillez remplir tout les champs"
        try:
            self.__database.execute(f"UPDATE produits set nom='{info[1]}',description='{info[2]}',prix={info[3]},quantite={info[4]},id_categorie={info[5]} where id={info[0]}")
        except:
            self.__database.execute("select id from categories")
            test=self.__database.fetchall()
            try:
                int(info[2])
                int(info[3])
            except:
                return "Les champs quantité et prix doivent être des nombres"
            else:
                return "Cette catégorie n'existe pas"
        else:
            self.__conn.commit()
        

    
