=====
About
=====


.. image:: https://img.shields.io/pypi/v/cryptoolz.svg
        :target: https://pypi.python.org/pypi/cryptoolz

.. image:: https://img.shields.io/travis/tanats_nir/cryptoolz.svg
        :target: https://travis-ci.com/tanats_nir/cryptoolz

.. image:: https://readthedocs.org/projects/cryptoolz/badge/?version=latest
        :target: https://cryptoolz.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

* Free software: GNU General Public License v3
* Documentation: https://cryptoolz.readthedocs.io.

What
----

This is a CLI app with crypto related tools and a high level slightly-circom-circuit-inspired crypto module. This is a heavy WIP, many more algorithms can be added, code can/must also be polished.

+-------------+-----------------------------------------------------------+
| Tool        | Description                                               |
+=============+===========================================================+
||            || Generates a keypair for a chosen network.                |
|| **keys**   || Encrypts the secret with a chosen algorithm combination. |
|| (offered)  || The public key is shown during generation!               |
||            || Can print a QR code or a basic PEM block!                |
+-------------+-----------------------------------------------------------+
|| **crypto** || crypto will offer options for the above,                 |
|| (planned)  || but generalized to plaintext encryption.                 |
+-------------+-----------------------------------------------------------+

Modules offered
^^^^^^^^^^^^^^^

**crypto** is a "circuit"-like (slightly circom inspired) wrapper for pyca cryptography with pydantic data validation and sensible defaults:

        * Composited: PBDKF2-AESGCM
        * Key Derivation Functions: PBDKF2 
        * Authenticated Encryption: AESGCM
        * Message Digests (Hash): BLAKE2b


Disclaimer
----------

The use of this library is at your own risk. The developer and contributors of cryptoolz are not liable for any types of damages caused through the use of anything which is part of this project.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


