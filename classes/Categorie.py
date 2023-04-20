import csv

class Categorie:
    def __init__(self,conn):
        self.__conn=conn
        self.__database=conn.cursor()
        #verifie l'existence de la table categories
        self.__database.execute("SHOW TABLES LIKE 'categories'")
        result = self.__database.fetchone()
        
        if not result:
            #creer la table categorie si inexistante et la remplie
            self.__database.execute("CREATE TABLE categories(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, nom varchar(255))")
            self.create_categorie('épicerie')
            self.create_categorie('alcool')
            self.create_categorie('légumes')
            self.create_categorie('fruits')
            self.create_categorie('vêtements')
    
    def delete_table_categorie(self):
        self.__database.execute("drop table categories")
            
    def delete_categorie(self,nom):
        try:
            self.__database.execute(f"delete from categories where nom='{nom}'")
        except:
            return False
        else:
            self.__conn.commit()
            return True
        
    def force_delete(self,nom):
        self.__database.execute(f"delete from produits where id_categorie=(select categories.id from categories where categories.nom='{nom}')")
        self.__conn.commit()
        self.__database.execute(f"delete from categories where nom='{nom}'")
        self.__conn.commit()  
        
    def create_categorie(self,nom,id=0):
        if id:
            self.__database.execute(f"insert into categories(id,nom) values ({id},'{nom[0]}')")
        else:
            self.__database.execute(f"insert into categories(nom) values ({nom})")
        self.__conn.commit()       
        
    def get_categorie_all(self):
        self.__database.execute("SELECT id,nom FROM categories")
        categories=self.__database.fetchall()
        return categories
        
    def get_categorie(self):
        list_categorie=[]
        self.__database.execute("SELECT categories.nom,produits.nom,description,prix,quantite,categories.id FROM categories inner JOIN produits ON id_categorie = categories.id order by categories.id")
        categories=self.__database.fetchall()
        categorie_save=""
        for categorie in categories:
            if categorie[0]!=categorie_save:
                list_categorie.append([f"Nom de la catégorie et ID", categorie[0],categorie[5],'red'])
                list_categorie.append(["Nom du produit","Description du produit", "Prix du produit", "Quantité du produit",'blue'])  
                list_categorie.append([categorie[1],categorie[2],categorie[3],categorie[4],"black"]) 
                categorie_save=categorie[0]
            else:
                list_categorie.append([categorie[1],categorie[2],categorie[3],categorie[4],"black"]) 
        return list_categorie     
    
    def get_one_categorie(self,nom):
        self.__database.execute(f"SELECT id,nom FROM categories where nom='{nom}'")
        categorie=self.__database.fetchone()
        return categorie
    
    def set_categorie(self,info):
        self.__database.execute(f"UPDATE categories set nom='{info[1]}' where id={info[0]}")   
        self.__conn.commit()

    def count_produit_in_categorie(self,categorie):
        self.__database.execute(f"SELECT count(produits.id) FROM produits inner JOIN categories where id_categorie=(select categories.id where categories.nom='{categorie}')")
        produit=self.__database.fetchone()
        return produit[0]