# Alumno.py modificado
from Conexion import *
from verificaciones import *

class CAlumno:
    def mostrarAlumnos():
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            # Agregamos el cálculo de la edad en la consulta SQL
            cursor.execute("""
            SELECT 
                ID, 
                Nombre, 
                Apellido, 
                Documento, 
                TIMESTAMPDIFF(YEAR, FechaNacimiento, CURDATE()) AS Edad, 
                Telefono, 
                Domicilio, 
                CursoID 
            FROM Alumno;
            """)
            miResultado = cursor.fetchall()
            cone.commit()
            cone.close()
            return miResultado
        
        except mysql.connector.Error as error:
            print("Error al mostrar los datos {}".format(error))

    def ingresarAlumno(nombre, apellido, documento, fechaNacimiento, telefono, domicilio, cursoID):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = "INSERT INTO Alumno VALUES (NULL, %s, %s, %s, %s, %s, %s, %s);"
            valores = (nombre, apellido, documento, fechaNacimiento, telefono, domicilio, cursoID)
            cursor.execute(sql, valores)
            cone.commit()
            print(cursor.rowcount, "Registro ingresado")
            cone.close()
        
        except mysql.connector.Error as error:
            print("Error al ingresar los datos {}".format(error))

    def modificarAlumno(idAlumno, nombre, apellido, documento, fechaNacimiento, telefono, domicilio, cursoID):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = ("UPDATE Alumno SET Nombre = %s, Apellido = %s, Documento = %s, "
                "FechaNacimiento = %s, Telefono = %s, Domicilio = %s, CursoID = %s "
                "WHERE ID = %s;")
            valores = (nombre, apellido, documento, fechaNacimiento, telefono, domicilio, cursoID, idAlumno)
            cursor.execute(sql, valores)
            cone.commit()
            print(cursor.rowcount, "Registro actualizado")
            cone.close()
        
        except mysql.connector.Error as error:
            print("Error al actualizar los datos {}".format(error))
    
    def eliminarAlumno(idAlumno):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = "DELETE FROM Alumno WHERE ID = %s;"
            valores = (idAlumno,)
            cursor.execute(sql, valores)
            cone.commit()
            print(cursor.rowcount, "Registro eliminado")
            cone.close()
        
        except mysql.connector.Error as error:
            print("Error al eliminar los datos {}".format(error))
            
    def ObtenerFechaNacimiento(idAlumno):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = "SELECT FechaNacimiento FROM Alumno WHERE ID = %s;"
            valores = (idAlumno,)
            cursor.execute(sql, valores)
            miResultado = cursor.fetchone()
            cone.commit()
            cone.close()
            resultado_final = VerificacionesFechas.convertir_fecha(str(miResultado))

            return resultado_final
        
        except mysql.connector.Error as error:
            print("Error al mostrar los datos {}".format(error))