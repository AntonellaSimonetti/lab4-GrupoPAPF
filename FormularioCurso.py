import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from Conexion import *
from Configuracion import *
from verificaciones import *
from Curso import CCurso  # Asegúrate de que tu clase Curso esté en un archivo llamado Curso.py

# Declaración de variables globales
base = None
textBoxId = None
textBoxNombreCurso = None
textBoxAnio = None
tree = None


"""from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry"""

# Modificación en la función `Formulario`
def Formulario(parent=None):
    global textBoxId, textBoxNombreCurso, textBoxAnio, tree

    try:
        if parent is None:
            raise ValueError("El argumento 'parent' es obligatorio para integrar el formulario en la interfaz principal")

        # GroupBox para los datos
        groupBox = LabelFrame(parent, text="Datos del Curso", padx=5, pady=5)
        groupBox.grid(row=0, column=0, padx=10, pady=10, sticky="N")

        # Campos de entrada
        Label(groupBox, text="Id:", font=('arial', 12)).grid(row=0, column=0)
        textBoxId = Entry(groupBox, state="readonly")  # Campo solo lectura
        textBoxId.grid(row=0, column=1)

        Label(groupBox, text="Nombre del Curso:", font=('arial', 12)).grid(row=1, column=0)
        textBoxNombreCurso = Entry(groupBox)
        textBoxNombreCurso.grid(row=1, column=1)

        Label(groupBox, text="Año:", font=('arial', 12)).grid(row=2, column=0)
        textBoxAnio = Entry(groupBox)
        textBoxAnio.grid(row=2, column=1)

        # Botones
        Button(groupBox, text="Guardar", width=10, command=guardarRegistros).grid(row=3, column=0)
        Button(groupBox, text="Modificar", width=10, command=modificarRegistros).grid(row=3, column=1)
        Button(groupBox, text="Eliminar", width=10, command=eliminarRegistros).grid(row=3, column=2)

        # GroupBox para la tabla
        groupBoxTabla = LabelFrame(parent, text="Lista de Cursos", padx=5, pady=5)
        groupBoxTabla.grid(row=0, column=1, padx=5, pady=5)

        # Tabla
        tree = ttk.Treeview(groupBoxTabla, columns=("Id", "Nombre del Curso", "Año"), show='headings', height=10)
        tree.column("# 1", anchor=CENTER, width=50)
        tree.heading("# 1", text="Id")
        tree.column("# 2", anchor=W, width=200)
        tree.heading("# 2", text="Nombre del Curso")
        tree.column("# 3", anchor=CENTER, width=100)
        tree.heading("# 3", text="Año")

        tree.bind("<<TreeviewSelect>>", seleccionarRegistro)  # Evento de selección
        tree.pack()
        if Configuracion.VerificarConfiguracion() == True and verificarVacio() == False:
            actualizarTreeView()

    except Exception as e:
        print(f"Error al inicializar la interfaz: {e}")


def guardarRegistros():
    try:
        nombreCurso = textBoxNombreCurso.get()
        #Las verificaciones tienen este formato
        if VerificacionesDatos.VerificarStringValido(nombreCurso) == False:
                messagebox.showerror("Error", "El nombre del curso no es valido, los siguentes caracteres no estan permitidos '.', ':', ';', ',', '´', '{', '}', '\\', '/'")
                return
            
        anio = textBoxAnio.get()
        if VerificacionesDatos.VerificarDNI(anio) == False:
                messagebox.showerror("Error", "El año no es valido")
                return

        if not nombreCurso or not anio:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        CCurso.ingresarCurso(nombreCurso, anio)
        messagebox.showinfo("Información", "Curso guardado correctamente")
        actualizarTreeView()

        textBoxNombreCurso.delete(0, END)
        textBoxAnio.delete(0, END)

    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar el curso: {e}")

def actualizarTreeView():
    try:
        # Eliminar todos los elementos actuales en la tabla
        for item in tree.get_children():
            tree.delete(item)

        # Agregar datos actualizados
        for row in CCurso.mostrarCursos():
            tree.insert("", "end", values=row)

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

            textBoxNombreCurso.delete(0, END)
            textBoxNombreCurso.insert(0, valores[1])

            textBoxAnio.delete(0, END)
            textBoxAnio.insert(0, valores[2])

    except Exception as e:
        print(f"Error al seleccionar un registro: {e}")

def modificarRegistros():
    try:
        idCurso = textBoxId.get()
        
        nombreCurso = textBoxNombreCurso.get()
        if VerificacionesDatos.VerificarStringValido(nombreCurso) == False:
                messagebox.showerror("Error", "El nombre del curso no es valido, los siguentes caracteres no estan permitidos '.', ':', ';', ',', '´', '{', '}', '\\', '/'")
                return
        
        anio = textBoxAnio.get()
        if VerificacionesDatos.VerificarDNI(anio) == False:
                messagebox.showerror("Error", "El año no es valido")
                return

        if not idCurso or not nombreCurso or not anio:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        CCurso.modificarCurso(idCurso, nombreCurso, anio)
        messagebox.showinfo("Información", "Curso modificado correctamente")
        actualizarTreeView()

        textBoxId.config(state=NORMAL)
        textBoxId.delete(0, END)
        textBoxId.config(state="readonly")
        textBoxNombreCurso.delete(0, END)
        textBoxAnio.delete(0, END)

    except Exception as e:
        messagebox.showerror("Error", f"Error al modificar el curso: {e}")

def eliminarRegistros():
    try:
        idCurso = textBoxId.get()

        if not idCurso:
            messagebox.showerror("Error", "Debe seleccionar un curso para eliminar")
            return

        CCurso.eliminarCurso(idCurso)
        messagebox.showinfo("Información", "Curso eliminado correctamente")
        actualizarTreeView()

        textBoxId.config(state=NORMAL)
        textBoxId.delete(0, END)
        textBoxId.config(state="readonly")
        textBoxNombreCurso.delete(0, END)
        textBoxAnio.delete(0, END)

    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar el curso: {e}")

#Formulario()
