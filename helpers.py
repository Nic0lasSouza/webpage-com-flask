import os
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField
from app import app

class FormularioJogo(FlaskForm):
    nome = StringField('Nome do jogo:', [validators.DataRequired(), validators.length(min=1, max=50)])
    categoria = StringField('Categoria:', [validators.DataRequired(), validators.length(min=1, max=40)])
    console = StringField('Console:', [validators.DataRequired(), validators.length(min=1, max=20)])
    salvar = SubmitField('salvar')
def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

    return 'capa_padrao.png'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.png':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))