from app.core.exceptions.client_exceptions import (
    BadRequestException,
    UnauthorizedException,
    NotFoundException
)


class EmailExistenteException(BadRequestException):
    pass


class UsuarioNaoAutorizadoException(UnauthorizedException):
    pass


class UsuarioNaoEncontradoException(NotFoundException):
    pass
