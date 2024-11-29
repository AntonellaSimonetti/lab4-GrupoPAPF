from Conexion import *
from verificaciones import *

class CDocente:
    def mostrarDocentes():
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            # Asegúrate de que la consulta devuelva exactamente 8 columnas
            cursor.execute("""
            SELECT 
                ID, 
                Nombre, 
                Apellido, 
                Documento, 
                TIMESTAMPDIFF(YEAR, FechaNacimiento, CURDATE()) AS Edad, 
                Telefono, 
                Domicilio, 
                MateriaID 
            FROM Docente;
            """)
            miResultado = cursor.fetchall()
            cone.commit()
            cone.close()
            return miResultado
        except mysql.connector.Error as error:
            print("Error al mostrar los datos {}".format(error))


    def ingresarDocente(nombre, apellido, documento, fechaNacimiento, telefono, domicilio, materiaID):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = "INSERT INTO Docente VALUES (NULL, %s, %s, %s, %s, %s, %s, %s);"
            valores = (nombre, apellido, documento, fechaNacimiento, telefono, domicilio, materiaID)
            cursor.execute(sql, valores)
            cone.commit()
            print(cursor.rowcount, "Registro ingresado")
            cone.close()
        except mysql.connector.Error as error:
            print("Error al ingresar los datos {}".format(error))

    def modificarDocente(idDocente, nombre, apellido, documento, fechaNacimiento, telefono, domicilio, materiaID):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = ("UPDATE Docente SET Nombre = %s, Apellido = %s, Documento = %s, "
                   "FechaNacimiento = %s, Telefono = %s, Domicilio = %s, MateriaID = %s "
                   "WHERE ID = %s;")
            valores = (nombre, apellido, documento, fechaNacimiento, telefono, domicilio, materiaID, idDocente)
            cursor.execute(sql, valores)
            cone.commit()
            print(cursor.rowcount, "Registro actualizado")
            cone.close()
        except mysql.connector.Error as error:
            print("Error al actualizar los datos {}".format(error))

    def eliminarDocente(idDocente):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = "DELETE FROM Docente WHERE ID = %s;"
            valores = (idDocente,)
            cursor.execute(sql, valores)
            cone.commit()
            print(cursor.rowcount, "Registro eliminado")
            cone.close()
        except mysql.connector.Error as error:
            print("Error al eliminar los datos {}".format(error))
            
    def obtenerFechaNacimiento(idDocente):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = "SELECT FechaNacimiento FROM Docente WHERE ID = %s;"
            valores = (idDocente,)
            cursor.execute(sql, valores)
            miResultado = cursor.fetchone()
            cone.commit()
            cone.close()
            resultado_final = VerificacionesFechas.convertir_fecha(str(miResultado))
            return resultado_final
        
        except mysql.connector.Error as error:
            print("Error al mostrar los datos {}".format(error))
