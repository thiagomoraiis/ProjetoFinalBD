import mysql.connector

conn = mysql.connector.connect(user='root', # Dados conexão
password='',
host='127.0.0.1')

cursor = conn.cursor() # Conexão e cursor para execuções

cursor.execute('CREATE DATABASE PABD_Flask;') # Execução dos comandos

cursor.execute('USE PABD_Flask;')

cursor.execute('CREATE TABLE posts (id INT AUTO_INCREMENT PRIMARY KEY,'

'post_name VARCHAR(20) NOT NULL,'

'message VARCHAR(50) NOT NULL,'

'owner VARCHAR(20) NOT NULL);')

conn.commit() # Aplica as execuções

cursor.close() # Fecha a conexão