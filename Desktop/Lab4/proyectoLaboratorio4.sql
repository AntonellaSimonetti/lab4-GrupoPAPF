DROP DATABASE colegiodb;
CREATE DATABASE colegiodb;
USE colegiodb;

CREATE TABLE Curso (
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
