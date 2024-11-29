import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
#instalar en la terminar pip install tkcalendar para que funcione
from tkcalendar import DateEntry, Calendar
from Conexion import *
from Configuracion import *
from verificaciones import *
from Docente import CDocente  # Clase de Docente
from Materia import CMateria  # Clase de Materia, usada para obtener las materias disponibles

# Declaración de variables globales
base = None
textBoxId = None
textBoxNombre = None
textBoxApellido = None
textBoxDocumento = None
textBoxFechaNacimiento = None
textBoxTelefono = None
textBoxDomicilio = None
comboMaterias = None
tree = None

"""from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry"""

# Modificación en la función `Formulario`
def Formulario(parent=None):
    global textBoxId, textBoxNombre, textBoxApellido, textBoxDocumento, textBoxFechaNacimiento
    global textBoxTelefono, textBoxDomicilio, comboMaterias, tree

    try:
        if parent is None:
            raise ValueError("El argumento 'parent' es obligatorio para integrar el formulario en la interfaz principal")

        # GroupBox para los datos
        groupBox = LabelFrame(parent, text="Datos del Docente", padx=5, pady=5)
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

        Label(groupBox, text="Materia:", font=('arial', 12)).grid(row=7, column=0)
        comboMaterias = ttk.Combobox(groupBox, postcommand=cargarMaterias)
        comboMaterias.grid(row=7, column=1)
        cargarMaterias()  # Carga las materias en el ComboBox

        # Botones
        Button(groupBox, text="Guardar", width=10, command=guardarRegistros).grid(row=8, column=0)
        Button(groupBox, text="Modificar", width=10, command=modificarRegistros).grid(row=8, column=1)
        Button(groupBox, text="Eliminar", width=10, command=eliminarRegistros).grid(row=8, column=2)

        # GroupBox para la tabla
        groupBoxTabla = LabelFrame(parent, text="Lista de Docentes", padx=5, pady=5)
        groupBoxTabla.grid(row=0, column=1, padx=5, pady=5)

        # Tabla
        tree = ttk.Treeview(groupBoxTabla,
                            columns=("Id", "Nombre", "Apellido", "Documento", "Edad", "Teléfono", "Domicilio", "Materia"),
                            show='headings', height=20)
        tree.column("#1", anchor=CENTER, width=50)
        tree.heading("#1", text="Id")
        tree.column("#2", anchor=W, width=100)
        tree.heading("#2", text="Nombre")
        tree.column("#3", anchor=W, width=100)
        tree.heading("#3", text="Apellido")
        tree.column("#4", anchor=W, width=100)
        tree.heading("#4", text="Documento")
        tree.column("#5", anchor=W, width=50)
        tree.heading("#5", text="Edad")
        tree.column("#6", anchor=W, width=100)
        tree.heading("#6", text="Teléfono")
        tree.column("#7", anchor=W, width=150)
        tree.heading("#7", text="Domicilio")
        tree.column("#8", anchor=W, width=150)
        tree.heading("#8", text="Materia")

        tree.bind("<<TreeviewSelect>>", seleccionarRegistro)  # Evento de selección
        tree.pack()
        if Configuracion.VerificarConfiguracion() == True and verificarVacio() == False:
            actualizarTreeView()


    except Exception as e:
        print(f"Error al inicializar la interfaz: {e}")



def cargarMaterias():
    """Carga las materias en el ComboBox desde la base de datos."""
    try:
        materias = CMateria.mostrarMaterias()
        comboMaterias['values'] = [f"{materia[0]} - {materia[1]}" for materia in materias]  # Ejemplo: "1 - Matemática"
        if materias:
            comboMaterias.current(0)  # Selecciona el primer elemento por defecto
    except Exception as e:
        print(f"Error al cargar las materias: {e}")

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
        
        fechaNacimiento = textBoxFechaNacimiento.get_date()
        print(fechaNacimiento)
        if VerificacionesDatos.ChequearFechaDocente(fechaNacimiento) == False:
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
        materiaSeleccionada = comboMaterias.get()

        if not nombre or not apellido or not documento or not fechaNacimiento or not telefono or not domicilio or not materiaSeleccionada:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        #materiaID = materiaSeleccionada.split(" - ")[0]  # Obtiene el ID de la materia desde el ComboBox
        CDocente.ingresarDocente(nombre, apellido, documento, fechaNacimiento, telefono, domicilio, materiaSeleccionada[0])
        messagebox.showinfo("Información", "Docente guardado correctamente")
        actualizarTreeView()
        

        textBoxNombre.delete(0, END)
        textBoxApellido.delete(0, END)
        textBoxDocumento.delete(0, END)
        textBoxFechaNacimiento.delete(0, END)
        textBoxTelefono.delete(0, END)
        textBoxDomicilio.delete(0, END)

    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar el docente: {e}")

def actualizarTreeView():
    try:
        # Eliminar todos los elementos actuales en la tabla
        for item in tree.get_children():
            tree.delete(item)


        # Agregar datos actualizados
        docentes = CDocente.mostrarDocentes()
        materias = {materia[0]: materia[1] for materia in CMateria.mostrarMaterias()}  # Diccionario para obtener nombres de materias

        for row in docentes:
            materiaNombre = materias.get(row[7], "Desconocido")  # row[7] es MateriaID
            tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], materiaNombre))
            

    except Exception as e:
    
        print(f"Error al actualizar la tabla: {e}")
        


def seleccionarRegistro(event):
    try:
        # Obtener el elemento seleccionado en el Treeview
        item = tree.focus()
        valores = tree.item(item, 'values')
        materias = CMateria.mostrarMaterias()


        for tupla in materias:
            if valores[7] in tupla:
                materia = tupla[0]
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

            # Edad no tiene campo editable, no lo asignamos
            # valores[4] corresponde a Edad (no editable)
            textBoxFechaNacimiento.set_date(CDocente.obtenerFechaNacimiento(valores[0]))  # Fecha Nacimiento

            textBoxTelefono.delete(0, END)
            textBoxTelefono.insert(0, valores[5])  # Teléfono

            textBoxDomicilio.delete(0, END)
            textBoxDomicilio.insert(0, valores[6])  # Domicilio

            comboMaterias.set(materia)  # Materia

    except Exception as e:
        print(f"Error al seleccionar un registro: {e}")


def modificarRegistros():
    try:
        idDocente = textBoxId.get()
        
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
        fechaNacimiento = textBoxFechaNacimiento.get_date()
        if VerificacionesDatos.ChequearFechaDocente(fechaNacimiento) == False:
                messagebox.showerror("Error", "La fecha de nacimiento no es valida")
                
        telefono = textBoxTelefono.get()
        if VerificacionesDatos.VerificarTelefono(telefono) == False:
                messagebox.showerror("Error", "El telefono no es valido")        
                return
            
        domicilio = textBoxDomicilio.get()
        if VerificacionesDatos.VerificarStringValido(domicilio) == False:
                messagebox.showerror("Error", "El domicilio no es valido, los siguentes caracteres no estan permitidos '.', ':', ';', ',', '´', '{', '}', '\\', '/'")
                return
            
        materiaSeleccionada = comboMaterias.get()

        if not idDocente or not nombre or not apellido or not documento or not fechaNacimiento or not telefono or not domicilio or not materiaSeleccionada:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        #materiaID = materiaSeleccionada.split(" - ")[0]  # Obtiene el ID de la materia desde el ComboBox
        CDocente.modificarDocente(idDocente, nombre, apellido, documento, fechaNacimiento, telefono, domicilio, materiaSeleccionada[0])
        messagebox.showinfo("Información", "Docente modificado correctamente")
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
        messagebox.showerror("Error", f"Error al modificar el docente: {e}")

def eliminarRegistros():
    try:
        idDocente = textBoxId.get()

        if not idDocente:
            messagebox.showerror("Error", "Debe seleccionar un docente para eliminar")
            return

        CDocente.eliminarDocente(idDocente)
        messagebox.showinfo("Información", "Docente eliminado correctamente")
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
        messagebox.showerror("Error", f"Error al eliminar el docente: {e}")

#Formulario()
