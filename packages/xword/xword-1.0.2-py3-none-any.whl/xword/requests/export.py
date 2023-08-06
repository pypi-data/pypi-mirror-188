""" httpclient 模块导入"""
import sys
from multidict import CIMultiDict

from yarl import URL

from rich.console import Console
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    SpinnerColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

console = Console()

progress_default_columns = Progress.get_default_columns()
progress_custom_columns  = [
    SpinnerColumn("line"),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    TimeElapsedColumn(),
]
