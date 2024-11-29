from Conexion import *

class CMateria:
    def mostrarMaterias():
        try: 
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            cursor.execute("SELECT * FROM Materia;")
            miResultado = cursor.fetchall()
            cone.commit()
            cone.close()
            return miResultado
        
        except mysql.connector.Error as error:
            print("Error al mostrar los datos {}".format(error))

    def ingresarMateria(nombreMateria, cursoID):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = "INSERT INTO Materia (NombreMateria, CursoID) VALUES (%s, %s);"
            valores = (nombreMateria, cursoID)
            cursor.execute(sql, valores)
            cone.commit()
            print(cursor.rowcount, "Registro ingresado")
            cone.close()
        
        except mysql.connector.Error as error:
            print("Error al ingresar los datos {}".format(error))

    def modificarMateria(idMateria, nombreMateria, cursoID):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = ("UPDATE Materia SET NombreMateria = %s, CursoID = %s "
                   "WHERE ID = %s;")
            valores = (nombreMateria, cursoID, idMateria)
            cursor.execute(sql, valores)
            cone.commit()
            print(cursor.rowcount, "Registro actualizado")
            cone.close()
        
        except mysql.connector.Error as error:
            print("Error al actualizar los datos {}".format(error))

    def eliminarMateria(idMateria):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = "DELETE FROM Materia WHERE ID = %s;"
            valores = (idMateria,)
            cursor.execute(sql, valores)
            cone.commit()
            print(cursor.rowcount, "Registro eliminado")
            cone.close()
        
        except mysql.connector.Error as error:
            print("Error al eliminar los datos {}".format(error))
