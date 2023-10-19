from flask import Flask, render_template, request, redirect, url_for
import cx_Oracle

app = Flask(__name__)

# Configura la conexión a la base de datos Oracle
# Reemplaza 'usuario', 'contraseña', 'host' y 'SID' con tus propias credenciales de Oracle XE
conn = cx_Oracle.connect('AIP/Up2020s1@localhost:1521/XEPDB1')

# Ruta de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para mostrar los miembros
@app.route('/mostrar_miembros')
def mostrar_miembros():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM AIP.Miembro')
    miembros = cursor.fetchall()
    cursor.close()
    return render_template('mostrar_miembros.html', miembros=miembros)

# Ruta para insertar un miembro
@app.route('/insertar_miembro', methods=['GET', 'POST'])
def insertar_miembro():
    if request.method == 'POST':
        id_miembro = request.form['id_miembro']
        nombre = request.form['nombre']
        id_direccion = request.form['id_direccion']
        id_membresia = request.form['id_membresia']

        cursor = conn.cursor()
        cursor.execute('INSERT INTO AIP.Miembro (ID_miembro, Nombre, Id_direccion, Id_membresia) VALUES (:1, :2, :3, :4)',
                       (id_miembro, nombre, id_direccion, id_membresia))
        conn.commit()
        cursor.close()

    return render_template('insertar_miembro.html')

# Ruta para eliminar un miembro
@app.route('/eliminar_miembro/<string:id_miembro>', methods=['POST'])
def eliminar_miembro(id_miembro):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM AIP.Miembro WHERE ID_miembro = :1', (id_miembro,))
    conn.commit()
    cursor.close()
    return redirect(url_for('mostrar_miembros'))

# Ruta para actualizar un miembro
@app.route('/actualizar_miembro/<string:id_miembro>', methods=['GET', 'POST'])
def actualizar_miembro(id_miembro):
    cursor = conn.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        id_direccion = request.form['id_direccion']
        id_membresia = request.form['id_membresia']

        cursor.execute('UPDATE AIP.Miembro SET Nombre = :1, Id_direccion = :2, Id_membresia = :3 WHERE ID_miembro = :4',
                       (nombre, id_direccion, id_membresia, id_miembro))
        conn.commit()

    cursor.execute('SELECT * FROM AIP.Miembro WHERE ID_miembro = :1', (id_miembro,))
    miembro = cursor.fetchone()
    cursor.close()
    return render_template('actualizar_miembro.html', miembro=miembro)

if __name__ == '__main__':
    app.run(debug=True)


