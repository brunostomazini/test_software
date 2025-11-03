import sqlite3
from agendamento import Agendamento

class AgendamentoDAO:
    def __init__(self, db_name="agendamentos.db"):
        self.conn = sqlite3.connect(db_name)
        self._criar_tabela()

    def _criar_tabela(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS agendamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                inicio TEXT NOT NULL,
                termino TEXT NOT NULL,
                participante TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def inserir(self, agendamento):
        cur = self.conn.cursor()
        cur.execute('''
            INSERT INTO agendamentos (data, inicio, termino, participante)
            VALUES (?, ?, ?, ?)
        ''', (agendamento.data, agendamento.inicio, agendamento.termino, agendamento.participante))
        self.conn.commit()
        agendamento.id = cur.lastrowid
        return agendamento.id

    def buscar_por_id(self, id):
        cur = self.conn.cursor()
        cur.execute('SELECT id, data, inicio, termino, participante FROM agendamentos WHERE id = ?', (id,))
        row = cur.fetchone()
        return Agendamento(*row[1:], id=row[0]) if row else None

    def listar_todos(self):
        cur = self.conn.cursor()
        cur.execute('SELECT id, data, inicio, termino, participante FROM agendamentos')
        return [Agendamento(id=row[0], data=row[1], inicio=row[2], termino=row[3], participante=row[4])
                for row in cur.fetchall()]

    def atualizar(self, agendamento):
        cur = self.conn.cursor()
        cur.execute('''
            UPDATE agendamentos
            SET data = ?, inicio = ?, termino = ?, participante = ?
            WHERE id = ?
        ''', (agendamento.data, agendamento.inicio, agendamento.termino, agendamento.participante, agendamento.id))
        self.conn.commit()
        if cur.rowcount == 0:
            raise ValueError("Agendamento não encontrado para atualização.")

    def excluir(self, id):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM agendamentos WHERE id = ?', (id,))
        self.conn.commit()
        if cur.rowcount == 0:
            raise ValueError("Agendamento não encontrado para exclusão.")

    def fechar(self):
        self.conn.close()
