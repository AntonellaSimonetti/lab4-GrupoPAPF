import tkinter as tk
from tkinter import ttk
from Conexion import *
from FormularioCurso import Formulario as FormularioCurso
from FormularioMateria import Formulario as FormularioMateria
from FormularioDocente import Formulario as FormularioDocente
from FormularioAlumno import Formulario as FormularioAlumno
from Configuracion import *

def InterfazPrincipal():
    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.geometry("1310x700")
    ventana.title("Gestión Escolar - Interfaz Unificada")

    # Crear un Notebook para pestañas
    notebook = ttk.Notebook(ventana)
    notebook.pack(expand=1, fill="both")

    # Crear un Frame para cada pestaña
    frameCursos = ttk.Frame(notebook)
    frameMaterias = ttk.Frame(notebook)
    frameDocentes = ttk.Frame(notebook)
    frameAlumnos = ttk.Frame(notebook)

    # Agregar las pestañas al Notebook
    notebook.add(frameCursos, text="Cursos")
    notebook.add(frameMaterias, text="Materias")
    notebook.add(frameDocentes, text="Docentes")
    notebook.add(frameAlumnos, text="Alumnos")

    # Cargar los formularios directamente en cada pestaña
    FormularioCurso(parent=frameCursos)
    FormularioMateria(parent=frameMaterias)
    FormularioDocente(parent=frameDocentes)
    FormularioAlumno(parent=frameAlumnos)

    ventana.mainloop()


if __name__ == "__main__":
    if Configuracion.VerificarConfiguracion() == False or verificarVacio() == True:    
        FormularioConfiguracion()
            
    InterfazPrincipal()
    
    
