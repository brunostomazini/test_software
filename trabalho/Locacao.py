
class Locacao:
    def __init__(self, cliente_nome, veiculo_id, data_inicio, data_fim,valor_total, id = None):
        self.id = None
        self.cliente_nome = cliente_nome
        self.veiculo_id = veiculo_id
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.valor_total = valor_total
        self.id=  id