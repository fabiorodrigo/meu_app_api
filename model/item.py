from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class Item(Base):
    __tablename__ = 'item'

    id = Column("pk_item", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    quantidade = Column(Integer)
    valor = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o item e o comentário.
    # Essa relação é implicita, não está salva na tabela 'item',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, nome:str, quantidade:int, valor:float,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Item

        Arguments:
            nome: nome do Item.
            quantidade: quantidade que se espera comprar daquele item
            valor: valor esperado para o item
            data_insercao: data de quando o item foi inserido à base
        """
        self.nome = nome
        self.quantidade = quantidade
        self.valor = valor

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao item
        """
        self.comentarios.append(comentario)
