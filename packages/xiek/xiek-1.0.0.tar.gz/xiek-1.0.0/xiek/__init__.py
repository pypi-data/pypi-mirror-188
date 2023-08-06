from . import httpclient
from .httpclient.request import HttpClient
from .httpclient.export import console
from .httpclient.utils import (
    make_open,
    user_agent_option
)

print = console.print
rule  = console.rule


__all__ = ["HttpClient"]
