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

    

def tomaDeReservas():
    meses = [1,2,3,4,5,6,7,8,9,10,11,12]
    mesDeBusqueda = int(input("Bienvenido! a continuación ingrese el numero del mes en el que le gustaria realizar la reserva :"))
    while mesDeBusqueda not in meses:
        mesDeBusqueda = int(input("Bienvenido! a continuación ingrese el numero del mes en el que le gustaria realizar la reserva :"))
    print("Mes elegido : ", mesDeBusqueda)
    
