import datetime


class VerificacionesFechas:
    def conseguirFecha():
        hoy = datetime.datetime.now()
        return hoy
    
    def convertir_fecha(fecha_str):
        # Evaluar la cadena para obtener el objeto datetime.date
        fecha_obj = eval(fecha_str)
        
        # Verificar si es una tupla con un solo elemento
        if isinstance(fecha_obj, tuple) and len(fecha_obj) == 1:
            fecha_obj = fecha_obj[0]
        
        # Convertir el objeto datetime.date al formato deseado
        if isinstance(fecha_obj, datetime.date):
            return fecha_obj.strftime('%Y-%m-%d')
        else:
            raise ValueError("El valor proporcionado no es una fecha válida")

class VerificacionesDatos:
    def ChequearFechaDocente(fechaNacimiento):
        #Calcula la edad en base a la fecha actual y la fecha de nacimiento
        print(fechaNacimiento)
        try:      
            if fechaNacimiento != None:             
                hoy = datetime.date.today()
                edad = hoy.year - fechaNacimiento.year - ((hoy.month, hoy.day) < (fechaNacimiento.month, fechaNacimiento.day))
            
            print(edad)
            
            if edad <= 17:
                return False
            else:
                return edad 
            
        except ValueError as error:
            print(f"Error al calcular la edad, error {error}")
            
    def ChequearFechaAlumno(fechaNacimiento):
        #Calcula la edad en base a la fecha actual y la fecha de nacimiento
        print(fechaNacimiento)
        try:      
            if fechaNacimiento != None:             
                hoy = datetime.date.today()
                edad = hoy.year - fechaNacimiento.year - ((hoy.month, hoy.day) < (fechaNacimiento.month, fechaNacimiento.day))
            
            print(edad)
            
            if edad <= 12:
                return False
            else:
                return edad 
            
        except ValueError as error:
            print(f"Error al calcular la edad, error {error}")
            
    """def VerificarDNI(DNI):
    #Verificar que el DNI sea un numero entero no negativo de 8 digitos
        if isinstance(DNI, str) and DNI.isdigit() and len(DNI) in range (1, 8) and DNI != "0":
            return True
        else:
            return False """ 
    
    def VerificarDNI(DNI):
        if isinstance(DNI, str) and DNI.isdigit() and len(DNI) == 8 and DNI != "0":
            return True
        else:
            return False


    def VerificarTelefono(telefono):
    #Verificar que el DNI sea un numero entero no negativo de 8 digitos
        if isinstance(telefono, str) and telefono.isdigit() and len(telefono) in range(8, 15):
            return True
        else:
            return False
     
        
    def VerificarStringValido(variable):
    # Caracteres prohibidos
        caracteres_prohibidos = ['.', ':', ';', ',', "'", '"', '|', '°', '´', '{', '}', '\\', '/']
        
        # Verifica si la variable es un string, tiene menos o igual a 25 caracteres y no contiene caracteres prohibidos
        if isinstance(variable, str) and variable != "" and len(variable) in range(3, 25) and not any(caracter in variable for caracter in caracteres_prohibidos):
            return True
        else:
            return False