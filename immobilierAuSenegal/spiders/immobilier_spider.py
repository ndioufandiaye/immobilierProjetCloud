import scrapy
# Assurez-vous d'importer le nouvel Item
from immobilierAuSenegal.items import ImmobilierausenegalItem

class ImmobilierSpider(scrapy.Spider):
    name = 'immo_senegal'
    allowed_domains = ['immobilier-au-senegal.com'] 
    start_urls = ['https://immobilier-au-senegal.com/'] 

    def parse(self, response):
        
        



        """
        Analyse la page et extrait les annonces individuelles en utilisant les sélecteurs trouvés.
        """
        # Cibler le conteneur principal de l'annonce (méthode robuste)
        annonces = response.css('div.rhea_detail_wrapper') 

        self.logger.info(f"Nombre d'annonces trouvées : {len(annonces)}")
        
        for annonce in annonces:
            item = ImmobilierausenegalItem()

            # 1. URL et Titre
            item['url_annonce'] = annonce.css('h3.rhea_heading_stylish a::attr(href)').get()
            item['type_de_bien'] = annonce.css('h3.rhea_heading_stylish a::text').get()
            
            # 2. Localisation
            # Le sélecteur 'span.rhea_address_pin + a::text' capture le texte après l'icône, puis nous nettoyons l'espace
            localisation_brut = annonce.css('.rhea_address_sty a::text').get()
            if localisation_brut:
                item['localisation'] = localisation_brut.strip()
            
            # 3. Prix
            prix_brut = annonce.css('p.rh_prop_card__price_sty::text').get()
            if prix_brut:
                # Nettoyage pour retirer les espaces et les caractères non numériques, sauf 'Fr' ou 'mois'
                prix_net = prix_brut.strip()
                item['prix'] = prix_net
                
            # 4. Détails des chambres/salles de bains (en utilisant la structure des métadonnées)
            # Cibler le span avec la classe 'figure' dans les conteneurs de métadonnées
            
            # Les sélecteurs doivent être précis car la surface est manquante, on utilise ici
            # la position relative des figures (Chambres = 1er, Salles de bains = 2ème)
            figures = annonce.css('.rhea_meta_icon_wrapper span.figure::text').getall()
            
            # Le champ 'surface' est remplacé par 'chambres' et 'salles_de_bains'
            item['chambres'] = figures[0] if len(figures) > 0 else 'N/A'
            item['salles_de_bains'] = figures[1] if len(figures) > 1 else 'N/A'
            
            # NOTE : N'oubliez pas de mettre à jour votre items.py pour inclure 'chambres' et 'salles_de_bains'
            
            yield item
            
##import boto3

import boto3
def upload_file_s3(file_path, bucket_name, object_name=None):
    if object_name is None:
        object_name = file_path

    s3 = boto3.client("s3")
    s3.upload_file(file_path, bucket_name, object_name)


# Exemple d'utilisation
## file_path = "data/file.json"
## file_name = "file.json"

file_path = "immobilierAuSenegal/annonces_senegal.csv"
file_name = "annonces_senegal.csv"

MY_BUCKET_NAME = "m2dsia-ndioufa-ndiaye"
upload_file_s3(file_path, MY_BUCKET_NAME, file_name)