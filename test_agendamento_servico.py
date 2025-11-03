import pytest
from agendamento_DAO import AgendamentoDAO
from agendamento_service import AgendamentoService
from agendamento import Agendamento

# ---------- FIXTURE PARA O SERVICE ----------
@pytest.fixture
def service():
    # Banco em memória para testes isolados
    dao = AgendamentoDAO(":memory:")
    svc = AgendamentoService(dao)
    yield svc
    svc.fechar_conexao()  # Fecha conexão após cada teste

# ---------- TESTES DE CADASTRO ----------
def test_cadastrar_agendamento_valido(service):
    ag = service.cadastrar_agendamento("2025-11-02", "10:00", "11:00", "Bruno")
    assert ag.id is not None
    assert ag.participante == "Bruno"
    todos = service.listar_todos()
    assert len(todos) == 1

def test_cadastrar_com_participante_em_branco(service):
    with pytest.raises(ValueError, match="Nome invalido, campo em branco!"):
        service.cadastrar_agendamento("2025-11-02", "10:00", "11:00", "")

def test_cadastrar_com_horario_invalido(service):
    with pytest.raises(ValueError, match="Horario invalido"):
        service.cadastrar_agendamento("2025-11-02", "12:00", "11:00", "Bruno")

def test_cadastrar_com_conflito(service):
    service.cadastrar_agendamento("2025-11-02", "10:00", "11:00", "Bruno")
    with pytest.raises(ValueError, match="Conflito de horário"):
        service.cadastrar_agendamento("2025-11-02", "10:30", "11:30", "Bruno")

# ---------- TESTES DE BUSCA ----------
def test_buscar_por_id_existente(service):
    ag = service.cadastrar_agendamento("2025-11-02", "10:00", "11:00", "Bruno")
    buscado = service.buscar_por_id(ag.id)
    assert buscado.id == ag.id

def test_buscar_por_id_inexistente(service):
    with pytest.raises(ValueError, match="Agendamento não encontrado"):
        service.buscar_por_id(999)

# ---------- TESTES DE LISTAGEM ----------
def test_listar_todos(service):
    service.cadastrar_agendamento("2025-11-02", "10:00", "11:00", "Bruno")
    service.cadastrar_agendamento("2025-11-02", "11:00", "12:00", "Maria")
    todos = service.listar_todos()
    assert len(todos) == 2
    assert isinstance(todos[0], Agendamento)

# ---------- TESTES DE ATUALIZAÇÃO ----------
def test_atualizar_agendamento_valido(service):
    ag = service.cadastrar_agendamento("2025-11-02", "10:00", "11:00", "Bruno")
    atualizado = service.atualizar_agendamento(ag.id, "2025-11-02", "11:00", "12:00", "Bruno")
    assert atualizado.inicio == "11:00"
    assert atualizado.termino == "12:00"

def test_atualizar_agendamento_inexistente(service):
    with pytest.raises(ValueError, match="Agendamento não encontrado"):
        service.atualizar_agendamento(999, "2025-11-02", "11:00", "12:00", "Bruno")

def test_atualizar_com_conflito(service):
    ag1 = service.cadastrar_agendamento("2025-11-02", "10:00", "11:00", "Bruno")
    ag2 = service.cadastrar_agendamento("2025-11-02", "11:00", "12:00", "Bruno")
    with pytest.raises(ValueError, match="Conflito de horário"):
        service.atualizar_agendamento(ag2.id, "2025-11-02", "10:30", "11:30", "Bruno")

# ---------- TESTES DE EXCLUSÃO ----------
def test_excluir_agendamento_valido(service):
    ag = service.cadastrar_agendamento("2025-11-02", "10:00", "11:00", "Bruno")
    service.excluir_agendamento(ag.id)
    todos = service.listar_todos()
    assert len(todos) == 0

def test_excluir_agendamento_inexistente(service):
    with pytest.raises(ValueError, match="Agendamento não encontrado"):
        service.excluir_agendamento(999)