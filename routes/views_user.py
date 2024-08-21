from flask import render_template, request, redirect, session, flash, url_for
from app import app
from db.models import Usuarios
from helpers import FormularioUsuario

@app.route('/login')
def login():
    form = FormularioUsuario()
    proxima = request.args.get('proxima')
    
    return render_template('login.html', proxima=proxima, form=form)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    form = FormularioUsuario(request.form)
    
    #AQUI VAI CONFERIR SE O USUARIO QUE VAI SE LOGAR CONSTA NO BANCO
    usuario = Usuarios.query.filter_by(nickname=form.nome.data).first()
    if usuario:
        if form.senha.data == usuario.senha:
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
