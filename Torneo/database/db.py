import psycopg2

from psycopg2 import DatabaseError
#from decouple import config

def get_connection():

    try:

        return psycopg2.connect(
            
            host="localhost",
            user="postgres",
            password="Yayel.2021",
            database="Torneo_Futbol"

        )

    except DatabaseError as ex:
        raise ex