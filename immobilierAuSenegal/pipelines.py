import csv
import boto3
import os
from datetime import datetime

class S3UploadPipeline:

    def open_spider(self, spider):
        # On définit le nom du fichier
        self.filename = "annonces_senegal.csv"
        # On initialise une liste pour stocker les items en mémoire
        self.items = []

    def process_item(self, item, spider):
        # On ajoute chaque item (dictionnaire) à notre liste
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        if not self.items:
            return

        # 1. Écriture du fichier CSV localement
        keys = self.items[0].keys()  # Récupère les noms des colonnes depuis le premier item
        
        with open(self.filename, "w", encoding="utf-8", newline="") as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.items)

        # 2. Upload vers AWS S3
        try:
            s3 = boto3.client("s3")
            bucket_name = "m2dsia-ndioufa-ndiaye"
            s3_key = os.path.basename(self.filename)

            s3.upload_file(self.filename, bucket_name, s3_key)
            print(f"Succès : {s3_key} a été envoyé sur S3 dans le bucket {bucket_name}")
            
            # Optionnel : Supprimer le fichier local après l'upload
            # os.remove(self.filename)
            
        except Exception as e:
            print(f"Erreur lors de l'upload S3 : {e}")