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

@app.route('/idtorneo',methods=['POST'])
def inicio_segundo():

    idtorneo=request.form['id_torneo']

    try:
        connection=get_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
    SELECT p."ID_partido", e_local."Nombre_equipo" AS nombre_local, e_visitante."Nombre_equipo" 
                           AS nombre_visitante
    FROM partidos p
    JOIN equipo e_local ON p."ID_local" = e_local."ID_equipo"
    JOIN equipo e_visitante ON p."ID_visitante" = e_visitante."ID_equipo"
    WHERE p."ID_torneo" = %s                
""", (idtorneo,))
            partidos=cursor.fetchall()
            print(partidos)
            connection.commit()
    
    except Exception as ex:
        raise Exception(ex)
    
    print(partidos)
    return render_template('menu.html',partidos=partidos)


@app.route('/login_admin')
def login():

    return render_template('login_admin.html')

@app.route('/stats')
def stats():
    nombres=[]
    try:
        connection=get_connection()

        with connection.cursor() as cursor:

            #cursor.execute("""SELECT * FROM torneo_equipo
                             #GROUP BY "ID_torneo","ID_equipo" ORDER BY "Puntos" DESC """)
        
            #salida=cursor.fetchall()
            #print(salida)

            cursor.execute("""SELECT te.*, e_equipo."Nombre_equipo"
                  FROM torneo_equipo te
                  JOIN equipo e_equipo ON te."ID_equipo" = e_equipo."ID_equipo"
                  GROUP BY te."ID_torneo", te."ID_equipo",e_equipo."Nombre_equipo"
                  ORDER BY te."Puntos" DESC""")
            
            salida=cursor.fetchall()
            print("AQUI ",salida)

            #salida_id = [lista[0] for lista in salida]

            #for id_equipo in salida_id:
                #cursor.execute("""SELECT "Nombre_equipo" FROM equipo WHERE "ID_equipo" = %s""" ,(id_equipo,))
                #nombre=cursor.fetchone()
                #nombres.append(nombre)

            #print(nombres)
    
    except Exception as ex:
        raise Exception(ex)

    return render_template('stats.html',salida=salida)

@app.route('/crear',methods=['POST'])
def crear():

    n_equipos=request.form['numEquipos']
    nombre_torneo=request.form['nombreTorneo']
    equipos = [request.form['equipo' + str(i)] for i in range(1, int(n_equipos) + 1)]
    print("equipos es: ",equipos)
    print(n_equipos)
    print(nombre_torneo)

    try:
        connection=get_connection()

        with connection.cursor() as cursor:
            #cursor.execute("SELECT * FROM equipo ")
            #salida=cursor.fetchall()
            #print(salida)
            cursor.execute("""INSERT INTO torneo ("ID_torneo", "Nombre_torneo", "Nro_Categoria","Nro_equipos")
                            VALUES (nextval('torneo_id_seq'),%s, %s, %s)""",
                           (nombre_torneo,3,n_equipos))
            cursor.execute("SELECT lastval()")
            id_torneo = cursor.fetchone()[0]
            for equipo in equipos:
                cursor.execute("""INSERT INTO equipo ("ID_equipo", "ID_categoria", "Nombre_equipo") VALUES (nextval('equipo_id_seq'),%s, %s)""",
                           (3,equipo))
                cursor.execute("SELECT lastval()")
                id_equipo = cursor.fetchone()[0]
                cursor.execute("""INSERT INTO torneo_equipo ("ID_torneo", "ID_equipo") VALUES (%s, %s)""",
                           (id_torneo,id_equipo))

            cursor.execute("""SELECT "ID_equipo" FROM equipo""")
            rows = cursor.fetchall()  
            lista_equipos=[]
            for row in rows:
                id_equipo = row[0]  
                lista_equipos.append(id_equipo)

            partidos=[(equipo1,equipo2) for equipo1 in lista_equipos for equipo2 in lista_equipos if equipo1 !=equipo2 ]
            for partido in partidos:
                id_local = partido[0]
                id_visitante = partido[1]
                cursor.execute("""INSERT INTO partidos ("ID_partido", "ID_local", "ID_visitante","ID_torneo") 
                           VALUES (nextval('id_partido_seq'), %s,%s,%s)""",
                           (id_local,id_visitante,id_torneo))
 
            connection.commit()

    except Exception as ex:
        raise Exception(ex)
    cont=cont=+1
    return render_template('menu.html')

@app.route('/editar',methods=['POST'])
def editar():

    id_partido=request.form['id_partido']
    goles_local=request.form['goles_local']
    goles_visitante=request.form['goles_visitante']

    print("AQUI ",goles_local)

    try:
        connection=get_connection()
        with connection.cursor() as cursor:

            
            cursor.execute("""SELECT "ID_local","ID_visitante" FROM partidos WHERE "ID_partido" = %s""" ,(id_partido,))
            id_local_visitante=cursor.fetchone()
            id_local=id_local_visitante[0]
            id_visitante=id_local_visitante[1]
            cursor.execute("""SELECT "ID_torneo" FROM partidos WHERE "ID_partido" = %s""" ,(id_partido,))
            id_torneo=cursor.fetchone()

            #ACTUALIZAR GOLESFAVOR Y GOLESCONTRA DEL EQUIPO LOCAL

            cursor.execute("""SELECT "gfavor_equipo","gcontra_equipo" FROM torneo_equipo WHERE "ID_equipo" = %s
                            AND "ID_torneo"=%s """ ,
                           (id_local,id_torneo))
            
            golesl=cursor.fetchone()
            goles_local_favor=golesl[0]
            actualizar_goles_local_favor=goles_local_favor+int(goles_local)
            goles_local_contra=golesl[1]
            actualizar_goles_local_contra=goles_local_contra+int(goles_visitante)

            #ACTUALIZAR GOLESFAVOR Y GOLESCONTRA DEL EQUIPO VISITANTE

            cursor.execute("""SELECT "gfavor_equipo","gcontra_equipo" FROM torneo_equipo WHERE "ID_equipo" = %s
                            AND "ID_torneo"=%s """ ,
                           (id_visitante,id_torneo))
            
            golesv=cursor.fetchone()
            goles_visitante_favor=golesv[0]
            actualizar_goles_visitante_favor=goles_visitante_favor+int(goles_visitante)
            goles_visitante_contra=golesv[1]
            actualizar_goles_visitante_contra=goles_visitante_contra+int(goles_local)

            #ACTUALIZAR GOLESFAVOR Y GOLESCONTRA DE EQUIPO LOCAL Y VISITANTE

            cursor.execute("""UPDATE torneo_equipo SET "gfavor_equipo" =%s,"gcontra_equipo" = %s 
                           WHERE "ID_equipo" =%s
                           AND  "ID_torneo"= %s""", (actualizar_goles_local_favor,
                                                     actualizar_goles_local_contra,id_local, id_torneo)) 


            cursor.execute("""UPDATE torneo_equipo SET "gfavor_equipo" =%s,"gcontra_equipo" = %s 
                           WHERE "ID_equipo" =%s
                           AND  "ID_torneo"= %s""", (actualizar_goles_visitante_favor,
                                                     actualizar_goles_visitante_contra,id_visitante, id_torneo)) 
            

            connection.commit()

            #ACTUALIZAR DIFERENCIA DE GOLES DEL EQUIPO LOCAL

            cursor.execute("""SELECT "gfavor_equipo","gcontra_equipo" FROM torneo_equipo WHERE "ID_equipo" = %s
                            AND "ID_torneo"=%s """ ,
                           (id_local,id_torneo))
            
            golesdiflocal=cursor.fetchone()
            goles_local_favor_dif=golesdiflocal[0]
            goles_local_contra_dif=golesdiflocal[1]
            goles_dif_calculados=goles_local_favor_dif-goles_local_contra_dif

            cursor.execute("""UPDATE torneo_equipo SET "dif_goles" = %s WHERE "ID_equipo" = %s AND "ID_torneo"=%s """,
                            (goles_dif_calculados,id_local,id_torneo)) 

            #ACTUALIZAR DIFERENCIA DE GOLES DEL EQUIPO VISITANTE

            cursor.execute("""SELECT "gfavor_equipo","gcontra_equipo" FROM torneo_equipo WHERE "ID_equipo" = %s
                            AND "ID_torneo"=%s """ ,
                           (id_visitante,id_torneo))
            
            golesdifvisitante=cursor.fetchone()
            goles_visitante_favor_dif=golesdifvisitante[0]
            goles_visitante_contra_dif=golesdifvisitante[1]
            goles_dif_calculados_visitante=goles_visitante_favor_dif-goles_visitante_contra_dif

            cursor.execute("""UPDATE torneo_equipo SET "dif_goles" = %s WHERE "ID_equipo" = %s AND "ID_torneo"=%s """,
                            (goles_dif_calculados_visitante,id_visitante,id_torneo)) 


            #ACTUALIZAR PARTIDOS JUGADOS, PARA EL EQUIPO LOCAL

            cursor.execute("""SELECT "cantidadjugados" FROM torneo_equipo WHERE "ID_equipo" = %s
                            AND "ID_torneo"=%s """ ,
                           (id_local,id_torneo))
            cantidadlocal=cursor.fetchone()
            cantidad_local=cantidadlocal[0]
            actualizar_cantidad_local=cantidad_local+1
            cursor.execute("""UPDATE torneo_equipo SET "cantidadjugados" = %s WHERE "ID_equipo" = %s AND "ID_torneo"=%s """,
                            (actualizar_cantidad_local,id_local,id_torneo)) 

            #ACTUALIZAR PARTIDOS JUGADOR, PARA EL EQUIPO VISITANTE

            cursor.execute("""SELECT "cantidadjugados" FROM torneo_equipo WHERE "ID_equipo" = %s
                            AND "ID_torneo"=%s """ ,
                           (id_visitante,id_torneo))
            cantidadvisitante=cursor.fetchone()
            cantidad_visitante=cantidadvisitante[0]
            actualizar_cantidad_visitante=cantidad_visitante+1
            cursor.execute("""UPDATE torneo_equipo SET "cantidadjugados" = %s WHERE "ID_equipo" = %s AND "ID_torneo"=%s """,
                            (actualizar_cantidad_visitante,id_visitante,id_torneo)) 


            if goles_local > goles_visitante:
                cursor.execute("""SELECT "ID_local" FROM partidos WHERE "ID_partido" = %s""" ,(id_partido,))
                id_local=cursor.fetchone()
                cursor.execute("""UPDATE partidos SET "ID_ganador" = %s WHERE "ID_partido" = %s""", (id_local, id_partido)) 
                cursor.execute("""SELECT "Puntos" FROM torneo_equipo WHERE "ID_equipo" = %s AND "ID_torneo"=%s """ ,(id_local,id_torneo))
                puntos = cursor.fetchone()
                valor=puntos[0]
                actualizar_win=valor+3
                cursor.execute("""UPDATE torneo_equipo SET "Puntos" = %s WHERE "ID_equipo" = %s AND "ID_torneo"=%s """, (actualizar_win, id_local,id_torneo)) 
                   
                #ACTUALIZAR NRO DE VICTORIAS DEL GANADOR

                cursor.execute("""SELECT "victorias" FROM torneo_equipo WHERE "ID_equipo" = %s AND "ID_torneo"=%s """ ,(id_local,id_torneo))
                victorias = cursor.fetchone()
                valor_victorias=victorias[0]
                actualizar_nvictorias=valor_victorias+1
                cursor.execute("""UPDATE torneo_equipo SET "victorias" = %s WHERE "ID_equipo" = %s AND "ID_torneo"=%s """, (actualizar_nvictorias, id_local,id_torneo))

                #ACTUALIZAR NRO DE DERROTAS DEL PERDEDOR

                cursor.execute("""SELECT "ID_visitante" FROM partidos WHERE "ID_partido" = %s""" ,(id_partido,))
                id_visitante=cursor.fetchone()
                cursor.execute("""SELECT "derrotas" FROM torneo_equipo WHERE "ID_equipo" = %s AND "ID_torneo"=%s """ ,(id_visitante,id_torneo))
                derrotas = cursor.fetchone()
                valor_derrotas=derrotas[0]
                actualizar_nderrotas=valor_derrotas+1
                cursor.execute("""UPDATE torneo_equipo SET "derrotas" = %s WHERE "ID_equipo" = %s AND "ID_torneo"=%s """, (actualizar_nderrotas, id_visitante,id_torneo))

                connection.commit()

            elif goles_local==goles_visitante:
                cursor.execute("""SELECT "ID_local","ID_visitante" FROM partidos WHERE "ID_partido" = %s""" ,(id_partido,))
                id_local_visitante=cursor.fetchone()
                id_local=id_local_visitante[0]
                id_visitante=id_local_visitante[1]
                cursor.execute("""SELECT "Puntos" FROM torneo_equipo WHERE "ID_equipo" = %s AND "ID_torneo"=%s""" ,(id_local,id_torneo))
                puntos = cursor.fetchone()
                valorlocal=puntos[0]
                actualizar_empate_local=valorlocal+1
                cursor.execute("""UPDATE torneo_equipo SET "Puntos" = %s WHERE "ID_equipo" = %s AND "ID_torneo"=%s""", (actualizar_empate_local, id_local,id_torneo))
                cursor.execute("""SELECT "Puntos" FROM torneo_equipo WHERE "ID_equipo" = %s AND "ID_torneo"=%s""" ,(id_visitante,id_torneo))
                puntos = cursor.fetchone()
                valorvisitante=puntos[0]
                actualizar_empate_visitante=valorvisitante+1
                cursor.execute("""UPDATE torneo_equipo SET "Puntos" = %s WHERE "ID_equipo" = %s AND "ID_torneo"=%s""", (actualizar_empate_visitante, id_visitante,id_torneo))
                    
                #ACTUALIZAR EMPATE EN LOCAL

                cursor.execute("""SELECT "empates" FROM torneo_equipo WHERE "ID_equipo" = %s AND "ID_torneo"=%s """ ,(id_local,id_torneo))
                empates_local = cursor.fetchone()
                valor_empates_local=empates_local[0]
                actualizar_nempates_local=valor_empates_local+1
                cursor.execute("""UPDATE torneo_equipo SET "empates" = %s WHERE "ID_equipo" = %s AND "ID_torneo"=%s """, (actualizar_nempates_local, id_local,id_torneo))

                #ACTUALIZAR EMPATE EN VISITANTE

                cursor.execute("""SELECT "empates" FROM torneo_equipo WHERE "ID_equipo" = %s AND "ID_torneo"=%s """ ,(id_visitante,id_torneo))
                empates_visitante = cursor.fetchone()
                valor_empates_visitante=empates_visitante[0]
                actualizar_nempates_visitante=valor_empates_visitante+1
                cursor.execute("""UPDATE torneo_equipo SET "empates" = %s WHERE "ID_equipo" = %s AND "ID_torneo"=%s """, (actualizar_nempates_visitante, id_visitante,id_torneo))

                connection.commit()
            else:
                cursor.execute("""SELECT "ID_visitante" FROM partidos WHERE "ID_partido" = %s""" ,(id_partido,))
                id_visitante=cursor.fetchone()
                cursor.execute("""UPDATE partidos SET "ID_ganador" = %s WHERE "ID_partido" = %s""", (id_visitante, id_partido)) 
                cursor.execute("""SELECT "Puntos" FROM torneo_equipo WHERE "ID_equipo" = %s AND "ID_torneo"=%s""" ,(id_visitante,id_torneo))
                puntos = cursor.fetchone()
                valor=puntos[0]
                actualizar_win=valor+3
                cursor.execute("""UPDATE torneo_equipo SET "Puntos" = %s WHERE "ID_equipo" = %s AND "ID_torneo"=%s""", (actualizar_win, id_visitante,id_torneo)) 

                #ACTUALIZAR NRO DE VICTORIAS DEL GANADOR

                cursor.execute("""SELECT "victorias" FROM torneo_equipo WHERE "ID_equipo" = %s AND "ID_torneo"=%s """ ,(id_visitante,id_torneo))
                victorias = cursor.fetchone()
                valor_victorias=victorias[0]
                actualizar_nvictorias=valor_victorias+1
                cursor.execute("""UPDATE torneo_equipo SET "victorias" = %s WHERE "ID_equipo" = %s AND "ID_torneo"=%s """, (actualizar_nvictorias, id_visitante,id_torneo))

                #ACTUALIZAR NRO DE DERROTAS DEL PERDEDOR

                cursor.execute("""SELECT "ID_local" FROM partidos WHERE "ID_partido" = %s""" ,(id_partido,))
                id_local=cursor.fetchone()
                cursor.execute("""SELECT "derrotas" FROM torneo_equipo WHERE "ID_equipo" = %s AND "ID_torneo"=%s """ ,(id_local,id_torneo))
                derrotas = cursor.fetchone()
                valor_derrotas=derrotas[0]
                actualizar_nderrotas=valor_derrotas+1
                cursor.execute("""UPDATE torneo_equipo SET "derrotas" = %s WHERE "ID_equipo" = %s AND "ID_torneo"=%s """, (actualizar_nderrotas, id_local,id_torneo))

                connection.commit()

            

    except Exception as ex:
        raise Exception(ex)


    return render_template('menu.html')


if __name__=='__main__':

    app.run(debug=True)


