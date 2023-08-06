""" 同步网络请求 request 封装 """
import os
import sys
import warnings
from time import sleep
from copy import deepcopy

import requests.exceptions
from requests.sessions import Session as _Session

from .base import BaseSesssion
from .export import (
    console,
    CIMultiDict,
    Progress,
    progress_custom_columns
)
from .utils import (
    user_agent_option,
    wraps,
    make_open
)



def capture_request_exc(function):
    """
    request装饰器: 用于捕获请求中的部分异常
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        max_retry, retry_info, retry_timeout = 12, {}, 0.5
        while True:
            try:
                response = function(*args, **kwargs)
                # 抛出部分请求状态码
                status = response.status_code
                if 403 <= status <= 410:
                    raise requests.exceptions.InvalidURL(
                        f"invalid url:\033[4;31m'{response.url}'\033[0m, "
                        f"status_code: \033[31m'{status}'\033[0m")
                return response

            # 超时异常 - 自动重试 直到达到最大重试次数抛出
            except requests.exceptions.Timeout:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                url    = exc_value.request.url
                reason = str(exc_value.args[0].reason.args[1])
                # 记录异常
                retry_info.setdefault(reason, 0)
                retry_info[reason] += 1
                # 达到最大重试次数
                if retry_info[reason] > max_retry:
                    raise
                warnings.warn(f"\033[33m'{url}'\033[0m {reason}\n")
                sleep(retry_timeout)

            # 无网络异常请求 - 死循环请求
            except requests.exceptions.ConnectionError:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                url    = exc_value.request.url
                reason = exc_value.args[0]
                if hasattr(reason, "reason"):
                    reason = reason.reason.args[0].rsplit(": ", 1)[-1]
                reason = str(reason)
                if "No address associated with hostname" not in reason:
                    raise
                warnings.warn(f"\033[33m'{url}'\033[0m {reason}\n")
                sleep(retry_timeout)
    return wrapper



class Session(BaseSesssion):
    """
    pip install requests
    对 requests 的封装, 修改了默认 UserAgent
    """

    def __init__(
        self, base_url=None, headers=None, timeout=None, keep_alive=False, **kwargs
    ):
        self._session    = None
        self._keep_alive = bool(keep_alive)
        super().__init__(base_url, headers, timeout, **kwargs)


    @property
    def session(self):
        """
        获取 requests.Sesssion()
        """
        session = getattr(self, "_session", None)
        if not getattr(self, "_keep_alive", False):
            session = _Session()
            setattr(self, "_session", session)

        if not isinstance(session, _Session):
            session = _Session()
            setattr(self, "_session", session)

        return session


    def request(self, method, url, *args, filename=None, **kwargs):
        """
        session = requests.Session()
        session.request
        新增参数 filename:
        """
        with console.status(f"[yellow b]Send Request:[/] [bright_blue u]{url}[/]"):
            response = self._request(method, url, *args, **kwargs)

        # 不保存文件
        if filename is None:
            return response

        # 响应流大小
        chunk_size, file_size = 1024, 0
        filename = os.path.abspath(filename)
        length   = response.headers.get("Content-Length")

        # 断点续传
        if os.path.isfile(filename):
            # 获取 filename 字节
            file_size = os.path.getsize(filename)
            kwargs.setdefault("headers", {})
            headers = kwargs["headers"]
            # 请求头添加 range 请求部分内容
            headers["Range"] = f"bytes={file_size}-"
            response = self._request(method, url, *args, **kwargs)
            length = response.headers.get("Content-Range")
            if length:
                length = length.rsplit("/", 1)[-1]

        length = int(length) if str(length).isdigit() else None

        # 保存文件
        with make_open(filename, "ab") as file:

            with Progress(
                *progress_custom_columns,
                console=console,
                # transient=True, # 完成后清除进度条
            ) as progress:
                task = progress.add_task(
                    f"[magenta b]{os.path.basename(filename)}[/]",
                    total=length)
                progress.update(task, advance=file_size)

                for chunk in response.iter_content(chunk_size=chunk_size):
                    file.write(chunk)
                    progress.update(task, advance=chunk_size)

        console.print(
            "[green b]File Saved Successfully[/]"
            f"[yellow] ->[/] [bright_blue u]'{filename}'[/]\n")

        return response


    @capture_request_exc
    def _request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
        user_agent=None,
    ):
        url = self.build_url(url, raw=True)
        raw_headers = deepcopy(self.headers)

        # 更新UserAgent
        if headers:
            raw_headers.update(CIMultiDict(headers))

        # 设置UserAgent
        if user_agent is not None and user_agent:
            if isinstance(user_agent, str):
                user_agent = [user_agent, False]
            user_agent = user_agent_option(*user_agent)
            raw_headers["user-agent"] = user_agent

        # 请求 timeout
        if (
            not isinstance(timeout, (int, float))
            or timeout <= 0
        ):
            timeout = self.timeout

        # verify
        verify = bool(self._verify) \
            if verify is None else bool(verify)

        return self.session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            headers=raw_headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json)


    def get(self, url, allow_redirects=True, **kwargs):
        return self.request("GET", url, allow_redirects=allow_redirects, **kwargs)

    def post(self, url, data=None, json=None, allow_redirects=True, **kwargs):
        return self.request("POST", url, data=data, json=json, allow_redirects=allow_redirects, **kwargs)

    def head(self, url, allow_redirects=False, **kwargs):
        return self.request("HEAD", url, allow_redirects=allow_redirects, **kwargs)

    def options(self, url, allow_redirects=True, **kwargs):
        return self.request("OPTIONS", url, allow_redirects=allow_redirects, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request("PUT", url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self.request("DELETE", url, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.request("PATCH", url, data=data, **kwargs)
