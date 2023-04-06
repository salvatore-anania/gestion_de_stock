import csv

class Export:
    def __init__(self,conn):
        self.__database=conn.cursor()
        
    def export(self):
        self.__database.execute('select * from produits')
        with open("liste_produits.csv","w") as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(col[0] for col in self.__database.description)
            for row in self.__database:
                writer.writerow(row)
                
    def export_categorie(self,categorie):
        self.__database.execute(f"SELECT produits.nom,description,prix,quantite FROM categories inner JOIN produits where id_categorie=(select categories.id where categories.nom='{categorie}')")
        with open(f"categorie_{categorie}.csv","w") as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(col[0] for col in self.__database.description)
            for row in self.__database:
                writer.writerow(row)