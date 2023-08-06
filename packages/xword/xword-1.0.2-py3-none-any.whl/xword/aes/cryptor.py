"""AES 加解密"""
from xword.aes._fmtdata import (
    BLOCK,
    FormatData,
    is_b64data,
    tobytes_from_base64
)



def no_padding(data, remove=False, pad=b"\x00"):
    """NoPadding填充模式"""
    # 消除 padding 字符
    if remove:
        return data.rstrip(pad)
    remainder = len(data) % BLOCK or BLOCK
    data += pad * (BLOCK - remainder)
    return data


def zero_padding(data, remove=False, pad=b"\x00"):
    """ZeroPadding填充模式"""
    # 消除 padding 字符
    if remove:
        return data.rstrip(pad)
    remainder = len(data) % BLOCK
    # 不填充
    data += pad * (BLOCK - remainder)
    return data


DEFAULT_PADDING = {
    "NoPadding"    : no_padding,
    "ZeroPadding"  : zero_padding,
    None : lambda data, *args, **kwagrs: data}


class AESCryptor(FormatData):
    """AES加解密"""

    def __init__(
        self, *args, padding="NoPadding", **kwargs
    ):
        self._padding = padding
        self.__padding_fmt()
        super().__init__(*args, **kwargs)


    def __padding_fmt(self, default=None):
        """加解密数据的填充方式"""
        padding = self._padding
        if (
            not (isinstance(padding, str) or padding is None)
            or padding not in DEFAULT_PADDING
        ):
            # 设置padding时, 若不存在使用默认值
            if default in DEFAULT_PADDING:
                self._padding = default
                return self

            raise ValueError(
                f"\033[31m'padding' must exist in the {list(DEFAULT_PADDING.keys())},"
                f" not '{padding}'\033[0m")
        return self


    @property
    def padding(self):
        """padding property"""
        return self._padding


    @padding.setter
    def padding(self, value):
        self._padding = value
        self.__padding_fmt("NoPadding")


    def encrypt(self, plaintext):
        """加密"""
        padding = DEFAULT_PADDING[self._padding]

        if isinstance(plaintext, str):
            plaintext = plaintext.encode(self._encode)
        elif not isinstance(plaintext, bytes):
            raise TypeError(
                "\033[31m'plaintext' type must be 'str' or 'bytes',"
                f" not '{type(plaintext).__name__}'\033[0m")

        # 创建 cipher , 加密
        self._create_cipher()
        plaintext = padding(plaintext)
        return self._cipher.encrypt(plaintext)


    def decrypt(self, ciphertext):
        """解密"""
        padding = DEFAULT_PADDING[self._padding]

        if isinstance(ciphertext, str):
            ciphertext = ciphertext.encode(self._encode)
        elif not isinstance(ciphertext, bytes):
            raise TypeError(
                "\033[31m'plaintext' type must be 'str' or 'bytes',"
                f" not '{type(ciphertext).__name__}'\033[0m")

        # 创建 cipher , 解密
        self._create_cipher()
        plaintext = self._cipher.decrypt(ciphertext)
        plaintext = padding(plaintext, True)
        return plaintext
