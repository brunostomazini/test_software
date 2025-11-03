from datetime import datetime
from agendamento import Agendamento

class AgendamentoService:
    def __init__(self, dao):
        self.dao = dao

    def cadastrar_agendamento(self, data, inicio, termino, participante):
        if not participante or participante.strip() == "":
            raise ValueError("Nome invalido, campo em branco!")
        try:
            hora_inicio = datetime.strptime(inicio, "%H:%M").time()
            hora_fim = datetime.strptime(termino, "%H:%M").time()
        except:
            raise ValueError("Horario invalido")
        
        if hora_fim <= hora_inicio:
            raise ValueError("Horario invalido")
        
        agendados = self.dao.listar_todos()
        for agend in agendados:
            if agend.participante == participante and data == agend.data:
                if not (hora_fim <= datetime.strptime(agend.inicio, "%H:%M").time() or hora_inicio >= datetime.strptime(agend.termino, "%H:%M").time()):
                    raise ValueError("Conflito de horário")

        novo_agendamento = Agendamento(data, inicio, termino, participante)
        self.dao.inserir(novo_agendamento)
        return novo_agendamento

    def buscar_por_id(self, id):
        agendamento = self.dao.buscar_por_id(id)
        if not agendamento:
            raise ValueError("Agendamento não encontrado.")
        return agendamento

    def listar_todos(self):
        return self.dao.listar_todos()

    def atualizar_agendamento(self, id, data, inicio, termino, participante):
        # Verifica se o agendamento existe
        agendamento_existente = self.dao.buscar_por_id(id)
        if not agendamento_existente:
            raise ValueError("Agendamento não encontrado para atualização.")

        if not participante or participante.strip() == "":
            raise ValueError("O campo participante não pode estar em branco.")

        try:
            hora_inicio = datetime.strptime(inicio, "%H:%M").time()
            hora_termino = datetime.strptime(termino, "%H:%M").time()
        except ValueError:
            raise ValueError("Horário inválido. Use o formato HH:MM.")

        if hora_inicio >= hora_termino:
            raise ValueError("O horário de início deve ser anterior ao término.")

        # Verificar conflitos (ignorando o próprio agendamento)
        agendamentos_existentes = self.dao.listar_todos()
        for ag in agendamentos_existentes:
            if ag.participante == participante and ag.data == data and ag.id != id:
                if not (hora_termino <= datetime.strptime(ag.inicio, "%H:%M").time() or
                        hora_inicio >= datetime.strptime(ag.termino, "%H:%M").time()):
                    raise ValueError("Conflito de horário para este participante.")

        agendamento_atualizado = Agendamento(data, inicio, termino, participante, id)
        self.dao.atualizar(agendamento_atualizado)
        return agendamento_atualizado

    def excluir_agendamento(self, id):
        agendamento = self.dao.buscar_por_id(id)
        if not agendamento:
            raise ValueError("Agendamento não encontrado para exclusão.")
        self.dao.excluir(id)

    def fechar_conexao(self):
        self.dao.fechar()