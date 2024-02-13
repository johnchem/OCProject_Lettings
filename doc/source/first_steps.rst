Premier pas
===========

Cette partie permettra de disposer d'une version de développement local.

Prérequis
---------
- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure
- Compte `Sentry <https://sentry.io>`_

Instruction d'installation
--------------------------
Clonage du répertoire
^^^^^^^^^^^^^^^^^^^^^
- ``cd /path/to/put/project/in``
- ``git clone https://github.com/johnchem/OCProject_Lettings.git``

Création de l'environnement virtuel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- ``cd /path/to/OCProject_Lettings``
- ``python -m venv venv``
- Pour Linux: ``apt-get install python3-venv`` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement ``source venv/bin/activate`` (Linux) ou ``venv\Scripts\activate`` (Windows)
- Confirmer que la commande ``python`` exécute l'interpréteur Python dans l'environnement virtuel ``which python``. Dans Windows, la commande ``powershell Get-Command python`` dois être utilisé.
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure ``python --version``
- Confirmer que la commande ``pip`` exécute l'exécutable pip dans l'environnement virtuel, ``which pip`` (Linux) ou ``powershell Get-Command python`` (Windows)
- Pour désactiver l'environnement, ``deactivate``

Installation du projet en développement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- ``cd /path/to/OCProject_Lettings``
- ``source venv/bin/activate`` ou ``venv\Scripts\activate``
- ``pip install -r requirements.txt``
- Créer un fichier ``.env`` sur base de la structure du fichier ``.env.exemple``

Creation d'un project dans Sentry.io
""""""""""""""""""""""""""""""""""""
- Dans votre compte Sentry, aller sur la page **Projects**
- Créer un nouveau projet en cliquand sur le bouton en haut à droite de la page
- Choisir la plateforme **Django**
- Régler vos préférences d'alerte
- Donner enfin un nom à votre projet dans sentry et attribuer une équipe
- Cliquer sur le bouton **Create Project** pour finaliser l'opération
- Sentry confirmera la création du projet, en fournissant quelques informations pour débuter. 
- Dans l'exenple de code, il fournira une clef **dns**.
- Copier cette clef dans le fichier ``.env``

Creation d'une clef secrete Django
""""""""""""""""""""""""""""""""""
- Ouvrir un terminal python avec la commande ``python``
- ``import secrets``
- ``print(secrets.token_urlsafe())``
- copier la valeur dans le fichier ``.env``

Adresse de la base de données
"""""""""""""""""""""""""""""
- Renseigner l'adresse de la base de donnée sur la structure ``sqlite:///nom_de_la_db.sqlite3``

Activation du mode Développement
""""""""""""""""""""""""""""""""
- Donner la valeur **True** à la variable **DEBUG** dans le fichier ``.env`` 

Lancement du site local
"""""""""""""""""""""""
- ``python manage.py runserver``
- Aller sur `http://localhost:8000 <http://localhost:8000>`_ dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

Démarrage rapide
----------------

Lancement des tests de Lintings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- ``cd /path/to/OCProject_Lettings``
- ``source venv/bin/activate`` ou ``venv\Scripts\activate``
- ``flake8``

Excécussion de la suite de tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- ``cd /path/to/OCProject_Lettings``
- ``source venv/bin/activate`` ou ``venv\Scripts\activate``
- ``pytest``

| Le projet fonctionne sur base de django 3.0.
| Cette version utilise encore la librairie distutils qui est obsoléte.
| Ceci génére des avertissements dans pytest mais sans affecter le fonctionnement

Panel d'administration
^^^^^^^^^^^^^^^^^^^^^^
- Aller sur ``http://localhost:8000/admin``
- Connectez-vous avec l'utilisateur ``admin``, mot de passe ``Abc1234!``

Technologie et languages
------------------------

Languages
^^^^^^^^^
- python 3.10
- CSS
- HTML
- javascript

Technologie
^^^^^^^^^^^
**Site web**
- Django 3.0
- SQLite3
- Bootstrap v5.1.3
- WhiteNoise v6.6.0

**Testing**
- BeautifulSoup4 v4.12
- Flake8 v3.7
- Coverage v7.4
- Pytest v7.4

**Documentation**
- Sphinx v7.2 
- Graphviz v2.42
