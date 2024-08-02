from flask import Flask, render_template, request, redirect


class Jogo:
    def __init__(self, nome, categoria, console, preco):
        self.nome = nome
        self.categoria = categoria
        self.console = console
        self.preco = preco

jogo1 = Jogo('Tetris', 'Puzzle', 'Atari', 8.99)
jogo2 = Jogo('God of War', 'Rack n slash', 'PS2', 29.99)
jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2', 12.99)
lista_jogo = [jogo1, jogo2, jogo3]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', titulo = 'Jogos', jogos = lista_jogo)

@app.route('/new')
def new():
    return render_template('add_game.html', titulo = 'Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    preco = request.form['preco']
    jogo = Jogo(nome, categoria, console, preco)
    lista_jogo.append(jogo)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)