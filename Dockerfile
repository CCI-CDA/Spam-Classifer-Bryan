# Utiliser l'image Python slim comme base
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exposer le port utilisé par l'application
EXPOSE 3778

# Commande pour démarrer l'application avec Uvicorn
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "3778"]
