import string
from typing import Union

from src.mask import Mask, build_binary


class Singleton(object):
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = object.__new__(cls)
        return cls._instances[cls]


class MyIP(Singleton):

    def __init__(self, uname: str):

        self._binary_gateway: str = ""
        self.__binary_network = None
        self._binary_wildcard = None
        self._broadcast: Union[dict[str], None] = None
        self._hosts: dict = {}
        self.__raw_gateway: list[int] = []
        self.__raw_network: list[int] = []
        self._gateway = None
        self._ip_address_binary = None
        self._network = None
        self._mask = None
        self._split_mask: list[int] = []
        self._wildcard: list[int] = []
        self._string_ip_address = None
        self._raw_ip_address = None
        self._ip_address = None
        self._raw_str_binary = None
        self._prefix: int = -1
        self._str_binary = None
        self._binary_list = None
        self._index_list = None
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
    def gateway(self):
        if not self._gateway:
            self.gateway = self.__raw_network
        return self._gateway

    @gateway.setter
    def gateway(self, raw_network: list[int]):
        if not self.__raw_network:
            self.network = str(self.mask.netmask).split(".")
        self.__raw_gateway = raw_network
        self.__raw_gateway[-1] += 1
        self._binary_gateway = ".".join(map(str, [build_binary(item) for item in self.__raw_gateway]))
        self._gateway = ".".join(map(str, self.__raw_gateway))

    @property
    def hosts(self):
        if not self._hosts:
            self.hosts = self.prefix
        return self._hosts["count"]

    @hosts.setter
    def hosts(self, prefix: int):
        __host_min = list(map(int, self.gateway.split(".")))
        __host_min[-1] += 1
        __broadcast = [self.__raw_network[i] + self._wildcard[i] for i in range(0, 4)]
        __broadcast[-1] -= 1
        __host_max = [
            item if __broadcast.index(item) != 3 else item - 1
            for item in __broadcast
        ]
        self._hosts: dict = {
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
        self._broadcast = {
            "bin": ".".join(map(str, [build_binary(item) for item in __broadcast])),
            "dec": __broadcast.__str__()[1:-1].replace(', ', '.')
        }
        del __host_max, __host_min

    @property
    def mask(self):
        if not self._mask:
            self.mask = self.prefix
        return self._mask

    @mask.setter
    def mask(self, prefix: int):
        __mask_tuple__ = Mask.__getitem__(f"MASK{prefix}").value
        try:
            __mask__ = __mask_tuple__[-1]
        except KeyError:
            __mask__ = __mask_tuple__
        self._mask = __mask__["dec"]
        self._split_mask = list(map(int, __mask__["bin"].split(".")))

    @property
    def network(self):
        if not self._network:
            self.network = str(self.mask).split(".")
        return self._network

    @network.setter
    def network(self, mask_binary):
        raw_network: list[list] = []
        for i in range(0, len(self._ip_address_binary)):
            raw_network.append([])
            mask_binary_item = bin(int(mask_binary[i])).replace("0b", "")
            mask_binary_parsed = f"{'0' * (8 - len(mask_binary_item))}{mask_binary_item}"
            for j in range(0, len(self._ip_address_binary[i])):
                raw_network[i].append(str(int(self._ip_address_binary[i][j]) * int(mask_binary_parsed[j])))
        network: list = []
        binary_network: list = []
        for item in raw_network:
            binary_network.append("".join(item))
            network.append(int(binary_network[-1], 2))
        self.__raw_network = network
        self.__binary_network = ".".join(binary_network)
        self._network = ".".join(map(str, network))
        del binary_network, raw_network, network

    @property
    def prefix(self):
        if self._prefix == -1:
            self.prefix = self._raw_str_binary
        return self._prefix

    @prefix.setter
    def prefix(self, raw_str_binary: str):
        if raw_str_binary:
            self._prefix = int(raw_str_binary[-3:], 2) + 19
        else:
            self._prefix = 19

    @property
    def wildcard(self):
        if not self._wildcard:
            self.wildcard = list(map(int, self.mask.split(".")))
        return self._wildcard

    @wildcard.setter
    def wildcard(self, split_mask: list[int]):
        self._wildcard = [255 - item for item in split_mask]
        self._binary_wildcard: str = ".".join([build_binary(item) for item in self._wildcard])

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
               f"c: Mask: {self.mask} | {'.'.join(map(str, self._split_mask))}\n" \
               f"d: WildCard: {self.wildcard.__str__()[1:-1].replace(', ', '.')} | {self._binary_wildcard}\n" \
               f"e: Hosts: {self.hosts}\n" \
               f"f: Network: {self.network} | {self.__binary_network}\n" \
               f"g: Gateway: {self.gateway} | {self._binary_gateway}\n" \
               f"h: HostMin: {self._hosts['min']['dec']} | {self._hosts['min']['bin']} \n" \
               f"i: HostMax: {self._hosts['max']['dec']} | {self._hosts['max']['bin']}\n" \
               f"j: Broadcast: {self._broadcast['dec']} | {self._broadcast['bin']}"


if __name__ == "__main__":
    Gil_IP = MyIP(uname="GilmetdinovInsaf")
    print(Gil_IP)
    print("\nUst\n")
    Ust_IP = MyIP(uname="UstyuzhaninKirill")
    print(Ust_IP)
