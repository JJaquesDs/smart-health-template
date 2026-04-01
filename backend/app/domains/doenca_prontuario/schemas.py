from pydantic import BaseModel


class DoencaProntuarioBase(BaseModel):
    doenca_id: int
    prontuario_id: int


class DoencaProntuarioCreate(DoencaProntuarioBase):
    pass


class DoencaProntuarioGet(DoencaProntuarioBase):
    doenca_prontuario_id: int

    class Config:
        from_attributes = True

