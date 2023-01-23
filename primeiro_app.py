from flask import Flask, render_template, request, url_for, flash, redirect
from flask_mysqldb import MySQL
import MySQLdb
from werkzeug.exceptions import abort

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'PABD_Flask'
app.config['SECRET_KEY'] = 'lUKASLINDOeJVGAY'

mysql = MySQL(app) # Aplicando as configurações


def get_connection():
    cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    return cursor


def get_post(post_id): # Função que retorna o item
    cursor = get_connection() # Pega a conexão com o banco
    cursor.execute('SELECT * FROM posts WHERE id = %s', [post_id]) # Executa query
    post = cursor.fetchone() # Salvar o resultado na variável
    cursor.close() # Fecha a conexão
    if post is None: # Retorna erro se não existir nenhum objeto
        abort(404)
    return post # Retorna o item


@app.route('/')
def index():
    cursor = get_connection()
    cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall()
    cursor.close()
    return render_template('index.html', posts=posts)

@app.route('/<int:post_id>') # Cada item gera uma página própria
def post(post_id):
    post = get_post(post_id) # Pega o item selecionado
    return render_template('post.html', post=post) # Retorna a página do item

@app.errorhandler(404)
def erro(e):
    return render_template('404.html'), 404

@app.route('/create', methods=['GET', 'POST'])
def create():
    title = None
    if request.method == 'POST': # Só aceita se for o método POST
        title = request.form['title'] # Pega o campo do form correspondente
        content = request.form['content'] # Pega o campo do form correspondente
        owner = request.form['owner'] # Pega o campo do form correspondente

    if not title:
        flash('Title is required!') # Mensagem de “alerta”

    else:
        cursor = get_connection()
        cursor.execute('INSERT INTO posts (post_name, message, owner) VALUES (%s, %s, %s)', [title, content, owner])
        mysql.connection.commit() # Efetiva as transações
        cursor.close()
        flash('Created Post') # Mensagem de “alerta”
        return redirect(url_for('index')) # Depois de criar, redireciona

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    title = None
    post = get_post(id) # Pega o post referente
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        owner = request.form['owner']
    if not title:
        flash('Title is required!')
    else:
        cursor = get_connection()
        cursor.execute('UPDATE posts SET post_name = %s, message = %s, owner = %s WHERE id = %s',[title, content, owner, id])
        mysql.connection.commit()
        cursor.close()
        flash('Edited Post')

        return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))

def delete(id):
    post = get_post(id)
    cursor = get_connection()
    cursor.execute('DELETE FROM posts WHERE id = %s', [id])
    mysql.connection.commit()
    cursor.close()
    flash("{} was successfully deleted!".format(post['post_name']))
    return redirect(url_for('index'))