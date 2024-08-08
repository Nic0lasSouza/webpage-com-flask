#INSTALAR pip install flask-sqlalchemy==2.5.1 E IMPORTAR
#PARA INICIAR O AMBIENTE VIRTUAL.venv\Scripts\activate 
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
class Jogo:
    def __init__(self, nome, categoria, console, preco):
        self.nome = nome
        self.categoria = categoria
        self.console = console
        #self.preco = preco

jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of War', 'Rack n slash', 'PS2')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2')
lista_jogo = [jogo1, jogo2, jogo3]


class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nick = nickname
        self.senha = senha

usuario1 = Usuario("admin", "adm", "admin")
usuario2 = Usuario("nicolas", "ns", "nicolas")
usuario3 = Usuario("silvio", "ss", "silvio")

usuarios = {
    usuario1.nick : usuario1,
    usuario2.nick : usuario2,
    usuario3.nick : usuario3,
    }
app = Flask(__name__)
app.secret_key = '123456'

app.config('SQLALCHEMY_DATABASE_URI') = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario='root',
        senha='123456789',
        servidor='127.0.0.1',
        database='jogoteca'
    )

db = SQLAlchemy(app)



@app.route('/')
def index():
    return render_template('index.html', titulo = 'Jogos', jogos = lista_jogo)

@app.route('/new')
def new():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('new')))
    else:
        return render_template('add_game.html', titulo = 'Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    #preco = request.form['preco']
    jogo = Jogo(nome, categoria, console)
    lista_jogo.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nome
            flash(usuario.nome + ' '+ '  logado com sucesso')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)

    #if 'admin' == request.form['senha']:
    #    session['usuario_logado'] = request.form['usuario']
    #    flash(session['usuario_logado'] + ' '+ '  logado com sucesso')
    #    proxima_pagina = request.form['proxima']
    #   return redirect(proxima_pagina)
    else:
        flash('Usuário não logado')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)