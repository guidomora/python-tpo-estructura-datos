import math

# define la can de dias de cada mes
def mesesMatriz(mes):
    dias = 31
    match mes:
        case 1 | 3 | 5 | 7 | 8| 10 | 12 :
            dias
        case 4 | 6 | 9 | 11:
            dias = 30
        case 2:
            dias = 28
    return dias
reservas = [] ## matriz de reservas

# crea la matriz del año
def creacionMatrizFechas():
    filas = 12
    matriz = []
    for i in range(1, filas + 1):
        fila = []
        dias = mesesMatriz(i)
        for c in range(dias):
            fila.append(c + 1)
        matriz.append(fila)
    print(matriz)

## muestra calendario mensual con una X en los dias no disponibles
def mostrarDisponibilidadMensual(mes, dias_ocupados):
    # dias_ocupados = [1, 10, 9, 10]
    dias = mesesMatriz(mes)
    filas = []

    for dia in range(1, dias + 1, 7):
        nueva_fila = []

        for d in range(dia, dia + 7):
            if d <= dias:
                nueva_fila.append(d if d not in dias_ocupados else 'X')

        filas.append(nueva_fila)
    
    print("Los dias no disponibles se marcaran con una X", "\n")
    
    print("Lun Mar Mie Jue Vie Sab Dom")
    
    for fila in filas:
        print(' '.join(f"{str(dia):>3}" for dia in fila))

def creacionUsuario():
    user_name = input("Bienvenido al siestema de reserva de salas de reuniones. Para empezar con el registro, escriba su nombre y apellido: ")
    while len(user_name) < 3:
        user_name = input("Error. El nombre de usuario debe ser mayor a 3 caracteres :")
    return user_name

## función para iniciar con una reserva
def tomaDeReservas(mes_de_busqueda, user):
    dias_ocupados = [1, 10, 9, 10]
    meses = [1,2,3,4,5,6,7,8,9,10,11,12]
    
    while mes_de_busqueda not in meses:
        mes_de_busqueda = int(input("Ingrese el numero del mes en el que le gustaria realizar la reserva o ingrese -1 para finalizar: "))
    
    mostrarDisponibilidadMensual(mes_de_busqueda, dias_ocupados)
    
    diaReservado = int(input("Ingrese el dia que quiere reservar: "))
    
    while diaReservado < 1 or diaReservado > mesesMatriz(mes_de_busqueda):
        diaReservado = int(input("Dia inexistente. Ingrese el dia que quiere reservar: "))
    
    # chequea si el dia esta reservado
    while diaReservado in dias_ocupados:
        diaReservado = int(input("El dia ingresado no se encuentra disponible, ingrese otro dia: "))
    dias_ocupados.append(diaReservado)
    reservas.append([len(reservas), mes_de_busqueda, diaReservado, user])
    
    print(reservas)
    
    

def main():
    user = creacionUsuario()
    continuar = True  # Variable para controlar si continúa reservando
    while continuar:
        mes_de_busqueda = int(input("A continuación ingrese el numero del mes en el que le gustaria realizar la reserva, ingrese -1 para finalizar: "))
        
        if mes_de_busqueda == -1:
            break
        
        tomaDeReservas(mes_de_busqueda, user)
        
        # Pregunta si desea hacer otra reserva
        respuesta = int(input("Le gustaria hacer otra reserva? 1 Si, 2 No: "))
        
        if respuesta != 1:  # Si no responde "s", termina el ciclo
            continuar = False

    print("Gracias por usar el sistema de reservas. Fin.")    

main()