from flask import Flask, request
from flaskext.mysql import MySQL
 
mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'webuser'
app.config['MYSQL_DATABASE_PASSWORD'] = 'webbruker'
app.config['MYSQL_DATABASE_DB'] = 'EmpData'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
 
@app.route("/")
def hello():
    return "Welcome to Python Flask App!"
 
@app.route("/Authenticate")
def Authenticate():
    username = request.args.get('UserName')
    password = request.args.get('Password')
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from User where Username='" + username + "' and Password='" + password + "'")
    data = cursor.fetchone()
    if data is None:
     return "Username or Password is wrong"
    else:
     return "Logged in successfully"
 
@app.route("/UserList")
def UserList():

    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from User")
    data = cursor.fetchone()
    if data is None:
        return "Username or Password is wrong"
    else:
        s = ""
        #s = data.keys()
        s += "<table>"
        # s += "<th><td></td>"
        
        while data:
            s += "<tr><td>" + str(data[0]) + "<td><td>" + str(data[1]) + "<td><tr>"
            data = cursor.fetchone()
            
        s += "</table>"
        
        return s
 
if __name__ == "__main__":
    app.run()
