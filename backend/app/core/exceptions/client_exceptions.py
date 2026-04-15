from app.core.base_exception import AppException


class BadRequestException(AppException):
    """ Exception de Bad Request '400' (Requisição inválida por padrão) """

    def __init__(self, message: str = "Requisição inválida"):
        """ Mensagem padrão pode ser sobrescrita para seu caso por parâmetro """

        super().__init__(message, status_code=400)


class NotFoundException(AppException):
    """ Exception de Not Found '404' (Recurso não encontrado por padrão) """

    def __init__(self, message: str = "Recurso não encontrado"):
        """ Mensagem padrão pode ser sobrescrita para seu caso por parâmetro """

        super().__init__(message, status_code=404)


class UnauthorizedException(AppException):
    """ Exception de Unauthorized '401' (Não autorizado por padrão) """

    def __init__(self, message: str = "Não autorizado"):
        """ Mensagem padrão pode ser sobrescrita para seu caso por parâmetro """

        super().__init__(message, status_code=401)


class ForbiddenException(AppException):
    """ Exception de Forbidden '403' (Acesso negado por padrão) """

    def __init__(self, message: str = "Acesso negado"):
        """ Mensagem padrão pode ser sobrescrita para seu caso por parâmetro """

        super().__init__(message, status_code=403)
