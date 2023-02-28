from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)


# CONEXION MYSQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskapp'
mysql = MySQL(app)

# CONFIGURACION
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM compradores')
    data = cur.fetchall()
    return render_template('index.html', compradores = data)

@app.route('/add_registro', methods=['POST'])
def add_registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        tipoDNI = request.form['tipoDNI']
        dni = request.form['dni']
        celular = request.form['celular']
        vinculo = request.form['vinculo']
        direccion = request.form['direccion']
        
        cur = mysql.connection.cursor()

        cur.execute('INSERT INTO compradores (nombre, apellido, tipoDNI, dni, celular, vinculo, direccion) VALUES (%s, %s, %s, %s, %s, %s, %s)',(nombre,apellido,tipoDNI,dni,celular,vinculo,direccion))
        mysql.connection.commit()

        flash('CONTACTO AGREGADO CORRECTAMENTE')

        return redirect(url_for('Index'))

@app.route('/edit/<string:id>')
def get_registro(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM compradores WHERE id = {0}'.format(id))
    data = cur.fetchall()

    cur2 = mysql.connection.cursor()
    cur2.execute('SELECT * FROM compradores')
    data2 = cur2.fetchall()

    return render_template('edit_registro.html', comprador = data[0], compradores = data2)

@app.route('/update/<id>', methods = ['POST'])
def update_registro(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        tipoDNI = request.form['tipoDNI']
        dni = request.form['dni']
        celular = request.form['celular']
        vinculo = request.form['vinculo']
        direccion = request.form['direccion']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE compradores
        SET nombre = %s,
            apellido = %s,
            tipoDNI = %s,
            dni = %s,
            celular = %s,
            vinculo = %s,
            direccion = %s
        WHERE id = %s
        """,(nombre,apellido,tipoDNI, dni, celular, vinculo, direccion, id))
        flash('Contacto actualizado correctamente')
        mysql.connection.commit()
    return redirect(url_for('Index'))


@app.route('/delete/<string:id>')
def delete_registro(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM compradores WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('CONTACTO ELIMINADO CORRECTAMENTE')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)