from flask import Flask
from flask import render_template,request,redirect,session
from datetime import datetime
from flask import send_from_directory
from database.db import get_connection

import os



app=Flask(__name__,template_folder='templates')
app.secret_key="torneo"

@app.route('/')
def inicio():

    return render_template('menu.html')

@app.route('/login_admin')
def login():

    return render_template('login_admin.html')

@app.route('/stats')
def stats():

    try:
        connection=get_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM equipo ")
            salida=cursor.fetchall()
            print(salida)
    
    except Exception as ex:
        raise Exception(ex)

    return render_template('stats.html')

@app.route('/crear',methods=['POST'])
def crear():

    n_equipos=request.form['numEquipos']
    nombre_torneo=request.form['nombreTorneo']
    print(n_equipos)
    print(nombre_torneo)

    try:
        connection=get_connection()

        with connection.cursor() as cursor:
            #cursor.execute("SELECT * FROM equipo ")
            #salida=cursor.fetchall()
            #print(salida)
            cursor.execute("""INSERT INTO torneo ("ID_torneo", "Nombre_torneo", "Nro_Categoria","Nro_equipos") VALUES (nextval('torneo_id_seq'),%s, %s, %s)""",
                           (nombre_torneo,3,n_equipos))
            connection.commit()
    
    except Exception as ex:
        raise Exception(ex)
    cont=cont=+1
    return render_template('menu.html')

if __name__=='__main__':

    app.run(debug=True)


