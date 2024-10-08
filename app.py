#INSTALAR pip install flask-sqlalchemy==2.5.1 E IMPORTAR
#PARA INICIAR O AMBIENTE VIRTUAL.venv\Scripts\activate 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.config.from_pyfile('config.py')
#INSTANCIANDO O DB 
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

from routes.views_games import *
from routes.views_user import *
if __name__ == "__main__":
    app.run(debug=True)