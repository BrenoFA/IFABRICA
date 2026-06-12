from werkzeug.security import generate_password_hash, check_password_hash

# =============================================================
# LoginSenha — composição com Funcionario
# Atributos: usuario, senha_hash, funcionario
# =============================================================
class LoginSenha:
    def __init__(self, usuario, senha, funcionario):
        # --- Validações no construtor ---
        if not usuario or len(usuario.strip()) < 3:
            raise ValueError("Usuário deve ter no mínimo 3 caracteres.")
        if not senha or len(senha) < 4:
            raise ValueError("Senha deve ter no mínimo 4 caracteres.")
        if funcionario is None:
            raise ValueError("O funcionário vinculado não pode ser None.")

        self.usuario = usuario.strip()
        self.senha_hash = generate_password_hash(senha)
        self.funcionario = funcionario

    # GETTERS E SETTERS
    def get_usuario(self):
        return self.usuario

    def set_usuario(self, usuario):
        if not usuario or len(usuario.strip()) < 3:
            raise ValueError("Usuário deve ter no mínimo 3 caracteres.")
        self.usuario = usuario.strip()

    def get_senha_hash(self):
        return self.senha_hash

    def get_funcionario(self):
        return self.funcionario

    def set_funcionario(self, funcionario):
        if funcionario is None:
            raise ValueError("O funcionário vinculado não pode ser None.")
        self.funcionario = funcionario

    def verificar_senha(self, senha_digitada):
        """Compara a senha digitada com o hash armazenado."""
        return check_password_hash(self.senha_hash, senha_digitada)
