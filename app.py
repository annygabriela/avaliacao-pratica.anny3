from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os


app = Flask(__name__)


# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('fabrica.db')
    conn.row_factory = sqlite3.Row
    return conn


# Função para inicializar o banco de dados
def start_db():
    conn = get_db_connection()
   
    # Ler e executar o schema.sql
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
   
    conn.commit()
    conn.close()


# Rota principal - Listar todos os alunos
@app.route('/')
def index():
    conn = get_db_connection()
    alunos = conn.execute('SELECT * FROM aluno').fetchall()
    conn.close()
    return render_template('index.html', alunos=alunos)


# Rota de cadastro - GET e POST
@app.route('/cadastro', methods=('GET', 'POST'))
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        curso = request.form['curso']
       
        conn = get_db_connection()
        conn.execute('INSERT INTO aluno (nome, idade, curso) VALUES (?, ?, ?)',
                    (nome, idade, curso))
        conn.commit()
        conn.close()
       
        return redirect(url_for('index'))
   
    return render_template('cadastro.html')


# Rota para editar aluno - GET e POST
@app.route('/editar/<int:id>', methods=('GET', 'POST'))
def editar(id):
    conn = get_db_connection()
   
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        curso = request.form['curso']
       
        conn.execute('UPDATE aluno SET nome = ?, idade = ?, curso = ? WHERE id = ?',
                    (nome, idade, curso, id))
        conn.commit()
        conn.close()
       
        return redirect(url_for('index'))
   
    aluno = conn.execute('SELECT * FROM aluno WHERE id = ?', (id,)).fetchone()
    conn.close()
   
    if aluno is None:
        return redirect(url_for('index'))
   
    return render_template('editar.html', aluno=aluno)


# Rota para excluir aluno
@app.route('/excluir/<int:id>')
def excluir(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM aluno WHERE id = ?', (id,))
    conn.commit()


    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    start_db()  # Inicializa o banco de dados
    app.run(debug=True)

