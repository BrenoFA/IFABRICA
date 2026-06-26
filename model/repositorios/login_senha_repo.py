from model.database import conectar
from model.repositorios.funcionario_repo import FuncionarioRepository

class LoginSenhaRepository:
    def __init__(self):
        self.funcionario_repo = FuncionarioRepository()
        
    def buscar_por_usuario(self, usuario):
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT senha_hash, funcionario_id
                FROM login_senha
                WHERE usuario = ?
            ''', (usuario,))
            row = cursor.fetchone()
            
            if row:
                funcionario = self.funcionario_repo.buscar_por_id(row['funcionario_id'])
                if funcionario:
                    return {
                        'senha_hash': row['senha_hash'],
                        'funcionario': funcionario
                    }
        return None
