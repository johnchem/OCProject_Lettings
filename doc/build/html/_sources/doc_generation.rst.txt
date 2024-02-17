Génération de la documentation
==============================

Configuration de sphinx
-----------------------

Le fichier ``doc/source/index.rst`` est la base de la documentation, il sert aussi de page d'acceuil.
Les différentes parties de la documentation sont rangées dans le dossier ``doc/source``.
La configuration se fait par via le fichier ``doc/source/conf.py``.

La construction de la documentation se fait avec la commande :
``sphinx-build -M html doc/source doc/build -D graphviz_dot="C:\Program Files\Graphviz\bin\dot.exe"``

Construction du diagramme de la base de données
-----------------------------------------------

Le diagramme de base de données est généré automatiquement sur base des modéles de chaque application.
pour cela, on utilise le module **Graph models** de la librairie **Django-extensions**.
Ce module crée un fichier dot pour le logiciel Graphviz. 

La configuration pour **Graph models** est ajouté dans le fichier ``oc_settings_site.settings.py``

.. code-block:: python

    # settings.py
    GRAPH_MODELS = {
      'all_applications': False,
      'group_models': False,
      'layout': "dot",
      'theme': "django2018",
    }

La configuration de Graphviz se fait dans le fichier de configuration pour Sphinx

.. code-block:: python

    # doc\source\conf.py
    graphviz_output_format = 'svg'

Enfin la création du diagramme se fait via la commande :
``python manage.py graph_models profiles lettings -o doc\source\project.dot``

Celle-ci prend la forme : 
``python manage.py graph-models <applications> -o <fichier_de_sortie>`` 

Configuration de Read the Docs
------------------------------

- Creation d'un fichier de configuration `.readthedocs.yaml` à la racine du projet
- Selection de l'OS pour la construction de la documentation et de la version de python.
  Les paramétres par défault sont conservées.

.. code-block::

  build:
    os: ubuntu-22.04
  tools:
    python: "3.12"

- Indiquer le chemin vers le fichier de configuration de sphinx

.. code-block::

  sphinx:
    configuration: doc/source/conf.py

- Indiquer le fichier de réquis pour l'installation des dépendances

.. code-block::

  python:
    install:
      - requirements: requirements.txt

- Sur le site de (readthedocs https://readthedocs.org/)_
- Connecter vous avec votre compte github
- Créer un nouveau projet et selectionner le dépôt avec le projet
- Ajouter les variables d'environnements dans le menu **admin** du projet