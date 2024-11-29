from datetime import datetime
import random

usuarios = []
reservas = []

# Función para determinar si un año es bisiesto o no.
def esBisiesto(anio):
    return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)

# Determina la asignación de días según el mes.
def mesesMatriz(mes, anio):
    dias = 31
    match mes:
        case 1 | 3 | 5 | 7 | 8 | 10 | 12:
            dias = 31
        case 4 | 6 | 9 | 11:
            dias = 30
        case 2:
            dias = 28 if not esBisiesto(anio) else 29
    return dias

# Valida si una fecha es válida utilizando "datetime".
def fechaValida(dia, mes, anio):
    try:
        datetime(anio, mes, dia)
        return True
    except ValueError:
        return False

# Devuelve el nombre de un mes dependiendo de su número.
def obtenerNombreMes(mes):
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", 
             "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    return meses[mes - 1] if 1 <= mes <= 12 else "Mes inválido"

# Verifica si una fecha está disponible o no.
def chequearDisponibilad(mes, dia, anio):
    for reserva in reservas:
        if reserva["fecha"]["mes"] == mes and reserva["fecha"]["dia"] == dia and reserva["fecha"]["año"] == anio:
            return False
    return True

#   Función para obtener la fecha actual.
def obtenerFechaActual():
    ahora = datetime.now()
    return {"mes": ahora.month, "dia": ahora.day, "anio": ahora.year}

# Genera reservas aleatorias, respetando la disponibilidad.
def generarReservasRandom(cantidad, reservas, anio):
    fecha_actual = obtenerFechaActual()
    personas = ["Torrez", "Alvarez", "Ramon", "Gallego", "Corral", "Merlo", "Von Reth", "Rossi", "Guerrero", "Morales"]
    for _ in range(cantidad):
        anio = random.randint(2024, 2025)
        mes = random.randint(1, 12)
        dia = random.randint(1, mesesMatriz(mes, anio))
        if fechaValida(dia, mes, anio) and chequearDisponibilad(mes, dia, anio):
            persona = random.choice(personas)
            nueva_reserva = {
                "fecha": {"dia": dia, "mes": mes, "año": anio},
                "apellido": persona,
                "id": max([r["id"] for r in reservas], default=0) + 1
            }
            reservas.append(nueva_reserva)

# Muestra todas las reservas en formato tabla
def mostrarReservas(reservas):
    print("-" * 50)
    print(f"{'ID':<3} {'MES':<10} {'DIA':<5} {'AÑO':<7} {'USUARIO':<10}")
    for reserva in reservas:
        id_reserva = reserva["id"]
        mes_reserva = obtenerNombreMes(reserva["fecha"]["mes"])
        dia_reserva = reserva["fecha"]["dia"]
        anio_reserva = reserva["fecha"]["año"]
        nom_reserva = reserva["apellido"]
        print(f'{id_reserva:<3} {mes_reserva:<10} {dia_reserva:<5} {anio_reserva:<7} {nom_reserva:<10}')

# Elimina una reserva según su ID.
def eliminarReserva(reservas, id):
    for i, reserva in enumerate(reservas):
        if reserva["id"] == id:
            del reservas[i]
            print("Reserva eliminada exitosamente")
            return
    print(f"No se encontró una reserva con el ID {id}")

# Obtiene los días ocupados para un mes específico.
def obtenerDiasOcupadosPorMes(mes, anio):
    return [reserva["fecha"]["dia"] for reserva in reservas if reserva["fecha"]["mes"] == mes and reserva["fecha"]["año"] == anio]

# Muestra un calendario mensual con días ocupados marcados como 'X'.
def mostrarDisponibilidadMensual(mes, dias_ocupados, anio):
    dias = mesesMatriz(mes, anio)
    print("-" * 50)
    print("Los días no disponibles se marcarán con una 'X'")
    print(obtenerNombreMes(mes), ":")
    for dia in range(1, dias + 1, 7):
        fila = ""
        for d in range(dia, dia + 7):
            if d > dias:
                break
            fila += f"{'X' if d in dias_ocupados else d:>3}"
        print(fila)

# Filtra reservas según un criterio dado.
def filtrarReservas(reservas, busqueda, clave_filtro):
    reservas_filtro = [reserva for reserva in reservas if reserva["fecha"].get(clave_filtro, reserva.get(clave_filtro)) == busqueda]
    mostrarReservas(reservas_filtro)

# Función para tomar una reserva del usuario.
def tomaDeReservas(reservas):
    fecha_actual = datetime.now()
    print("¡Puede elegir una fecha dentro de un año desde la fecha actual!")
    
    anio_de_reserva = inputEnteroConSalida(-1, fecha_actual.year, fecha_actual.year + 1, 
                                           "**Ingrese el año de la reserva: ")
    if anio_de_reserva == -1:
        return

    if anio_de_reserva == fecha_actual.year:
        mes_de_busqueda = inputEnteroConSalida(-1, fecha_actual.month, 12, 
                                               "***Ingrese el número del mes de la reserva: ")
    else:
        mes_de_busqueda = inputEnteroConSalida(-1, 1, 12, 
                                               "***Ingrese el número del mes de la reserva: ")

    if mes_de_busqueda == -1:
        return

    dias_ocupados = obtenerDiasOcupadosPorMes(mes_de_busqueda, anio_de_reserva)
    mostrarDisponibilidadMensual(mes_de_busqueda, dias_ocupados, anio_de_reserva)

    dia_reservado = inputEnteroConSalida(-1, 1, mesesMatriz(mes_de_busqueda, anio_de_reserva),
                                         "****Ingrese el día que quiere reservar: ")
    if dia_reservado == -1:
        return

    # Crear objeto datetime para la fecha de reserva y la actual.
    fecha_reserva = datetime(anio_de_reserva, mes_de_busqueda, dia_reservado)

    # Validar si la fecha está expirada o reservada.
    while fecha_reserva <= fecha_actual or dia_reservado in dias_ocupados:
        print("Fecha no disponible o inválida.")
        dia_reservado = inputEnteroConSalida(-1, 1, mesesMatriz(mes_de_busqueda, anio_de_reserva),
                                             "****Ingrese otra fecha válida: ")
        if dia_reservado == -1:
            return
        fecha_reserva = datetime(anio_de_reserva, mes_de_busqueda, dia_reservado)

    apellido_reserva = input("*****Ingrese apellido de la reserva: ").title()

    nueva_reserva = {
        "fecha": {
            "mes": mes_de_busqueda,
            "dia": dia_reservado,
            "año": anio_de_reserva,
        },
        "apellido": apellido_reserva,
        "id": len(reservas) + 1
    }

    reservas.append(nueva_reserva)
    print("Reserva realizada exitosamente:")
    mostrarReservas(reservas)


# Entrada de un entero con validación
def inputEnteroConSalida(numero_salida, valor_minimo, valor_maximo, texto):
    while True:
        try:
            value = int(input(texto))
            if valor_minimo <= value <= valor_maximo or value == numero_salida:
                return value
            else:
                print("Número fuera de rango.")
        except ValueError:
            print("Entrada no válida.")

# Función para tomar una reserva del usuario.
def filtrarReservas(reservas, busqueda, clave_filtro):
    if clave_filtro in ["mes", "dia", "año"]:
        reservas_filtro = [reserva for reserva in reservas if reserva["fecha"][clave_filtro] == busqueda]
    else:
        reservas_filtro = [reserva for reserva in reservas if reserva[clave_filtro] == busqueda]

    # Mostrar las reservas filtradas.
    if reservas_filtro:
        print("-" * 50)
        print(f"{'ID':<3} {'MES':<10} {'DIA':<5} {'AÑO':<7}{'USUARIO':<10}")
        for reserva in reservas_filtro:
            id_reserva = reserva["id"]
            mes_reserva = obtenerNombreMes(reserva["fecha"]["mes"])
            dia_reserva = reserva["fecha"]["dia"]
            anio_reserva = reserva["fecha"]["año"]
            nom_reserva = reserva["apellido"]
            print(f'{id_reserva:<3} {mes_reserva:<10} {dia_reserva:<5} {anio_reserva:<7}{nom_reserva:<10}')
    else:
        print("No se encontraron reservas que coincidan con el filtro.")

# Función para eliminar todas las reservas.
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


# Programa principal
def main():
    print("Sistema de reservas de salas")
    generarReservasRandom(10, reservas, 2024)
    while True:
        opcion = inputEnteroConSalida(-1, 1, 5, 
            "1: Reservar, 2: Mostrar, 3: Eliminar, 4: Filtrar, 5: Borrar todas las reservas, -1: Salir: ")
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
            eliminarTodasLasReservas(reservas)



main()

