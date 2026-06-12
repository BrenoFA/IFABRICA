import webbrowser
from functools import wraps
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session
from model.pessoa import Operador, Supervisor
from model.login_senha import LoginSenha

# Inicializa a aplicação Flask
app = Flask(__name__)
app.secret_key = 'fabrica_pecas_sprint4_chave_secreta'

# =============================================================
# DADOS — Funcionários cadastrados no sistema
# =============================================================
operadores = [
    Operador(
        codigoPessoa=1,
        nome="Breno",
        identificacao="OP-2026",
        turno="Matutino",
        maquinaAtribuida="Impressora 3D",
        matricula="MAT-001",
        data_admissao="2023-03-15"
    ),
    Operador(
        codigoPessoa=2,
        nome="Ana",
        identificacao="OP-2027",
        turno="Vespertino",
        maquinaAtribuida="Torno CNC",
        matricula="MAT-002",
        data_admissao="2023-07-20"
    ),
]

supervisores = [
    Supervisor(
        codigoPessoa=3,
        nome="ElPepe",
        identificacao="SUP-1010",
        turno="Integral",
        setor="Tecnologia da Informação",
        matricula="MAT-003",
        data_admissao="2022-01-10"
    ),
    Supervisor(
        codigoPessoa=4,
        nome="Carlos",
        identificacao="SUP-1011",
        turno="Matutino",
        setor="Produção",
        matricula="MAT-004",
        data_admissao="2021-06-01"
    ),
]

# =============================================================
# CREDENCIAIS — Lista de LoginSenha (composição com Funcionario)
# Formato: LoginSenha(usuario, senha_em_texto, funcionario)
# =============================================================
credenciais = [
    LoginSenha("Breno",   "op2026", operadores[0]),
    LoginSenha("Ana",     "op2027", operadores[1]),
    LoginSenha("ElPepe",  "sup1010", supervisores[0]),
    LoginSenha("Carlos",  "sup1011", supervisores[1]),
]

print('--- VERIFICAÇÃO DIRETA ---')
for op in operadores:
    print(op.exibir_papel(), '| Menus:', op.menus_permitidos())
for sup in supervisores:
    print(sup.exibir_papel(), '| Menus:', sup.menus_permitidos())


# =============================================================
# DECORADOR — Protege rotas que exigem sessão ativa
# =============================================================
def login_required(f):
    @wraps(f)
    def verificar(*args, **kwargs):
        if 'funcionario_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return verificar


# =============================================================
# ROTA — Servir CSS estático
# =============================================================
@app.route('/css/<path:filename>')
def css(filename):
    return send_from_directory('css', filename)


# =============================================================
# ROTA — Login (GET exibe formulário / POST autentica)
# =============================================================
@app.route('/', methods=['GET', 'POST'])
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario_digitado = request.form.get('usuario', '').strip()
        senha_digitada   = request.form.get('senha', '').strip()

        # Validação de campos vazios ou curtos (camada Controller)
        if len(usuario_digitado) < 3 or len(senha_digitada) < 4:
            return render_template('login.html', erro='Preencha usuário e senha corretamente.')

        # Percorre as credenciais e verifica com hash
        for cred in credenciais:
            if usuario_digitado == cred.get_usuario() and cred.verificar_senha(senha_digitada):
                func = cred.get_funcionario()
                # Salva dados na sessão
                session['funcionario_id']   = func.get_codigoPessoa()
                session['funcionario_nome'] = func.get_nome()
                session['menus']            = func.menus_permitidos()
                return redirect(url_for('principal'))

        # Credenciais não encontradas
        return render_template('login.html', erro='Usuário ou senha inválidos.')

    # GET: exibe o formulário limpo
    return render_template('login.html')


# =============================================================
# ROTA — Logout: limpa sessão e redireciona ao login
# =============================================================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# =============================================================
# ROTA — Página principal (protegida)
# =============================================================
@app.route('/principal')
@app.route('/principal.html')
@login_required
def principal():
    return render_template(
        'principal.html',
        usuario=session.get('funcionario_nome'),
        menus=session.get('menus', []),
        operadores=operadores,
        supervisores=supervisores
    )


# =============================================================
# ROTA — Administração (protegida + autorização por papel)
# =============================================================
@app.route('/admin')
@app.route('/admin.html')
@login_required
def admin():
    if 'admin' not in session.get('menus', []):
        return redirect(url_for('principal'))
    return render_template('admin.html')


# =============================================================
# DEMAIS ROTAS (protegidas por login_required)
# =============================================================
@app.route('/cargos')
@app.route('/cargos.html')
@login_required
def cargos():
    return render_template('cargos.html')

@app.route('/departamentos')
@app.route('/departamentos.html')
@login_required
def departamentos():
    return render_template('departamentos.html')

@app.route('/fornecedores')
@app.route('/fornecedores.html')
@login_required
def fornecedores():
    return render_template('fornecedores.html')

@app.route('/funcionarios')
@app.route('/funcionarios.html')
@login_required
def funcionarios():
    return render_template('funcionarios.html')

@app.route('/crudfuncionarios')
@app.route('/crudfuncionarios.html')
@login_required
def crudfuncionarios():
    return render_template('crudfuncionarios.html', operadores=operadores)

@app.route('/setores')
@app.route('/setores.html')
@login_required
def setores():
    return render_template('setores.html')


# =============================================================
# Inicia o servidor em modo de desenvolvimento
# =============================================================
if __name__ == '__main__':
    #webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=True)