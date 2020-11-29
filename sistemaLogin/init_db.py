import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            ('Teste', 'teste@teste.com', 'senha12345senha')
            )

connection.commit()
connection.close()