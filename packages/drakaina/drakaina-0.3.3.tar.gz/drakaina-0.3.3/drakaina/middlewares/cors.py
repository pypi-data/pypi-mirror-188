from typing import Iterable
from typing import Optional
from typing import Union
from drakaina.middlewares.base import BaseMiddleware
from drakaina.typing_ import WSGIApplication
from drakaina.typing_ import WSGIEnvironment
from drakaina.typing_ import WSGIResponse
from drakaina.typing_ import WSGIStartResponse


__all__ = ("CORSMiddleware",)

DEFAULT_HEADERS = (
    "Accept, Accept-Encoding, Authorization, Content-Type, DNT, "
    "Origin, User-Agent, X-Requested-With"
)
DEFAULT_METHODS = "GET, POST, OPTIONS"


def _parse_iterable_arg(s: Union[str, Iterable[str]]) -> str:
    if isinstance(s, Iterable) and not isinstance(s, str):
        return ", ".join(s)
    return s


class CORSMiddleware(BaseMiddleware):
    """Simple middleware to provide CORS headers.

    See: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

    :param allow_origin: The "Access-Control-Allow-Origin" header.
                         Default: "*".
    :type allow_origin: Union[str, Iterable[str]]
    :param allow_methods: The "Access-Control-Allow-Methods" header.
                          Default: "GET, POST, OPTIONS".
    :type allow_methods: Union[str, Iterable[str]]
    :param allow_headers: The "Access-Control-Allow-Headers" header.
                          Default: "Accept, Accept-Encoding, Authorization,
                          Content-Type, DNT, Origin, User-Agent,
                          X-Requested-With".
    :type allow_headers: Union[str, Iterable[str]]
    :param allow_credentials: The "Access-Control-Allow-Credentials" header.
                              Default: None.
    :type allow_credentials: bool
    :param expose_headers: The "Access-Control-Expose-Headers" header.
                           Default: None.
    :type expose_headers: Union[str, Iterable[str]]
    :param max_age: The "Access-Control-Max-Age" header.
                    Default: 86400 sec. (1 day).
    :type max_age: Union[int, str]

    """

    __slots__ = ("_cors_headers", "_cors_options_headers", "_whitelist")

    def __init__(
        self,
        app: WSGIApplication,
        allow_origin: Optional[Union[str, Iterable[str]]] = None,
        allow_methods: Optional[Union[str, Iterable[str]]] = None,
        allow_headers: Optional[Union[str, Iterable[str]]] = None,
        allow_credentials: Optional[bool] = None,
        expose_headers: Optional[Union[str, Iterable[str]]] = None,
        max_age: Union[int, str] = 86400,
        **kwargs,
    ):
        assert (
            isinstance(max_age, int)
            or isinstance(max_age, str)
            and max_age.isdigit()
        ), "`max_age` must be a number"

        super().__init__(app, **kwargs)

        self._whitelist = _parse_iterable_arg(allow_origin or "*")
        self._cors_headers = [("Access-Control-Allow-Origin", self._whitelist)]
        if expose_headers is not None:
            self._cors_headers.append(
                (
                    "Access-Control-Expose-Headers",
                    _parse_iterable_arg(expose_headers),
                )
            )

        self._cors_options_headers = [
            (
                "Access-Control-Allow-Headers",
                _parse_iterable_arg(allow_headers or DEFAULT_HEADERS),
            ),
            (
                "Access-Control-Allow-Methods",
                _parse_iterable_arg(allow_methods or DEFAULT_METHODS),
            ),
            ("Access-Control-Max-Age", str(max_age)),
            ("Content-Length", "0"),
        ]
        if allow_credentials is not None:
            self._cors_options_headers.append(
                ("Access-Control-Allow-Credentials", allow_credentials)
            )

    def __wsgi_call__(
        self,
        environ: WSGIEnvironment,
        start_response: WSGIStartResponse,
    ) -> WSGIResponse:
        origin = environ.get("HTTP_ORIGIN")
        if self._validate_origin(origin):
            if environ.get("REQUEST_METHOD") == "OPTIONS":
                return self.options(environ, start_response)
            return self.app(environ, self._add_cors_headers(start_response))
        else:
            return self.app(environ, start_response)

    def options(
        self,
        environ: WSGIEnvironment,
        start_response: WSGIStartResponse,
    ) -> WSGIResponse:
        response_headers = self._cors_headers + self._cors_options_headers
        start_response("200 OK", response_headers)
        yield b""

    def _add_cors_headers(
        self,
        start_response: WSGIStartResponse,
    ) -> WSGIStartResponse:
        """Wraps the start_response method, and includes the CORS header
        for the specified origin.
        """

        def cors_allowed_response(status, headers, exc_info=None):
            headers.extend(self._cors_headers)
            return start_response(status, headers, exc_info)

        return cors_allowed_response

    def _validate_origin(self, origin: str) -> bool:
        return origin and (origin in self._whitelist or self._whitelist == "*")
