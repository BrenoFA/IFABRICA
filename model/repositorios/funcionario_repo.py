import sqlite3
from model.database import conectar
from model.pessoa import Operador, Supervisor

class FuncionarioRepository:
    def buscar_por_id(self, id):
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT f.*, o.maquina_responsavel, s.setor as setor_supervisor
                FROM funcionarios f
                LEFT JOIN operadores o ON f.id = o.funcionario_id
                LEFT JOIN supervisores s ON f.id = s.funcionario_id
                WHERE f.id = ?
            ''', (id,))
            row = cursor.fetchone()
            
            if row:
                codigo_pessoa = row['codigo_pessoa']
                nome = row['nome']
                identificacao = row['identificacao']
                turno = row['turno']
                matricula = row['matricula']
                data_admissao = row['data_admissao']
                
                if row['maquina_responsavel']:
                    return Operador(
                        codigoPessoa=codigo_pessoa, 
                        nome=nome, 
                        identificacao=identificacao, 
                        turno=turno, 
                        maquinaAtribuida=row['maquina_responsavel'],
                        matricula=matricula,
                        data_admissao=data_admissao
                    )
                elif row['setor_supervisor']:
                    return Supervisor(
                        codigoPessoa=codigo_pessoa, 
                        nome=nome, 
                        identificacao=identificacao, 
                        turno=turno, 
                        setor=row['setor_supervisor'],
                        matricula=matricula,
                        data_admissao=data_admissao
                    )
        return None

    def listar_operadores(self):
        operadores = []
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT f.*, o.maquina_responsavel
                FROM funcionarios f
                INNER JOIN operadores o ON f.id = o.funcionario_id
            ''')
            rows = cursor.fetchall()
            for row in rows:
                operadores.append(Operador(
                    codigoPessoa=row['codigo_pessoa'],
                    nome=row['nome'],
                    identificacao=row['identificacao'],
                    turno=row['turno'],
                    maquinaAtribuida=row['maquina_responsavel'],
                    matricula=row['matricula'],
                    data_admissao=row['data_admissao']
                ))
        return operadores
        
    def listar_supervisores(self):
        supervisores = []
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT f.*, s.setor as setor_supervisor
                FROM funcionarios f
                INNER JOIN supervisores s ON f.id = s.funcionario_id
            ''')
            rows = cursor.fetchall()
            for row in rows:
                supervisores.append(Supervisor(
                    codigoPessoa=row['codigo_pessoa'],
                    nome=row['nome'],
                    identificacao=row['identificacao'],
                    turno=row['turno'],
                    setor=row['setor_supervisor'],
                    matricula=row['matricula'],
                    data_admissao=row['data_admissao']
                ))
        return supervisores
