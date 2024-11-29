from datetime import datetime
import random

usuarios = []
reservas = []


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
        if(reserva["fecha"]["mes"] == mes and reserva["fecha"]["dia"] == dia and reserva["fecha"]["año"] == anio):
            esta_disponible = False
            break
    return esta_disponible

def obtenerFechaActual():
    ahora = datetime.now()
    return {
        "mes": ahora.month,
        "dia": ahora.day,
        "anio": ahora.year
    }


def generarReservasRandom(cantidad, reservas, anio):
    fecha_actual = obtenerFechaActual()
    personas = ["Torrez","Alvarez","Ramon","Gallego","Corral","Merlo","Von Reth","Rossi","Guerrero","Morales"]

    for i in range(cantidad):
        anio = random.randint(2024,2025)
        mes = random.randint(1, 12)
        dia = random.randint(1, mesesMatriz(mes, anio))            
        if (anio == fecha_actual["anio"] 
            and mes > fecha_actual["mes"] 
            and dia > fecha_actual["dia"]) or (anio > fecha_actual["anio"] 
            and mes < fecha_actual["mes"] and dia < fecha_actual["dia"]):
            # Verificar disponibilidad
            esta_disponible = chequearDisponibilad(mes, dia, anio)
            if esta_disponible:
                persona = random.choice(personas)
                nueva_reserva = {
                    "fecha": {
                        "dia": dia,
                        "mes": mes,
                        "año": anio
                    },
                    "apellido": persona,
                    "id": len(reservas)
                }
                reservas.append(nueva_reserva)

generarReservasRandom(10, reservas, 2024)

def mostrarReservas(reservas):
    print("-"*50)
    print(f"{'ID':<3} {'MES':<10} {'DIA':<5} {'AÑO':<7}{'USUARIO':<10}")
    for reserva in reservas:
        id_reserva = reserva["id"]
        mes_reserva = obtenerNombreMes(reserva["fecha"]["mes"])
        dia_reserva = reserva["fecha"]["dia"]
        anio_reserva = reserva["fecha"]["año"]
        nom_reserva = reserva["apellido"]

        print(f'{id_reserva:<3} {mes_reserva:<10} {dia_reserva:<5} {anio_reserva:<7}{nom_reserva:<10}')

mostrarReservas(reservas)

def obtenerDiasOcupadosPorMes(mes, anio):
    dias_ocupados = []
    for reserva in reservas:
        if(reserva["fecha"]["mes"] == mes and reserva["fecha"]["año"] == anio):
            dias_ocupados.append(reserva["fecha"]["dia"])
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

    print("-"*50)
    print("Los días no disponibles se marcarán con una 'X'")
    print(obtenerNombreMes(mes),":")

    for fila in filas:
        fila_formateada = ""
        for dia in fila:
            fila_formateada += " " * (3 - len(dia)) + dia
        print(fila_formateada)


def filtrarReservas(reservas, busqueda, clave_filtro):
    reservas_filtro = []
    for reserva in reservas:
        if(clave_filtro == "mes" or clave_filtro == "año"):
            if reserva["fecha"][clave_filtro] == busqueda:
                reservas_filtro.append(reserva)
        else:
            if reserva[clave_filtro] == busqueda:
                reservas_filtro.append(reserva)

    print(f"{'ID':<3} {'MES':<10} {'DIA':<5} {'AÑO':<7}{'USUARIO':<10}")
    for reserva in reservas_filtro:
        id_reserva = reserva["id"]
        mes_reserva = obtenerNombreMes(reserva["fecha"]["mes"])
        dia_reserva = reserva["fecha"]["dia"]
        anio_reserva = reserva["fecha"]["año"]
        nom_reserva = reserva["apellido"]

        print(f'{id_reserva:<3} {mes_reserva:<10} {dia_reserva:<5} {anio_reserva:<7}{nom_reserva:<10}')
    

def eliminarReserva(reservas, id):
    id_existe = any(reserva["id"] == id for reserva in reservas)

    if id_existe:
        # Filtramos las reservas que no tienen el ID que queremos eliminar.
        reservas = list(filter(lambda reserva: reserva["id"] != id, reservas))
        print("Reserva eliminada exitosamente")
    else:
        print(f"No se encontró una reserva con el ID {id}")
    mostrarReservas(reservas)
    

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


def tomaDeReservas(reservas):
    fecha_actual = obtenerFechaActual()
    print("Solamente Puede elegir la fecha dentro de un Año!")
    anio_de_reserva = inputEnteroConSalida(-1, fecha_actual["anio"], fecha_actual["anio"]+1,"**Ingrese el año de la reserva: ")
    if anio_de_reserva == -1:
        return

    if anio_de_reserva == fecha_actual["anio"]:
        mes_de_busqueda = inputEnteroConSalida(-1, fecha_actual["mes"], 12,"***Ingrese el número del mes de la reserva: ")
    else:
        mes_de_busqueda = inputEnteroConSalida(-1, 1, fecha_actual["mes"],"***Ingrese el número del mes de la reserva: ")
    
    if mes_de_busqueda == -1:
        return

    dias_ocupados = obtenerDiasOcupadosPorMes(mes_de_busqueda, anio_de_reserva) 

    mostrarDisponibilidadMensual(mes_de_busqueda, dias_ocupados, anio_de_reserva)

    dia_reservado = int(input("****Ingrese el día que quiere reservar: "))

    while (anio_de_reserva == fecha_actual["anio"] and mes_de_busqueda <= fecha_actual["mes"] and dia_reservado <= fecha_actual["dia"]) or (anio_de_reserva > fecha_actual["anio"] and mes_de_busqueda >= fecha_actual["mes"] and dia_reservado > fecha_actual["dia"]) or dia_reservado not in range(1, mesesMatriz(mes_de_busqueda, anio_de_reserva)+1) or dia_reservado in dias_ocupados:
        print("Solamente Puede elegir la fecha dentro de un Año!")
        dia_reservado = int(input("****Día no disponible o inválido. Ingrese otro día: "))
    
    nombre = input("*****Ingrese apellido de la reserva: ")
    apellido_reserva = nombre.title()

    nuevaReserva = {
        "fecha": {
            "mes": mes_de_busqueda,
            "dia": dia_reservado,
            "año": anio_de_reserva,
        },
        "apellido": apellido_reserva,
        "id": len(reservas) + 1
    }

    reservas.append(nuevaReserva)
    mostrarReservas(reservas)


def main():
    print("-"*50)
    print("Bienvenido al sistema de reserva de salas de reuniones.")
    continuar = True
    
    
    while continuar:
        opcion = inputEnteroConSalida(-1, 1, 4, "*Ingrese 1 para reservar, 2 para ver todas las reservas, 3 para eliminar, 4 para filtrar, o -1 para salir: ")
        
        if(opcion == 1):
            tomaDeReservas(reservas)

        elif(opcion == 2):
            mostrarReservas(mostrarReservas)
        
        elif(opcion == 3):
            id = inputEnteroConSalida(-1, 0, 1000, "**Ingrese el numero de id de la reserva a eliminar: ")
            eliminarReserva(reservas, id)
            
        elif(opcion == 4):
            filtro=inputEnteroConSalida(-1, 1, 4, "1 para filtrar por ID, 2 para filtrar por Mes, 3 para filtrar por Año, 4 para filtrar por Usuario: ")
            if (filtro == 1):
                busqueda = inputEnteroConSalida(-1, 1,len(reservas)+1, "**Ingrese el numero del ID que quiere buscar: ")
                if busqueda == -1:
                    break
                filtrarReservas(reservas, busqueda, "id")
            elif (filtro == 2):
                busqueda = inputEnteroConSalida(-1, 1,12, "**Ingrese el numero del mes que quiere buscar: ")
                if busqueda == -1:
                    break
                filtrarReservas(reservas, busqueda, "mes")
            elif (filtro == 3):
                busqueda = inputEnteroConSalida(-1, 2024,2026, "**Ingrese el numero del año que quiere buscar: ")
                if busqueda == -1:
                    break
                filtrarReservas(reservas, busqueda, "año")
            elif (filtro == 4):
                titulo = str(input("**Ingrese el usuario que quiere buscar: "))
                busqueda = titulo.title()
                if busqueda == -1:
                    break
                filtrarReservas(reservas, busqueda, "apellido")

            
        print("-"*50)
        respuesta = inputEnteroConSalida(-1, 1, 2, "**¿Desea continuar? Ingrese 1 para continuar o -1 para salir: ")

        if respuesta != 1:
            continuar = False

    print("Gracias por usar el sistema de reservas. Fin.\n")


main()