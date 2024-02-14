## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`

## Déploiement
### Introduction
- Modification du code source et commit des changements vers le repertoire distant
- Lancement de la suite de test
- Lancement du test de couverture du code
- Lancement du test de Linting
- Création du conteneur Docker par CircleCI si la suite de test se termine avec succés 
- Envoie de l'image sur dockerHub aprés avoir reçu un tag unique, 
- Dockerhub signal à Render la réception d'une nouvelle version de l'image  
- Récupéreration de la nouvelle image par Render 
- Lancement d'une série de commande pour lancer le conteneur, distribuer les fichiers statiques et lancer le serveur Django

### Configuration de CircleCI

- Créer un nouveau projet dans circleCI
- Introduire un nom de projet
- Créer une clef SSH vers github, la clef public est passé dans github et la clef privé doit être passé dans le formulaire
- Indiquer le répertoire du projet et identifier si un fichier de configuration existe sous `.circleci/config.yml`
- Créer un contexte avec les variables **DOCKERHUB_PASSWORD** et **DOCKERHUB_USERNAME** avec vos informations du dockerHub
- Créer les variables d'environments selon les indications du fichier `.env.exemple`. La **SECRET_KEY** ne doit pas être celle utilisé pour la mise en production

### Configuration de Render
- Créer un nouveau **Web Service** dans votre dashboard Render. 
- Selectionner **Deploy an existing image from a registry**
- Introduire l'adresse URL de l'image sur Dockerhub `docker.io/<namespace>/<image_name>:<version>`
- Ajouter dans les variables d'environment : **ENV_PATH; /etc/secrets/.env**.
- cliquer sur le boutton "Advanced" pour afficher plus d'options de configuration
- Ajouter un fichier `.env` en cliquant sur le boutton **+ Add Secret File**. le nom sera **.env** et les valeurs seront le contenu du fichier **.env.exemple** avec les champs remplis selon les intructions.
- Sous l'option **Docker Command** introduisez : `/bin/sh -c python3 manage.py collectstatic --noinput && python3 manage.py runserver 0.0.0.0:8000`
- Enfin cliquer sur **Create Web Service** pour deployer le site.

La dernière étape est la configuration du *Web hook* pour le deploiement automatique :

- Dans le dashbord, allez dans les **settings** du web service et dans le sous-menu **settings**
- Copier l'url `Deploy Hook` et l'introduire dans le sous-menu **Web Hook** de DockerHub