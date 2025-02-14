from pydantic import BaseModel
from typing import List, Optional

class ObrigacaoAcessoriaBase(BaseModel):
    nome: str
    periodicidade: str

class ObrigacaoAcessoriaCreate(ObrigacaoAcessoriaBase):
    pass

class ObrigacaoAcessoria(ObrigacaoAcessoriaBase):
    id: int
    empresa_id: int

    class Config:
        orm_mode = True

class EmpresaBase(BaseModel):
    nome: str
    cnpj: str
    endereco: str
    email: str
    telefone: str

class EmpresaCreate(EmpresaBase):
    pass

class Empresa(EmpresaBase):
    id: int
    obrigacoes: List[ObrigacaoAcessoria] = []

    class Config:
        orm_mode = True