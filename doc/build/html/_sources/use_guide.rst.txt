Guide d'utilisation
===================
Structure du projet
^^^^^^^^^^^^^^^^^^^^
le projet est structuré selon 3 applications :

* **oc_lettings_site :** gestion du site et des pages générales
* **lettings :** gestion des adresses et des locations
* **profiles :** gestion des profiles utilisateur

Les applications sont composées des éléments:

* **models.py :** représentation de la structure des objets dans la base de données
* **urls.py :** liste des chemins urls pour l'application
* **views.py :** fichier avec les vues 
* **templates/ :** repertoire contenant les templates HTML
* **tests.py :** suite de tests unitaires de l'application
* **fixtures/ :** fixtures pour les tests unitiares

L'application **oc_lettings_site** nécéssite 2 des élélents supplémentaires :

* **admin.py :** paramétrage de la page par défaut ``/admin``
* **settings.py :** paramétrage de l'ensemble de l'application

Les images et fichier CSS sont servis à partir du fichier ``static/`` placé à la racine du projet.


Création ou modification d'un modéle
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
La création ou modification d'un modéle est réalisé via le fichier ``models.py``

- Créer ou modifier le modéles accordément à la documentation de Django
- ``django-admin makemigrations``
- ``django-admin migrate``


Création d'une nouvelle vue
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Ecriture de la vue dans le fichier ``views.py``
- Création d'un nouveau template dans ``templates/`` pour afficher la vue
- Création d'un chemin url dans ``urls.py`` pour appeler la vue

Ecriture des tests unitaires
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Les tests unitaires doivent permettre de tester chaque sous-élements que soit les modéles, les urls ou les vues.

Test des urls
""""""""""""""
Pour tester les urls, on utilise la fonction ``django.urls.reverse`` pour obtenir le chemin d'accés.
on vérifie que ce chemin méne au bon lien urls. 
Enfin avec la fonction ``django.urls.resolve``, on vérifie que l'on retrouve le nom initial de l'url.

.. code-block::

    def test_letting_index_url(self):
        path = reverse('lettings_index')
        assert path == "/lettings/"
        assert resolve(path).view_name == "lettings_index"

Test des vues
""""""""""""""
La réponse HTML à l'appel de la page est obtenu via la fonction ``client.get(url)``. 
La librairie **BeautifulSoup4** permet d'inspecter la réponse.
Le test vérifie le statut HTTP de la résponse et la présente de contenu spécifique à la page désirée. 
Par exemple pour tester une page **LIST**: on passera en fixture une liste d'objets et on vérifiera que l'on retrouve l'ensemble des objects sur la page avec le bon titre.

.. code-block::
    
    def test_letting_detail_view(self, client):
        expected_data = [
            [...]
        ]

        path = reverse('letting', kwargs={'letting_id': 4})
        resp = client.get(path)
        soup = BeautifulSoup(resp.content, features="html.parser")
        card = soup.find("div", "card")
        result = [x.string for x in card.find_all("p")]

        for data, expected in zip(result, expected_data):
            assert data == expected

Test des modéles
""""""""""""""""
Pour les tests des modéles, on testera les paramétres CRUD, la validations des champs et les relations entre les objets.

.. code-block::

    def test_create_letting(self, client, capsys):
        address_ref = Address.objects.create(
            [...]
        )
        title = "Museum of Modern Art"

        letting = Letting.objects.create(
            title=title,
            address=address_ref
        )
        print(letting)
        captured = capsys.readouterr()
        assert captured.out == title+"\n"
        assert letting.address.street == "West 53 Street"
