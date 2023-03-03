from enum import Enum


def build_binary(value: int) -> str:
    binary_int = bin(value).replace("0b", "")
    return f"{'0' * (8 - len(binary_int))}{binary_int}"


class Mask(Enum):
    MASK0: dict = {
        "bin": f"{'0' * 8}." * 3 + '0' * 8,
        "dec": "0.0.0.0"
    }
    MASK1: dict = {
        "bin": f"{build_binary(128)}" + f".{'0' * 8}" * 3,
        "dec": "128.0.0.0"
    }
    MASK2: dict = {
        "bin": f"{build_binary(192)}" + f".{'0' * 8}" * 3,
        "dec": "192.0.0.0"
    }
    MASK3: dict = {
        "bin": f"{build_binary(224)}" + f".{'0' * 8}" * 3,
        "dec": "224.0.0.0"
    }
    MASK4: dict = {
        "bin": f"{build_binary(240)}" + f".{'0' * 8}" * 3,
        "dec": "240.0.0.0"
    }
    MASK5: dict = {
        "bin": f"{build_binary(248)}" + f".{'0' * 8}" * 3,
        "dec": "248.0.0.0"
    }
    MASK6: dict = {
        "bin": f"{build_binary(252)}" + f".{'0' * 8}" * 3,
        "dec": "252.0.0.0"
    }
    MASK7: dict = {
        "bin": f"{build_binary(254)}" + f".{'0' * 8}" * 3,
        "dec": "254.0.0.0"
    }
    MASK8: dict = {
        "bin": f"{build_binary(255)}" + f".{'0' * 8}" * 3,
        "dec": "255.0.0.0"
    }
    MASK9: dict = {
        "bin": f"{build_binary(255)}.{build_binary(128)}" + f".{'0' * 8}" * 2,
        "dec": "255.128.0.0"
    }
    MASK10: dict = {
        "bin": f"{build_binary(255)}.{build_binary(192)}" + f".{'0' * 8}" * 2,
        "dec": "255.192.0.0"
    }
    MASK11: dict = {
        "bin": f"{build_binary(255)}.{build_binary(224)}" + f".{'0' * 8}" * 2,
        "dec": "255.224.0.0"
    }
    MASK12: dict = {
        "bin": f"{build_binary(255)}.{build_binary(240)}" + f".{'0' * 8}" * 2,
        "dec": "255.240.0.0"
    }
    MASK13: dict = {
        "bin": f"{build_binary(255)}.{build_binary(248)}" + f".{'0' * 8}" * 2,
        "dec": "255.248.0.0"
    }
    MASK14: dict = {
        "bin": f"{build_binary(255)}.{build_binary(252)}" + f".{'0' * 8}" * 2,
        "dec": "255.252.0.0"
    }
    MASK15: dict = {
        "bin": f"{build_binary(255)}.{build_binary(254)}" + f".{'0' * 8}" * 2,
        "dec": "255.254.0.0"
    }
    MASK16: dict = {
        "bin": f"{build_binary(255)}.{build_binary(255)}" + f".{'0' * 8}" * 2,
        "dec": "255.255.0.0"
    }
    MASK17: dict = {
        "bin": f"{build_binary(255)}." * 2 + f"{build_binary(128)}.{'0' * 8}",
        "dec": "255.255.128.0"
    }
    MASK18: dict = {
        "bin": f"{build_binary(255)}." * 2 + f"{build_binary(192)}.{'0' * 8}",
        "dec": "255.255.192.0"
    }
    MASK19: dict = {
        "bin": f"{build_binary(255)}." * 2 + f"{build_binary(224)}.{'0' * 8}",
        "dec": "255.255.224.0"
    }
    MASK20: dict = {
        "bin": f"{build_binary(255)}." * 2 + f"{build_binary(240)}.{'0' * 8}",
        "dec": "255.255.240.0"
    },
    MASK21: dict = {
        "bin": f"{build_binary(255)}." * 2 + f"{build_binary(248)}.{'0' * 8}",
        "dec": "255.255.248.0"
    },
    MASK22: dict = {
        "bin": f"{build_binary(255)}." * 2 + f"{build_binary(252)}.{'0' * 8}",
        "dec": "255.255.252.0"
    },
    MASK23: dict = {
        "bin": f"{build_binary(255)}." * 2 + f"{build_binary(254)}.{'0' * 8}",
        "dec": "255.255.254.0"
    },
    MASK24: dict = {
        "bin": f"{build_binary(255)}." * 3 + f"{'0' * 8}",
        "dec": "255.255.225.0"
    },
    MASK25: dict = {
        "bin": f"{build_binary(255)}." * 3 + f"{build_binary(128)}",
        "dec": "255.255.225.128"
    },
    MASK26: dict = {
        "bin": f"{build_binary(255)}." * 3 + f"{build_binary(192)}",
        "dec": "255.255.255.192"
    },
    MASK27: dict = {
        "bin": f"{build_binary(255)}." * 3 + f"{build_binary(224)}",
        "dec": "255.255.255.224"
    },
    MASK28: dict = {
        "bin": f"{build_binary(255)}." * 3 + f"{build_binary(240)}",
        "dec": "255.255.255.240"
    },
    MASK29: dict = {
        "bin": f"{build_binary(255)}." * 3 + f"{build_binary(248)}",
        "dec": "255.255.255.248"
    },
    MASK30: dict = {
        "bin": f"{build_binary(255)}." * 3 + f"{build_binary(252)}",
        "dec": "255.255.255.252"
    },
    MASK31: dict = {
        "bin": f"{build_binary(255)}." * 3 + f"{build_binary(254)}",
        "dec": "255.255.225.254"
    },
    MASK32: dict = {
        "bin": ".".join([build_binary(255) for i in range(0, 4)]),
        "dec": "255.255.255.255"
    }


if __name__ == "__main__":
    print(Mask.MASK2.value)
