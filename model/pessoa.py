from abc import ABC, abstractmethod

# =============================================================
# Classe base abstrata — atributos: codigoPessoa, nome, turno
# =============================================================
class Pessoa(ABC):
    def __init__(self, codigoPessoa, nome, turno):
        if not nome or len(nome.strip()) < 2:
            raise ValueError("Nome deve ter ao menos 2 caracteres.")
        self.codigoPessoa = codigoPessoa
        self.nome = nome
        self.turno = turno

    # GETTERS E SETTERS
    def get_codigoPessoa(self):
        return self.codigoPessoa

    def set_codigoPessoa(self, codigoPessoa):
        self.codigoPessoa = codigoPessoa

    def get_nome(self):
        return self.nome

    def set_nome(self, nome):
        self.nome = nome

    def get_turno(self):
        return self.turno

    def set_turno(self, turno):
        self.turno = turno

    @abstractmethod
    def exibir_papel(self):
        """
        Método abstrato.
        Qualquer classe concreta que herdar de Pessoa é obrigada
        a implementar este método com sua própria lógica.
        """
        pass


# =============================================================
# Classe intermediária concreta — atributos: identificacao,
# matricula, data_admissao
# =============================================================
class Funcionario(Pessoa):
    def __init__(self, codigoPessoa, nome, turno, identificacao, matricula, data_admissao):
        super().__init__(codigoPessoa, nome, turno)
        self.identificacao = identificacao
        self.matricula = matricula
        self.data_admissao = data_admissao

    # GETTERS E SETTERS
    def get_identificacao(self):
        return self.identificacao

    def set_identificacao(self, identificacao):
        self.identificacao = identificacao

    def get_matricula(self):
        return self.matricula

    def set_matricula(self, matricula):
        self.matricula = matricula

    def get_data_admissao(self):
        return self.data_admissao

    def set_data_admissao(self, data_admissao):
        self.data_admissao = data_admissao

    def menus_permitidos(self):
        """Retorna lista vazia na classe base — sobrescrito nas subclasses."""
        return []

    def exibir_papel(self):
        return f"Funcionário {self.nome} (Matrícula: {self.matricula})"


# =============================================================
# Operador — atributo específico: maquinaAtribuida
# =============================================================
class Operador(Funcionario):
    def __init__(self, codigoPessoa, nome, identificacao, turno, maquinaAtribuida,
                 matricula="OP-MAT", data_admissao="2024-01-01"):
        super().__init__(codigoPessoa, nome, turno, identificacao, matricula, data_admissao)
        self.maquinaAtribuida = maquinaAtribuida

    def get_maquinaAtribuida(self):
        return self.maquinaAtribuida

    def set_maquinaAtribuida(self, maquinaAtribuida):
        self.maquinaAtribuida = maquinaAtribuida

    def menus_permitidos(self):
        """Operador acessa apenas o menu principal e produção."""
        return ['principal', 'producao']

    def exibir_papel(self):
        return f"Operador(a) {self.nome} - Máquina: {self.maquinaAtribuida} (Turno: {self.turno})"


# =============================================================
# Supervisor — atributo específico: setor
# =============================================================
class Supervisor(Funcionario):
    def __init__(self, codigoPessoa, nome, identificacao, turno, setor,
                 matricula="SUP-MAT", data_admissao="2024-01-01"):
        super().__init__(codigoPessoa, nome, turno, identificacao, matricula, data_admissao)
        self.setor = setor

    def get_setor(self):
        return self.setor

    def set_setor(self, setor):
        self.setor = setor

    def menus_permitidos(self):
        """Supervisor acessa menus administrativos completos."""
        return ['principal', 'admin', 'departamentos', 'cargos', 'crudcargos']

    def exibir_papel(self):
        return f"Supervisor(a) {self.nome} - Setor: {self.setor} (Turno: {self.turno})"