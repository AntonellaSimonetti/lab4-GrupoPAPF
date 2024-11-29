import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
#instalar en la terminar pip install tkcalendar para que funcione
from tkcalendar import DateEntry, Calendar
from Conexion import *
from Configuracion import *
from verificaciones import *
from Alumno import CAlumno  # Clase de Alumno
from Curso import CCurso  # Clase de Curso, usada para obtener los cursos disponibles
import datetime

# Declaración de variables globales
base = None
textBoxId = None
textBoxNombre = None
textBoxApellido = None
textBoxDocumento = None
textBoxFechaNacimiento = None
textBoxTelefono = None
textBoxDomicilio = None
comboCursos = None
tree = None



"""from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry"""

# Modificación en la función `Formulario`
def Formulario(parent=None):
    global textBoxId, textBoxNombre, textBoxApellido, textBoxDocumento, textBoxFechaNacimiento
    global textBoxTelefono, textBoxDomicilio, comboCursos, tree

    try:
        if parent is None:
            raise ValueError("El argumento 'parent' es obligatorio para integrar el formulario en la interfaz principal")

        # GroupBox para los datos
        groupBox = LabelFrame(parent, text="Datos del Alumno", padx=5, pady=5)
        groupBox.grid(row=0, column=0, padx=10, pady=10, sticky="N")

        # Campos de entrada
        Label(groupBox, text="Id:", font=('arial', 12)).grid(row=0, column=0)
        textBoxId = Entry(groupBox, state="readonly")  # Campo solo lectura
        textBoxId.grid(row=0, column=1)

        Label(groupBox, text="Nombre:", font=('arial', 12)).grid(row=1, column=0)
        textBoxNombre = Entry(groupBox)
        textBoxNombre.grid(row=1, column=1)

        Label(groupBox, text="Apellido:", font=('arial', 12)).grid(row=2, column=0)
        textBoxApellido = Entry(groupBox)
        textBoxApellido.grid(row=2, column=1)

        Label(groupBox, text="Documento:", font=('arial', 12)).grid(row=3, column=0)
        textBoxDocumento = Entry(groupBox)
        textBoxDocumento.grid(row=3, column=1)

        # Reemplazo de textBoxFechaNacimiento con DateEntry
        Label(groupBox, text="Fecha Nacimiento (yyyy/mm/dd):", font=('arial', 12)).grid(row=4, column=0)
        textBoxFechaNacimiento = DateEntry(groupBox, width=12, background='darkblue', 
                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        textBoxFechaNacimiento.grid(row=4, column=1)

        Label(groupBox, text="Teléfono:", font=('arial', 12)).grid(row=5, column=0)
        textBoxTelefono = Entry(groupBox)
        textBoxTelefono.grid(row=5, column=1)

        Label(groupBox, text="Domicilio:", font=('arial', 12)).grid(row=6, column=0)
        textBoxDomicilio = Entry(groupBox)
        textBoxDomicilio.grid(row=6, column=1)

        Label(groupBox, text="Curso:", font=('arial', 12)).grid(row=7, column=0)
        comboCursos = ttk.Combobox(groupBox, postcommand=cargarCursos)
        comboCursos.grid(row=7, column=1)
        cargarCursos()  # Carga los cursos en el ComboBox

        # Botones
        Button(groupBox, text="Guardar", width=10, command=guardarRegistros).grid(row=8, column=0)
        Button(groupBox, text="Modificar", width=10, command=modificarRegistros).grid(row=8, column=1)
        Button(groupBox, text="Eliminar", width=10, command=eliminarRegistros).grid(row=8, column=2)

        # GroupBox para la tabla
        groupBoxTabla = LabelFrame(parent, text="Lista de Alumnos", padx=5, pady=5)
        groupBoxTabla.grid(row=0, column=1, padx=5, pady=5)

        # Tabla
        tree = ttk.Treeview(groupBoxTabla,
                            columns=("Id", "Nombre", "Apellido", "Documento", """ "Edad",""" "Teléfono",
                                     "Domicilio", "Curso"), show='headings', height=20)
        tree.column("# 1", anchor=CENTER, width=30)
        tree.heading("# 1", text="Id")
        tree.column("# 2", anchor=W, width=100)
        tree.heading("# 2", text="Nombre")
        tree.column("# 3", anchor=W, width=100)
        tree.heading("# 3", text="Apellido")
        tree.column("# 4", anchor=W, width=100)
        tree.heading("# 4", text="Documento")
        """tree.column("# 5", anchor=W, width=120)
        tree.heading("# 5", text="Edad")"""
        tree.column("# 5", anchor=W, width=100)
        tree.heading("# 5", text="Teléfono")
        tree.column("# 6", anchor=W, width=100)
        tree.heading("# 6", text="Domicilio")
        tree.column("# 7", anchor=W, width=100)
        tree.heading("# 7", text="Curso")

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
        comboCursos['values'] = [f"{curso[0]} - {curso[1]}" for curso in cursos]  # Ejemplo: "1 - Matemática"
        if cursos:
            comboCursos.current(0)  # Selecciona el primer elemento por defecto
    except Exception as e:
        print(f"Error al cargar los cursos: {e}")

def guardarRegistros():
    try:
        nombre = textBoxNombre.get()
        #Las verificaciones tienen este formato
        if VerificacionesDatos.VerificarStringValido(nombre) == False:
                messagebox.showerror("Error", "El nombre no es valido, los siguentes caracteres no estan permitidos '.', ':', ';', ',', '´', '{', '}', '\\', '/'")
                return
        
        apellido = textBoxApellido.get()
        if VerificacionesDatos.VerificarStringValido(apellido) == False:
                messagebox.showerror("Error", "El apeliido no es valido, los siguentes caracteres no estan permitidos '.', ':', ';', ',', '´', '{', '}', '\\', '/'")                
                return
        
        documento = textBoxDocumento.get()
        if VerificacionesDatos.VerificarDNI(documento) == False:
                messagebox.showerror("Error", "El DNI no es valido")
                return
        
        fechaNacimiento = textBoxFechaNacimiento.get_date()  # Esto debería obtener la fecha en el formato correcto
        if VerificacionesDatos.ChequearFechaAlumno(fechaNacimiento) == False:
                messagebox.showerror("Error", "La fecha de nacimiento no es valida")
                return
        
        telefono = textBoxTelefono.get()
        if VerificacionesDatos.VerificarTelefono(telefono) == False:
                messagebox.showerror("Error", "El telefono no es valido")        
                return
        
        domicilio = textBoxDomicilio.get()
        if VerificacionesDatos.VerificarStringValido(domicilio) == False:
                messagebox.showerror("Error", "El domicilio no es valido, los siguentes caracteres no estan permitidos '.', ':', ';', ',', '´', '{', '}', '\\', '/'")
                return
        
        cursoSeleccionado = comboCursos.get()

        if not nombre or not apellido or not documento or not fechaNacimiento or not telefono or not domicilio or not cursoSeleccionado:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        #cursoID = cursoSeleccionado.split(" - ")[0]  # Obtiene el ID del curso desde el ComboBox
        CAlumno.ingresarAlumno(nombre, apellido, documento, fechaNacimiento, telefono, domicilio, cursoSeleccionado[0])
        messagebox.showinfo("Información", "Alumno guardado correctamente")
        actualizarTreeView()
        
        textBoxNombre.delete(0, END)
        textBoxApellido.delete(0, END)
        textBoxDocumento.delete(0, END)
        textBoxFechaNacimiento.delete(0, END)
        textBoxTelefono.delete(0, END)
        textBoxDomicilio.delete(0, END)

    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar el alumno: {e}")

def actualizarTreeView():
    try:
        # Eliminar todos los elementos actuales en la tabla
        for item in tree.get_children():
            tree.delete(item)

        # Agregar datos actualizados
        alumnos = CAlumno.mostrarAlumnos()
        cursos = {curso[0]: curso[1] for curso in CCurso.mostrarCursos()}  # Diccionario para obtener nombres de cursos

        #Cone = CConexion.ConexionBaseDeDatos()
        #cursor = Cone.cursor()

        
        for row in alumnos:
            cursoID = cursos.get(row[7], "Desconocido") 
            #cursoNombre = cursoID
            #print(cursoID)
            #cursor.execute(f"SELECT NombreCurso FROM Curso WHERE ID = {cursoID}")
            #cursoNombre = cursor.fetchone()
            tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[5], row[6], cursoID))  # Aquí se incluye row[4] para Fecha Nacimiento

    except Exception as e:
        print(f"Error al actualizar la tabla: {e}")


def seleccionarRegistro(event):
    try:
        item = tree.focus()
        valores = tree.item(item, 'values')
        cursos = CCurso.mostrarCursos()


        for tupla in cursos:
            if valores[6] in tupla:
                curso = tupla[0]
                break

        if valores:
            # Asignar cada valor a su campo correspondiente
            textBoxId.config(state=NORMAL)
            textBoxId.delete(0, END)
            textBoxId.insert(0, valores[0])  # Id
            textBoxId.config(state="readonly")

            textBoxNombre.delete(0, END)
            textBoxNombre.insert(0, valores[1])  # Nombre

            textBoxApellido.delete(0, END)
            textBoxApellido.insert(0, valores[2])  # Apellido

            textBoxDocumento.delete(0, END)
            textBoxDocumento.insert(0, valores[3])  # Documento

            # Asignar la fecha de nacimiento al DateEntry
            textBoxFechaNacimiento.set_date(CAlumno.ObtenerFechaNacimiento(valores[0]))  # Fecha Nacimiento

            textBoxTelefono.delete(0, END)
            textBoxTelefono.insert(0, valores[4])  # Teléfono

            textBoxDomicilio.delete(0, END)
            textBoxDomicilio.insert(0, valores[5])  # Domicilio

            comboCursos.set(curso)  # Curso seleccionado

    except Exception as e:
        return



def modificarRegistros():
    try:
        # Obtener datos del formulario
        idAlumno = textBoxId.get()
        
        nombre = textBoxNombre.get()
        if VerificacionesDatos.VerificarStringValido(nombre) == False:
                messagebox.showerror("Error", "El nombre no es valido, los siguentes caracteres no estan permitidos '.', ':', ';', ',', '´', '{', '}', '\\', '/'")
                return
            
        apellido = textBoxApellido.get()
        if VerificacionesDatos.VerificarStringValido(apellido) == False:
                messagebox.showerror("Error", "El apeliido no es valido, los siguentes caracteres no estan permitidos '.', ':', ';', ',', '´', '{', '}', '\\', '/'")                
                return
        
        documento = textBoxDocumento.get()
        if VerificacionesDatos.VerificarDNI(documento) == False:
                messagebox.showerror("Error", "El DNI no es valido")
                return
        
        fechaNacimiento = textBoxFechaNacimiento.get_date()  # Obtener la fecha seleccionada
        if VerificacionesDatos.ChequearFechaAlumno(fechaNacimiento) == False:
                messagebox.showerror("Error", "La fecha de nacimiento no es valida")
                return
        
        telefono = textBoxTelefono.get()
        if VerificacionesDatos.VerificarTelefono(telefono) == False:
                messagebox.showerror("Error", "El telefono no es valido")        
                return
        
        domicilio = textBoxDomicilio.get()
        if VerificacionesDatos.VerificarStringValido(domicilio) == False:
                messagebox.showerror("Error", "El domicilio no es valido, los siguentes caracteres no estan permitidos '.', ':', ';', ',', '´', '{', '}', '\\', '/'")
                return
        
        cursoSeleccionado = comboCursos.get()

        # Validar que no haya campos vacíos
        if not idAlumno or not nombre or not apellido or not documento or not fechaNacimiento or not telefono or not domicilio or not cursoSeleccionado:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        # Depuración de la fecha
        #print(f"Fecha Nacimiento: {fechaNacimiento}")

        # Extraer el ID del curso seleccionado
        #cursoID = cursoSeleccionado.split(" - ")[0]  # Ejemplo: "1 - Matemática"

        #HOLA ANTO, aca estuve teniendo problemas con la funcion split, me tiro error de dato asi que simplemente use el string original y lo trate como una lista

        # Llamar al método de modificación en la clase `CAlumno`
        CAlumno.modificarAlumno(idAlumno, nombre, apellido, documento, fechaNacimiento, telefono, domicilio, cursoSeleccionado[0])

        # Mostrar mensaje de éxito
        messagebox.showinfo("Información", "Alumno modificado correctamente")

        # Actualizar el Treeview
        actualizarTreeView()

        # Limpiar los campos del formulario
        textBoxId.config(state=NORMAL)
        textBoxId.delete(0, END)
        textBoxId.config(state="readonly")
        textBoxNombre.delete(0, END)
        textBoxApellido.delete(0, END)
        textBoxDocumento.delete(0, END)
        textBoxFechaNacimiento.set_date(VerificacionesFechas.conseguirFecha())  # Limpiar el DateEntry
        textBoxTelefono.delete(0, END)
        textBoxDomicilio.delete(0, END)

    except Exception as e:
        messagebox.showerror("Error", f"Error al modificar el alumno: {e}")


def eliminarRegistros():
    try:
        idAlumno = textBoxId.get()

        if not idAlumno:
            messagebox.showerror("Error", "Debe seleccionar un alumno para eliminar")
            return

        CAlumno.eliminarAlumno(idAlumno)
        messagebox.showinfo("Información", "Alumno eliminado correctamente")
        actualizarTreeView()

        textBoxId.config(state=NORMAL)
        textBoxId.delete(0, END)
        textBoxId.config(state="readonly")
        textBoxNombre.delete(0, END)
        textBoxApellido.delete(0, END)
        textBoxDocumento.delete(0, END)
        textBoxFechaNacimiento.delete(0, END)
        textBoxTelefono.delete(0, END)
        textBoxDomicilio.delete(0, END)

    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar el alumno: {e}")

#Formulario()
