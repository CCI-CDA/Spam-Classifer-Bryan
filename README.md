# Spam-Classifier
Projet ayant pour but de réaliser une application web qui permette de classifier des messages SMS en ‘spam’ ou ‘ham’
commande docker:
docker build --tag grpccicdaacr.azurecr.io/spam-classifier-bryan .
commande github:

uvicorn server:app --reload
pip install -r requirements.txt

Dupliquer la bd local sur le serv distant
host dans image docker 0000