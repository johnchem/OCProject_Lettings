Mise en production
==================

Flux de travail
---------------
#. Modification du code source
#. Commit des changements vers le repertoire distant
#. Déclanchement automatique de la routine CircleCI
#. Lancement de la suite de test
#. Lancement du test de couverture du code
#. Lancement du test de Linting
#. Création du conteneur Docker par CircleCI si la suite de test se termine avec succés 
#. Envoie de l'image sur dockerHub aprés avoir reçu un tag unique, 
#. Dockerhub signal à Render la réception d'une nouvelle version de l'image  
#. Récupéreration de la nouvelle image par Render 
#. Lancement d'une série de commande pour lancer le conteneur, distribuer les fichiers statiques et lancer le serveur Django

.. note:: Les résultats du test de Linting et de couverture ne sont pas blocants


Configuration du fichier dockerfile pour la conteneurisation
------------------------------------------------------------
La structure du fichier d'instruction pour la contruction de l'image docker est décrit ci-dessous : 

- Obtention d'une image docker de base

.. code-block::
  
  FROM python:3.10-alpine3.19

- Mise à jour de l'OS, git est nécéssaire pour l'importation du répertoire lors de la dockeurisation par circleCI, gcc et g++ sont utilisé par pygraphviz-dev

.. code-block::
  
  RUN apk update \
  && apk add --no-cache git \
  && apk add --no-cache gcc \
  && apk add --no-cache g++ \
  && apk add --no-cache --upgrade bash \
  && apk add --no-cache graphviz-dev

- Changement du dossier de travail et copie des fichiers sources

.. code-block::
  
  WORKDIR /OCProject_Lettings
  COPY . /OCProject_Lettings

- Création de l'environnement virtuel et installation des librairies

.. code-block::
  
  ENV VIRTUAL_ENV=/venv
  RUN python3 -m venv $VIRTUAL_ENV
  ENV PATH="$VIRTUAL_ENV/bin:$PATH"

  RUN pip3 install --upgrade pip \
  && pip3 install -r requirements.txt --no-cache-dir

- Configuration du port de sortie, et paramétres pour limiter la formation de cache

.. code-block::
  
  EXPOSE 8000

  ENV DJANGO_SETTINGS_MODULE=oc_lettings_site.settings
  ENV PYTHONDONTWRITEBYTECODE 1 #av
  ENV PYTHONUNBUFFERED 1

- Le script d'exécution est lancé par la commande ci-dessous. 

.. code-block::
  
  CMD sh ./script.sh

- Enfin, créer un nouveau fichier `script.sh` à la racine du projet

.. code-block::

  #/bin/sh
  python3 manage.py collectstatic --noinput
  python3 manage.py runserver 0.0.0.0:8000

Configuration du fichier config.yml pour circleCI
-------------------------------------------------

Le fichier ``.circleci/config.yml`` permet de configurer une série de tâche. Par défaut, ces tâches sont excécutées dans leurs ordres de définitions. Il est possible de créer des workflows pour définir un flux personnalisé selon les besoins. 

Configuration des suites de tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Exemple de configuration pour la réalisation des tests unitaire
* selectionner une image docker depuis circleCI

.. code-block::
   
   docker:
    - image: cimg/python:3.10

* charger les variables d'environnement. Dans notre cas, on défini la variable ALLOWED_HOSTS pour django

.. code-block::
   
   environment:
    - ALLOWED_HOSTS: localhost

* On viens définir ensuite les étapes de notre taches
    *  récupération du code depuis github
    
    .. code-block::
       
       - checkout

    * circleCI va chercher à restorer un cache ayant un tag unique composé du nom de la branche et du checksum basé sur requirements.txt
    
    .. code-block::

       - restore_cache: 
           key: deps1-{{ .Branch }}-{{ checksum "requirements.txt" }}

    * mise à jour des paquets de l'image docker et installation de graphviz pour la l'exécution de la documentation.

    .. code-block::

      - run:
          command: |
            sudo apt update -y
            sudo apt install graphviz-dev -y

    *  La suite des instructions permet de créer un environment virtuel, son exécecution et l'installation des librairies. Si un fichier de cache existe, les instructions seront évalué mais les actions sont déjà réalisées.

      .. code-block::

         python3 -m venv venv
         . venv/bin/activate
         pip install -U pip setuptools
         pip install -r requirements.txt

    * on créer un cache pour faciliter la prochaine exécution.

      .. code-block::

         key: deps1-{{ .Branch }}-{{ checksum "requirements.txt" }}
          paths:
           - "venv"

    * Enfin on excécute la commande d'interêt. Dans ce cas, on active l'environment virtuel et on exécute le module pytest

      .. code-block::

         name: Running tests
         command: |
           . venv/bin/activate
           python3 -m pytest

Configuration de la conteneurisation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* chargement d'une image docker pour l'excecution des commandes de conteneurisation

.. code-block::

     docker:
       - image: cimg/base:2022.09
         auth:
           username: $DOCKERHUB_USERNAME
           password: $DOCKERHUB_PASSWORD

* Lancement des étapes de conteneurisation

  * récupération du code source

  .. code-block::
    
    - checkout
    
  * cette ligne permet l'excecution des commandes `docker` et `docker-compose` localement sur la machine 

  .. code-block::

     - setup_remote_docker
    
  * chargement d'un cache si existant
    
  .. code-block::

     - restore_cache:
           keys:
             - v1-{{ .Branch }}
  
  * chargement des caches Docker

  .. code-block::

    - run:
        name: Load Docker image layer cache
        command: |
          set +o pipefail
          docker load -i /caches/app.tar | true
      
  * création d'une variable pour l'identification de l'image Docker
  
  .. code-block::

    - run: echo "$CIRCLE_SHA1" >> .tag

  * création d'une variable `TAG` et utilisation de celle-ci pour l'identification de l'image. Puis, connection au repertoire docker. Enfin, on pousse l'image sur dockerhub

  .. code-block::

     name: Build and Push application Docker image
     command: |
        docker build -t $DOCKERHUB_USERNAME/orange_county:$(cat .tag) -t $DOCKERHUB_USERNAME/orange_county:latest .
        echo $DOCKERHUB_PASSWORD | docker login -u $DOCKERHUB_USERNAME --password-stdin
        docker push --all-tags $DOCKERHUB_USERNAME/orange_county
    
  * on créer un cache pour faciliter la prochaine exécution

  .. code-block::
     
     - save_cache:
       key: 
         - v1-{{ .Branch }}
       paths:
         - /caches/app.tar

Configuration des workflows
^^^^^^^^^^^^^^^^^^^^^^^^^^^

on attribut un nom de workflow au sommet de l'arbre. Puis on viens définir les différentes tâches nécéssaires dans le workflow. 
Quand 2 taches sont au même niveau, les tâches sont exécutées de manière concurente. 
Pour définir une excécution séquentielle, il faut utiliser l'option `requires`. 
Cette option définie que la tâche ne doit pas être exécutée si l'une des tâches renseignées ne se termine pas avec un succés.
L'option `filters` définie les différents cas de figure dans lesquels la tâche doit être exécutée. 

.. code-block::

   test_build_and_push:
   jobs:
     - pytest
     - coverage
     - linting
     - container:
         context:
           - docker_hub_creds
         requires:
           - pytest
         filters:
           branches:
             only: master


Configuration du projet dans circleCI
-------------------------------------

Lors de la creation du projet dans circleCI, le formulaire demande un nom de projet et la creation d'une clef SSH vers github. 
La clef public est passé dans github et la clef privé doit être passé dans le formulaire. 
Enfin le formulaire va demander d'indiquer le répertoire du projet et identifier si un fichier de configuration existe sous `.circleci/config.yml`.

Dans les paramétres d'organisations, on va créer un contexte qui permettra de maintenir les identifiants connection à dockerhub commun à plusieurs projet. 
Dans le sous-menu **contexts**, cliquez sur **Create Context**. Créer un context nommé **docker_hub_creds** puis **Add Environmnent Variable**. 
Créer les variables **DOCKERHUB_PASSWORD** et **DOCKERHUB_USERNAME**.

Dans les paramétres du projet, on va venir créer les variables d'environment nécéssaire à l'exécution et aux tests du projet. 
Ces variables sont les mêmes que celles du fichier `.env`. 
En effet, le fichier contenant les variables n'est pas disponible dans le répertoire publique. 
CircleCI doit donc servir celles-ci lors des tests.

Configuration de Render pour le déploiement
-------------------------------------------

- Créer un nouveau **Web Service** dans votre dashboard Render. 
- Selectionner **Deploy an existing image from a registry**
- Introduire l'adresse URL de l'image sur Dockerhub ``docker.io/<namespace>/<image_name>:<version>``, par exemple : ``docker.io/johnchem/orange_county:latest``
- Définir un nom pour le web service et selectionner les paramétres de service pour le service
- Ajouter dans les variables d'environment : **ENV_PATH; /etc/secrets/.env**. Cette variable permet d'indiquer le chemin du fichier ``.env`` nécéssaire lors de l'exécution du module ``oc_letting_site.settings.py``.
- cliquer sur le boutton "Advanced" pour afficher plus d'options de configuration
- Ajouter un fichier ``.env`` en cliquant sur le boutton **+ Add Secret File**. le nom sera **.env** et les valeurs seront le contenu du fichier **.env.exemple** avec les champs remplis selon les intructions.
- Sous l'option **Docker Command** introduisez : ``/bin/sh -c python3 manage.py collectstatic --noinput && python3 manage.py runserver 0.0.0.0:8000``. La commande va exécuter la migration des fichiers statiques sur le serveur puis lancer le serveur docker sur le port 8000.
- Enfin cliquer sur **Create Web Service** pour deployer le site.

La dernière étape est la configuration du *Web hook* pour le deploiement automatique :

- Dans le dashbord, allez dans les **settings** du web service et dans le sous-menu **settings**
- Copier l'url ``Deploy Hook`` et l'introduire dans le sous-menu **Web Hook** de DockerHub
