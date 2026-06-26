import webbrowser
from functools import wraps
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from model.database import inicializar_banco
from model.repositorios.funcionario_repo import FuncionarioRepository
from model.repositorios.login_senha_repo import LoginSenhaRepository

# Inicializa a aplicação Flask
app = Flask(__name__)
app.secret_key = 'fabrica_pecas_sprint4_chave_secreta'

# =============================================================
# BANCO DE DADOS E REPOSITÓRIOS
# =============================================================
inicializar_banco()
funcionario_repo = FuncionarioRepository()
login_repo = LoginSenhaRepository()


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

        # Busca credenciais no banco e verifica o hash da senha
        dados_login = login_repo.buscar_por_usuario(usuario_digitado)
        if dados_login and check_password_hash(dados_login['senha_hash'], senha_digitada):
            func = dados_login['funcionario']
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
    operadores_db = funcionario_repo.listar_operadores()
    supervisores_db = funcionario_repo.listar_supervisores()
    return render_template(
        'principal.html',
        usuario=session.get('funcionario_nome'),
        menus=session.get('menus', []),
        operadores=operadores_db,
        supervisores=supervisores_db
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
    operadores_db = funcionario_repo.listar_operadores()
    return render_template('crudfuncionarios.html', operadores=operadores_db)

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