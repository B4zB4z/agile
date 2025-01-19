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
db.execute("""CREATE TABLE IF NOT EXISTS projects
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 Title TEXT,
                 Description TEXT,
                 Consultant TEXT,
                 Client TEXT,
                 Deadline DATE,
                 Status TEXT)
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

@app.route('/edit_client')
def edit_client():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    client_list = cursor.execute("SELECT * FROM clients")
    return render_template('edit_client.html', clients=client_list)

@app.route("/edit/<int:client_id>", methods=["GET", "POST"])
def edit(client_id):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    # For GET request: Get client data by ID
    if request.method == 'GET':
        client = conn.execute('SELECT * FROM clients WHERE id = ?', (client_id,)).fetchone()
        conn.close()

        # Ensure that client data is passed correctly to the template
        if client:
            # Convert client tuple to dictionary for easy access in the template
            client_data = {
                'id': client[0],
                'company_name': client[1],
                'industry': client[2],
                'address': client[3],
                'phone': client[4],
                'company_size': client[5],
                'tin': client[6]
            }
            return render_template('edit.html', clients=client_data)
        else:
            return "Client not found", 404

    # For POST request: Update client data
    elif request.method == 'POST':
        column1 = request.form['column1']
        column2 = request.form['column2']
        column3 = request.form['column3']
        column4 = request.form['column4']
        column5 = request.form['column5']
        column6 = request.form['column6']

        conn.execute(
            '''
            UPDATE clients
            SET company_name = ?, industry = ?, address = ?, phone = ?, company_size = ?, tin = ?
            WHERE id = ?
            ''',
            (column1, column2, column3, column4, column5, column6, client_id)
        )
        conn.commit()
        conn.close()
        return redirect('/clients')


    


@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if request.method=='POST':
        company_name = request.form["company_name"]
        industry = request.form["industry"]
        address = request.form["address"]
        phone = request.form["phone"]
        company_size = request.form["company_size"]
        tin = request.form["tin"]
        conn=sqlite3.connect("data.db")
        cursor=conn.cursor()
        cursor.execute('''
            INSERT INTO clients (company_name, industry, address, phone, company_size, tin)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (company_name, industry, address, phone, company_size, tin))
        conn.commit()
        return redirect('/clients')
    else:
        return render_template('add_client.html')
    

@app.route('/projects')
def projects():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    projects_list = cursor.execute("SELECT * FROM projects")
    return render_template('projects.html', projects=projects_list)


@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method=='POST':
        title = request.form["Title"]
        description = request.form["Description"]
        consultant = request.form["Consultant"]
        client = request.form["Client"]
        deadline = request.form["Deadline"]
        status = request.form["Status"]
        conn=sqlite3.connect("data.db")
        cursor=conn.cursor()
        cursor.execute('''
            INSERT INTO projects (Title, Description, Consultant, Client, Deadline, Status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, description, consultant, client, deadline, status))
        conn.commit()
        return redirect('/projects')
    else:
        return render_template('add_project.html')

@app.route('/edit_project')
def edit_project():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    project_list = cursor.execute("SELECT * FROM projects")
    return render_template('edit_projects.html', projects=project_list)

@app.route("/editp/<int:project_id>", methods=["GET", "POST"])
def editp(project_id):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    # For GET request: Get client data by ID
    if request.method == 'GET':
        project = conn.execute('SELECT * FROM projects WHERE id = ?', (project_id,)).fetchone()
        conn.close()

        # Ensure that client data is passed correctly to the template
        if project:
            # Convert client tuple to dictionary for easy access in the template
            project_data = {
                'id': project[0],
                'Title': project[1],
                'Description': project[2],
                'Consultant': project[3],
                'Client': project[4],
                'Deadline': project[5],
                'Status': project[6]
            }
            return render_template('editp.html', projects=project_data)
        else:
            return "Project not found", 404

    # For POST request: Update client data
    elif request.method == 'POST':
        column1 = request.form['column1']
        column2 = request.form['column2']
        column3 = request.form['column3']
        column4 = request.form['column4']
        column5 = request.form['column5']
        column6 = request.form['column6']

        conn.execute(
            '''
            UPDATE projects
            SET Title = ?, Description = ?, Consultant = ?, Client = ?, Deadline = ?, Status = ?
            WHERE id = ?
            ''',
            (column1, column2, column3, column4, column5, column6, project_id)
        )
        conn.commit()
        conn.close()
        return redirect('/projects')


if __name__ == '__main__':
   app.run()
