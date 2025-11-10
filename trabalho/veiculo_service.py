from .VeiculoDAO import VeiculoDAO
from .Veiculo import Veiculo

class VeiculoService:

    def CadastraVeiculo(self, modelo, placa, ano, diaria):
        veiculoDAO = VeiculoDAO()
        veiculo = Veiculo(modelo,placa,ano,diaria,True)

        if veiculo.modelo == None:
            raise ValueError("Campo modelo nulo")
        if veiculo.modelo.strip() == "":
            raise ValueError("Campo modelo vazio")
        
        if veiculo.placa == None:
            raise ValueError("Campo placa nulo")
        if veiculo.placa.strip() == "":
            raise ValueError("Campo placa vazio")
        
        '''if veiculo.modelo == None:
            raise ValueError("Campo modelo nulo")
        if veiculo.modelo.strip() == "":
            raise ValueError("Campo modelo vazio")'''
        

        veiculoDAO.inserir(veiculo)
        return veiculo
    
    def obter_por_placa(placa_nao_cadastrada):
        veiculoDAO = VeiculoDAO()
        return veiculoDAO.obter_por_placa(placa_nao_cadastrada)
