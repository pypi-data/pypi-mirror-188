.. highlight:: shell

============
Installation
============


Stable release
--------------

First of all, you want to make sure you have **python** and **pipx** installed on your device.

python
^^^^^^

Here are a few Python installation guides (it's quick):

* `Install Python on Windows <https://docs.python-guide.org/starting/install3/win/#install3-windows>`_
* `Install Python on MacOS <https://docs.python-guide.org/starting/install3/osx/#install3-osx>`_
* `Install Python on Linux <https://docs.python-guide.org/starting/install3/linux/#install3-linux>`_

pipx
^^^^

On macOS:

.. code-block:: console

    $ brew install pipx
    $ pipx ensurepath

Otherwise, install via pip (requires pip 19.0 or later):

.. code-block:: console

    $ python3 -m pip install --user pipx
    $ python3 -m pipx ensurepath

cryptoolz
^^^^^^^^


The best way to install cryptoolz after this, for regular users, is as follows:

.. code-block:: console

    $ pipx install --suffix <SOME SUFFIX OF YOUR CHOICE> cryptoolz

We want to essentially be absolutely sure that our local installation is always able to decrypt some data, so instead of updating cryptoolz we should simply always have a fresh install with a new suffix. As such, we never upgrade once downloaded versions.

This does not mean that the library won't be backwards compatible, but this is simply the safest option for regular users.

Instead when using as a library the regular:

.. code-block:: console

    $ pip install cryptoolz

Is used as usual.

From sources
------------

The sources for cryptoolz can be downloaded from the `Codeberg repo`_.

You can clone the public repository:

.. code-block:: console

    $ git clone git://codeberg.com/tanats_nir/cryptoolz

.. _Codeberg repo: https://codeberg.com/tanats_nir/cryptoolz
