from enum import Enum


class StatusEsp(str, Enum):
    """ Enuns de roles para permissões de Usuarioss"""

    ESPECIALISTA = "especialista",
    RESIDENTE = "residente",
    POS_GRADUANDO = "pós_graduando",
    ESPECIALIZACAO = "especialização",
    GENERALISTA = "generalista"
