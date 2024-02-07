Mise en production
==================

flux de travail
---------------
#. Modification du code source
#. Commit des changements vers le repertoire distant
#. Déclanchement automatique de la routine CircleCI
#. Lancement de la suite de test
#. Lancement du test de couverture du code
#. Lancement du test de Linting
#. Les résultats du test de Linting et de courverture ne sont pas blocant
#. Si la suite de test se termine avec succés, circleCI à la création du conteneur Docker
#. Aprés avoir reçu un tag unique, l'image est envoyé sur dockerHub
#. La réception d'une nouvelle image sur dockerHub déclanche la routina par Render
#. Render, au signal d'une nouvelle image, va récupérer celle-ci.
#. Lancer une série de commande pour lancer le conteneur, distribuer les fichiers statiques et lancer le serveur Django

Gestion du deploiement
----------------------

Configuration du fichier config.yml
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Le fichier `.circleci/config.yml` permet de configurer une série de tâche. Par défaut, ces tâches sont excécutées dans leurs ordres de définitions. Il est possible de créer des workflows pour définir un flux personnalisé selon les besoins. 

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

on attribut un nom de workflow au sommet de l'arbre. Puis on viens définir les différentes tâches nécéssaires dans le workflow. Quand 2 taches sont au même niveau, les tâches sont exécutées de manière concurente. Pour définir une excécution séquentielle, il faut utiliser l'option `requires`. Cette option définie que la tâche ne doit pas être exécutée si l'une des tâches renseignées ne se termine pas avec un succés.
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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Gestion de l'application et du deploiement
------------------------------------------

* chargement d'une image docker pour l'excecution des commandes de conteneurisation

.. code-block::

     docker:
       - image: cimg/base:2022.09
         auth:
           username: $DOCKERHUB_USERNAME
           password: $DOCKERHUB_PASSWORD

* chargement dans les variables d'environment du hash de commit pour l'identification de l'image docker

.. code-block::

     environment:
       COMMIT_HASH: <<pipeline.trigger_parameters.github_app.commit_sha>>
         #   username: $DOCKERHUB_USERNAME
         #   password: $DOCKERHUB_PASSWORD

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
           paths:
             - /caches/app.tar
  
  * création d'une variable `TAG` et utilisation de celle-ci pour l'identification de l'image. Puis, connection au repertoire docker. Enfin, on pousse l'image sur dockerhub

  .. code-block::

     name: Build and Push application Docker image
     command: |
       TAG=$COMMIT_HASH
       docker build -t $DOCKERHUB_USERNAME/orange_county:$TAG -t $DOCKERHUB_USERNAME/orange_county:latest .
       echo $DOCKERHUB_PASSWORD | docker login -u $DOCKERHUB_USERNAME --password-stdin
       docker push $DOCKERHUB_USERNAME/orange_county:$TAG
    
  * on créer un cache pour faciliter la prochaine exécution

  .. code-block::
     
     - save_cache:
       key: 
         - v1-{{ .Branch }}
       paths:
         - /caches/app.tar

