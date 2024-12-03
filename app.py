from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Aluno
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API de Gerenciamento de Alunos", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
aluno_tag = Tag(name="Aluno", description="Adição, visualização, atualização e remoção de alunos à base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')


@app.post('/aluno', tags=[aluno_tag],
          responses={"200": AlunoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_aluno(form: AlunoSchema):
    """Adiciona um novo Aluno à base de dados.

    Retorna uma representação do aluno adicionado.
    """
    aluno = Aluno(
        nome=form.nome,
        matricula=form.matricula,
        classe=form.classe,
        turno=form.turno,
        email=form.email
    )
    logger.debug(f"Adicionando aluno com nome: '{aluno.nome}'")
    try:
        session = Session()
        session.add(aluno)
        session.commit()
        logger.debug(f"Aluno adicionado com sucesso: '{aluno.nome}'")
        return apresenta_aluno(aluno), 200

    except IntegrityError:
        error_msg = "Aluno com o mesmo email ou matrícula já está cadastrado na base."
        logger.warning(f"Erro ao adicionar aluno '{aluno.nome}': {error_msg}")
        return {"message": error_msg}, 409

    except Exception:
        error_msg = "Não foi possível salvar o novo aluno."
        logger.warning(f"Erro ao adicionar aluno '{aluno.nome}': {error_msg}")
        return {"message": error_msg}, 400


@app.get('/alunos', tags=[aluno_tag],
         responses={"200": ListagemAlunoSchema, "404": ErrorSchema})
def get_alunos():
    """Busca por todos os Alunos cadastrados.

    Retorna uma listagem de alunos.
    """
    logger.debug(f"Coletando alunos")
    session = Session()
    alunos = session.query(Aluno).all()

    if not alunos:
        return {"alunos": []}, 200
    else:
        logger.debug(f"{len(alunos)} alunos encontrados")
        return apresenta_alunos(alunos), 200


@app.get('/aluno', tags=[aluno_tag],
         responses={"200": AlunoViewSchema, "404": ErrorSchema})
def get_aluno(query: AlunoBuscaSchema):
    """Busca por um Aluno a partir do nome.

    Retorna os detalhes do aluno.
    """
    aluno_nome = unquote(query.nome)
    logger.debug(f"Buscando aluno com nome: '{aluno_nome}'")
    session = Session()
    aluno = session.query(Aluno).filter(Aluno.nome == aluno_nome).first()

    if not aluno:
        error_msg = "Aluno não encontrado na base."
        logger.warning(f"Erro ao buscar aluno '{aluno_nome}': {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Aluno encontrado: '{aluno.nome}'")
        return apresenta_aluno(aluno), 200


@app.put('/aluno', tags=[aluno_tag],
         responses={"200": AlunoViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_aluno(query: AlunoBuscaSchema, form: AlunoUpdateSchema):
    """Atualiza os dados de um Aluno a partir do nome.

    Retorna os detalhes do aluno atualizado.
    """
    aluno_nome = unquote(query.nome)
    logger.debug(f"Atualizando aluno com nome: '{aluno_nome}'")
    session = Session()
    aluno = session.query(Aluno).filter(Aluno.nome == aluno_nome).first()

    if not aluno:
        error_msg = "Aluno não encontrado na base."
        logger.warning(f"Erro ao atualizar aluno '{aluno_nome}': {error_msg}")
        return {"message": error_msg}, 404

    try:
        # Atualizando os dados do aluno
        if form.nome: aluno.nome = form.nome
        if form.matricula: aluno.matricula = form.matricula
        if form.classe: aluno.classe = form.classe
        if form.turno: aluno.turno = form.turno
        if form.email: aluno.email = form.email
        session.commit()

        logger.debug(f"Aluno atualizado com sucesso: '{aluno.nome}'")
        return apresenta_aluno(aluno), 200

    except IntegrityError:
        error_msg = "Email ou matrícula já está sendo usado por outro aluno."
        logger.warning(f"Erro ao atualizar aluno '{aluno.nome}': {error_msg}")
        return {"message": error_msg}, 400

    except Exception:
        error_msg = "Erro inesperado ao atualizar o aluno."
        logger.warning(f"Erro ao atualizar aluno '{aluno.nome}': {error_msg}")
        return {"message": error_msg}, 400


@app.delete('/aluno', tags=[aluno_tag],
            responses={"200": AlunoDelSchema, "404": ErrorSchema})
def del_aluno(query: AlunoBuscaSchema):
    """Deleta um Aluno a partir do nome informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    aluno_nome = unquote(query.nome)
    logger.debug(f"Deletando aluno com nome: '{aluno_nome}'")
    session = Session()
    count = session.query(Aluno).filter(Aluno.nome == aluno_nome).delete()
    session.commit()

    if count:
        logger.debug(f"Aluno deletado com sucesso: '{aluno_nome}'")
        return {"message": "Aluno removido", "nome": aluno_nome}
    else:
        error_msg = "Aluno não encontrado na base."
        logger.warning(f"Erro ao deletar aluno '{aluno_nome}': {error_msg}")
        return {"message": error_msg}, 404
