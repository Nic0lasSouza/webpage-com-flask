#IMPORTANDO A BIBLIOTECA MYSQL CONNECTOR

import mysql.connector
from mysql.connector import errorcode

print("Conectando ao banco.....")
#TENTATIVA DE CONEXÃO COM O BANCO DE DADOS
try:
    #TENTANDO ESTABELECER UMA CONEXÃO COM O BANCO
    cnx = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='123456789',
        )
    #TRATAMENTOS DE ERROS
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo de errado no nome de usuário ou senha')
    else:
        print(err)

#UM OBJETO QUE PERMITE EXECUTAR COMANDOS SQL
cursor = cnx.cursor()

#EXECUTANDO O COMANDO SQL REMOVENDO O BANCO DE DADOS CASO ELE EXISTA
cursor.execute("DROP DATABASE IF EXISTS jogoteca;")

#EXECUTANDO O COMANDO SQL CRIANDO O BANCO DE DADOS
cursor.execute("CREATE DATABASE jogoteca;")

#EXECUTANDO O COMANDO SQL DEFINE O BANCO DE DADOS COM O ATUAL PARA AS OPERAÇÕES
cursor.execute("USE jogoteca;")

#CRIACAO DE TABELAS 
TABLES = {}

#DEFINE A TABELA JOGOS COM COLUNAS ID,NOME,CATEGORIA,CONSOLE E O ID AUTO INCREMENTAVEL
TABLES['jogos']=('''
    CREATE TABLE `jogos`(
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `nome` varchar(50) NOT NULL,
        `categoria` varchar(40) NOT NULL,
        `console` varchar(20) NOT NULL,
        PRIMARY KEY (`id`)           
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

#DEFINE A TABELA USUARIOS NOME, NICKNAME E SENHA SENDO O NICKNAME A CHAVE PRIMARIA
TABLES['usuarios']=('''
    CREATE TABLE `usuarios`(
        `nome` varchar(20) NOT NULL,
        `nickname` varchar(8) NOT NULL,
        `senha` varchar(100) NOT NULl,
        PRIMARY KEY (`nickname`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
    #EXECUTANDO O COMANDO SQL CRIANDO A TABELA(PARA CADA TABELA DEFINIDA TENTA CRIAR NO BANCO)
    tabela_sql = TABLES[tabela_nome]
    #TENTA CRIAR TABELA NO BANCO DE DADOS
    try:
        print('Criando tabela {}:'.format(tabela_nome), end=' ')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as erro:
        #INDICA ERRO QUE A TABELA JA EXISTE
        if erro.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Tabela {} já existe'.format(tabela_nome))
        #OUTROS ERROS IMPRESSOS NA TELA
        else:
            print(erro.msg)
    
    else:
        print('OK')

#INSERINDO DADOS NAS TABELAS
#COMANDO SQL PARA INSERIR DADOS NA TABELA USUARIOS
usuarios_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios =[
    ('João', 'joao', '123'),
    ('Maria', 'maria', '456'),
    ('Pedro', 'pedro', '789')
]
#EXECUTA O COMANDO SQL PARA CADA USUARIO DA LISTA USUARIOS
cursor.executemany(usuarios_sql,usuarios)
#EXECUTA UM COMANDO SQL PARA SELECIONAR TODOS OS DADOS DA TABELA USUARIOS
cursor.execute('select * from jogoteca.usuarios')
print('-------------  Usuários:  -------------')
#RECUPERA TODOS OS RESULTADOS DA SELEÇÃO
for user in cursor.fetchall():
    #PARA CADA USUARIO,IMPRIMIRA O NOME
    print(user[0], user[1])

#INSERINDO DADOS DE JOGOS NA TABELA
jogos_sql = 'INSERT INTO jogos (nome, categoria, console) VALUES (%s, %s, %s)'
jogos= [
    ('Tetris', 'Puzzle', 'Atari'),
    ('God of War', 'Hack n Slash', 'PS2'),
    ('Mortal Kombat', 'Luta', 'PS2'),
    ('Valorant', 'FPS', 'PC'),
    ('Crash Bandicoot', 'Hack n Slash', 'PS2'),
    ('Need for Speed', 'Corrida', 'PS2'),
    ('Sonic', 'Corrida', 'PS2'),
    ('Resident Evil', 'Survival', 'PS2'),
    ('Street Fighter', 'Luta', 'PS2'),
]
#EXECUTA O COMANDO SQL PARA CADA USUARIO DA LISTA USUARIOS
cursor.executemany(jogos_sql, jogos)
#EXECUTA UM COMANDO SQL PARA SELECIONAR TODOS OS DADOS DA TABELA USUARIOS
cursor.execute('select * from jogoteca.jogos')
print('-------------  Jogos:  -------------')
#RECUPERA TODOS OS RESULTADOS DA SELEÇÃO
for jogo in cursor.fetchall():
    #PARA CADA USUARIO,IMPRIMIRA O NOME
    print(jogo[1], jogo[3])

#CONFIRMA TODAS AS MUDANÇAS FEITAS NO BANCO DE DADOS DURANTE A SESSAO ATUAL
cnx.commit()

#FECHA O CURSOR
cursor.close()
#FECHA A CONEXAO COM O BANCO DE DADOS
cnx.close()