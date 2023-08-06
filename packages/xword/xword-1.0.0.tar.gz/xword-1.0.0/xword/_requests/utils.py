"""HttpClient 工具模块"""
import os
from functools import wraps
from itertools import product
from collections import Counter
from difflib import get_close_matches

from .export import CIMultiDict



# User-Agnet
UA_ANDROID     = "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36"
UA_WINDOWNS    = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
UA_MAC         = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
UA_IPHONE      = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
UA_IPAD        = "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1"
UA_SYMBIAN     = "Mozilla/5.0 (Symbian/3; Series60/5.2 NokiaN8-00/012.002; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/533.4 (KHTML, like Gecko) NokiaBrowser/7.3.0 Mobile Safari/533.4 3gpp-gba"
UA_ANDROID_PAD = "Mozilla/5.0 (Linux; Android 11; Phh-Treble vanilla Build/RQ3A.211001.001;) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.91 Safari/537.36"

UA_ALL = {
    "android"     : UA_ANDROID,
    "windows"     : UA_WINDOWNS,
    "mac"         : UA_MAC,
    "iphone"      : UA_IPHONE,
    "ipad"        : UA_IPAD,
    "symbian"     : UA_SYMBIAN,
    "android_pad" : UA_ANDROID_PAD,
}


def user_agent_option(
    user_agent: str=UA_ANDROID, overwrite: bool=False
) -> str:
    """返回 UserAgent """
    if overwrite:
        return user_agent
    ret = get_close_matches(
        user_agent.lower(), UA_ALL, n=1)
    if ret:
        return UA_ALL[ret[0]]
    return UA_ANDROID


def default_headers():
    """请求默认headers"""
    headers = CIMultiDict()
    headers.add(key="user-agent", value=user_agent_option())
    return headers


# makedirs open
def open_decorate(func):
    """内置方法open装饰器 用于w模式下创建不存在的目录"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 获取 mode 值
        mode = kwargs.get("mode") \
            if kwargs.__contains__("mode") else args[1] if len(args) > 1 else "r"
        # Counter 传入一个可迭代对象 统计每项出现的次数 返回字典 - 查找变位词
        # product 求多个可迭代对象的笛卡尔积
        if Counter(mode) in [
            Counter("".join(item))
                for item in product(["a", "w"], ["b", "+", "b+", ""])
        ]:
            folder = os.path.dirname(args[0])
            if not os.path.isdir(folder):
                os.makedirs(folder)
        return func(*args, **kwargs)
    return wrapper

make_open = open_decorate(open)
