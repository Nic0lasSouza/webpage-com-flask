from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from app import app, db
from models import Jogos,Usuarios
from helpers import recupera_imagem

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
    #ANALISAR SE JA POSSUI O JOGO NA LISTA
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

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}.jpg')
    return redirect(url_for('index'))

@app.route('/edit/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('edit')))
    jogo =Jogos.query.filter_by(id=id).first()
    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', titulo = 'Editando jogo', jogo=jogo, capa_jogo=capa_jogo)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    jogo =Jogos.query.filter_by(id=request.form['id']).first()
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']

    db.session.add(jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    arquivo.save(f'{upload_path}/capa{jogo.id}.jpg')
    return redirect(url_for('index'))

@app.route('/deletar<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    
    jogo = Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo {} deletado com sucesso'.format(jogo))
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

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

