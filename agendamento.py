
class Agendamento:
    def __init__(self, data, inicio, termino, participante, id=None):
        self.id = id
        self.data = data
        self.inicio = inicio
        self.termino = termino
        self.participante = participante
        