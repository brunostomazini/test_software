import pytest
from .veiculo_service import VeiculoService
from .Veiculo import Veiculo

@pytest.fixture(scope="session")
def placa_nao_cadastrada():
    return "IQJ-5887"

@pytest.fixture(scope="session")
def veiculo_servico_base():
    return VeiculoService()

@pytest.fixture(scope="function")
def veiculo_servico(placa_nao_cadastrada, veiculo_servico_base):
    exisite = veiculo_servico_base.veiculoDAO.obter_por_placa(placa_nao_cadastrada)
    if exisite and exisite.id:
            veiculo_servico_base.veiculoDAO.deletar(exisite.id)
    yield veiculo_servico_base    
    exisite = veiculo_servico_base.veiculoDAO.obter_por_placa(placa_nao_cadastrada)
    if exisite and exisite.id:
            veiculo_servico_base.veiculoDAO.deletar(exisite.id)

def test_caminhoFeliz():

    veiculo = VeiculoService.CadastraVeiculo(
        "a","b",1,1,1
    )
    assert veiculo is not None
    assert veiculo.id >0


#modelo, placa, ano, diaria, disponivel
def test_dados_vazios_feliz():
    veiculo = VeiculoService.CadastraVeiculo(
        "a","b",1,1,1
    )
    assert veiculo is not None
    assert veiculo.id >0

def test_dados_vazios_modelo():
    with pytest.raises(ValueError):
        veiculo = VeiculoService.CadastraVeiculo(
        None,"b",1,1,1
    )
    

def test_dados_vazios_placa():
    with pytest.raises(ValueError):
        veiculo = VeiculoService.CadastraVeiculo(
        "a","",1,1,1
    )
        

def test_cadastrar_sucesso_retorna_objeto_com_id(veiculo_servico,placa_nao_cadastrada):
    veiculo = veiculo_servico.CadastraVeiculo(modelo="Gol 1.0", placa=placa_nao_cadastrada, ano=2015, diaria=123.45)
    assert isinstance(veiculo, Veiculo)
    assert isinstance(veiculo.id, int) and veiculo.id > 0
    assert veiculo.modelo == "Gol 1.0"
    assert veiculo.placa == placa_nao_cadastrada
    assert veiculo.ano == 2015
    assert veiculo.diaria == pytest.approx(123.45)
    assert veiculo.disponivel is True

    # Confere se persistiu corretamente via DAO
    db_veiculo = veiculo_servico.dao.obter_por_id(veiculo.id)
    assert db_veiculo is not None
    assert db_veiculo.placa ==placa_nao_cadastrada
    assert db_veiculo.disponivel is True