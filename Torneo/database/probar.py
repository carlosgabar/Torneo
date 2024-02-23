import psycopg2
from psycopg2 import OperationalError

try:
    # Establecer la conexión a la base de datos
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
    cursor.execute("""INSERT INTO torneo ("ID_torneo", "Nombre_torneo", "Nro_Categoria","Nro_equipos") VALUES (4,'liga', 3,4 )""")
    connection.commit()


    # Si no se ha producido ninguna excepción, la conexión se ha realizado con éxito
    print("Conexión exitosa a la base de datos")

    # Realizar operaciones con la base de datos aquí

except Exception as ex:
    # Capturar excepciones de error de conexión
    print(ex)

finally:
    # Cerrar la conexión
    if connection is not None:
        connection.close()
        print("Conexión cerrada")