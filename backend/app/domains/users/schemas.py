from typing import Optional

from pydantic import BaseModel, EmailStr, Field, model_validator

from  app.domains.users.enums import UserRole


PROFESSIONAL_ROLES = {UserRole.MEDICO, UserRole.ADMIN}


class UserProfessionalMixin(BaseModel):
    registro_profissional: Optional[str] = None
    especialidade_principal: Optional[str] = None
    instituicao: Optional[str] = None
    universidade: Optional[str] = None
    ano_formacao: Optional[int] = None
    residencia_medica: Optional[str] = None
    especializacoes: Optional[list[str]] = None


class User(UserProfessionalMixin):
    """ Classe base de usuarios """
    email: EmailStr
    senha: str
    nome: str
    telefone: str
    role: UserRole

    @model_validator(mode="after")
    def validate_professional_fields(self):
        if self.role in PROFESSIONAL_ROLES:
            missing_fields = [
                field_name
                for field_name in (
                    "registro_profissional",
                    "especialidade_principal",
                    "instituicao",
                    "universidade",
                    "ano_formacao",
                    "residencia_medica",
                )
                if getattr(self, field_name) in (None, "")
            ]

            if not self.especializacoes:
                missing_fields.append("especializacoes")

            if missing_fields:
                fields = ", ".join(missing_fields)
                raise ValueError(
                    f"Campos profissionais obrigatórios para a role {self.role}: {fields}"
                )

        return self


class UserPublic(UserProfessionalMixin):
    """ Classe Pública usada para retornar dados pela API sem expor informações sensiveis """

    usuario_id: int
    nome: str
    telefone: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True  # Serialização dos dados, dizendo que virão de um orm SQLAlchemy


class UserCreate(BaseModel):
    """ Schema para criacao de novo usuario"""
    email: EmailStr
    senha: str
    nome: str
    telefone: str
    role: UserRole
    registro_profissional: Optional[str] = None
    especialidade_principal: Optional[str] = None
    instituicao: Optional[str] = None
    universidade: Optional[str] = None
    ano_formacao: Optional[int] = None
    residencia_medica: Optional[str] = None
    especializacoes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_professional_fields(self):
        return User(**self.model_dump())


class UserUpdate(UserProfessionalMixin):
    """ Classe de atualização de usuarios """

    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    role: Optional[UserRole] = None

