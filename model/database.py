import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fabrica.db')
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'schema.sql')

def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def inicializar_banco():
    banco_existe = os.path.exists(DB_PATH)
    
    with conectar() as conn:
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
    
    if not banco_existe:
        popular_dados_iniciais()

def popular_dados_iniciais():
    with conectar() as conn:
        cursor = conn.cursor()
        
        # Inserir Carlos (Operador)
        cursor.execute('''
            INSERT INTO funcionarios (codigo_pessoa, nome, identificacao, turno, matricula, data_admissao)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (1, 'Carlos', 'OP-001', 'Matutino', 'MAT-OP-1', '2024-01-01'))
        carlos_id = cursor.lastrowid
        
        cursor.execute('''
            INSERT INTO operadores (funcionario_id, codigo_operador, funcao, setor, maquina_responsavel)
            VALUES (?, ?, ?, ?, ?)
        ''', (carlos_id, 101, 'Operador CNC', 'Produção', 'Torno CNC 01'))
        
        # Inserir Ana (Operadora)
        cursor.execute('''
            INSERT INTO funcionarios (codigo_pessoa, nome, identificacao, turno, matricula, data_admissao)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (2, 'Ana', 'OP-002', 'Vespertino', 'MAT-OP-2', '2024-02-01'))
        ana_id = cursor.lastrowid
        
        cursor.execute('''
            INSERT INTO operadores (funcionario_id, codigo_operador, funcao, setor, maquina_responsavel)
            VALUES (?, ?, ?, ?, ?)
        ''', (ana_id, 102, 'Operadora 3D', 'Impressão', 'Impressora 3D 02'))
        
        # Inserir Joao (Supervisor)
        cursor.execute('''
            INSERT INTO funcionarios (codigo_pessoa, nome, identificacao, turno, matricula, data_admissao)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (3, 'Joao', 'SUP-001', 'Integral', 'MAT-SUP-1', '2023-01-01'))
        joao_id = cursor.lastrowid
        
        cursor.execute('''
            INSERT INTO supervisores (funcionario_id, codigo_supervisor, nivel_responsabilidade, setor, turno_supervisionado)
            VALUES (?, ?, ?, ?, ?)
        ''', (joao_id, 201, 'Alta', 'Geral', 'Integral'))
        
        senha_hash = generate_password_hash('123456')
        
        # Credenciais
        cursor.execute('''
            INSERT INTO login_senha (usuario, senha_hash, funcionario_id)
            VALUES (?, ?, ?)
        ''', ('Carlos', senha_hash, carlos_id))
        
        cursor.execute('''
            INSERT INTO login_senha (usuario, senha_hash, funcionario_id)
            VALUES (?, ?, ?)
        ''', ('Ana', senha_hash, ana_id))
        
        cursor.execute('''
            INSERT INTO login_senha (usuario, senha_hash, funcionario_id)
            VALUES (?, ?, ?)
        ''', ('Joao', senha_hash, joao_id))
        
        conn.commit()
