from drakaina.middlewares.base import BaseMiddleware


def get_user_id() -> int:
    return 1


class JWTAuthenticationMiddleware(BaseMiddleware):
    ...
