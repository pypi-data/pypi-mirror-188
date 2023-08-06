class BaseClientError(Exception):
    _code = 000
    _message = "Base client error"

    def __repr__(self):
        return f"<{self.__class__.__name__} code={self._code}, message={self._message}>"

    def __str__(self):
        return self.__repr__()


class RequestError(BaseClientError):
    def __init__(self, code, message):
        self._code = code
        self._message = message


class UnknownError(BaseClientError):
    _code = '999'
    _message = 'Unknown error'
