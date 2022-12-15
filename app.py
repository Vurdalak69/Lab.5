import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="5156278353Yi",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
            return render_template('account.html', full_name=records[0][1])
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if (not name):
            return render_template('error.html')
        elif (not login) or (not password):
            return render_template('alert.html')
        if name:
            cursor.execute('SELECT * FROM service.users')   #Помечаем таблицу users в PgAdmin4
            ab = cursor.fetchall()                          #Выбираем весь массив с информацией
            for a in ab:                                    #Данные каждого пользователя прогоняются по массиву
                if name == a[1]:                            #Сравнимаем name с 1й переменной массива данных пользователя
                    return render_template('error.html')
        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES(%s, %s, %s);',(str(name), str(login), str(password)))
        conn.commit()
        return redirect('/login/')
    return render_template('registration.html')
