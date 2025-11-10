from .VeiculoDAO import VeiculoDAO
from .Veiculo import Veiculo

class VeiculoService():
     
    def __init__(self):
        self.veiculoDAO = VeiculoDAO()

    @classmethod
    def CadastraVeiculo(modelo, placa, ano, diaria, disponivel):

                
        veiculo = Veiculo(modelo,placa,ano,diaria, disponivel)

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
        

        self.veiculoDAO.inserir(veiculo)
        return veiculo
    
    