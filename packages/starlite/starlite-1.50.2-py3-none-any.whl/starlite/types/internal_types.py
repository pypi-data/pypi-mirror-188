from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Literal,
    NamedTuple,
    Optional,
    Type,
    Union,
)

from starlite.types import Method

if TYPE_CHECKING:
    from starlite.app import Starlite  # noqa: TC004
    from starlite.controller import Controller  # noqa: TC004
    from starlite.handlers.asgi import ASGIRouteHandler  # noqa: TC004
    from starlite.handlers.http import HTTPRouteHandler  # noqa: TC004
    from starlite.handlers.websocket import WebsocketRouteHandler  # noqa: TC004
    from starlite.response import Response  # noqa: TC004
    from starlite.router import Router  # noqa: TC004
else:
    Starlite = Any
    ASGIRouteHandler = Any
    WebsocketRouteHandler = Any
    HTTPRouteHandler = Any
    Response = Any
    Controller = Any
    Router = Any

ReservedKwargs = Literal["request", "socket", "headers", "query", "cookies", "state", "data"]
StarliteType = Starlite
RouteHandlerType = Union[HTTPRouteHandler, WebsocketRouteHandler, ASGIRouteHandler]
ResponseType = Type[Response]
ControllerRouterHandler = Union[Type[Controller], RouteHandlerType, Router, Callable[..., Any]]
RouteHandlerMapItem = Dict[Union[Method, Literal["websocket"], Literal["asgi"]], RouteHandlerType]


class PathParameterDefinition(NamedTuple):
    """Path parameter tuple."""

    name: str
    full: str
    type: Type
    parser: Optional[Callable[[str], Any]]
