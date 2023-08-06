"""实现 httpclient 基类封装"""
from .export import CIMultiDict, URL
from .utils import default_headers



class BaseSesssion:
    """
    pip install requests
    对 requests 封装基类
    """

    # 默认超时时间
    DEFAULT_TIMEOUT = 7
    # DEFAULT_LIMIT   = 64

    def __init__(
        self,
        base_url: str or URL=None,
        headers: dict or CIMultiDict=None,
        timeout: int or float=None,
        verify: bool=True,
    ):
        self._base_url = base_url
        self._headers  = headers
        self._timeout  = timeout
        self._verify   = bool(verify)
        # self._limit    = limit
        self.__initialization_attr()


    def __initialization_attr(self):
        self.__init_base_url()
        self.__init_headers()
        self.__init_timeout()
        # self.__init_limit()


    def __init_base_url(self):
        base_url = getattr(self, "_base_url", None)
        if not base_url:
            self._base_url = None
            return

        # base_url 格式错误
        if not isinstance(base_url, (str, URL)):
            raise TypeError(
                "\033[31m'base_url' type must be a 'str' or 'URL', "
                f"not '{type(base_url).__name__}'\033[0m")

        # 只有绝对路径 url 才能是base_url
        base_url = URL(str(base_url))
        if base_url.is_absolute():
            setattr(self, "_base_url", base_url)
        else:
            setattr(self, "_base_url", None)


    def __init_headers(self, overwrite=False):
        raw_headers = default_headers() if not overwrite else CIMultiDict()
        headers = getattr(self, "_headers", None)
        if headers:
            headers = CIMultiDict(headers)
        else:
            headers = CIMultiDict()
        raw_headers.update(headers)
        setattr(self, "_headers", raw_headers)


    def __init_timeout(self):
        timeout = getattr(self, "_timeout", self.DEFAULT_TIMEOUT)
        if (
            not isinstance(timeout, (int, float))
            or timeout <= 0
        ):
            timeout = self.DEFAULT_TIMEOUT
        # self._timeout = timeout
        setattr(self, "_timeout", timeout)


    def __init_limit(self):
        limit = getattr(self, "_limit", self.DEFAULT_LIMIT)
        if (
            not isinstance(limit, int)
            or limit <= 0
        ):
            limit = self.DEFAULT_LIMIT
        # self._limit = limit
        setattr(self, "_limit", limit)


    def build_url(
        self, url: str or URL, raw: bool=False
    ) -> str or URL:
        """
        构建完整 url, base_url=None 将抛出错误
        raw=True 返回字符串
        """
        if isinstance(url, str):
            url = URL(url)

        elif not isinstance(url, URL):
            raise TypeError(
                "\033[31m'url' type must be a 'str' or 'URL', "
                f"not '{type(url).__name__}'\033[0m"
            )

        if not url.is_absolute():
            if self.base_url is None:
                raise ValueError(f"\033[31murl '{url}' not absolute\033[0m")
            url = self._base_url.join(url)
        # 原生数据
        if raw:
            url = str(url)
        return url


    @property
    def base_url(self):
        if not hasattr(self, "_base_url"):
            setattr(self, "_base_url", None)
        base_url = getattr(self, "_base_url")
        if base_url:
            base_url = str(base_url)
        return base_url

    @base_url.setter
    def base_url(self, value):
        setattr(self, "_base_url", value)
        self.__init_base_url()

    @property
    def headers(self):
        if not hasattr(self, "_headers"):
            setattr(self, "_headers", CIMultiDict())
        return getattr(self, "_headers")

    @headers.setter
    def headers(self, value):
        setattr(self, "_headers", value)
        self.__init_headers(overwrite=True)

    @property
    def timeout(self):
        if not hasattr(self, "_timeout"):
            setattr(self, "_timeout", self.DEFAULT_TIMEOUT)
        return getattr(self, "_timeout")

    @timeout.setter
    def timeout(self, value):
        setattr(self, "_timeout", value)
        self.__init_timeout()

    @property
    def limit(self):
        if not hasattr(self, "_limit"):
            setattr(self, "_limit", self.DEFAULT_LIMIT)
        return getattr(self, "_limit")

    @limit.setter
    def limit(self, value):
        setattr(self, "_limit", value)
        self.__init_limit()
