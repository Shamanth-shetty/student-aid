
from flask import Flask,render_template,request,redirect,session
import mysql.connector
import os
import functools
from pprint import pprint
from Google import Create_Service

app=Flask(__name__)
app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="localhost", user="root", database="gnNhSpM5zK", password="")
cursor=conn.cursor(buffered=True)

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/relogin')
def relogin():
    return render_template('loginwrong.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return  redirect('/')


@app.route('/UPLOAD')
def upload():
    return render_template('upload.html')


app.config['assignment_upload'] = r"C:\Users\Shamanth\Desktop\SHM APP\static\assignments"
@app.route('/UPLOADER', methods=['POST'])
def UPLOADER():
    usn=request.form.get('usn')
    subject=request.form.get('subject')
    assignment=request.form.get('Assignment')
    file1=request.files.get('file1')
    file1.save(os.path.join(app.config['assignment_upload'],file1.filename))
    

    cursor.execute("SELECT login_id FROM login WHERE usn =('{}')".format(usn))
    res=cursor.fetchone()
    file_id =str (functools.reduce(lambda sub, ele: sub * 10 + ele, res))
    cursor.execute("INSERT INTO assignment (assignment_id, subject, file_name, assignment) VALUES ('{}', '{}', '{}', '{}')".format(file_id,subject,assignment,file1.filename))
    conn.commit()
    return render_template('upload.html')

@app.route('/UPDATE')
def UPDATE():
    return render_template('update.html')

@app.route('/UPDATER', methods=['POST'])
def UPDATER():
    assignmentold=request.form.get('Assignmentold')
    assignmentnew=request.form.get('Assignmentnew')
    file2=request.files.get('file2')
    file2.save(os.path.join(app.config['assignment_upload'],file2.filename))
    


    cursor.execute("UPDATE assignment SET file_name = ('{}'), assignment = ('{}') WHERE file_name = ('{}')".format(assignmentnew,file2.filename,assignmentold))
    conn.commit()
    return render_template('update.html')

@app.route('/DELETE')
def delete():
    return render_template('delete.html')


@app.route('/DELETER', methods=['POST'])
def deleter():
    assignmentdel=request.form.get('Assignmentdel')
    cursor.execute("DELETE FROM assignment  WHERE file_name = ('{}')".format(assignmentdel))
    conn.commit()

    return render_template('delete.html')

@app.route('/calendar')
def calendar():
    CLIENT_SECRET_FILE = 'client_secret_key.json.json'
    API_NAME = 'calendar'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)

    #inserting a calendar
    request_body = { 
        'summary' : 'BMSIT ISE EVENTS'
    }

    response = service.calendars().insert(body=request_body).execute()
    print(response)




@app.route('/login_validation',methods=['POST'])
def login_validation():
    emailid=request.form.get('email')
    password=request.form.get('password')


    cursor.execute("SELECT * FROM login WHERE emailid LIKE '{}' AND password LIKE '{}'".format(emailid,password))
    users=cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        return redirect('/home')
    else:
        return redirect('/relogin')

@app.route('/add_user',methods=['POST'])
def add_user():
    email=request.form.get('email')
    password=request.form.get('password')
    name=request.form.get('name')
    usn=request.form.get('usn')
    branch=request.form.get('branch')
    sem=request.form.get('sem')
    section=request.form.get('section')
    phno=request.form.get('phno')


    cursor.execute("INSERT INTO login (login_id, emailid, password, name, usn,  phonenumber) VALUES (NULL, '{}', '{}', '{}', '{}', '{}')".format(email,password,name,usn,phno))
    cursor.execute("SELECT login_id FROM login WHERE name =('{}')".format(name))
    res=cursor.fetchone()
    branchid =str (functools.reduce(lambda sub, ele: sub * 10 + ele, res))
    cursor.execute("INSERT INTO branch (branch_id, branch) VALUES ('{}', '{}')".format(branchid,branch))

    cursor.execute("INSERT INTO sem (sem_id, sem) VALUES ('{}', '{}')".format(branchid,sem))

    cursor.execute("INSERT INTO sec (sec_id, sec) VALUES ('{}', '{}')".format(branchid,section))
    conn.commit()
    return render_template('registerdone.html')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')




if __name__=="__main__":
    app.run(debug=True)