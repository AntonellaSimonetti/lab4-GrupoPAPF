import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from Conexion import *
from Configuracion import *
from verificaciones import *
from Materia import CMateria  # Clase de Materia
from Curso import CCurso  # Clase de Curso, usada para obtener los cursos disponibles

# Declaración de variables globales
base = None
textBoxId = None
textBoxNombreMateria = None
comboCursos = None
tree = None


"""from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry"""

# Modificación en la función `Formulario`
def Formulario(parent=None):
    global textBoxId, textBoxNombreMateria, comboCursos, tree

    try:
        if parent is None:
            raise ValueError("El argumento 'parent' es obligatorio para integrar el formulario en la interfaz principal")

        # GroupBox para los datos
        groupBox = LabelFrame(parent, text="Datos de la Materia", padx=5, pady=5)
        groupBox.grid(row=0, column=0, padx=10, pady=10, sticky="N")

        # Campos de entrada
        Label(groupBox, text="Id:", font=('arial', 12)).grid(row=0, column=0)
        textBoxId = Entry(groupBox, state="readonly")  # Campo solo lectura
        textBoxId.grid(row=0, column=1)

        Label(groupBox, text="Nombre de la Materia:", font=('arial', 12)).grid(row=1, column=0)
        textBoxNombreMateria = Entry(groupBox)
        textBoxNombreMateria.grid(row=1, column=1)

        
        Label(groupBox, text="Curso:", font=('arial', 12)).grid(row=2, column=0)
        
        comboCursos = ttk.Combobox(groupBox, postcommand=cargarCursos) #Agrue el postcommand que implica que la funcion se ejecuta cuando se abre el combobox
        comboCursos.grid(row=2, column=1)
        # Carga los cursos en el ComboBox
        cargarCursos()

        # Botones
        Button(groupBox, text="Guardar", width=10, command=guardarRegistros).grid(row=3, column=0)
        Button(groupBox, text="Modificar", width=10, command=modificarRegistros).grid(row=3, column=1)
        Button(groupBox, text="Eliminar", width=10, command=eliminarRegistros).grid(row=3, column=2)

        # GroupBox para la tabla
        groupBoxTabla = LabelFrame(parent, text="Lista de Materias", padx=5, pady=5)
        groupBoxTabla.grid(row=0, column=1, padx=5, pady=5)

        # Tabla
        tree = ttk.Treeview(groupBoxTabla, columns=("Id", "Nombre de la Materia", "Curso"), show='headings', height=10)
        tree.column("# 1", anchor=CENTER, width=50)
        tree.heading("# 1", text="Id")
        tree.column("# 2", anchor=W, width=200)
        tree.heading("# 2", text="Nombre de la Materia")
        tree.column("# 3", anchor=W, width=150)
        tree.heading("# 3", text="Curso")

        tree.bind("<<TreeviewSelect>>", seleccionarRegistro)  # Evento de selección
        tree.pack()
        if Configuracion.VerificarConfiguracion() == True and verificarVacio() == False:
            actualizarTreeView()

    except Exception as e:
        print(f"Error al inicializar la interfaz: {e}")
 

def cargarCursos():
    """Carga los cursos en el ComboBox desde la base de datos."""
    try:
        cursos = CCurso.mostrarCursos()
        comboCursos['values'] = cursos
        #comboCursos['values'] = [f"{curso[0]} - {curso[1]}" for curso in cursos]  # Ejemplo: "1 - Matemática"
        if cursos:
            comboCursos.current(0)  # Selecciona el primer elemento por defecto
    except Exception as e:
        print(f"Error al cargar los cursos: {e}")

def guardarRegistros():
    try:
        nombreMateria = textBoxNombreMateria.get()
        #Las verificaciones tienen este formato
        if VerificacionesDatos.VerificarStringValido(nombreMateria) == False:
                messagebox.showerror("Error", "El nombre de la materia no es valido, los siguentes caracteres no estan permitidos '.', ':', ';', ',', '´', '{', '}', '\\', '/'")
                return
            
        cursoSeleccionado = comboCursos.get()

        if not nombreMateria or not cursoSeleccionado:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        #cursoID = cursoSeleccionado.split("-")[0]  # Obtiene el ID del curso desde el ComboBox
        print(cursoSeleccionado[0])
        CMateria.ingresarMateria(nombreMateria, cursoSeleccionado[0])
        messagebox.showinfo("Información", "Materia guardada correctamente")
        actualizarTreeView()
        
        textBoxNombreMateria.delete(0, END)

    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar la materia: {e}")

def actualizarTreeView():
    try:
        # Eliminar todos los elementos actuales en la tabla
        for item in tree.get_children():
            tree.delete(item)

        # Agregar datos actualizados
        materias = CMateria.mostrarMaterias()
        cursos = {curso[0]: curso[1] for curso in CCurso.mostrarCursos()}  # Diccionario para obtener nombres de cursos

        for row in materias:
            cursoNombre = cursos.get(row[2], "Desconocido")  # row[2] es el CursoID
            tree.insert("", "end", values=(row[0], row[1], cursoNombre))

    except Exception as e:
        print(f"Error al actualizar la tabla: {e}")

def seleccionarRegistro(event):
    try:
        item = tree.focus()
        valores = tree.item(item, 'values')

        if valores:
            textBoxId.config(state=NORMAL)
            textBoxId.delete(0, END)
            textBoxId.insert(0, valores[0])
            textBoxId.config(state="readonly")

            textBoxNombreMateria.delete(0, END)
            textBoxNombreMateria.insert(0, valores[1])

            comboCursos.set(valores[2])  # Selecciona el curso en el ComboBox

    except Exception as e:
        print(f"Error al seleccionar un registro: {e}")

def modificarRegistros():
    try:
        idMateria = textBoxId.get()
        
        nombreMateria = textBoxNombreMateria.get()
        if VerificacionesDatos.VerificarStringValido(nombreMateria) == False:
                messagebox.showerror("Error", "El nombre de la materia no es valido, los siguentes caracteres no estan permitidos '.', ':', ';', ',', '´', '{', '}', '\\', '/'")
                return
        
        cursoSeleccionado = comboCursos.get()
        

        if not idMateria or not nombreMateria or not cursoSeleccionado:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        #cursoID = cursoSeleccionado.split(" - ")[0]  # Obtiene el ID del curso desde el ComboBox
        CMateria.modificarMateria(idMateria, nombreMateria, cursoSeleccionado[0])
        messagebox.showinfo("Información", "Materia modificada correctamente")
        actualizarTreeView()

        textBoxId.config(state=NORMAL)
        textBoxId.delete(0, END)
        textBoxId.config(state="readonly")
        textBoxNombreMateria.delete(0, END)

    except Exception as e:
        messagebox.showerror("Error", f"Error al modificar la materia: {e}")

def eliminarRegistros():
    try:
        idMateria = textBoxId.get()

        if not idMateria:
            messagebox.showerror("Error", "Debe seleccionar una materia para eliminar")
            return

        CMateria.eliminarMateria(idMateria)
        messagebox.showinfo("Información", "Materia eliminada correctamente")
        actualizarTreeView()

        textBoxId.config(state=NORMAL)
        textBoxId.delete(0, END)
        textBoxId.config(state="readonly")
        textBoxNombreMateria.delete(0, END)

    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar la materia: {e}")

#Formulario()
