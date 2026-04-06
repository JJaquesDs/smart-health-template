from enum import Enum


class UserRole(str, Enum):
    """ Enuns de roles para permissões de Usuarioss"""

    USER = "user",
    SUPERUSER = "superuser",
    ADMIN = "admin",
    SECRETARIA = "secretaria",
    MEDICO = "medico"
