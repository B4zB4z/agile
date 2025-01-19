from flask import Flask, render_template, request, redirect, session
import sqlite3


app = Flask(__name__)

#placeholder for testing 
db = sqlite3.connect("data.db")
db.execute("""CREATE TABLE IF NOT EXISTS clients 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 CompanyName TEXT,
                 Industry TEXT,
                 Address TEXT,
                 Phone TEXT,
                 CompanySize TEXT,
                 TIN INTEGER)
           """)

#placeholder for testing 
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'assdasddasdakdgasjhdsajdgashjgdiasudg'

conn = sqlite3.connect('auth.db')
conn.execute("""
            CREATE TABLE IF NOT EXISTS users 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT,
             password TEXT,
             role TEXT)
            """)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        data = request.form
        username = data['username']
        password = data['password']
        db = sqlite3.connect('auth.db')
        user = db.execute("SELECT * FROM users WHERE username=? AND password=?", 
                          (username, password)).fetchone()
        if user is None:
            return render_template('login.html', error='Wrong credentials')
        else:
            session.clear()
            session['username'] = username
            session['role'] = user[3]
            if user[3] == 'user':
                return redirect('/dashboard')
            elif user[3] == 'admin':
                return redirect('/dashboard_admin')
            else:
                return render_template('login.html', error='Unknown role')
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/login')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/dashboard_admin")
def dashboard_admin():
    return render_template('dashboard_admin.html')

@app.route('/clients')
def clients():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    client_list = cursor.execute("SELECT * FROM clients")
    return render_template('clients.html', clients=client_list)



@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if request.method=='POST':
        data=request.form 
        client_name=data['clients']
        conn=sqlite3.connect("data.db")
        cursor=conn.cursor()
        cursor.execute("INSERT INTO clients (name) VALUES ('" + client_name + "')")
        conn.commit()
        return redirect('/clients')
    else:
        return render_template('add_client.html')



if __name__ == '__main__':
   app.run()
