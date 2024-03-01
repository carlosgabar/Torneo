import psycopg2
from psycopg2 import OperationalError

try:
   
    connection = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="Yayel.2021",
        database="Torneo_Futbol"

    )

    cursor=connection.cursor()
    #cursor.execute("SELECT * FROM torneo")
    #row=cursor.fetchone()
    #print(row)
    #sql="INSERT INTO torneo (ID_torneo, Nombre_torneo, Nro_Categoria,Nro_equipos) VALUES (NULL,%s, %s, %s);"
    #datos=("ucl",3,4)
    #cursor.execute(sql,datos)
    #connection.commit()
    #ESTE FUNCIONA cursor.execute("""INSERT INTO torneo ("ID_torneo", "Nombre_torneo", "Nro_Categoria","Nro_equipos") VALUES (4,'liga', 3,4 )""")
    
    cursor.execute("""
    SELECT p."ID_partido", e_local."Nombre_equipo" AS nombre_local, e_visitante."Nombre_equipo" AS nombre_visitante
    FROM partidos p
    JOIN equipo e_local ON p."ID_local" = e_local."ID_equipo"
    JOIN equipo e_visitante ON p."ID_visitante" = e_visitante."ID_equipo"
""")
    rows = cursor.fetchall()

    for row in rows:
        id_partido = row[0]
        nombre_local = row[1]
        nombre_visitante = row[2]
        print(f"ID Partido: {id_partido}, Nombre Equipo Local: {nombre_local}, Nombre Equipo Visitante: {nombre_visitante}")    

    id_partido=5

    
    cursor.execute("""SELECT "gfavor_equipo","gcontra_equipo" FROM torneo_equipo WHERE "ID_equipo" = %s
                            AND "ID_torneo"=%s """ ,
                           (3,1))
            
    golesl=cursor.fetchone()
    goles_local_favor=golesl[0]

    print(goles_local_favor)
    print(golesl)


    cursor.execute("""UPDATE partidos SET "ID_ganador" = %s WHERE "ID_partido" = %s""", (2, id_partido)) 
    cursor.execute("""SELECT "Puntos" FROM equipo WHERE "ID_equipo" = %s""" ,(2,))
    rows = cursor.fetchone()
    print("AQUI",rows)
    valor=rows[0]
    actualizar_win=valor+3
    cursor.execute("""UPDATE equipo SET "Puntos" = %s WHERE "ID_equipo" = %s""", (actualizar_win, 2)) 
                   
    connection.commit()

    cursor.execute("""SELECT "ID_equipo" FROM equipo""")

    rows = cursor.fetchall()  
    lista_equipos=[]
    for row in rows:
        id_equipo = row[0] 
        print("ID_equipo:", id_equipo)
        lista_equipos.append(id_equipo)

    print(lista_equipos)
    partidos=[(equipo1,equipo2) for equipo1 in lista_equipos for equipo2 in lista_equipos if equipo1 !=equipo2 ]
    print(partidos)
    for partido in partidos:
        id_local = partido[0]
        id_visitante = partido[1]
        print(f"ID local: {id_local}")
        print(f"ID visitante: {id_visitante}")
        
    print("Conexión exitosa a la base de datos")



except Exception as ex:
   
    print(ex)

finally:
    # Cerrar la conexión
    if connection is not None:
        connection.close()
        print("Conexión cerrada")