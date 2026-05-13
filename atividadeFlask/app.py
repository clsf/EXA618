from flask import Flask, request, make_response, session, redirect, url_for, render_template_string

app = Flask(__name__)

app.secret_key = "minha_chave_secreta"

usuario_cadastrado = ""
senha_cadastrada = ""

@app.route("/")
def home():

    nome = request.cookies.get("nome")

    if nome:
        saudacao = f"Olá, {nome}!"
    else:
        saudacao = "Olá, visitante!"

    visitas = request.cookies.get("visitas")

    if visitas:
        visitas = int(visitas) + 1
    else:
        visitas = 1

    resposta = make_response(f"""
        <h1>{saudacao}</h1>
        <h2>Você visitou esta página {visitas} vezes.</h2>

        <a href="/login">Login</a><br>
        <a href="/cadastro">Cadastrar</a>
    """)

    resposta.set_cookie("visitas", str(visitas))

    return resposta


@app.route("/nome/<nome>")
def salvar_nome(nome):

    resposta = make_response(f"""
        <h1>Nome {nome} salvo com sucesso!</h1>
        <a href="/">Voltar</a>
    """)

    resposta.set_cookie("nome", nome)

    return resposta



USUARIO = "admin"
SENHA = "123"


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        if usuario == USUARIO and senha == SENHA or usuario == usuario_cadastrado and senha == senha_cadastrada:

            session["usuario"] = usuario

            return redirect(url_for("perfil"))

        else:
            return """
                <h1>Usuário ou senha inválidos!</h1>
                <a href="/login">Tentar novamente</a><br>
                <a href="/cadastro">Cadastrar</a>
            """

    return render_template_string("""
        <h1>Login</h1>

        <form method="POST">
            Usuário:
            <input type="text" name="usuario"><br><br>

            Senha:
            <input type="password" name="senha"><br><br>

            <button type="submit">Entrar</button>
        </form>
    """)


@app.route("/perfil")
def perfil():

    if "usuario" not in session:
        return redirect(url_for("login"))

    usuario = session["usuario"]

    return f"""
        <h1>Perfil do usuário</h1>

        <h2>Bem-vindo, {usuario}!</h2>

        <a href="/logout">Logout</a>
    """


@app.route("/logout")
def logout():

    session.pop("usuario", None)

    return redirect(url_for("login"))

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    global usuario_cadastrado
    global senha_cadastrada

    if request.method == "POST":

        usuario_cadastrado = request.form.get("usuario")
        senha_cadastrada = request.form.get("senha")

        return redirect(url_for("login"))

    return render_template_string("""
        <h1>Cadastro</h1>

        <form method="POST">

            <label>Nome:</label><br>
            <input type="text" name="usuario"><br><br>

            <label>Senha:</label><br>
            <input type="password" name="senha"><br><br>

            <button type="submit">Cadastrar</button>

        </form>
    """)
