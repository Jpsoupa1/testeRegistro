from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'Shelby1!'


#   Configurando Banco de dados

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Shelby1!",
    database = "clientes"
)

@app.route('/')
def home():
    if 'nome' in session:
        return f"Olá, {session['nome']}! <a href='/logout'>Sair</a>"
    return 'Você não está logado! <a href="/login">Login ou<a href="/register">Registrar</a>'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nome = %s", (nome,))
        user = cursor.fetchone()

        if user:
            flash('Usuário existente!')
            return redirect('/register')
        

        hashed_password = generate_password_hash(senha, method='pbkdf2:sha256')

        cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (%s, %s)", (nome, hashed_password))
        db.commit()
        cursor.close()
        flash("Registrado com sucesso! Faça o login.")
        return redirect('/login')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        cursor = db.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE nome = %s', (nome,))
        user  = cursor.fetchone()
        cursor.close()


        if user and check_password_hash(user[2], senha):
            session['nome'] = user[1]
            return redirect('/')
        
        else:
            flash('Usuário ou senha incorretos!')
            return redirect('/login')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('nome', None)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)