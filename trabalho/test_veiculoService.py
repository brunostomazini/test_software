import pytest
from veiculo_service import VeiculoService

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
        

def test_dados_vazios_ano():
    with pytest.raises(ValueError):
        veiculo = VeiculoService.CadastraVeiculo(
        "a","b",None,1,1
        )

def test_dados_vazios_diaria():
    with pytest.raises(ValueError):
        veiculo = VeiculoService.CadastraVeiculo(
        "a","b",1,None,1
        )

def test_dados_vazios_disponivel():
    with pytest.raises(ValueError):
        veiculo = VeiculoService.CadastraVeiculo(
        "a","",1,1,None
        )
