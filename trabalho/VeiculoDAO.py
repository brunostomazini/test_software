import sqlite3
from Veiculo import Veiculo
from DB import conecao;
class VeiculoDAO:
    def __init__(self, conn=conecao):
        self.conn = conn
        self.conn.row_factory = sqlite3.Row
        self.conn.execute('''CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modelo TEXT,
            placa TEXT,
            ano INTEGER,
            diaria REAL,
            disponivel INTEGER
        )''')

    def inserir(self, veiculo):
        cursor = self.conn.execute("""
            INSERT INTO veiculos (modelo, placa, ano, diaria, disponivel)
            VALUES (?, ?, ?, ?, ?)
        """, (veiculo.modelo, veiculo.placa, veiculo.ano, veiculo.diaria, int(bool(veiculo.disponivel))))
        self.conn.commit()
        veiculo.id = cursor.lastrowid
        return veiculo

    def obter_por_id(self, veiculo_id):
        # (veiculo_id,) é tupla
        row = self.conn.execute("SELECT * FROM veiculos WHERE id = ?", (veiculo_id,)).fetchone()
        if not row:
            return None
        return Veiculo(
            id=row["id"],
            modelo=row["modelo"],
            placa=row["placa"],
            ano=row["ano"],
            diaria=row["diaria"],
            disponivel=bool(row["disponivel"])
        )

    def obter_por_placa(self, placa):
        row = self.conn.execute("SELECT * FROM veiculos WHERE placa = ?", (placa,)).fetchone()
        if not row:
            return None
        return Veiculo(
            id=row["id"],
            modelo=row["modelo"],
            placa=row["placa"],
            ano=row["ano"],
            diaria=row["diaria"],
            disponivel=bool(row["disponivel"])
        )

    def listar(self):
        rows = self.conn.execute("SELECT * FROM veiculos ORDER BY id").fetchall()
        return [
            Veiculo(
                id=r["id"],
                modelo=r["modelo"],
                placa=r["placa"],
                ano=r["ano"],
                diaria=r["diaria"],
                disponivel=bool(r["disponivel"])
            )
            for r in rows
        ]

    def atualizar(self, veiculo):
        if veiculo.id is None:
            raise ValueError("ID do veículo é obrigatório para atualizar.")
        self.conn.execute("""
            UPDATE veiculos
               SET modelo = ?, placa = ?, ano = ?, diaria = ?, disponivel = ?
             WHERE id = ?
        """, (veiculo.modelo, veiculo.placa, veiculo.ano, veiculo.diaria, int(bool(veiculo.disponivel)), veiculo.id))
        self.conn.commit()
        return veiculo

    def deletar(self, veiculo_id):
        self.conn.execute("DELETE FROM veiculos WHERE id = ?", (veiculo_id,))  # tupla
        self.conn.commit()

