"""
"""
This middleware modifies the `client` and `scheme` information so that they reference
the connecting client, rather than the connecting proxy.

https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers#Proxies
"""
from typing import List, Optional, Tuple, Union, cast

from uvicorn._types import (
    ASGI3Application,
    ASGIReceiveCallable,
    ASGISendCallable,
    HTTPScope,
    Scope,
    WebSocketScope,
)


class ProxyHeadersMiddleware:
    def __init__(
        self,
        app: "ASGI3Application",
        trusted_hosts: Union[List[str], str] = "127.0.0.1",
    ) -> None:
        self.app = app
        if isinstance(trusted_hosts, str):
            self.trusted_hosts = {item.strip() for item in trusted_hosts.split(",")}
        else:
            self.trusted_hosts = set(trusted_hosts)
        self.always_trust = "*" in self.trusted_hosts

    def get_trusted_client_host(
        self, x_forwarded_for_hosts: List[str]
    ) -> Optional[str]:
        if self.always_trust:
            return x_forwarded_for_hosts[0]

        for host in reversed(x_forwarded_for_hosts):
            if host not in self.trusted_hosts:
                return host

        return None

    async def __call__(
        self, scope: "Scope", receive: "ASGIReceiveCallable", send: "ASGISendCallable"
    ) -> None:
        if scope["type"] in ("http", "websocket"):
            scope = cast(Union["HTTPScope", "WebSocketScope"], scope)
            client_addr: Optional[Tuple[str, int]] = scope.get("client")
            client_host = client_addr[0] if client_addr else None

            if self.always_trust or client_host in self.trusted_hosts:
                headers = dict(scope["headers"])

                if b"x-forwarded-proto" in headers:
                    # Determine if the incoming request was http or https based on
                    # the X-Forwarded-Proto header.
                    x_forwarded_proto = (
                        headers[b"x-forwarded-proto"].decode("latin1").strip()
                    )
                    if scope["type"] == "websocket":
                        scope["scheme"] = (
                            "wss" if x_forwarded_proto == "https" else "ws"
                        )
                    else:
                        scope["scheme"] = x_forwarded_proto

                if b"x-forwarded-for" in headers:
                if b"x-forwarded-for" in headers:
                    # Decode the x_forwarded_for header using latin1 encoding
                    x_forwarded_for = headers[b"x-forwarded-for"].decode("latin1")
                    # Split the x_forwarded_for header by comma and strip each item
                    x_forwarded_for_hosts = [
                        item.strip() for item in x_forwarded_for.split(",")
                    ]

        return await self.app(scope, receive, send)
