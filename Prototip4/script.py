import mysql.connector
from mysql.connector import Error

def listar_usuarios():
    try:
        # Conexión a la base de datos--Només per llistar usuaris
        # Si es vol fer una altra consulta, cal modificar la consulta SQL (com al BackendP4.py)
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='TapatApp'
        )
        
        if connection.is_connected():
            print("✅ Conexión a la base de datos establecida")
            
            # Crear cursor y ejecutar consulta
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM User")
            
            # Obtener resultados
            usuarios = cursor.fetchall()
            
            # Imprimir resultados
            for usuario in usuarios:
                print(usuario)
    
    except Error as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
    
    finally:
        # Cerrar conexión
        if 'cursor' in locals():
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("🔌 Conexión cerrada")

if __name__ == "__main__":
    listar_usuarios()