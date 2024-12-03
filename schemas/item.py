from pydantic import BaseModel
from typing import Optional, List
from model.item import Item

from schemas import ComentarioSchema


class ItemSchema(BaseModel):
    """ Define como um novo item a ser inserido deve ser representado
    """
    nome: str = "Banana Prata"
    quantidade: Optional[int] = 12
    valor: float = 12.50


class ItemBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do item.
    """
    nome: str = "Teste"


class ListagemItemSchema(BaseModel):
    """ Define como uma listagem de itens será retornada.
    """
    itens:List[ItemSchema]


def apresenta_itens(itens: List[Item]):
    """ Retorna uma representação do item seguindo o schema definido em
        itemViewSchema.
    """
    result = []
    for item in itens:
        result.append({
            "nome": item.nome,
            "quantidade": item.quantidade,
            "valor": item.valor,
        })

    return {"itens": result}


class ItemViewSchema(BaseModel):
    """ Define como um item será retornado: item + comentários.
    """
    id: int = 1
    nome: str = "Banana Prata"
    quantidade: Optional[int] = 12
    valor: float = 12.50
    total_cometarios: int = 1
    comentarios:List[ComentarioSchema]


class ItemDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_item(item: item):
    """ Retorna uma representação do item seguindo o schema definido em
        itemViewSchema.
    """
    return {
        "id": item.id,
        "nome": item.nome,
        "quantidade": item.quantidade,
        "valor": item.valor,
        "total_cometarios": len(item.comentarios),
        "comentarios": [{"texto": c.texto} for c in item.comentarios]
    }