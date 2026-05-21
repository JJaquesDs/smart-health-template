from sqlalchemy.orm import Session

from app.domains.exames.imagem.models import UploadExameImagem, ExameImagem, ResultadoExameImagemIa


def save_upload_image(
        session: Session,
        upload: UploadExameImagem
) -> UploadExameImagem:
    """ Função que salva 'Upload' Exame Imagem no Banco de Dados """

    session.add(upload)
    session.flush()

    return upload


def save_exam_image(
        session: Session,
        exame: ExameImagem
) -> ExameImagem:
    """ Função que salva 'Upload' Exame Imagem no Banco de Dados """

    session.add(exame)
    session.flush()

    return exame


def get_exame_image(
        session: Session,
        exame_id: int
) -> ExameImagem | None:

    """ Função que retorna se existe um Exame de Imagem instanciado """

    return session.query(ExameImagem).filter_by(exame_id=exame_id).first()


def get_resultado_analise_exame_img(
        session: Session,
        exame_imagem_id: int
) -> ResultadoExameImagemIa | None:
    """ Função para retornar se já existe um resultado a partir do 'id' (evitar duplicação oa chamar a rota mais de uma vez)"""

    return session.query(ResultadoExameImagemIa).filter(
        ResultadoExameImagemIa.exame_imagem_id == exame_imagem_id
    ).first()


def save_result_analise_exame_img(
        session: Session,
        resultado: ResultadoExameImagemIa
) -> ResultadoExameImagemIa:
    """Função para persistir o resultado de análise de exame de imagem por IA"""

    session.add(resultado)

    #Flush para garantir o 'id' auto-increment
    session.flush()

    return resultado
