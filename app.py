from flask import Flask, render_template, request, redirect, flash, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)  # __name__ : it used to collect current names in pgm

# mysql server connection :
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "dinesh"
app.config["MYSQL_DB"] = "crud"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


# loading homepage:
@app.route('/')
def homepage():
    conn = mysql.connection.cursor()
    sql = "select * from users"
    conn.execute(sql)
    result = conn.fetchall()
    return render_template('homepage.html', datas=result)


# new user:
@app.route('/add_users', methods=['GET', 'POST'])
def addusers():
    if request.method == 'POST':
        name = request.form['name']
        Age = request.form['age']
        City = request.form['city']
        conn = mysql.connection.cursor()
        sql = "insert into users (NAME,AGE,CITY) value (%s, %s, %s)"
        conn.execute(sql, [name, Age, City])
        mysql.connection.commit()
        conn.close()
        flash('User details Added')
        return redirect(url_for('homepage'))
    return render_template('add_users.html')


# updateuser :
@app.route("/Edit/<string:id>", methods=['GET', 'POST'])
def Edit(id):
    conn = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        Age = request.form['age']
        City = request.form['city']
        sql = "update users set NAME=%s, AGE=%s, CITY=%s where ID=%s"
        conn.execute(sql, [name, Age, City, id])
        mysql.connection.commit()
        conn.close()
        flash('User details Updated')
        return redirect(url_for('homepage'))
        conn = mysql.connection.cursor()

    sql = "select * from users where ID=%s"
    conn.execute(sql, [id])
    result = conn.fetchone()
    return render_template("Edit.html", datas=result)


# delete user details:
@app.route("/deleteusers/<string:id>", methods=['GET', 'POST'])
def deleteusers(id):
    conn = mysql.connection.cursor()
    sql = "delete  from users where ID=%s"
    conn.execute(sql, [id])
    mysql.connection.commit()
    conn.close()
    flash('User details deleted')
    return redirect(url_for('homepage'))


if __name__ == '__main__':
    app.secret_key = '123dinesh'
    app.run(debug=True)
