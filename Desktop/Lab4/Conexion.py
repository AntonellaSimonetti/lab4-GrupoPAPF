#para instalarlo hay que abrir la terminal y poner pip install mysql-connector-python
import mysql.connector
from Configuracion import *

class CConexion: #cc por clase y conexion
    def ConexionBaseDeDatos():
        try: #sinos sale un error nos muestra cual es
            if Configuracion.VerificarConfiguracion() == True and verificarVacio() == False:    
                configConexion = Configuracion.LeerConfiguracion()
                conexion = mysql.connector.connect(user = configConexion[0], password = configConexion[1], host = configConexion[2], database = configConexion[3], raise_on_warnings = True) #database es como se llama la base de datos que cree en mysql
                #print("Conexion correcta")
            
                return conexion
        except mysql.connector.Error as error:
            print("error a conectarse a la base de datos {}".format(error))
            return conexion
    
    
def ChequearTablas():
    conexion = CConexion.ConexionBaseDeDatos()
    
    cursor = conexion.cursor()
        
    cursor.execute(f"SHOW TABLES LIKE 'curso'")
    resultado = cursor.fetchone()
    if resultado == None:
        cursor.execute(f"CREATE TABLE Curso (ID INT AUTO_INCREMENT PRIMARY KEY,NombreCurso VARCHAR(50),Año INT)")
        
    cursor.execute(f"SHOW TABLES LIKE 'Materia'")
    resultado = cursor.fetchone()
    if resultado == None:
        cursor.execute(f"CREATE TABLE Materia (ID INT AUTO_INCREMENT PRIMARY KEY,NombreMateria VARCHAR(50),CursoID INT,FOREIGN KEY (CursoID) REFERENCES Curso(ID))")
    
    cursor.execute(f"SHOW TABLES LIKE 'Docente'")
    resultado = cursor.fetchone()
    if resultado == None:
        cursor.execute(f"CREATE TABLE Docente (ID INT AUTO_INCREMENT PRIMARY KEY,Nombre VARCHAR(50),Apellido VARCHAR(50),Documento VARCHAR(20),FechaNacimiento DATE,Telefono VARCHAR(20),Domicilio VARCHAR(100),MateriaID INT,FOREIGN KEY (MateriaID) REFERENCES Materia(ID))")
    
    cursor.execute(f"SHOW TABLES LIKE 'Alumno'")
    resultado = cursor.fetchone()
    if resultado == None:
        cursor.execute(f"CREATE TABLE Alumno (ID INT AUTO_INCREMENT PRIMARY KEY,Nombre VARCHAR(50),Apellido VARCHAR(50),Documento VARCHAR(20),FechaNacimiento DATE,Telefono VARCHAR(20),Domicilio VARCHAR(100),CursoID INT,FOREIGN KEY (CursoID) REFERENCES Curso(ID))")
        
#   ConexionBaseDeDatos()
    
    
"""CREATE TABLE Curso (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NombreCurso VARCHAR(50),
    Año INT
);

CREATE TABLE Materia (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NombreMateria VARCHAR(50),
    CursoID INT,
    FOREIGN KEY (CursoID) REFERENCES Curso(ID)
);

CREATE TABLE Docente (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(50),
    Apellido VARCHAR(50),
    Documento VARCHAR(20),
    FechaNacimiento DATE,
    Telefono VARCHAR(20),
    Domicilio VARCHAR(100),
    MateriaID INT,
    FOREIGN KEY (MateriaID) REFERENCES Materia(ID)
);

CREATE TABLE Alumno (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(50),
    Apellido VARCHAR(50),
    Documento VARCHAR(20),
    FechaNacimiento DATE,
    Telefono VARCHAR(20),
    Domicilio VARCHAR(100),
    CursoID INT,
    FOREIGN KEY (CursoID) REFERENCES Curso(ID)
);
"""