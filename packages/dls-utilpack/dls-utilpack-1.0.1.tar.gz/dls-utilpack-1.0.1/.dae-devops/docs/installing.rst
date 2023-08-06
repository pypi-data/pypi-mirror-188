.. # ********** Please don't edit this file!
.. # ********** It has been generated automatically by dae_devops version 0.4.0.
.. # ********** For repository_name dls-utilpack

Installing
=======================================================================


You will need python 3.8 or later. 

On a Diamond Light Source internal computer, you can achieve Python 3.8 by::

    $ module load python/3.8

You can check your version of python by typing into a terminal::

    $ python3 --version

It is recommended that you install into a virtual environment so this
installation will not interfere with any existing Python software::

    $ python3 -m venv /scratch/$USER/myvenv
    $ source /scratch/$USER/myvenv/bin/activate
    $ pip install --upgrade pip


You can now use ``pip`` to install the library and its dependencies::

    $ export PIP_FIND_LINKS=/dls_sw/apps/bxflow/artifacts
    $ python3 -m pip install dls-utilpack

If you require a feature that is not currently released you can also install
from git::

    $ python3 -m pip install git+https://gitlab.diamond.ac.uk/scisoft/dls-utilpack.git

The library should now be installed and the commandline interface on your path.
You can check the version that has been installed by typing::

    $ dls-utilpack --version
    $ dls-utilpack --version-json

.. # dae_devops_fingerprint 3fa22d7148c64ac933cb47eaf77d77e6
