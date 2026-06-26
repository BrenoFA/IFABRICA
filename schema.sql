CREATE TABLE IF NOT EXISTS funcionarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_pessoa INTEGER UNIQUE NOT NULL,
    nome TEXT NOT NULL,
    identificacao TEXT NOT NULL,
    turno TEXT NOT NULL,
    matricula TEXT UNIQUE NOT NULL,
    data_admissao TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS operadores (
    funcionario_id INTEGER PRIMARY KEY,
    codigo_operador INTEGER UNIQUE NOT NULL,
    funcao TEXT,
    setor TEXT,
    maquina_responsavel TEXT,
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS supervisores (
    funcionario_id INTEGER PRIMARY KEY,
    codigo_supervisor INTEGER UNIQUE NOT NULL,
    nivel_responsabilidade TEXT,
    setor TEXT,
    turno_supervisionado TEXT,
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS login_senha (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    senha_hash TEXT NOT NULL,
    funcionario_id INTEGER UNIQUE NOT NULL,
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id) ON DELETE CASCADE
);
