from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base

class Aluno(Base):
    __tablename__ = 'aluno'

    id = Column("pk_item", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    matricula = Column(Integer)
    classe = Column(String(140))
    turno = Column(String(140))
    email = Column(String(140), unique=True)
    data_cadastro = Column(DateTime, default=datetime.now())

    def __init__(self, nome:str, matricula:int, classe:str, turno:str, email:str, 
                 data_cadastro:Union[DateTime, None] = None):
        """"
        Cria um novo registro de Aluno

        Arguments:
            nome: nome do Aluno(a)
            matricula: matricula do Aluno(a)
            classe: clase em que o aluno(a) está matriculado(a)
            turno: turno da classe em que o aluno(a) está matriculado(a)
            email: email de contato do aluno(a)
            data_cadastro: data de quando o aluno(a) foi registrada na base
        """

        self.nome = nome
        self.matricula = matricula
        self.classe = classe
        self.turno = turno
        self.email = email

        # se não for informada, será o data exata da inserção no banco
        if data_cadastro:
            self.data_cadastro = data_cadastro