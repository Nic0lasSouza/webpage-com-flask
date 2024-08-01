from flask import Flask, render_template

class Jogo:
    def __init__(self, nome, categoria, console, preco):
        self.nome = nome
        self.categoria = categoria
        self.console = console
        self.preco = preco
app = Flask(__name__)

@app.route('/home')
def home():
    jogo1 = Jogo('Tetris', 'Puzzle', 'Atari', 8.99)
    jogo2 = Jogo('God of War', 'Rack n slash', 'PS2', 29.99)
    jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2', 12.99)
    lista_jogo = [jogo1, jogo2, jogo3]
    return render_template('index.html', titulo = 'Jogos', jogos = lista_jogo)

app.run()