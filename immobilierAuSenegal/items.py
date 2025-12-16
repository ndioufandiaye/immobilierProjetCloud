# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ImmobilierausenegalItem(scrapy.Item):
    # Les champs mis à jour
    type_de_bien = scrapy.Field()  
    localisation = scrapy.Field() 
    prix = scrapy.Field()
    url_annonce = scrapy.Field()
    
    # Nouveaux champs basés sur l'inspection
    chambres = scrapy.Field() # Nouveau
    salles_de_bains = scrapy.Field() # Nouveau