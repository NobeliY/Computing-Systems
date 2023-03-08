import string

from mask import Mask, build_binary


class Singleton(object):
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = object.__new__(cls)
        return cls._instances[cls]


class MyIP(Singleton):

    def __init__(self, uname: str):
        self._string_ip_address = None
        self._ip_address = None
        self._raw_ip_address = None
        self._ip_address_binary = None
        self._str_binary = None
        self._raw_str_binary = None

        self._cached_: dict = {}

        if uname:
            self.uname = list(uname.lower()[:7])
        else:
            raise ValueError("uname is empty")
        self.load()

    def load(self):
        self._u_code()
        self._bytes_array()
        self.str_binary()
        self.split_ip_address()
        self.load_properties()

    def load_properties(self):
        _ = [
            self.prefix,
            self.mask,
            self.wildcard,
            self.network,
            self.gateway,
            self.hosts
        ]

    @property
    def gateway(self) -> dict:
        _gateway = self._cached_.get("gateway")
        if not _gateway:
            self.gateway = self.network["raw"]
        return self._cached_["gateway"]

    @gateway.setter
    def gateway(self, raw_network: list[int]):
        _raw_gateway = raw_network
        _raw_gateway[-1] += 1
        _binary_gateway = ".".join(map(str, [build_binary(item) for item in _raw_gateway]))
        _gateway = ".".join(map(str, _raw_gateway))
        self._cached_["gateway"]: dict = {
            "bin": _binary_gateway,
            "dec": _gateway,
            "raw": _raw_gateway
        }
        del _binary_gateway, _gateway, _raw_gateway

    @property
    def hosts(self) -> dict:
        _hosts = self._cached_.get("hosts")
        if not _hosts:
            self.hosts = self.prefix
        return self._cached_["hosts"]

    @hosts.setter
    def hosts(self, prefix: int):
        __host_min = self.gateway["raw"]
        __host_min[-1] += 1
        __broadcast = [self.network["raw"][i] + self.wildcard["dec"][i] for i in range(0, 4)]
        __broadcast[-1] -= 1
        __host_max = [
            item if __broadcast.index(item) != 3 else item - 1
            for item in __broadcast
        ]
        self._cached_["hosts"]: dict = {
            "count": 2 ** (32 - prefix) - 2,
            "min": {
                "bin": ".".join(map(str, [build_binary(item) for item in __host_min])),
                "dec": __host_min.__str__()[1:-1].replace(', ', '.')
            },
            "max": {
                "bin": ".".join(map(str, [build_binary(item) for item in __host_max])),
                "dec": __host_max.__str__()[1:-1].replace(', ', '.')
            }
        }
        self._cached_["broadcast"] = {
            "bin": ".".join(map(str, [build_binary(item) for item in __broadcast])),
            "dec": __broadcast.__str__()[1:-1].replace(', ', '.')
        }
        del __host_max, __host_min

    @property
    def mask(self) -> dict:
        _mask = self._cached_.get("mask")
        if not _mask:
            self.mask = self.prefix
        return self._cached_["mask"]

    @mask.setter
    def mask(self, prefix: int):
        __mask_tuple__ = Mask.__getitem__(f"MASK{prefix}").value
        try:
            __mask__ = __mask_tuple__[-1]
        except KeyError:
            __mask__ = __mask_tuple__
        self._cached_["mask"]: dict = {
            "dec": __mask__["dec"],
            "split_mask": list(map(int, __mask__["bin"].split(".")))
        }

    @property
    def network(self) -> dict:
        _network = self._cached_.get("network")
        if not _network:
            self.network = str(self.mask["dec"]).split(".")
        return self._cached_["network"]

    @network.setter
    def network(self, mask_binary):
        raw_network: list[list] = []
        for i in range(0, len(self._ip_address_binary)):
            raw_network.append([])
            mask_binary_item = bin(int(mask_binary[i])).replace("0b", "")
            mask_binary_parsed = f"{'0' * (8 - len(mask_binary_item))}{mask_binary_item}"
            for j in range(0, len(self._ip_address_binary[i])):
                raw_network[i].append(str(int(self._ip_address_binary[i][j]) * int(mask_binary_parsed[j])))
        network: list[int] = []
        binary_network: list = []
        for item in raw_network:
            binary_network.append("".join(item))
            network.append(int(binary_network[-1], 2))
        self._cached_["network"]: dict = {
            "raw": network,
            "bin": ".".join(binary_network),
            "dec": ".".join(map(str, network))
        }
        del binary_network, raw_network, network

    @property
    def prefix(self) -> int:
        _prefix = self._cached_.get("prefix")
        if not _prefix:
            self.prefix = self._raw_str_binary
        del _prefix
        return self._cached_["prefix"]

    @prefix.setter
    def prefix(self, raw_str_binary: str):
        self._cached_["prefix"] = int(raw_str_binary[-3:], 2) + 19 if raw_str_binary else 19

    @property
    def wildcard(self) -> dict:
        _wildcard = self._cached_.get("wildcard")
        if not _wildcard:
            self.wildcard = list(map(int, self.mask["dec"].split(".")))
        return self._cached_["wildcard"]

    @wildcard.setter
    def wildcard(self, split_mask: list[int]):
        self._cached_["wildcard"]: dict = {
            "dec": [255 - item for item in split_mask]
        }
        self._cached_["wildcard"]["bin"]: str = ".".join([build_binary(item)
                                                          for item in self._cached_["wildcard"]["dec"]])

    def return_u_code(self):
        return self._index_list

    def return_bytes_array(self):
        return self._binary_list

    def return_str_binary(self):
        return self._str_binary

    def return_ip_address(self):
        return self._ip_address

    def _u_code(self):
        self._index_list: list[int] = [string.ascii_lowercase.index(item) + 1 for item in self.uname]

    def _bytes_array(self):
        binary_list: list = [bin(item).replace("0b", "") for item in self._index_list]
        self._binary_list: list = [
            f"{'0' * (5 - len(binary_list[i]))}{binary_list[i]}" for i in range(0, len(binary_list))
        ]
        return self._binary_list

    def str_binary(self):
        self._raw_str_binary = "".join(self._binary_list)
        self._str_binary = self._raw_str_binary[:-3]

    def split_ip_address(self):
        n = 8
        self._ip_address_binary = [self._str_binary[i:i + n] for i in range(0, len(self._str_binary), n)]
        self._raw_ip_address = ".".join(self._ip_address_binary)
        self._ip_address = [int(item, 2) for item in self._ip_address_binary]
        self._string_ip_address = str(self._ip_address)[1:-1].replace(", ", ".")

    def get_class_ip(self) -> str:
        if self._ip_address[0] < 128:
            classes = "A"
        elif 128 <= self._ip_address[0] < 192:
            classes = "B"
        else:
            classes = "C"
        return classes

    def __str__(self):
        return f"a: Address: {self._string_ip_address} | {self._raw_ip_address}\n" \
               f"b: Class: {self.get_class_ip()} | Prefix: {self.prefix}\n" \
               f"c: Mask: {self.mask['dec']} | {'.'.join(map(str, self.mask['split_mask']))}\n" \
               f"d: WildCard: {self.wildcard['dec'].__str__()[1:-1].replace(', ', '.')} | {self.wildcard['bin']}\n" \
               f"e: Hosts: {self.hosts['count']}\n" \
               f"f: Network: {self.network['dec']} | {self.network['bin']}\n" \
               f"g: Gateway: {self.gateway['dec']} | {self.gateway['bin']}\n" \
               f"h: HostMin: {self.hosts['min']['dec']} | {self.hosts['min']['bin']} \n" \
               f"i: HostMax: {self.hosts['max']['dec']} | {self.hosts['max']['bin']}\n" \
               f"j: Broadcast: {self._cached_['broadcast']['dec']} | {self._cached_['broadcast']['bin']}"


if __name__ == "__main__":
    Gil_IP = MyIP(uname="GilmetdinovInsaf")
    print(Gil_IP)
    print("\nUst\n")
    Ust_IP = MyIP(uname="UstyuzhaninKirill")
    print(Ust_IP)
