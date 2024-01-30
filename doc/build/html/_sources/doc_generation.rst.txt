Génération de la documentation
==============================

Construction du diagramm de la base de données
----------------------------------------------

config django_extension

.. code-block:: python

    # settings.py
    GRAPH_MODELS = {
      'all_applications': False,
      'group_models': False,
      'layout': "dot",
      'theme': "django2018",
    }

``python manage.py graph_models profiles lettings -o doc\source\project.dot``

configuration de graphiviz::
.. code-block::python

    # doc\source\conf.py
    graphviz_output_format = 'svg'

``sphinx-build -M html doc/source doc/build -D graphviz_dot="C:\Program Files\Graphviz\bin\dot.exe"``

