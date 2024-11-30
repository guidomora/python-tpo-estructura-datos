from datetime import datetime
import random

usuarios = []
reservas = []
apellido_index = 4
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
        while True:
            anio = random.randint(2024,2025)
            mes = random.randint(1, 12)
            dia = random.randint(1, mesesMatriz(mes, anio))
            
            if (anio == fecha_actual["anio"] and mes > fecha_actual["mes"] and dia > fecha_actual["dia"]) or (anio > fecha_actual["anio"] and mes < fecha_actual["mes"] and dia < fecha_actual["dia"]):
                # Verificar disponibilidad
                esta_disponible = chequearDisponibilad(mes, dia, anio)
                if esta_disponible:
                    persona = random.choice(personas)
                    reservas.append([len(reservas)+1, mes, dia, anio,persona])
                    break  # Salir del ciclo while

generarReservasRandom(10, reservas, 2024)

def mostrarReservas():
    print("-"*50)
    print(f"{'ID':<3} {'MES':<10} {'DIA':<5} {'AÑO':<7}{'USUARIO':<10}")
    for reserva in reservas:
        id_reserva = reserva[id_index]
        mes_reserva = obtenerNombreMes(reserva[mes_index])
        dia_reserva = reserva[dia_index]
        anio_reserva = reserva[año_index]
        nom_reserva = reserva[apellido_index]

        print(f'{id_reserva:<3} {mes_reserva:<10} {dia_reserva:<5} {anio_reserva:<7}{nom_reserva:<10}')

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

    print("-"*50)
    print("Los días no disponibles se marcarán con una 'X'")
    print(obtenerNombreMes(mes),":")

    for fila in filas:
        fila_formateada = ""
        for dia in fila:
            fila_formateada += " " * (3 - len(dia)) + dia
        print(fila_formateada)

def filtrarReservasRecursivo(reservas, busqueda, limite, indice=0, reservas_filtro=None):
    if reservas_filtro is None:
        reservas_filtro = []
    if indice >= len(reservas):
        return reservas_filtro
    if reservas[indice][limite] == busqueda:
        reservas_filtro.append(reservas[indice])
    return filtrarReservasRecursivo(reservas, busqueda, limite, indice + 1, reservas_filtro)

def filtrarReservas(reservas, busqueda, limite):
    reservas_filtro = filtrarReservasRecursivo(reservas, busqueda, limite)
    print(f"{'ID':<3} {'MES':<10} {'DIA':<5} {'AÑO':<7}{'USUARIO':<10}")
    for reserva in reservas_filtro:
        id_reserva = reserva[id_index]
        mes_reserva = obtenerNombreMes(reserva[mes_index])
        dia_reserva = reserva[dia_index]
        anio_reserva = reserva[año_index]
        nom_reserva = reserva[apellido_index]

        print(f'{id_reserva:<3} {mes_reserva:<10} {dia_reserva:<5} {anio_reserva:<7}{nom_reserva:<10}')

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
    fecha_actual = obtenerFechaActual()
    print("Solamente Puede elegir la fecha dentro de un Año!")
    anio_de_reserva = inputEnteroConSalida(-1, fecha_actual["anio"], fecha_actual["anio"]+1,"**Ingrese el año de la reserva (o -1 para volver): ")
    if anio_de_reserva == -1:
        return

    if anio_de_reserva == fecha_actual["anio"]:
        mes_de_busqueda = inputEnteroConSalida(-1, fecha_actual["mes"], 12,"***Ingrese el número del mes de la reserva (o -1 para volver): ")
    else:
        mes_de_busqueda = inputEnteroConSalida(-1, 1, 12,"***Ingrese el número del mes de la reserva (o -1 para volver): ")
    
    if mes_de_busqueda == -1:
        return

    dias_ocupados = obtenerDiasOcupadosPorMes(mes_de_busqueda, anio_de_reserva) 

    mostrarDisponibilidadMensual(mes_de_busqueda, dias_ocupados, anio_de_reserva)

    while True:
        dia_reservado = inputEnteroConSalida(-1, 1, mesesMatriz(mes_de_busqueda, anio_de_reserva), "****Ingrese el día que quiere reservar (o -1 para volver): ")
        if dia_reservado == -1:
            return
        if (anio_de_reserva == fecha_actual["anio"] and mes_de_busqueda <= fecha_actual["mes"] and dia_reservado <= fecha_actual["dia"]) or \
           (anio_de_reserva > fecha_actual["anio"] and mes_de_busqueda > fecha_actual["mes"] and dia_reservado < fecha_actual["dia"]) or \
           (dia_reservado in dias_ocupados):
            print("El día seleccionado no está disponible. Por favor, elija otro día.")
        else:
            break

    nombre = input("*****Ingrese apellido de la reserva: ")
    apellido_reserva = nombre.title()
    reservas.append([len(reservas) + 1, mes_de_busqueda, dia_reservado, anio_de_reserva, apellido_reserva])
    mostrarReservas()

def cambiarReserva():
    mostrarReservas(reservas)  # Mostrar todas las reservas
    id_reserva = inputEnteroConSalida(-1, 1, len(reservas), "**Ingrese el ID de la reserva que desea cambiar (o -1 para volver): ")
    if id_reserva == -1:
        return

    for reserva in reservas:
        if reserva["id"] == id_reserva:
            print(f"Reserva actual: ID={reserva['id']}, Mes={obtenerNombreMes(reserva['fecha']['mes'])}, Día={reserva['fecha']['dia']}, Año={reserva['fecha']['año']}, Hora={reserva['hora']}, Usuario={reserva['apellido']}")
            nuevo_anio = inputEnteroConSalida(-1, obtenerFechaActual()["anio"], obtenerFechaActual()["anio"] + 1, "Ingrese el nuevo año de la reserva (o -1 para volver): ")
            if nuevo_anio == -1:
                return

            nuevo_mes = inputEnteroConSalida(-1, 1, 12, "Ingrese el nuevo mes de la reserva (o -1 para volver): ")
            if nuevo_mes == -1:
                return

            dias_ocupados = obtenerDiasOcupadosPorMes(nuevo_mes, nuevo_anio)
            mostrarDisponibilidadMensual(nuevo_mes, dias_ocupados, nuevo_anio)

            while True:
                nuevo_dia = inputEnteroConSalida(-1, 1, mesesMatriz(nuevo_mes, nuevo_anio), "****Ingrese el día que quiere reservar (o -1 para volver): ")
                if nuevo_dia == -1:
                    return
                if (nuevo_anio == obtenerFechaActual()["anio"] and nuevo_mes == obtenerFechaActual()["mes"] and nuevo_dia <= obtenerFechaActual()["dia"]) or \
                   (nuevo_anio == obtenerFechaActual()["anio"] and nuevo_mes < obtenerFechaActual()["mes"]) or \
                   (nuevo_anio > obtenerFechaActual()["anio"] and nuevo_mes > obtenerFechaActual()["mes"] and nuevo_dia < obtenerFechaActual()["dia"]):
                    print("El día seleccionado no está disponible. Por favor, elija otro día.")
                else:
                    break

            while True:
                nueva_hora = inputEnteroConSalida(-1, 0, 23, "Ingrese la nueva hora de la reserva (0 a 23) (o -1 para volver): ")
                if nueva_hora == -1:
                    return
                if not chequearDisponibilad(nuevo_mes, nuevo_dia, nuevo_anio, nueva_hora):
                    print("La hora seleccionada no está disponible. Por favor, elija otra hora.")
                else:
                    break

            cambiar_nombre = inputEnteroConSalida(-1, 1, 2, "¿Desea cambiar el nombre de la reserva? Ingrese 1 para sí, 2 para no, o -1 para volver: ")
            if cambiar_nombre == -1:
                return
            elif cambiar_nombre == 1:
                nuevo_usuario = input("Ingrese el nuevo apellido de la reserva: ").title()
            else:
                nuevo_usuario = reserva["apellido"]

            reserva["fecha"]["mes"] = nuevo_mes
            reserva["fecha"]["dia"] = nuevo_dia
            reserva["fecha"]["año"] = nuevo_anio
            reserva["apellido"] = nuevo_usuario
            reserva["hora"] = nueva_hora
            print("Reserva cambiada exitosamente.")
            break
    else:
        print(f"No se encontró una reserva con el ID {id_reserva}")
    mostrarReservas(reservas)  # Mostrar todas las reservas al final

def eliminarTodasLasReservas(reservas):
    if not reservas:
        print("No hay reservas para eliminar.")
        return
    
    confirmar = input("¿Estás seguro de que deseas eliminar todas las reservas? (S/N): ").strip().lower()
    if confirmar == 's':
        reservas.clear()
        print("Todas las reservas han sido eliminadas.")
    else:
        print("Operación cancelada.")

def main():
    print("Sistema de reservas de salas")
    generarReservasRandom(10, reservas)
    while True:
        opcion = inputEnteroConSalida(-1, 1, 6, 
            "1: Reservar sala, 2: Mostrar reservas, 3: Eliminar reserva, 4: Filtrar reservas, 5: Cambiar reserva, 6: Borrar todas las reservas, -1: Salir: ")
        if opcion == -1:
            print("Gracias por usar el sistema de reservas.")
            break
        elif opcion == 1:
            tomaDeReservas(reservas)
        elif opcion == 2:
            mostrarReservas(reservas)
        elif opcion == 3:
            id_reserva = inputEnteroConSalida(-1, 1, 1000, "ID de la reserva a eliminar: ")
            if id_reserva != -1:
                eliminarReserva(reservas, id_reserva)
        elif opcion == 4:
            print("Opciones de filtro: 1: ID, 2: Mes, 3: Año, 4: Usuario")
            filtro = inputEnteroConSalida(-1, 1, 4, "Seleccione un tipo de filtro: ")
            if filtro == 1:
                busqueda = inputEnteroConSalida(-1, 1, len(reservas) + 1, "Ingrese el ID que desea buscar: ")
                if busqueda != -1:
                    filtrarReservas(reservas, busqueda, "id")
            elif filtro == 2:
                busqueda = inputEnteroConSalida(-1, 1, 12, "Ingrese el número del mes que desea buscar: ")
                if busqueda != -1:
                    filtrarReservas(reservas, busqueda, "mes")
            elif filtro == 3:
                busqueda = inputEnteroConSalida(-1, 2024, 2026, "Ingrese el año que desea buscar: ")
                if busqueda != -1:
                    filtrarReservas(reservas, busqueda, "año")
            elif filtro == 4:
                busqueda = input("Ingrese el apellido del usuario que desea buscar: ").title()
                filtrarReservas(reservas, busqueda, "apellido")
        elif opcion == 5:
            cambiarReserva()
        elif opcion == 6:
            eliminarTodasLasReservas(reservas)

main()
