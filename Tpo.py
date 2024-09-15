"""Esta es la función "fusiona" la anterior con la que hice yo aparte. Agrega cosas como el año, la posibilidad de detectar si ese año es bisiesto, aparte acomode un toque las cosas
y aproveché para "aclarar" para que sirve cada función. Feli."""
 

import random

# Lista para almacenar usuarios.
usuarios = []

# Lista para almacenar las reservas realizadas.
reservas = []

# INDEX DE CADA VALOR
año_index = 3;
dia_index = 2;
mes_index = 1;
id_index = 0;

# Función para determinar si un año es bisiesto o no.
def esBisiesto(anio):
    if anio % 4 == 0:
        if anio % 100 != 0 or anio % 400 == 0:
            return True
    return False

# Función que define la cantidad de días que hay en un mes.
def mesesMatriz(mes, anio):
    dias = 31
    match mes:
        case 1 | 3 | 5 | 7 | 8 | 10 | 12:
            dias
        case 4 | 6 | 9 | 11:
            dias = 30
        case 2:
            dias = 28 if not esBisiesto(anio) else 29
    return dias

# Función que aclara el nombre del mes.
def obtenerNombreMes(mes):
    match mes:
        case 1:
            return 'Enero'
        case 2:
            return 'Febrero'
        case 3:
            return 'Marzo'
        case 4:
            return 'Abril'
        case 5:
            return 'Mayo'
        case 6:
            return 'Junio'
        case 7:
            return 'Julio'
        case 8:
            return 'Agosto'
        case 9:
            return 'Septiembre'
        case 10:
            return 'Octubre'
        case 11:
            return 'Noviembre'
        case 12:
            return 'Diciembre'
        
def chequearDisponibilad(mes, dia, anio):
    esta_disponible = True
    for reserva in reservas:
        if(reserva[1] == mes and reserva[2] == dia and reserva[3] == anio):
            esta_disponible = False
            break
    return esta_disponible

# Función para generar reservas aleatorias.
def generarReservasRandom(cantidad, reservas, anio):
    for i in range(cantidad):
        reserva = []
        mes = random.randint(1,12)
        reserva.append(mes)
        dia = random.randint(1, mesesMatriz(mes, anio))
        esta_disponible = chequearDisponibilad(mes, dia, anio)
        if(esta_disponible):
            reservas.append([len(reservas), mes, dia, anio])

generarReservasRandom(10, reservas, 2023)

# Muestra las reservas.
def mostrarReservas():
    print(f"{'ID':<3} {'MES':<10} {'DIA':<5} {'AÑO':<7}")
    for reserva in reservas:
        id_reserva = reserva[id_index]
        mes_reserva = obtenerNombreMes(reserva[mes_index])
        dia_reserva = reserva[dia_index]
        anio_reserva = reserva[año_index]
        print(f'{id_reserva:<3} {mes_reserva:<10} {dia_reserva:<5} {anio_reserva:<7}')

mostrarReservas()

def obtenerDiasOcupadosPorMes(mes, anio):
    dias_ocupados = []
    for reserva in reservas:
        if(reserva[mes_index] == mes and reserva[año_index] == anio):
            dias_ocupados.append(reserva[2])
    return dias_ocupados

# Muestra los días disponibles, los días ocupados son marcados con 'X'.
def mostrarDisponibilidadMensual(mes, dias_ocupados, anio):
    dias = mesesMatriz(mes, anio)
    filas = []

    for dia in range(1, dias + 1, 7):
        nueva_fila = []
        for d in range(dia, dia + 7):
            if d <= dias:
                nueva_fila.append("%d" % d if d not in dias_ocupados else 'X')
        filas.append(nueva_fila)

    print("Los días no disponibles se marcarán con una 'X'.")
    print("Lun Mar Mie Jue Vie Sab Dom")

    for fila in filas:
        fila_formateada = ""
        for dia in fila:
            fila_formateada += " " * (3 - len(dia)) + dia
        print(fila_formateada)
        
def filtrarReservasPorMes(reservas, mes):
    reservasPorMes = []
    for reserva in reservas:
        if reserva[1] == mes:
            reservasPorMes.append(reserva)
    print(f"{'ID':<3} {'MES':<10} {'DIA':<5} {'AÑO':<7}")
    for reserva in reservasPorMes:
        id_reserva = reserva[id_index]
        mes_reserva = obtenerNombreMes(reserva[mes_index])
        dia_reserva = reserva[dia_index]
        anio_reserva = reserva[año_index]

        print(f'{id_reserva:<3} {mes_reserva:<10} {dia_reserva:<5} {anio_reserva:<7}')

def eliminarReserva(reservas, id):
    for reserva in reservas:
        if reserva[0] == id:
            reservas.remove(reserva)
    print("Reserva eliminada exitosamente")
    mostrarReservas()
    

# Función para crear un usuario.
def creacionUsuario():
    user_name = input("Ingrese el nombre y apellido del usuario que reservó la sala: ")
    while len(user_name) < 3:
        user_name = input("Error. El nombre de usuario debe ser mayor a 3 caracteres: ")
    return user_name

def inputEnteroConSalida(numero_salida, valor_minimo, valor_maximo, texto):
    value = int(input(texto))        
    rangoDeValor = list(range(valor_minimo, valor_maximo + 1))
    while value not in rangoDeValor and value != numero_salida:  # Corrección en la condición
        value = int(input(texto))
    return value
    

# Función para tomar reservas.
def tomaDeReservas():
    mes_de_busqueda = inputEnteroConSalida(-1, 1, 12,"Ingrese el número del mes en el que le gustaría realizar la reserva o ingrese -1 para finalizar: ")
      
    if mes_de_busqueda == -1:
        return
    
    anio_de_reserva = int(input("Ingrese el año de la reserva: "))
    
    dias_ocupados = obtenerDiasOcupadosPorMes(mes_de_busqueda, anio_de_reserva) ## devuelve array con los dias ocupados en ese mes

    mostrarDisponibilidadMensual(mes_de_busqueda, dias_ocupados, anio_de_reserva)

    dia_reservado = int(input("Ingrese el día que quiere reservar: "))

    while dia_reservado not in range(1, mesesMatriz(mes_de_busqueda, anio_de_reserva)) or dia_reservado in dias_ocupados:
        dia_reservado = int(input("Día no disponible o inválido. Ingrese otro día: "))
    
    nombre_reserva = input("Ingrese nombre de la reserva");
    reservas.append([len(reservas) + 1, mes_de_busqueda, dia_reservado, anio_de_reserva, nombre_reserva])
    mostrarReservas()


# Función principal.
def main():
    print("Bienvenido al sistema de reserva de salas de reuniones.")
    continuar = True
    
    
    while continuar:
        opcion = inputEnteroConSalida(-1, 1, 4, "Ingrese 1 para reservar, 2 para ver todas las reservas, 3 para eliminar, 4 para filtrar, o -1 para salir: ")
        print(opcion)
        
        if(opcion == 1):
            tomaDeReservas()


        if(opcion == 2):
            mostrarReservas()
        
        if(opcion == 3):
            id = inputEnteroConSalida(-1, 0, 1000, "Ingrese el numero de id de la reserva a eliminar: ")
            eliminarReserva(reservas, id)
            
        if(opcion == 4):
            mes = inputEnteroConSalida(-1, 1,12, "Ingrese el numero del mes que quiere buscar: ")
            filtrarReservasPorMes(reservas, mes)
            
        respuesta = int(input("¿Le gustaría utilizar otra opción? 1. Sí  2. No: "))

        if respuesta != 1:
            continuar = False

    print("Gracias por usar el sistema de reservas. Fin.")


main()
