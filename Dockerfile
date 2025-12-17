# Utilisation d'une image Python stable et légère
FROM python:3.10-slim



# Installation des dépendances système (nécessaires pour compiler certaines libs Python)
RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Installation des bibliothèques Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du contenu de votre projet
COPY . .

# Lancement automatique du spider au démarrage du conteneur
CMD ["scrapy", "crawl", "immo_senegal", "-o", "annonces_senegal.csv"]

#scrapy crawl immo_senegal -o annonces_senegal.csv