import csv
import os

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox

path = './config.csv'

class Configuracion():
    
    def VerificarConfiguracion():
        existe = os.path.exists(path) 
        return existe

    def LeerConfiguracion():
        with open(path, 'r') as archivo:
            config = []
            lineas = archivo.readlines()
            
            for linea in lineas:
                config.append(linea.strip())
        return config
                
#Formulario para la configuracion de la conexion de la base de datos              
def FormularioConfiguracion():
    
    global base
    global groupBox
    global textBoxUsuario
    global textBoxPassword
    global textBoxHost
    global textBoxBaseDeDatos
    
    try:
        base = Tk()
        base.geometry("255x220")
        base.title("Configuracion Base de Datos")

        groupBox = LabelFrame(base, text="Datos de la Base de Datos",  padx=5, pady=5)
        groupBox.grid(row=0, column=0, padx=10, pady=10)
        
        labelUsuario = Label(groupBox, text="Usuario").grid(row=0, column=0, padx=5, pady=5)
        textBoxUsuario = Entry(groupBox)
        textBoxUsuario.grid(row=0, column=1, padx=5, pady=5)
        
        
        labelPassword = Label(groupBox, text="Password").grid(row=1, column=0, padx=5, pady=5)
        textBoxPassword = Entry(groupBox)
        textBoxPassword.grid(row=1, column=1, padx=5, pady=5)
        
        
        labelHost = Label(groupBox, text="Host").grid(row=2, column=0, padx=5, pady=5)
        textBoxHost = Entry(groupBox)
        textBoxHost.grid(row=2, column=1, padx=5, pady=5)
        
        
        labelBaseDeDatos = Label(groupBox, text="Base de Datos").grid(row=3, column=0, padx=5, pady=5)
        textBoxBaseDeDatos = Entry(groupBox)
        textBoxBaseDeDatos.grid(row=3, column=1, padx=5, pady=5)
        Button(groupBox, text="Guardar", width=10, command=GuardarConfiguracion).grid(row=4, column=0, padx=5, pady=5)
        
    except ValueError as error:
        print(f"Error al mostrar la interfaz, error {error}")

def GuardarConfiguracion():
    global textBoxUsuario
    global textBoxPassword
    global textBoxHost
    global textBoxBaseDeDatos
    
    try:
        if textBoxUsuario is None or textBoxPassword is None or textBoxHost is None or textBoxBaseDeDatos is None:
            return
        
        configConexion = [textBoxUsuario.get(), textBoxPassword.get(), textBoxHost.get(), textBoxBaseDeDatos.get()]
        
        try:
            with open(path, 'w+') as archivo:
                for dato in configConexion:
                    archivo.write(dato)
                    archivo.write('\n')
        
            messagebox.showinfo("Informacion", "Configuracion Guardada, el programa se cerrara.")
            exit(1)
            
        except Exception as error:
            print(f"Error al guardar la configuracion, error {error}")
        
    
    except ValueError as error:
        print(f"Error al guardar la configuracion, error {error}")
        
def verificarVacio():
    datos = Configuracion.LeerConfiguracion()
    if datos[0] == "" or datos[1] == "" or datos[2] == "" or datos[3] == "":
        os.remove(path)
        return True
    else:
        return False