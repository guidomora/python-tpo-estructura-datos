from datetime import datetime
import random
import json

usuarios = []
PRIMER_HORARIO = 9
ULTIMO_HORARIO = 18

def cargarReservasDesdeArchivo():
    try:
        archivo = open('./reservas_db.json', 'r')  
        reservas = json.load(archivo)  
        archivo.close()  
        return reservas
    except FileNotFoundError:
        return []  
    except json.JSONDecodeError:
        print("Error al leer el archivo JSON.")
        return []
    except Exception as e:  
        print(f"Ocurrió un error inesperado: {e}")
        return []




reservas = cargarReservasDesdeArchivo()


def guardarReservasEnArchivo(reservas):
    try:
        archivo = open('./reservas_db.json', 'w') 
        json.dump(reservas, archivo, indent=4)  
    except IOError as e:
        print(f"Error al guardar en el archivo JSON: {e}")
    finally:
        if archivo:
            archivo.close()  


def esBisiesto(anio):
    return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)

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

def fechaValida(dia, mes, anio):
    try:
        datetime(anio, mes, dia)
        return True
    except ValueError:
        return False

def obtenerNombreMes(mes):
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", 
             "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    return meses[mes - 1] if 1 <= mes <= 12 else "Mes inválido"


def chequearDisponibilad(mes, dia, anio, hora):
    for reserva in reservas:
        if (reserva["fecha"]["mes"] == mes and
            reserva["fecha"]["dia"] == dia and
            reserva["fecha"]["año"] == anio and
            reserva["hora"] == hora):  
            return False
    return True



def obtenerFechaActual():
    ahora = datetime.now()
    return {"mes": ahora.month, "dia": ahora.day, "anio": ahora.year}

def generarReservasRandom(cantidad, reservas):
    fecha_actual = obtenerFechaActual()
    personas = ["Torrez", "Alvarez", "Ramon", "Gallego", "Corral", "Merlo", "Von Reth", "Rossi", "Guerrero", "Morales"]
    
    for i in range(cantidad):
        while True:
            anio = random.randint(fecha_actual["anio"], 2025)
            mes = random.randint(
                fecha_actual["mes"] if anio == fecha_actual["anio"] else 1, 
                12
            )
            dia = random.randint(
                fecha_actual["dia"] if anio == fecha_actual["anio"] and mes == fecha_actual["mes"] else 1, 
                mesesMatriz(mes, anio)
            )
            
            hora = random.randint(PRIMER_HORARIO, ULTIMO_HORARIO)  
            
            if fechaValida(dia, mes, anio) and chequearDisponibilad(mes, dia, anio, hora):
                persona = random.choice(personas)
                nueva_reserva = {
                    "fecha": {"dia": dia, "mes": mes, "año": anio},
                    "hora": hora,  
                    "apellido": persona,
                    "id": max([r["id"] for r in reservas], default=0) + 1
                }
                reservas.append(nueva_reserva)
                guardarReservasEnArchivo(reservas)
                break  


def mostrarReservas():
    reservas = cargarReservasDesdeArchivo()
    print("-" * 60)
    print(f"{'ID':<3} {'MES':<10} {'DIA':<5} {'AÑO':<7} {'HORA':<5} {'USUARIO':<10}")
    for reserva in reservas:
        id_reserva = reserva["id"]
        mes_reserva = obtenerNombreMes(reserva["fecha"]["mes"])
        dia_reserva = reserva["fecha"]["dia"]
        anio_reserva = reserva["fecha"]["año"]
        hora_reserva = reserva["hora"]
        nom_reserva = reserva["apellido"]
        print(f'{id_reserva:<3} {mes_reserva:<10} {dia_reserva:<5} {anio_reserva:<7} {hora_reserva:<5} {nom_reserva:<10}')


def eliminarReserva(reservas, id, archivo):
    for i, reserva in enumerate(reservas):
        if reserva["id"] == id:
            del reservas[i]  
            print("Reserva eliminada exitosamente")
            
            f = open(archivo, "w")  
            try:
                json.dump(reservas, f, indent=4)
            except IOError as e:
                print(f"Error al guardar en el archivo JSON: {e}")
            finally:
                f.close() 
            
            return
    
    print(f"No se encontró una reserva con el ID {id}")


def obtenerDiasOcupadosPorMes(mes, anio):
    cantidad_de_horarios = ULTIMO_HORARIO - PRIMER_HORARIO 
    dias = dict.fromkeys(range(mesesMatriz(mes, anio), 1), 0)

    for reserva in reservas:
        if reserva["fecha"]["mes"] == mes and reserva["fecha"]["año"] == anio:
            dia = reserva["fecha"]["dia"]
            if dia in dias:  
                dias[dia] += 1

    print(dias)
    return [dia for dia, ocupados in dias.items() if ocupados >= cantidad_de_horarios]


def mostrarDisponibildidadHoraria(reservas, mes, anio, dia):
    horarios_usados = [hora for hora in range(PRIMER_HORARIO, ULTIMO_HORARIO + 1)]
    for reserva in reservas:
        if reserva["fecha"]["mes"] == mes and reserva["fecha"]["año"] == anio and dia == reserva["fecha"]["dia"]:
            horarios_usados.remove(reserva["hora"])
    print('horarios disponibles')
    horarios_disponibles = '-'.join(str(hora) for hora in horarios_usados)
    print(horarios_disponibles)

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

def tomaDeReservas(reservas):
    fecha_actual = datetime.now()
    print("¡Puede elegir una fecha y hora dentro de un año desde la fecha actual!")

    anio_de_reserva = inputEnteroConSalida(-1, fecha_actual.year, fecha_actual.year + 1, 
                                           "**Ingrese el año de la reserva (o -1 para volver): ")
    if anio_de_reserva == -1:
        return

    if anio_de_reserva == fecha_actual.year:
        mes_de_busqueda = inputEnteroConSalida(-1, fecha_actual.month, 12, 
                                               "***Ingrese el número del mes de la reserva: (o -1 para volver) ")
    else:
        mes_de_busqueda = inputEnteroConSalida(-1, 1, 12, 
                                               "***Ingrese el número del mes de la reserva (o -1 para volver): ")

    if mes_de_busqueda == -1:
        return 

    dias_ocupados = obtenerDiasOcupadosPorMes(mes_de_busqueda, anio_de_reserva)
    mostrarDisponibilidadMensual(mes_de_busqueda, dias_ocupados, anio_de_reserva)

    dia_reservado = inputEnteroConSalida(-1, 1, mesesMatriz(mes_de_busqueda, anio_de_reserva),
                                         "****Ingrese el día que quiere reservar (o -1 para volver): ")
    if dia_reservado == -1:
        return
    
    mostrarDisponibildidadHoraria(reservas, mes_de_busqueda, anio_de_reserva, dia_reservado)

    hora_reservada = inputEnteroConSalida(-1, PRIMER_HORARIO, ULTIMO_HORARIO, 
                                          "*****Ingrese la hora (9 a 18) que desea reservar: (o -1 para volver) ")
    if hora_reservada == -1:
        return

    if not chequearDisponibilad(mes_de_busqueda, dia_reservado, anio_de_reserva, hora_reservada):
        print("Fecha y hora no disponibles.")
        return

    apellido_reserva = input("*****Ingrese apellido de la reserva: ").title()

    nueva_reserva = {
        "fecha": {
            "mes": mes_de_busqueda,
            "dia": dia_reservado,
            "año": anio_de_reserva,
        },
        "hora": hora_reservada,  
        "apellido": apellido_reserva,
        "id": len(reservas) + 1
    }

    reservas.append(nueva_reserva)
    guardarReservasEnArchivo(reservas)
    print("Reserva realizada exitosamente:")
    mostrarReservas()

def obtenerMesConMasReservas(reservas):
    if not reservas:
        print("No hay reservas registradas.")
        return

    conteo_mensual = {}
    for reserva in reservas:
        mes = reserva["fecha"]["mes"]
        if mes not in conteo_mensual:
            conteo_mensual[mes] = 0
        conteo_mensual[mes] += 1

    mes_mas_reservas = max(conteo_mensual, key=conteo_mensual.get)
    cantidad_reservas = conteo_mensual[mes_mas_reservas]

    nombre_mes = obtenerNombreMes(mes_mas_reservas)
    print("-" * 50)
    print(f"El mes con más reservas es {nombre_mes} con {cantidad_reservas} reservas.")
    print("-" * 50)
    return nombre_mes, cantidad_reservas


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

def filtrarReservasRecursivoGeneral(reservas, busqueda, clave_filtro, indice=0, reservas_filtro=None):
    if reservas_filtro is None:
        reservas_filtro = []
    
    if indice >= len(reservas):
        return reservas_filtro

    if clave_filtro in ["mes", "dia", "año"]:
        if reservas[indice]["fecha"][clave_filtro] == busqueda:
            reservas_filtro.append(reservas[indice])
    else:
        if reservas[indice][clave_filtro] == busqueda:
            reservas_filtro.append(reservas[indice])

    return filtrarReservasRecursivoGeneral(reservas, busqueda, clave_filtro, indice + 1, reservas_filtro)

def filtrarReservas(reservas, busqueda, clave_filtro):
    reservas_filtro = filtrarReservasRecursivoGeneral(reservas, busqueda, clave_filtro)
    
    if reservas_filtro:
        print("-" * 50)
        print(f"{'ID':<3} {'MES':<10} {'DIA':<5}{'HORA':<5}{'AÑO':<7}{'USUARIO':<10}")
        for reserva in reservas_filtro:
            id_reserva = reserva["id"]
            mes_reserva = obtenerNombreMes(reserva["fecha"]["mes"])
            dia_reserva = reserva["fecha"]["dia"]
            anio_reserva = reserva["fecha"]["año"]
            nom_reserva = reserva["apellido"]
            hora = reserva["hora"]
            print(f'{id_reserva:<3} {mes_reserva:<10} {dia_reserva:<5}{hora:<5}{anio_reserva:<7}{nom_reserva:<10}')
    else:
        print(f"No se encontraron reservas que coincidan con el {clave_filtro} dado.")


def eliminarTodasLasReservas(reservas, archivo):
    if not reservas:
        print("No hay reservas para eliminar.")
        return
    
    confirmar = input("¿Estás seguro de que deseas eliminar todas las reservas? (S/N): ").strip().lower()
    if confirmar == 's':
        reservas.clear()  

        f = open(archivo, "w")
        json.dump(reservas, f, indent=4)
        f.close()  

        print("Todas las reservas han sido eliminadas.")
    else:
        print("Operación cancelada.")


def filtradoOpciones():
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
            
def cambiarReserva():
    mostrarReservas()
    id_reserva = inputEnteroConSalida(-1, 1, len(reservas), "**Ingrese el ID de la reserva que desea cambiar (o -1 para volver): ")
    if id_reserva == -1:
        return

    for reserva in reservas:
        if reserva["id"] == id_reserva:
            print(f"Reserva actual: ID={reserva['id']}, Mes={obtenerNombreMes(reserva['fecha']['mes'])}, Día={reserva['fecha']['dia']}, Año={reserva['fecha']['año']}, Hora={reserva['hora']}, Usuario={reserva['apellido']}")

            nuevo_anio = inputEnteroConSalida(-1, obtenerFechaActual()["anio"], obtenerFechaActual()["anio"] + 1, "Ingrese el nuevo año de la reserva (o -1 para volver): ")
            if nuevo_anio == -1:
                return

            while True:
                nuevo_mes = inputEnteroConSalida(-1, 1, 12, "Ingrese el nuevo mes de la reserva (o -1 para volver): ")
                if nuevo_mes == -1:
                    return
                if nuevo_anio == obtenerFechaActual()["anio"] and nuevo_mes < obtenerFechaActual()["mes"]:
                    print("No puede seleccionar un mes anterior al mes actual. Por favor, elija otro mes.")
                else:
                    break

            dias_ocupados = obtenerDiasOcupadosPorMes(nuevo_mes, nuevo_anio)
            mostrarDisponibilidadMensual(nuevo_mes, dias_ocupados, nuevo_anio)

            while True:
                nuevo_dia = inputEnteroConSalida(-1, 1, mesesMatriz(nuevo_mes, nuevo_anio), "**Ingrese el día que quiere reservar (o -1 para volver): ")
                if nuevo_dia == -1:
                    return
                if (nuevo_dia in dias_ocupados) or \
                   (nuevo_anio == obtenerFechaActual()["anio"] and nuevo_mes == obtenerFechaActual()["mes"] and nuevo_dia <= obtenerFechaActual()["dia"]) or \
                   (nuevo_anio == obtenerFechaActual()["anio"] and nuevo_mes < obtenerFechaActual()["mes"]) or \
                   (nuevo_anio > obtenerFechaActual()["anio"] and nuevo_mes > obtenerFechaActual()["mes"] and nuevo_dia < obtenerFechaActual()["dia"]):
                    print("El día seleccionado no está disponible. Por favor, elija otro día.")
                else:
                    break

            while True:
                nueva_hora = inputEnteroConSalida(-1, 9, 18, "Ingrese la nueva hora de la reserva (9 a 18) (o -1 para volver): ")
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

            guardarReservasEnArchivo(reservas)
            print("Reserva cambiada exitosamente.")
            break
    else:
        print(f"No se encontró una reserva con el ID {id_reserva}")

    mostrarReservas()
    
        
# Programa principal
def main():
    print("Sistema de reservas de salas")
    generarReservasRandom(10, reservas)
    while True:
        opcion = inputEnteroConSalida(-1, 1, 7, 
            "1: Reservar sala, 2: Mostrar reservas, 3: Eliminar reserva, 4: Filtrar reservas, 5: Borrar todas las reservas, 6: Mes con mas reservas, 7: Modificar reserva -1: Salir: ")
        if opcion == -1:
            print("Gracias por usar el sistema de reservas.")
            break
        elif opcion == 1:
            tomaDeReservas(reservas)
        elif opcion == 2:
            mostrarReservas()
        elif opcion == 3:
            id_reserva = inputEnteroConSalida(-1, 1, 1000, "ID de la reserva a eliminar: ")
            if id_reserva != -1:
                eliminarReserva(reservas, id_reserva, './reservas_db.json')
        elif opcion == 4:
            filtradoOpciones()
        elif opcion == 5:
            eliminarTodasLasReservas(reservas, './reservas_db.json')
        elif opcion == 6:
            obtenerMesConMasReservas(reservas)
        elif opcion == 7:
            cambiarReserva()
    


main()

