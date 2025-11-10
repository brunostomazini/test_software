# db.py
import sqlite3
conecao: sqlite3.Connection = sqlite3.connect("base.db") 
conecao.row_factory = sqlite3.Row