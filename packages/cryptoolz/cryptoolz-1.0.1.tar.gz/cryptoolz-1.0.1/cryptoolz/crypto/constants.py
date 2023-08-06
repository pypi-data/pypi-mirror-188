from typing import Callable

# FORMAT: { n: k }
# PRIME: 2**n - k
PRIMES_BITNUM_CLOSEST_LOWER = {
    64: 59,  # 0
    128: 159,  # 1
    256: 189,  # 2
    384: 317,  # 3
    512: 569,  # 4
}

# FORMAT: [p]
# PRIME: 2**p - 1
PRIMES_MERSENNE = [
    2,
    3,
    5,
    7,
    13,
    17,
    19,
    31,
    61,
    89,
    107,
    127,
    521,
    607,
    1279,
    2203,
    2281,
    3217,
    4253,
    4423,
    9689,
    9941,
    11213,
    19937,
]


class Primes:
    @staticmethod
    def get_closest_lower(bitnum: int):
        return 2**bitnum - PRIMES_BITNUM_CLOSEST_LOWER[bitnum]

    @staticmethod
    def get_mersenne(bitnum: int):
        if bitnum in PRIMES_MERSENNE:
            return 2**bitnum - 1
        else:
            raise ValueError(f"Primes.get_mersenne: 2^{bitnum} - 1 is not prime.")
