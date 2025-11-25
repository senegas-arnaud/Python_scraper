# Python Scraper - Books to Scrape

Un script Python permettant d’extraire automatiquement les données du site Books to Scrape, de les enregistrer dans des fichiers CSV et de télécharger les images de chaque livre classées par catégorie.


## Prérequis

Avant d'exécuter le script, assurez-vous d'avoir :

- **Python 3.10 ou supérieur** installé sur votre machine  (le projet a été développé avec Python 3.13)
- Une connexion Internet (le script télécharge des pages web et des images)
  

## Utilisation du script

- Recréer l'environnement virtuel 
- Activer l'environnement virtuel 
- Installer les dépendances : `pip install -r requirements.txt`
- Dans la fonction explore_website, la ligne 20 limite volontairement le scraper aux trois premières catégories :
    - Supprimez cette ligne pour permettre l’exploration de l’ensemble du site.
    - Vous pouvez également modifier le chiffre dans les crochets pour ajuster le nombre de catégories à scraper.
- Exécuter le code : `python main.py`


## Résultat

- Les données extraites seront stockées dans un fichier CSV à la racine du projet, contenant un fichier CSV pour chaque catégorie.
- Un dossier photos sera créé à la racine du projet, contenant un sous-dossier avec les couvertures des livres pour chaque catégorie.

