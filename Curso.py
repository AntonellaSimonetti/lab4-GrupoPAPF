from Conexion import *

class CCurso:
    def mostrarCursos():
        try: 
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            cursor.execute("SELECT * FROM Curso;")
            miResultado = cursor.fetchall()
            cone.commit()
            cone.close()
            return miResultado
        
        except mysql.connector.Error as error:
            print("Error al mostrar los datos {}".format(error))

    def ingresarCurso(nombreCurso, anio):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = "INSERT INTO Curso VALUES (NULL, %s, %s);"
            valores = (nombreCurso, anio)
            cursor.execute(sql, valores)
            cone.commit()
            print(cursor.rowcount, "Registro ingresado")
            cone.close()
        
        except mysql.connector.Error as error:
            print("Error al ingresar los datos {}".format(error))

    def modificarCurso(idCurso, nombreCurso, anio):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = ("UPDATE Curso SET NombreCurso = %s, Año = %s "
                   "WHERE ID = %s;")
            valores = (nombreCurso, anio, idCurso)
            cursor.execute(sql, valores)
            cone.commit()
            print(cursor.rowcount, "Registro actualizado")
            cone.close()
        
        except mysql.connector.Error as error:
            print("Error al actualizar los datos {}".format(error))

    def eliminarCurso(idCurso):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = "DELETE FROM Curso WHERE ID = %s;"
            valores = (idCurso,)
            cursor.execute(sql, valores)
            cone.commit()
            print(cursor.rowcount, "Registro eliminado")
            cone.close()
        
        except mysql.connector.Error as error:
            print("Error al eliminar los datos {}".format(error))
