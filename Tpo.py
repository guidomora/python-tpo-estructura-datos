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
def mostrarDisponibilidadMensual(mes):
    dias_ocupados = [1, 10, 9, 10]
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


## función para iniciar con una reserva
def tomaDeReservas():
    meses = [1,2,3,4,5,6,7,8,9,10,11,12]
    mesDeBusqueda = int(input("Bienvenido! a continuación ingrese el numero del mes en el que le gustaria realizar la reserva: "))
    
    while mesDeBusqueda not in meses:
        mesDeBusqueda = int(input("Bienvenido! a continuación ingrese el numero del mes en el que le gustaria realizar la reserva: "))
    
    mostrarDisponibilidadMensual(mesDeBusqueda)
    
    diaReservado = int(input("Ingrese el dia que quiere reservar"))
    
    while diaReservado < 1 or diaReservado > mesesMatriz(mesDeBusqueda):
        diaReservado = int(input("Ingrese el dia que quiere reservar"))
    ## falta agregar logica para buscar en la matriz de reservas si ya esta reservada la fecha
    ## quizá podriamos agregar nombre y apellido para que quede un poco mas llena la matriz
        
    reservas.append([len(reservas), mesDeBusqueda, diaReservado])
    
    print(reservas)
    
    
tomaDeReservas()