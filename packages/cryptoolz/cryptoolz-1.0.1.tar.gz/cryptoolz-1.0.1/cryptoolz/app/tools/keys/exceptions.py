from cryptoolz.crypto.exceptions import WrongDecryptionInputs


def reveal_exception_handler(e: Exception) -> None:
    if isinstance(e, WrongDecryptionInputs):
        print("Decryption unsuccessful! Either the passphrase or settings are wrong!")
        exit(1)
    else:
        raise e


def default_exception_handler(e: Exception) -> None:
    raise e
