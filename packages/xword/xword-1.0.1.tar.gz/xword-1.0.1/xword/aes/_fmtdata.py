"""AES加解密 数据初始化"""
import re
import base64
from Crypto.Cipher import AES


# 目前支持的模式
MODES = {
    "ECB": 1,  "CBC": 2, "CFB": 3,
    "OFB": 5,  "CTR": 6, "OPENPGP": 7,
    "EAX": 9,  "CCM": 8, "SIV": 10,
    "GCM": 11, "OCB": 12}

# 块大小 - 16
BLOCK = AES.block_size

# key 长度区间
KEY_SIZE = AES.key_size

# base64 数据类型 正则表达式判断
B64_RE_PATTERN   = re.compile(r"^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$")
B64_RE_PATTERN_B = re.compile(rb"^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$")


def is_b64data(data: str or bytes) -> bool:
    """判断base64数据类型 return: bool"""
    if isinstance(data, bytes):
        return bool(B64_RE_PATTERN_B.match(data))

    if isinstance(data, str):
        return bool(B64_RE_PATTERN.match(data))

    #  str 或 bytes 以外类型返回 False
    return False


def tobytes_from_base64(data: str or bytes, encoding="UTF-8"):
    """
    base64数据类型 转化为bytes
    如果不为base64数据类型 则返回原始数据
    """
    if (
        not isinstance(data, (str, bytes))
        or not is_b64data(data)
    ):
        return False, data

    if isinstance(data, str):
        data = data.encode(encoding)

    return True, base64.b64decode(data)


class FormatData:
    """AES数据初始化"""

    def __init__(
        self, key, iv=None, mode="CBC", encode="UTF-8", **kwargs
    ):
        self._key  = key
        self._mode = mode
        self._iv   = iv
        self._encode = encode
        self._cipher = None
        self.__state = kwargs
        self.__initialization()


    def __initialization(self):
        """初始化 key mode iv"""
        self.__key_to_bytes()
        self.__mode_fmt()
        self.__iv_to_bytes()
        # self._create_cipher()


    def __key_to_bytes(self):
        """key 转换为 bytes"""
        key = self._key
        if isinstance(key, str):
            key = key.encode(self._encode)

        elif not isinstance(key, bytes):
            raise TypeError(
                "\033[31m'key' type must be 'str' or 'bytes',"
                f" not '{type(key).__name__}'\033[0m")

        # key 长度判断
        key_lenght = len(key)
        if key_lenght not in KEY_SIZE:
            raise ValueError(
                f"\033[31m'key' lenght must be {KEY_SIZE},"
                f" not '{key_lenght}'\033[0m")
        self._key = key
        return self


    def __mode_fmt(self):
        """mode 判断"""
        mode = self._mode
        if (
            isinstance(mode, str)
            and MODES.__contains__(mode.upper())
        ):
            mode = MODES[mode.upper()]

        if  (
            not isinstance(mode, int)
            or mode not in MODES.values()
        ):
            mode_val = list(MODES.keys())
            mode_val.extend(list(MODES.values()))
            raise TypeError(
                f"\033[31mmode must exist in the {mode_val},"
                f" not '{mode}'\033[0m")
        self._mode = mode
        return self


    def __iv_to_bytes(self):
        """iv 转换为 bytes"""
        if self._iv is None:
            if self._mode != MODES["CBC"]:
                return self
            self._iv = self._key[:16]

        iv = self._iv
        if isinstance(iv, str):
            iv = iv.encode(self._encode)

        elif not isinstance(iv, bytes):
            raise TypeError(
                "\033[31m'iv' type must be 'str' or 'bytes',"
                f" not '{type(iv).__name__}'\033[0m")

        # iv 长度判断
        iv_lenght = len(iv)
        if iv_lenght != BLOCK:
            raise ValueError(
                f"\033[31m'iv' lenght must be equal to '{BLOCK}'"
                f", not '{iv_lenght}'\033[0m")
        self._iv = iv
        return self


    def _create_cipher(self):
        """ 创建 cipher """
        state = self.__state.copy()
        state["key"]  = self._key
        state["mode"] = self._mode

        if self._iv is not None:
            state["iv"] = self._iv

        cipher = AES.new(**state)
        self._cipher = cipher
        return self


    @property
    def key(self):
        """key property"""
        return self._key

    @key.setter
    def key(self, value):
        self._key = value
        self.__initialization()

    @property
    def mode(self):
        """mode property"""
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = value
        self.__initialization()

    @property
    def iv(self):
        """iv property"""
        return self._iv

    @iv.setter
    def iv(self, value):
        self._iv = value
        self.__initialization()
