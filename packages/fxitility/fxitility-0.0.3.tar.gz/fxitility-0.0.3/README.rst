FXITILY
=======

Requirements
------------

-  **Python** 3 or later.
-  Several Python packages:

   -  **re**, to support regular expression..

Installation of utilities
-------------------------

Use ``pip3`` to install Python packages:

::

   pip install fxitilty

Basic usage
-----------

::

   from fxitily import Fxility

   obj = Fxility()
   obj.pip_delta(1.1010,1.1020) # Returns -10
