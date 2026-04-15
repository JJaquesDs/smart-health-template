from fastapi import HTTPException

from sqlalchemy.orm import Session, InstrumentedAttribute

from typing import Any


class BaseRepository:
    """ Classe base de repositório para todos os repositórios (Repository Pattern) """

    def __init__(self, model, campo_id: str = "id"):
        """ Construtor """

        self.model = model
        self.campo_id = campo_id

    def get_or_not_found(
            self,
            session: Session,
            campo: InstrumentedAttribute,
            valor: Any,
            exception: Exception
    ):
        """ Método que retorna se um model existe por uma consulta no campo baseado no valor passado se não lança 404 ('id', por exemplo) """

        obj_output = self.get_one_by_campo(session=session, campo=campo, valor=valor)

        # Se não houver o model no banco, lança exception que pode ser alterada aqui por parâmetro
        if not obj_output:
            raise exception

        # Retorna dado caso encontre
        return obj_output

    def get_by_id(self, session: Session, obj_id: int):
        """ Método base para consultar models por 'id' (retorna um apenas)"""

        campo = getattr(self.model, self.campo_id)

        return session.query(_entity=self.model).filter(campo == obj_id).first()

    def get_all(self, session: Session):
        """ Método base para retornar todos models (retorna em lote)"""

        return session.query(_entity=self.model).all()

    def get_by_campo(
            self,
            session: Session,
            campo: InstrumentedAttribute,  # Para poder tipar de maneira certa, usando atributos do SQLALCHEMY
            valor: Any
    ):
        """ Método base para retornar models por campo da tabela (retorna todos os dados) """

        return session.query(_entity=self.model).filter(campo == valor).all()

    def get_one_by_campo(
            self,
            session: Session,
            campo: InstrumentedAttribute,
            valor: Any
    ):
        """ Método que retorna apenas um dado pelo campo consultado """

        return session.query(self.model).filter(campo == valor).first()

    def get_by_ids(self, session: Session, ids: list[int]):
        """ Método que retorna Models por 'ids' (Retorna somente os que existem na consulta) """

        # Se não houver 'ids' apenas retorna nada (lista vazia)
        if not ids:
            return []

        campo = getattr(__o=self.model, __name=self.campo_id)

        # Retorna uma consulta de models filtrando pelo campo 'id' da talela (todos os dados encontrados)
        return session.query(self.model).filter(campo.in_(ids)).all()

    def get_by_ids_or_not_found(self, session: Session, ids: list[int]):
        """ Método que retorna a consulta dos 'ids' ou retorna 404-Not Found (Se pelo menos um não estiver já retorna 404) """

        # Puxando os que estão no banco
        registros = self.get_by_ids(session=session, ids=ids)

        # Puxando os que foram encontrados
        encontrados = {
            getattr(reg, self.campo_id) for reg in registros
        }

        # Analisando se falta algum 'id'
        faltantes = set(ids) - encontrados

        # Se houver pelo menos um faltante, lança 'exception'
        if faltantes:
            raise HTTPException(
                status_code=404,
                detail=f"{self.model.__name__} não encontrados: {list(faltantes)}"
            )

        return registros

    def create(self, session: Session, obj_input):
        """ Método para instânciar model no banco de dados """

        # Cria o obj do modelo usando os dados de entrada
        db_obj_model = self.model(obj_input)

        session.add(instance=db_obj_model)
        session.flush()

        return db_obj_model

    def update(self, session: Session, obj_input):
        """ Método para instânciar model no banco de dados """

        # Cria o obj do modelo usando os dados de entrada
        db_obj_model = self.model(obj_input)

        session.add(instance=db_obj_model)
        session.flush()

        return db_obj_model

    def create_com_relacoes(
            self,
            session: Session,
            obj_input: dict,
            relacoes: dict[str, list[Any]]
    ):
        """ Método para criar Models com relacionamentos entre tabelas """

        db_obj = self.model(**obj_input)  # Cria o obj do modelo usando os dados de entrada a linha '**obj_input' desempacota o dicionário

        # Setando no model para o banco o campo e valor da tabela
        for campo, valor in relacoes.items():
            setattr(__obj=db_obj, __name=campo, __value=valor)

        session.add(instance=db_obj)
        session.flush()

        return db_obj

    def delete(self, session: Session, obj_model):
        """ Método para deletar Model"""
        session.delete(instance=obj_model)

        return obj_model

