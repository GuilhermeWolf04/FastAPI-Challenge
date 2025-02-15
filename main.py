from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/empresas/", response_model=schemas.Empresa)
def create_empresa(empresa: schemas.EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = models.Empresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.get("/empresas/", response_model=List[schemas.Empresa])
def read_empresas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    empresas = db.query(models.Empresa).offset(skip).limit(limit).all()
    return empresas

@app.post("/obrigacoes/", response_model=schemas.ObrigacaoAcessoria)
def create_obrigacao(obrigacao: schemas.ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == obrigacao.empresa_id).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa not found")
    db_obrigacao = models.ObrigacaoAcessoria(**obrigacao.dict())
    db.add(db_obrigacao)
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

@app.get("/obrigacoes/", response_model=List[schemas.ObrigacaoAcessoria])
def read_obrigacoes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    obrigacoes = db.query(models.ObrigacaoAcessoria).offset(skip).limit(limit).all()
    return obrigacoes