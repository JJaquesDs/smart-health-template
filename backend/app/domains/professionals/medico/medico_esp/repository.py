from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository

from app.domains.professionals.medico.medico_esp.model import MedicoEspecialidade


class MedicoEspRepository(BaseRepository):
    """ Repository Pattern de 'MedicoEspecialidade' herdando de 'BaseRepository' """

    def __init__(self):
        """ Inicialização da classe """

        super().__init__(  # Pegando tudo da SuperClasse ou Classe Pai
            model=MedicoEspecialidade,
            campo_id="med_esp_id"
        )

    def create_relacoes_med_esp(
            self,
            session: Session,
            medico_id: int,
            especialidades_input: list[dict]
    ) -> list[MedicoEspecialidade]:
        """ Método quee cria relacões 'MedicoEspecialidade' (Pode criar mais de uma por vez, apenas passando o dicionário) [{id: 1, status: "RESIDENTE"}, {id: 2, status: "ESPECIALISTA"] """

        # Criando uma lista de 'MedicoEspecialidade' que itera de acordo com o dict input  'especialidades_input'
        esps = [
            MedicoEspecialidade(
                medico_id=medico_id,
                esp_id=item["especialidades.esp_id"],
                status=item["status"]
            )
            for item in especialidades_input
        ]

        session.add_all(instances=esps)
        session.flush()

        return esps
