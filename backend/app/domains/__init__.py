""" Importando todos os models para inicialização via alembic """

from .consultas.models import *
from .doenca_prontuario.model import *
from .doencas.models import *
from .exames.imagem.models import *
from .exames.clinicos.models import *
from .habitos_vida.models import *
from .medicamentos.models import *
from app.domains.pacientes.models import *
from .professionals.medico.models import *
from .professionals.medico.especialidade.models import *
from .professionals.medico.medico_esp.model import *
from .professionals.secretaria.models import *
from .prontuarios.models import *
from .users.models import *
