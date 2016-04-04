# http://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972

from flask import Flask, render_template, request,  json
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'AXS_Serv'
app.config['MYSQL_DATABASE_PASSWORD'] = 'axs*sxa'
app.config['MYSQL_DATABASE_DB'] = 'Axs_db'
app.config['MYSQL_DATABASE_HOST'] = 'rwe1814.asuscomm.com'
mysql.init_app(app)   
    
@app.route("/")
def main():
    return render_template('index.html')
    
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')
    
@app.route('/testDb')
def testDb():
    conn = mysql.connect() # ion.cursor()
    cursor = conn.cursor()
    
    cur.execute("SELECT * FROM Axs_db.axs_url")
    rv = cur.fetchall()
    return str(rv)

    
@app.route('/signUp',methods=['POST'])
def signUp():
 
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
 
    # validate the received values
    if _name and _email and _password:
        
        conn = mysql.connect()
        cursor = conn.cursor()
        
        cursor. callproc('sp_createUser',(_name,_email,_hashed_password))
        data = cursor.fetchall()
         
        if len(data) is 0:
            # conn.commit()
            return json.dumps({'message':'User created successfully !'})
        else:
            return json.dumps({'error':str(data[0])})
         
        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})
        
    
if __name__ == "__main__":
    app.run()
