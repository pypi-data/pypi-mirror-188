"""
MIT License

Copyright (c) 2023 Akash

Octra ltd
"""

class OctraException(Exception):
    """Base exception for all errors."""

    pass

class HTTPException(OctraException):
    """
    Raised when an HTTP request fails.

    Attributes
    ----------
    response: :class:`aiohttp.ClientResponse`
        The response for the request that failed.
    messsage: Optional[:class:`str`]
       The message for the request that failed.
    """

    def __init__(self, response, message=""):
        self.response = response
        self.message = message
        super().__init__(f"{response.status} {message}")

class InvalidToken(HTTPException):
    """Raised when a token is invalid."""

    def __init__(self, response, message=""):
        super().__init__(response, message)

class Forbidden(HTTPException):
    """Raised when something is forbidden."""

    def __init__(self, response, message=""):
        super().__init__(response, message)

class Conflict(HTTPException):
    """Raised when another instance of the bot is running."""

    def __init__(self, response, message=""):
        super().__init__(response, message)