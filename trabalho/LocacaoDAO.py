import sqlite3
from Locacao import Locacao

class LocacaoDAO:
    def __init__(self, db_path="locacao.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute('''CREATE TABLE IF NOT EXISTS locacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_nome TEXT NOT NULL,
            veiculo_id   INTEGER NOT NULL,
            data_inicio  TEXT NOT NULL,  -- ISO YYYY-MM-DD
            data_fim     TEXT,           -- ISO YYYY-MM-DD
            valor_total  REAL
        )''')
        self.conn.commit()

    def inserir(self, locacao: Locacao):
        cursor = self.conn.execute("""
            INSERT INTO locacoes (cliente_nome, veiculo_id, data_inicio, data_fim, valor_total)
            VALUES (?, ?, ?, ?, ?)
        """, (locacao.cliente_nome, locacao.veiculo_id, locacao.data_inicio, locacao.data_fim, locacao.valor_total))
        self.conn.commit()
        locacao.id = cursor.lastrowid
        return locacao

    def obter_por_id(self, locacao_id: int):
        row = self.conn.execute("SELECT * FROM locacoes WHERE id = ?", (locacao_id,)).fetchone()
        if not row:
            return None
        return Locacao(
            id=row["id"],
            cliente_nome=row["cliente_nome"],
            veiculo_id=row["veiculo_id"],
            data_inicio=row["data_inicio"],
            data_fim=row["data_fim"],
            valor_total=row["valor_total"]
        )

    def listar(self):
        rows = self.conn.execute("SELECT * FROM locacoes ORDER BY id").fetchall()
        return [
            Locacao(
                id=r["id"],
                cliente_nome=r["cliente_nome"],
                veiculo_id=r["veiculo_id"],
                data_inicio=r["data_inicio"],
                data_fim=r["data_fim"],
                valor_total=r["valor_total"]
            )
            for r in rows
        ]

    def atualizar(self, locacao: Locacao):
        if locacao.id is None:
            raise ValueError("ID da locação é obrigatório para atualizar.")
        self.conn.execute("""
            UPDATE locacoes
               SET cliente_nome = ?, veiculo_id = ?, data_inicio = ?, data_fim = ?, valor_total = ?
             WHERE id = ?
        """, (locacao.cliente_nome, locacao.veiculo_id, locacao.data_inicio, locacao.data_fim, locacao.valor_total, locacao.id))
        self.conn.commit()
        return locacao

    def atualizar_fim_valor(self, locacao_id: int, data_fim_iso: str, valor_total: float):
        self.conn.execute("""
            UPDATE locacoes
               SET data_fim = ?, valor_total = ?
             WHERE id = ?
        """, (data_fim_iso, valor_total, locacao_id))
        self.conn.commit()

    def deletar(self, locacao_id: int):
        self.conn.execute("DELETE FROM locacoes WHERE id = ?", (locacao_id,))  # tupla
        self.conn.commit()

    def fechar(self):
        self.conn.close()

    # ------- Utilitários de consulta úteis -------
    def listar_por_veiculo(self, veiculo_id: int):
        rows = self.conn.execute("SELECT * FROM locacoes WHERE veiculo_id = ? ORDER BY id", (veiculo_id,)).fetchall()
        return [
            Locacao(
                id=r["id"],
                cliente_nome=r["cliente_nome"],
                veiculo_id=r["veiculo_id"],
                data_inicio=r["data_inicio"],
                data_fim=r["data_fim"],
                valor_total=r["valor_total"]
            )
            for r in rows
        ]

    def obter_ativa_por_veiculo(self, veiculo_id: int):
        # “Ativa” = sem data_fim
        row = self.conn.execute("""
            SELECT * FROM locacoes
             WHERE veiculo_id = ? AND data_fim IS NULL
             ORDER BY id DESC
             LIMIT 1
        """, (veiculo_id,)).fetchone()
        if not row:
            return None
        return Locacao(
            id=row["id"],
            cliente_nome=row["cliente_nome"],
            veiculo_id=row["veiculo_id"],
            data_inicio=row["data_inicio"],
            data_fim=row["data_fim"],
            valor_total=row["valor_total"]
        )
