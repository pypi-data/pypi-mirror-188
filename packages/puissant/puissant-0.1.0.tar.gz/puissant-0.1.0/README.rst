puissant
==========================================================

validated user input over command line the easy way
------------------------------------------------------

**puissant** is a collection of Python functions to implement validated user input
from command line

Dependencies
-------------

* Python version required: `3.7+`
* If documentation is to be generated ``sphinx`` and ``sphinx_rtd_theme`` packages are required:

.. code-block:: console

    pip install sphinx sphinx_rtd_theme

Installation
-------------

Simply type ::

  pip install puissant

  
Documentation
----------------

Documentation can be found @ `readthedocs <https://puissant.readthedocs.io>`_

Examples
-----------

* yes/no question

.. code-block:: python

  >>> from  puissant import *
  >>> yes_no(prompt = "Are you happy")
  Are you happy [y/n]?maybe
   input must be one of y, n, yes, no.
  Are you happy [y/n]?yes
  True

* yes/no question with default value

.. code-block:: python
  
  >>> yes_no(prompt = "Are you happy", default = 'y')
  Are you happy [y/n]?(default:y) True


* Single option menu:

.. code-block:: python
  
  >>> menu(prompt = 'what next?', options = ['restart', 'continue', 'quit'])
  what next?
   1 - restart
   2 - continue
   3 - quit
  select an item [range: 1..3]: 4
  input must be in range 1..3.
  select an item [range: 1..3]: quit
  input must be of type int.
  select an item [range: 1..3]: 1
  'restart'

* Tickbox (multiple selection) menu:

.. code-block:: python

  
  >>> tickbox_menu('add extras', ['mayo', 'ketchup', 'garlic', 'tabasco']) 
  add extras
  1  [ ] - mayo
  2  [ ] - ketchup
  3  [ ] - garlic
  4  [ ] - tabasco

  - type a number to tick the option.
  - "a" selects all.
  - "n" de-selects all.
  - "d" selection done.

  Option? : 1
  add extras
  1  [x] - mayo
  2  [ ] - ketchup
  3  [ ] - garlic
  4  [ ] - tabasco

  - type a number to tick the option.
  - "a" selects all.
  - "n" de-selects all.
  - "d" selection done.

  Option? : 3
  add extras
  1  [x] - mayo
  2  [ ] - ketchup
  3  [x] - garlic
  4  [ ] - tabasco

  - type a number to tick the option.
  - "a" selects all.
  - "n" de-selects all.
  - "d" selection done.

  Option? : d
  [(0, 'mayo'), (2, 'garlic')]



