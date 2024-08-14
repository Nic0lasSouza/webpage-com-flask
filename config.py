import os
SECRET_KEY= '123456'

SQLALCHEMY_DATABASE_URI= \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario='root',
        senha='123456789',
        servidor='127.0.0.1',
        database='jogoteca'
    )

UPLOAD_PATH =os.path.dirname(os.path.abspath(__file__))+ '/uploads'