#INSTALAR pip install flask-sqlalchemy==2.5.1 E IMPORTAR
#PARA INICIAR O AMBIENTE VIRTUAL.venv\Scripts\activate 
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = '123456'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario='root',
        senha='123456789',
        servidor='127.0.0.1',
        database='jogoteca'
    )

db = SQLAlchemy(app)
class Jogos(db.Model):
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    nome= db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    #CRIANDO FUNCAO DE INICIACAO
    def __repr__(self):
        return '<Name %r>'% self.nome
    
class Usuarios(db.Model):
    nickname=db.Column(db.String(8), primary_key=True,)
    nome= db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    #CRIANDO FUNCAO DE INICIACAO
    def __repr__(self):
        return '<Name %r>'% self.nome


@app.route('/')
def index():
    #PEGAR OS JOGOS E FAZER UMA QUERY, ORDENAR A LISTA PELO ID
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('index.html', titulo = 'Jogos', jogos = lista)

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
    
    jogo = Jogos.query.filter_by(nome=nome).first()
    #ANALISAR SE OJA POSSUI O JOGO NA LISTA
    if jogo:
        flash('Jogo já existe na lista')
        return redirect(url_for('index'))
    else:
        #INCLUSÃO DE NOVO JOGO
        novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
        #INCLUIR ELE NO BANCO DE DADOS
        db.session.add(novo_jogo)
        #COMITANDO O JOGO NO BANCO DE DADOS
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    #AQUI VAI CONFERIR SE O USUARIO QUE VAI SE LOGAR CONSTA NO BANCO
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
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