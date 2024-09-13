"""Esta es la función "fusiona" la anterior con la que hice yo aparte. Agrega cosas como el año, la posibilidad de detectar si ese año es bisiesto, aparte acomode un toque las cosas
y aproveché para "aclarar" para que sirve cada función. Feli."""
 

import random

# Lista para almacenar usuarios.
usuarios = []

# Lista para almacenar las reservas realizadas.
reservas = []

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

# Función para generar reservas aleatorias.
def generarReservasRandom(cantidad, reservas, anio):
    for i in range(cantidad):
        mes = random.randint(1, 12)
        dia = random.randint(1, mesesMatriz(mes, anio))
        reservas.append([len(reservas) + 1, mes, dia, anio])

# Muestra las reservas.
def mostrarReservas():
    print("ID   Mes         Día   Año    Usuario")
    for reserva in reservas:
        id_reserva = reserva[0]
        mes_reserva = obtenerNombreMes(reserva[1])
        dia_reserva = reserva[2]
        anio_reserva = reserva[3]
        usuario = reserva[4]

        # Agrega los espacios para que quede bonito.
        print(
            " " * (3 - len(str(id_reserva))) + "%d" % id_reserva + "  " +
            mes_reserva + " " * (12 - len(mes_reserva)) +
            " " * (5 - len(str(dia_reserva))) + "%d" % dia_reserva +
            "  " + "%d" % anio_reserva, usuario
        )

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

# Función para crear un usuario.
def creacionUsuario():
    user_name = input("Ingrese el nombre y apellido del usuario que reservó la sala: ")
    while len(user_name) < 3:
        user_name = input("Error. El nombre de usuario debe ser mayor a 3 caracteres: ")
    return user_name

# Función para tomar reservas.
def tomaDeReservas(mes_de_busqueda, anio_de_reserva, user):
    meses = list(range(1, 13))

    while mes_de_busqueda not in meses:
        mes_de_busqueda = int(input("Ingrese el número del mes en el que le gustaría realizar la reserva o ingrese -1 para finalizar: "))

    dias_ocupados = []
    for reserva in reservas:
        if reserva[1] == mes_de_busqueda and reserva[3] == anio_de_reserva:
            dias_ocupados.append(reserva[2])

    mostrarDisponibilidadMensual(mes_de_busqueda, dias_ocupados, anio_de_reserva)

    dia_reservado = int(input("Ingrese el día que quiere reservar: "))

    while dia_reservado < 1 or dia_reservado > mesesMatriz(mes_de_busqueda, anio_de_reserva) or dia_reservado in dias_ocupados:
        dia_reservado = int(input("Día no disponible o inválido. Ingrese otro día: "))

    reservas.append([len(reservas) + 1, mes_de_busqueda, dia_reservado, anio_de_reserva, user])
    mostrarReservas()

# Función principal.
def main():
    print("Bienvenido al sistema de reserva de salas de reuniones.")
    continuar = True
    while continuar:
        user = creacionUsuario()
        anio_de_reserva = int(input("Ingrese el año de la reserva: "))
        mes_de_busqueda = int(input("Ingrese el número del mes en el que le gustaría realizar la reserva o ingrese -1 para finalizar: "))

        if mes_de_busqueda == -1:
            break

        tomaDeReservas(mes_de_busqueda, anio_de_reserva, user)

        respuesta = int(input("¿Le gustaría hacer otra reserva? 1. Sí  2. No: "))

        if respuesta != 1:
            continuar = False

    print("Gracias por usar el sistema de reservas. Fin.")


main()
