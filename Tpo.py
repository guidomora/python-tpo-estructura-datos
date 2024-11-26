
 
from datetime import datetime
import random

usuarios = []
reservas = []
año_index = 3
dia_index = 2
mes_index = 1
id_index = 0

def esBisiesto(anio):
    if anio % 4 == 0:
        if anio % 100 != 0 or anio % 400 == 0:
            return True
    return False

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

# def obtenerFechaActual():
#     """Devuelve la fecha actual como un diccionario con día, mes y año."""
#     ahora = datetime.now()  # Obtiene la fecha y hora actual
#     return {
#         "mes": obtenerNombreMes(ahora.month),
#         "dia": ahora.day,
#         "anio": ahora.year
#     }

# # Ejemplo de uso:
# fecha_actual = obtenerFechaActual()
# print(f"Hoy es {fecha_actual['dia']}/{fecha_actual['mes']}/{fecha_actual['anio']}")



# def generarReservasRandom(cantidad, reservas, anio):
#     for i in range(cantidad):
#         reserva = []
#         mes = random.randint(1,12)
#         reserva.append(mes)
#         dia = random.randint(1, mesesMatriz(mes, anio))
#         esta_disponible = chequearDisponibilad(mes, dia, anio)
#         if(esta_disponible):
#             reservas.append([len(reservas), mes, dia, anio])

# generarReservasRandom(10, reservas, 2024)

def obtenerFechaActual():
    ahora = datetime.now()
    return {
        "mes": ahora.month,
        "dia": ahora.day,
        "anio": ahora.year
    }

def generarReservasRandom(cantidad, reservas, anio):
    fecha_actual = obtenerFechaActual()

    for i in range(cantidad):
        while True:
            mes = random.randint(fecha_actual["mes"], 12)
            dia = random.randint(1, mesesMatriz(mes, anio))
            if mes > fecha_actual["mes"] or (mes == fecha_actual["mes"] and dia >= fecha_actual["dia"]):
                # Verificar disponibilidad
                esta_disponible = chequearDisponibilad(mes, dia, anio)
                if esta_disponible:
                    reservas.append([len(reservas), mes, dia, anio])
                    break  # Salir del ciclo while

generarReservasRandom(10, reservas, 2024)

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

# def eliminarReserva(reservas, id):
#     for reserva in reservas:
#         if reserva[0] == id:
#             reservas.remove(reserva)
#     print(reservas)
#     print("Reserva eliminada exitosamente")
#     mostrarReservas()

def eliminarReserva(reservas, id):
    id_existe = False
    for reserva in reservas:
        if reserva[0] == id:
            id_existe = True
            break
    if id_existe:
        reservas[:] = [reserva for reserva in reservas if reserva[0] != id]
        print("Reserva eliminada exitosamente")
    else:
        print(f"No se encontró una reserva con el ID {id}")
    mostrarReservas()
    

def creacionUsuario():
    user_name = input("Ingrese el nombre y apellido del usuario que reservó la sala: ")
    while len(user_name) < 3:
        user_name = input("Error. El nombre de usuario debe ser mayor a 3 caracteres: ")
    return user_name

def inputEnteroConSalida(numero_salida, valor_minimo, valor_maximo, texto):
    while True:
        try:
            value = int(input(texto))
            rangoDeValor = list(range(valor_minimo, valor_maximo + 1))
            if value in rangoDeValor or value == numero_salida:
                return value 
            else:
                print(f"Por favor, ingrese un número valido.")
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número valido.")

    

def tomaDeReservas():
    mes_de_busqueda = inputEnteroConSalida(-1, 1, 12,"Ingrese el número del mes en el que le gustaría realizar la reserva o ingrese -1 para finalizar: ")
      
    if mes_de_busqueda == -1:
        return
    
    anio_de_reserva = int(input("Ingrese el año de la reserva: "))
    
    dias_ocupados = obtenerDiasOcupadosPorMes(mes_de_busqueda, anio_de_reserva) 

    mostrarDisponibilidadMensual(mes_de_busqueda, dias_ocupados, anio_de_reserva)

    dia_reservado = int(input("Ingrese el día que quiere reservar: "))

    while dia_reservado not in range(1, mesesMatriz(mes_de_busqueda, anio_de_reserva)) or dia_reservado in dias_ocupados:
        dia_reservado = int(input("Día no disponible o inválido. Ingrese otro día: "))
    
    nombre_reserva = input("Ingrese nombre de la reserva")
    reservas.append([len(reservas) + 1, mes_de_busqueda, dia_reservado, anio_de_reserva, nombre_reserva])
    mostrarReservas()


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
            
        respuesta = inputEnteroConSalida(-1, 1, 2, "¿Desea continuar? Ingrese 1 para continuar o -1 para salir: ")

        if respuesta != 1:
            continuar = False

    print("Gracias por usar el sistema de reservas. Fin.")


main()
