.. {{cookiecutter.project_name}} documentation master file.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to {{cookiecutter.project_name}}'s documentation!
==========================================================

This documentation is generated from the template defined in ``./docsrc/source/index.rst``.

Since not everybody knows the reStructured Text syntax cold, it does help to have a good reference or two.

* `reStructured Text Cheat Sheet`_

Example notebook added to documentation using `NBSphinx`_...

.. toctree::
    :maxdepth: 2

    Notebook Template <_notebooks/notebook-template>

Example of using the `Sphinx Autodoc`_ extension to document the automatically included support library for this project located in ``./src/{{cookiecutter.support_library}}``.

.. automodule:: {{cookiecutter.support_library}}
    :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _reStructured Text Cheat Sheet: https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html
.. _NBSphinx: https://nbsphinx.readthedocs.io/en/0.8.8/
.. _Sphinx Autodoc: https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html