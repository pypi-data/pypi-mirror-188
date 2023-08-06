"""Main Module."""

# Abstract base class logic implementor module
import abc

# Some types we need for type hints
from typing import Any, Optional, NamedTuple, List

# To get a safe random hex str for the private key
from secrets import token_hex

# To assign plaintext with Secrets immediately
from pydantic import SecretBytes, BaseModel

# Wanted to collapse execution logic into some pattern,
# but went too far (and it's also ugly), need to instead read through stuff
# below again, and make this nicer, it was essentially just
# addiction driving the abstractions imported below.
# It works though.
from cryptoolz.base import Checkpoint, Checkpointed

# For predicates for above
from operator import gt

# Cryptograhic circuits and data models which hold our input and output data which are transformed later on
from cryptoolz.crypto.circuits import (
    EncryptPBDKF2_AESGCM,
    DecryptPBDKF2_AESGCM,
    OutsEncryptAESGCM,
    OutsDecryptAESGCM,
)

# For private to public key calc (gives same results as piper's eth_account.Account.from_key)
from eth_hash.auto import keccak
from coincurve import PublicKey
from eth_utils.address import to_checksum_address as checksum

# For (file)path type vars
from pathlib import Path

# Object which formats and sends output to either file or stdout
from cryptoolz.printer import Printer, PEMWriter, QRCodeWriter, HexWriter, PlainWriter

# An instance factory
from cryptoolz.factory import Factory

# The exception handlers for the factory
from .exceptions import default_exception_handler, reveal_exception_handler

# For picking values out from below
from cryptoolz.utils import match_value, match_values

# The following are basically configs for this module and
# also input data which is ugly when inlined

# Circuits for mode for algorithm keyword

CIRCUIT_TYPES = {
    "CREATE": {
        "AESGCM": EncryptPBDKF2_AESGCM,
    },
    "REVEAL": {
        "AESGCM": DecryptPBDKF2_AESGCM,
    },
}

# Circuit arg identifiers for mode for algorithm keyword

CIRCUIT_ARGS = {
    "CREATE": {
        "AESGCM": [
            "pbdkf2_passphrase",
            "aesgcm_plaintext",
        ]
    },
    "REVEAL": {
        "AESGCM": [
            "pbdkf2_passphrase",
            "aesgcm_cyphertext",
        ]
    },
}

# Dict key for output identifier for mode for circuit

CIRCUIT_OUTPUT_KEY = {
    "CREATE": {"AESGCM": "aesgcm_cyphertext"},
    "REVEAL": {"AESGCM": "aesgcm_plaintext"},
}

# Format we print the data with (needs editing or removal)

PRINT_FORMATS = {
    "CREATE": {
        "AESGCM": {
            "PEM": [
                [
                    "\nYour Ethereum Public Key:\n\n{}\n",
                    "The encrypted private key block:\n\n{}\n",
                ],
                [
                    "\nYour Ethereum Public Key:\n\n{}\n",
                    "Private key digest:\n\n{}\n",
                    "The encrypted private key block:\n\n{}\n",
                ],
            ],
            "QR": [
                ["\nYour Ethereum Public Key:\n\n{}\n"],
                ["\nYour Ethereum Public Key:\n\n{}\n", "PrivateKeyDigest:\n\n{}\n"],
            ],
        }
    },
    "REVEAL": {
        "AESGCM": {
            "PEM": [["\nThe decrypted private key (note it down!):\n\n{}\n"]],
            "QR": [["\nThe decrypted private key (note it down!):\n\n{}\n"]],
        }
    },
}  # TODO: steganography

PRINT_WRITERS = {
    "CREATE": {
        "AESGCM": {
            "PEM": PEMWriter,
            "QR": QRCodeWriter,
            "HEX": HexWriter,
            "PLAIN": PlainWriter,
        },
    },
    "REVEAL": {
        "AESGCM": {
            "PEM": PEMWriter,
            "QR": QRCodeWriter,
            "HEX": HexWriter,
            "PLAIN": PlainWriter,
        }
    },
}

# Created factory types

EthKeyEncryptor = Factory[OutsEncryptAESGCM]

EthKeyDecryptor = Factory[OutsDecryptAESGCM]

# Mapping for them

FACTORY_TYPES = {
    "CREATE": {"ETHEREUM": EthKeyEncryptor},
    "REVEAL": {"ETHEREUM": EthKeyDecryptor},
}

FACTORY_EXCEPTION_HANDLERS = {
    "CREATE": default_exception_handler,
    "REVEAL": reveal_exception_handler,
}

# Classes and logic


class KeysOptions:
    get: bool
    mode: str
    outpath: Path
    algorithm: str
    network: str
    digest: bool
    format: str
    header: str
    keynum: int

    def __init__(self, **options):
        _mode = options.get("mode")
        _algorithm = options.get("algorithm")
        _network = options.get("network")
        _format = options.get("format")
        _header = options.get("header")

        self.get = options.get("_get") or False
        self.mode = _mode and _mode.upper()
        self.outpath = options.get("outpath")
        self.algorithm = _algorithm and _algorithm.upper()
        self.network = _network and _network.upper()
        self.digest = options.get("digest")
        self.format = _format and _format.upper()
        self.header = _header and _header.upper()
        self.keynum = options.get("keynum")


class Keypair(BaseModel, abc.ABC):
    private_key: SecretBytes
    private_key_digest: Optional[bytes] = None
    public_key: str

    def __init__(self, hash_fn: Any = None, **kwargs):
        private_key = self.gen_private_key()

        private_key_digest = None

        if hash_fn:
            private_key_digest = self.calc_private_key_digest(private_key, hash_fn)

        public_key = self.calc_public_key(private_key)

        super().__init__(
            private_key=private_key,
            private_key_digest=private_key_digest,
            public_key=public_key,
        )

    @abc.abstractmethod
    def calc_public_key(self, private_key: SecretBytes) -> None:
        pass

    @abc.abstractmethod
    def gen_private_key(self) -> SecretBytes:
        pass

    def calc_private_key_digest(
        self, private_key: SecretBytes, hash_fn: Any
    ) -> Optional[bytes]:
        return None


class EthKeypair(Keypair):  # TODO: pk digest, trash eth_hash
    def calc_public_key(self, private_key: SecretBytes) -> str:
        if private_key is None:
            return None

        hex_addr = PublicKey.from_valid_secret(private_key.get_secret_value()).format(
            compressed=False
        )[1:]

        return str(checksum(keccak(hex_addr)[-20:].hex()))

    def gen_private_key(self) -> SecretBytes:
        return SecretBytes(bytes.fromhex(token_hex(32)))


class FactoryCheckpoint(Checkpoint):
    def __init__(self, index: int):
        super().__init__(index)

    def _logic(self, options: KeysOptions) -> Factory:
        FactoryType = match_values([options.mode, options.network], FACTORY_TYPES)
        ConstructorType = match_values([options.mode, options.algorithm], CIRCUIT_TYPES)
        exception_handler = match_value(options.mode, FACTORY_EXCEPTION_HANDLERS)

        return FactoryType(ConstructorType(), exception_handler)


class PrinterCheckpoint(Checkpoint):
    def _logic(self, options: KeysOptions) -> Printer:
        return Printer[
            match_values(
                [options.mode, options.algorithm, options.format], PRINT_WRITERS
            )
        ]()


class KeypairCheckpoint(Checkpoint):
    def _logic(self, options: KeysOptions) -> List[Keypair]:
        KeypairType = match_value(
            options.network,
            {
                "ETHEREUM": EthKeypair,
            },
        )
        return [KeypairType() for _ in range(0, options.keynum)]


class AbstractRunCheckpoint(Checkpoint):
    class RunVars(NamedTuple):
        key: Any
        input_names: List[str]
        formats: List[str]

    def _get_run_vars(
        self,
        options: KeysOptions,
    ) -> RunVars:
        input_names = match_values([options.mode, options.algorithm], CIRCUIT_ARGS)

        key = match_values([options.mode, options.algorithm], CIRCUIT_OUTPUT_KEY)

        formats = match_values(
            [options.mode, options.algorithm, options.format], PRINT_FORMATS
        )

        return AbstractRunCheckpoint.RunVars(key, input_names, formats)


class AbstractCryptoHandler(Checkpointed, abc.ABC):
    _factory: FactoryCheckpoint = FactoryCheckpoint(1)
    _printer: PrinterCheckpoint = PrinterCheckpoint(2)

    def __init__(self):
        super().__init__(lambda a, b: gt(a, b) or a == 0)

    @Checkpointed.EnforceCallOrder("_factory")
    def factory(self, options: KeysOptions) -> Factory:
        return self._factory(options)

    @Checkpointed.EnforceCallOrder("_printer")
    def printer(self, options: KeysOptions) -> Printer:
        return self._printer(options)

    @abc.abstractmethod
    def inputs(self, *args, **kwargs) -> Any:
        pass

    @abc.abstractmethod
    def run(self, *args, **kwargs) -> None:
        pass


class CreateHandler(AbstractCryptoHandler):
    class RunCheckpoint(AbstractRunCheckpoint):
        def _logic(
            self,
            options: KeysOptions,
            passphrases: List[SecretBytes],
            keypairs: List[Keypair],
            factory: Factory,
            printer: Printer,
        ) -> None:
            run_vars = self._get_run_vars(options)

            has_digest: bool = False

            if keypairs[0].private_key_digest:
                has_digest = True

            if options.format == "PEM":
                printer.writer.set_format([options.header] * 2)

            for i in range(options.keynum):
                factory.put(
                    {
                        run_vars.input_names[0]: passphrases[i],
                        run_vars.input_names[1]: keypairs[i].private_key,
                    }
                )

                arguments = []

                format_index = 0

                cyphertext = getattr(factory.create(), run_vars.key)

                arguments.append(keypairs[i].public_key)

                if has_digest:
                    format_index = 1
                    arguments.append(keypairs[i].private_key_digest)

                if options.format == "PEM":
                    arguments.append(printer.writer.encode(cyphertext))

                elif options.format == "QR":
                    printer.put(cyphertext, encode=True)

                printer.put(
                    [
                        run_vars.formats[format_index][i].format(arguments[i])
                        for i in range(len(run_vars.formats[format_index]))
                    ]
                )

    _keypairs: KeypairCheckpoint = KeypairCheckpoint(3)
    _run: RunCheckpoint = RunCheckpoint(0)

    def __init__(self):
        super().__init__()

    @Checkpointed.EnforceCallOrder("_keypairs")
    def inputs(self, options: KeysOptions, *args) -> List[Keypair]:
        return self._keypairs(options)

    @Checkpointed.EnforceCallOrder("_run")
    def run(
        self,
        options: KeysOptions,
        passphrases: List[SecretBytes],
        keypairs: List[Keypair],
        factory: Factory,
        printer: Printer,
    ) -> None:
        self._run(
            options,
            passphrases,
            keypairs,
            factory,
            printer,
        )


class CyphertextCheckpoint(Checkpoint):
    def _logic(self, options: KeysOptions, cyphertexts: List[str]) -> List[bytes]:
        get_encoder = match_values(
            [options.mode, options.algorithm, options.format], PRINT_WRITERS
        )

        encoder = get_encoder()

        if options.format == "PEM":
            encoder.set_format([options.header] * 2)

        return [encoder.decode(cyphertext) for cyphertext in cyphertexts]


class RevealHandler(AbstractCryptoHandler):
    class RunCheckpoint(AbstractRunCheckpoint):
        def _logic(
            self,
            options: KeysOptions,
            passphrases: List[SecretBytes],
            cyphertexts: List[bytes],
            factory: Factory,
            printer: Printer,
        ) -> None:
            run_vars = self._get_run_vars(options)

            for i in range(options.keynum):
                factory.put(
                    {
                        run_vars.input_names[0]: passphrases[i],
                        run_vars.input_names[1]: cyphertexts[i],
                    }
                )

                arguments = []

                format_index = 0

                plaintext = getattr(factory.create(), run_vars.key)

                if options.algorithm == "AESGCM":
                    plaintext = plaintext.get_secret_value().hex()

                arguments.append(plaintext)

                printer.put(
                    [
                        run_vars.formats[format_index][i].format(arguments[i])
                        for i in range(len(run_vars.formats[format_index]))
                    ]
                )

    _cyphertexts: CyphertextCheckpoint = CyphertextCheckpoint(3)
    _run: RunCheckpoint = RunCheckpoint(0)

    def __init__(self):
        super().__init__()

    @Checkpointed.EnforceCallOrder("_cyphertexts")
    def inputs(self, options: KeysOptions, cyphertexts: List[str]) -> List[bytes]:
        return self._cyphertexts(options, cyphertexts)

    @Checkpointed.EnforceCallOrder("_run")
    def run(
        self,
        options: KeysOptions,
        passphrases: List[SecretBytes],
        cyphertexts: List[bytes],
        factory: Factory,
        printer: Printer,
    ) -> None:
        self._run(
            options,
            passphrases,
            cyphertexts,
            factory,
            printer,
        )


class Keys:
    options: KeysOptions

    def __init__(self, **run_options):
        self.options = KeysOptions(**run_options)

    def run(self, run_args: List[Any]) -> Any:
        if not self.options.mode:
            raise ValueError("keys.run: No command to run picked!")

        n_passphrases = len(run_args[0])

        single_passphrase = n_passphrases == 1

        if self.options.keynum:
            if not single_passphrase and self.options.keynum != n_passphrases:
                raise ValueError(
                    "keys.run: Either create one key for one passphrase or all keys with one passphrase!"
                )
        else:
            self.options.keynum = n_passphrases

        if single_passphrase:
            single_pass_value = run_args[0][0]

            for _ in range(1, self.options.keynum):
                run_args[0].append(single_pass_value)

        # instances

        checkpoints = None

        mode = self.options.mode

        if mode == "CREATE":
            checkpoints = CreateHandler()
        elif mode == "REVEAL":
            checkpoints = RevealHandler()

        if not checkpoints:
            raise ValueError(f"keys.run: mode {mode} does not exist!")

        factory = checkpoints.factory(self.options)

        printer = checkpoints.printer(self.options)

        inputs = checkpoints.inputs(self.options, run_args[-1])

        if not factory.empty():
            raise ValueError("keys.run: factory is not empty")

        checkpoints.run(self.options, run_args[0], inputs, factory, printer)

        if self.options.get:
            results = []

            while not printer.empty():
                results.append(printer.get())

            return results
        else:
            printer.print(po=self.options.outpath)

        return None
