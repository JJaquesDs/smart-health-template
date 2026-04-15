class AppException(Exception):
    """ Classe base de Excessões """

    def __init__(self, message: str, status_code: int):
        """ Inicialização da classe, passe as messagens e o status code por parâmetro """

        self.message = message
        self.status_code = status_code

        super().__init__(message)