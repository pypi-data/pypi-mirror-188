=====
Usage
=====

Read the :doc:`installation` guidelines first!

Even though functions may be part of a subcommand, they are listed "horizontally" here.

Before each function, there is a help output pasted such that the command may be inspected while reading.

The help output describes the exact usage, and the guidelines below help to explain "safe" usage.

create
======

.. code-block:: text

    Usage: cryptoolz keys create [OPTIONS] [NUMBER_PASSPHRASES]
                                 [NUMBER_KEYS_CREATED]

      This command creates a keypair for a chosen network and encrypts the secret
      with a chosen algorithm combination (designated by the keyword shown in
      options), formats it into a chosen format, and also writes (depending on
      format or choice etc.) it into a file or stdout. Note that the options may
      also be appended at the end, but it is advisable to prepend them before
      commands.

      NUMBER_PASSPHRASES is the number of passphrases used for key creation. We
      demand either 1 passphrase for all keys, or multiple keys, for the SAME
      NUMBER_KEYS_CREATED.
      
    Options:
      -n, --network [ethereum]  The network to create keys for.
      -a, --algorithm [aesgcm]  The keyword for the set of algorithms which should
                                be used. For example, aesgcm is currently pbdkf2 +
                                aesgcm.
      -f, --format [pem|qr]     The default output format for encrypted data.
      -o, --outfile FILE        The file to print the created data to.
      --header TEXT             The custom header to use for PEM blocks.
      --digest / --no-digest    Before encryption, compute the digest of the
                                private key. Currently only a dummy option. NOTE:
                                Do NOT send this with encrypted text.
      -h, --help                Show this message and exit.


1. As mentioned, first download the program. For serious data, always use a fixed pipx installed version with a suffix, as mentioned.

2. Disconnect from the internet.

3. Try generating multiple dummy examples based on your settings. For example:

.. code-block:: bash

    cryptoolz keys create --header TEST # this is equal to cryptoolz keys create 1 1 --header TEST
    cryptoolz keys create 2 2 --header TEST
    cryptoolz keys create --format qr --outfile <specify filepath here>
    cryptoolz keys create 2 2 --format qr --outfile <specify filepath here>

4. These should generate outputs, either one or multiple pem blocks in the following format:

.. code-block:: text

    Your Ethereum Public Key:

    0xBa171cc5D6c3813744592422b026b9392FD4FD05

    The encrypted private key block:

    -----BEGIN KEYS-----

    7Tve5fCIpL/ICTCo46pIR46EucPdecIipxhPilSX9b+zc/0VOKLACstf8xtDIlfO
    oQ00nz3H+qZGQP8BohBIwfq1XL4dZEqWh4qrjubsk5bVpkAw06fLLeSNNTQ=

    -----END KEYS-----

5. Or a QR code, the corresponding public key will be printed to console like the above:

.. image:: resources/sample.png

.. warning:: 
    When making a QR code, the public key is printed to console only.
    If you cannot find (???) it for some reason, then redo the operation.

6. Possibly reboot the machine, then only reconnect to the internet, also possibly remove the files beforehand from your device. It all depends on your threat model.

This is the entire create process, but you would also probably at least reveal once to check whether everything worked properly.

This is described next.

reveal
======

.. code-block:: text

    Usage: cryptoolz keys reveal [OPTIONS] [NUMBER_PASSPHRASES] FILEPATHS...

      This command is used to decrypt the encrypted format you have received, as
      output of the `create` command into some file or stdout. This format must be
      pasted into preferably ONE file and then given as input to the command, with
      the right options, according to how you encrypted your data.

      NOTE that for QR codes, the QR code must be scanned by the user and only the
      "plaintext" cyphertext should be pasted into a file, see the docs for more.

      NUMBER_PASSPHRASES is the number of passphrases which will be SEQUENTIALLY
      used to decrypt the inputted key data which is read from files. FILEPATHS
      are the paths to the files which contain the key data.

    Options:
      -n, --network [ethereum]  The network the keys belong to.
      -a, --algorithm [aesgcm]  The keyword for the set of algorithms which the
                                data is encrypted with.
      -f, --format [pem|qr]     Format of the formatted input cyphertext. In
                                future will be automatic.  [required]
      -o, --outfile FILE        The file to print the decrypted data to.
      --digest / --no-digest    Verify private key digest during decryption.
                                Currently a dummy option.
      -h, --help                Show this message and exit.

1. Disconnect from the internet, airgap the device, the plaintext secret key will be either printed to file or console now.

2. Take any dummy examples you generated and know the passphrases for, then (following the above samples):

3. For PEM blocks, paste either the entire paste data, or just the following part, BUT DON'T MODIFY THE FORMAT, including NEWLINES, INDENTATION:

.. code-block:: text

    -----BEGIN KEYS-----

    7Tve5fCIpL/ICTCo46pIR46EucPdecIipxhPilSX9b+zc/0VOKLACstf8xtDIlfO
    oQ00nz3H+qZGQP8BohBIwfq1XL4dZEqWh4qrjubsk5bVpkAw06fLLeSNNTQ=

    -----END KEYS-----

4. For QR codes, scan it, then copy the data into a text file sequentially, noting that the ending '=' are IMPORTANT:

.. code-block:: text

    Nx2IA2tsu/Xzl07kmkJKdGr3Qz9JTcvv/Fp4nAf42/+CFGxuNAws5KN71FLt+Iw5dHdDIioeIKPiLa0Dl/Ss86vlRdyQeoktaeD44nf3jZPIF+GaOXM5vwcWkBk=
    lRzkK4S9qR8KjyXo9ygxehGhDcGPz4CGZgcrIbqt9vVB5VuCzoNYcVkvTm/bcLfDIordhfo6DH8Q8ge35Mujygv93ks6YFzyOx9Z07+lhrre8sCwpffdGTJfW6w=

5. The format must be specified for the reveal command, it won't automatically detect it:

.. code-block:: bash

    cryptoolz keys reveal 1 <path to file with data> # will print to stdout
    cryptoolz keys reveal 2 <path to file with data> # 2 for the "2 2" case
    cryptoolz keys reveal 1 <path to file with data> -o <path to file you want pk written to>
    cryptoolz keys reveal 2 <path to file with data> -o <path to file you want pk written to>

7. The password for the above sample qrcode is "test" (you can just save it), it should print (or save) the following:

.. code-block:: text

    The decrypted private key (note it down!):

    d2eeaeaada730c9fa996635faa870c796b17fae2415522b6c473f61efddbbe80

8. Keep the device disconnected and save the key somewhere, either onto a USB, or into a KeepassXC database, a software wallet... Secure erase (data shredding) (or just erase) the plaintext data from the device.

9.  Reboot.

tl;dr be careful

crypto
======

.. code-block:: python

    from cryptoolz.crypto import SecretBytes
    from cryptoolz.crypto.circuits import EncryptPBDKF2_AESGCM, DecryptPBDKF2_AESGCM

    ecirc = EncryptPBDKF2_AESGCM(
        pbdkf2_passphrase=SecretBytes("Some passphrase.".encode('ascii')),
        aesgcm_plaintext=SecretBytes("Secret text.".encode('ascii'))
    )

    outs = ecirc()
    print(outs)

    dcirc = DecryptPBDKF2_AESGCM(
        pbdkf2_passphrase=SecretBytes("Some passphrase.".encode('ascii')),
        aesgcm_cyphertext=outs.aesgcm_cyphertext
    )

    print(dcirc().aesgcm_plaintext.get_secret_value())
