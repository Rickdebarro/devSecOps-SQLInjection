import os
from flask import Flask, render_template, request
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from markupsafe import Markup 

#db_connect = create_engine('mysql://root:my-password@db/my_database')
db_connect = create_engine('sqlite:///../mydb.db', echo=True)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_connect

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    conn = db_connect.connect()
    
    if request.method == 'POST':
        # Recuperar parâmetros passados via formuláruo
        username_from_form = request.form.get('username')
        password_from_form = request.form.get('password')
        
        if not (username_from_form and password_from_form):
            return 'Informe um usuário e senha!', 400
        

        sql_query = text("SELECT * FROM users WHERE username = :username AND password = :password")
        result = conn.execute(sql_query, {"username": username_from_form, "password": password_from_form})

    elif request.method == 'GET':
        username_from_url = request.args.get('username')
        password_from_url = request.args.get('password')
        
        if not (username_from_url and password_from_url):
             return 'Parâmetros ausentes!', 400

        sql_query = text("SELECT * FROM users WHERE username = :username AND password = :password")
        result = conn.execute(sql_query, {"username": username_from_url, "password": password_from_url})

    content = "<table><tr><th>id</th><th>username</th><th>password</th></tr>"
    for column in result:
        content += f"<tr><td>{column[0]}</td><td>{column[1]}</td><td>{column[2]}</td></tr>"
    content += "</table>"
    
    return render_template('index.html', result=Markup(content))

if __name__ == "__main__":
    app.run()