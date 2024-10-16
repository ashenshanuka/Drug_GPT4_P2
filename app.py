from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM medications")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', medications=data)

@app.route('/add', methods=['GET', 'POST'])
def add_medication():
    if request.method == 'POST':
        name = request.form['name']
        stock = request.form['stock']
        cost = request.form['cost']
        shelf_life = request.form['shelf_life']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO medications (name, stock, cost, shelf_life) VALUES (%s, %s, %s, %s)", (name, stock, cost, shelf_life))
        mysql.connection.commit()
        flash('Medication Added Successfully')
        return redirect(url_for('index'))
    
    return render_template('add.html')


@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit_medication(id):
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        stock = request.form['stock']
        cost = request.form['cost']
        shelf_life = request.form['shelf_life']
        
        cur.execute("""
            UPDATE medications 
            SET name=%s, stock=%s, cost=%s, shelf_life=%s 
            WHERE id=%s
            """, (name, stock, cost, shelf_life, id))
        mysql.connection.commit()
        flash('Medication Updated Successfully')
        return redirect(url_for('index'))
    
    cur.execute("SELECT * FROM medications WHERE id=%s", [id])
    data = cur.fetchone()
    cur.close()
    
    return render_template('edit.html', medication=data)

@app.route('/delete/<string:id>', methods=['GET'])
def delete_medication(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM medications WHERE id=%s", [id])
    mysql.connection.commit()
    flash('Medication Removed Successfully')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
