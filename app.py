#INSTALAR pip install flask-sqlalchemy==2.5.1 E IMPORTAR
#PARA INICIAR O AMBIENTE VIRTUAL.venv\Scripts\activate 
from flask import Flask
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
#INSTANCIANDO O DB 
db = SQLAlchemy(app)


if __name__ == "__main__":
    app.run(debug=True)