from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from app import app, db
from db.models import Jogos
from helpers import recupera_imagem,deleta_arquivo, FormularioJogo
import time

@app.route('/')
def index():
    #PEGAR OS JOGOS E FAZER UMA QUERY, ORDENAR A LISTA PELO ID
    lista = Jogos.query.order_by(Jogos.id).all()

    for jogo in lista:
        jogo.imagem = recupera_imagem(jogo.id)
    
    return render_template('index.html', titulo = 'Lista de Jogos', jogos = lista)


@app.route('/new')
def new():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('new')))
    
    form = FormularioJogo()
    return render_template('add_game.html', titulo = 'Novo Jogo', form=form)

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
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg')
    flash('Jogo criado com sucesso')
    return redirect(url_for('index'))


@app.route('/edit/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('edit')))
    jogo =Jogos.query.filter_by(id=id).first()
    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    
    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', titulo = 'Editando jogo', id=id, capa_jogo=capa_jogo, form =form)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioJogo(request.form)
    if form.validate_on_submit():
        jogo =Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data

        db.session.add(jogo)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(jogo.id)
        arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')
        flash('Jogo editado com sucesso')
    return redirect(url_for('index'))

@app.route('/deletar<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    jogo = Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo deletado com sucesso')
    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)