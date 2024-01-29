Guide d'utilisation
===================
Structure du projet
^^^^^^^^^^^^^^^^^^^^
le projet est structuré selon 3 applications :
* oc_lettings_site : gestion du site et des pages générales
* lettings : gestion des adresses et des locations
* profiles : gestion des profiles utilisateur

Les applications sont composés des éléments:
* models.py : représentation de la structure des objets dans la base de données
* urls.py : liste des chemins urls pour l'application
* views.py : fichier avec les vues 
* templates/ : repertoire contenant les templates HTML
* tests.py : suite de tests unitaires de l'application
* fixtures/ : fixtures pour les tests unitiares

L'application oc_lettings_site requiered 2 des élélents supplémentaire:
* admin.py : paramétrage de la page par défaut /admin
* settings.py : paramétrage de l'ensemble de l'application

Les images et fichier CSS sont servis à partir du fichier **static/** placé à la racine du projet.


Création ou modification d'un modéle
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
La création ou modification d'un modéle est réalisé via le fichier **models.py**
- Créer ou modifier le modéles accordément à la documentation de Django
- ``django-admin makemigrations``
- ``django-admin migrate``


Création d'une nouvelle vue
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Ecriture de la vue dans le fichier **views.py**
- Création d'un nouveau template dans **templates/** pour afficher la vue
- Création d'un chemin url dans **urls.py** pour appeler la vue

Ecriture des tests unitaires
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Les tests unitaires doivent permettre de tester chaque sous-élements que soit les modéles, les urls ou les vues.

test des urls
""""""""""""""
Pour tester les urls, on utilise la fonction ``django.urls.reverse`` pour obtenir le chemin d'accés.
on vérifie que ce chemin méne au bon lien urls. Enfin avec la fonction ``django.urls.resolve``, on vérifie que l'on retrouve le nom initial de l'url.

test des vues
""""""""""""""
La réponse HTML à l'appel de la page est obtenu via la fonction ``client.get(url)``. La librairie **BeautifulSoup4** permet d'inspecter la réponse.
On va vérifier le statut HTTP de la résponse et la présente de contenu spécifique à la page désiré. 
Par exemple pour tester une page **LIST**: on passera en fixture une liste d'objets et on vérifiera que l'on retrouve l'ensemble des objects sur la page avec le bon titre.   

test des modéles
""""""""""""""""
Pour les tests des modéles, on testera les paramétres CRUD, la validations des champs et les relations entre les objets.