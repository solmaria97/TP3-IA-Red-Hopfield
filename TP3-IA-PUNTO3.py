"""TP3 - Red de Hopfield: imagenes de 10 x 10.
"""
import random

LADO = 10
N = LADO * LADO
SEMILLA = 21
MAX_CICLOS = 50
TOL = 1e-9


def crear_patron(fila, columna):
    """Contorno cuadrado 5x5 y escuadra fija; coordenadas desde cero."""
    imagen = [-1] * N
    for f in range(fila, fila + 5):
        for c in range(columna, columna + 5):
            if f in (fila, fila + 4) or c in (columna, columna + 4):
                imagen[f * LADO + c] = 1
    for f, c in [(7, 0), (8, 0), (9, 0), (9, 1), (9, 2)]:
        imagen[f * LADO + c] = 1
    return imagen


def mostrar(imagen):
    for fila in range(LADO):
        print(' '.join('#' if x == 1 else '.'
                       for x in imagen[fila * LADO:(fila + 1) * LADO]))


def distancia(a, b):
    """Distancia de Hamming: cantidad de pixeles diferentes."""
    return sum(x != y for x, y in zip(a, b))


def agregar_ruido(patron, cantidad, semilla):
    """Invierte exactamente cantidad pixeles distintos, sin reemplazo."""
    salida = patron[:]
    indices = random.Random(semilla).sample(range(N), cantidad)
    for i in indices:
        salida[i] *= -1
    return salida


def invertir(matriz):
    """Gauss-Jordan con pivoteo parcial para la pequena matriz de Gram.
    Esta formula requiere patrones linealmente independientes.
    """
    n = len(matriz)
    a = [[float(x) for x in fila] +
         [float(i == j) for j in range(n)]
         for i, fila in enumerate(matriz)]
    for columna in range(n):
        pivote = max(range(columna, n), key=lambda i: abs(a[i][columna]))
        if abs(a[pivote][columna]) < TOL:
            raise ValueError('Patrones dependientes: no se puede invertir U^T U.')
        a[columna], a[pivote] = a[pivote], a[columna]
        divisor = a[columna][columna]
        a[columna] = [x / divisor for x in a[columna]]
        for fila in range(n):
            if fila != columna:
                factor = a[fila][columna]
                a[fila] = [a[fila][j] - factor * a[columna][j]
                           for j in range(2 * n)]
    return [fila[n:] for fila in a]


class Hopfield:
    def __init__(self, patrones, metodo):
        self.patrones = [p[:] for p in patrones]
        self.metodo = metodo
        self.pesos = [[0.0] * N for _ in range(N)]
        q = len(patrones)
        if metodo == 'Hebb':
            # W_ij = suma de productos de los pixeles / N.
            for i in range(N):
                for j in range(i + 1, N):
                    w = sum(p[i] * p[j] for p in patrones) / N
                    self.pesos[i][j] = self.pesos[j][i] = w
        elif metodo == 'Pseudoinversa':
            # U tiene los patrones como columnas.
            # W = U (U^T U)^(-1) U^T, antes de anular la diagonal.
            gram = [[sum(a * b for a, b in zip(p, r))
                     for r in patrones] for p in patrones]
            inversa = invertir(gram)
            auxiliar = [[sum(patrones[k][i] * inversa[k][b]
                            for k in range(q)) for b in range(q)]
                         for i in range(N)]
            for i in range(N):
                for j in range(i + 1, N):
                    w = sum(auxiliar[i][b] * patrones[b][j] for b in range(q))
                    self.pesos[i][j] = self.pesos[j][i] = w
        else:
            raise ValueError('Metodo desconocido')
        # En ambos casos la diagonal queda en cero: sin autoconexiones.

    def energia(self, estado):
        # E = -1/2 sum_ij W_ij s_i s_j; umbrales cero.
        return -sum(self.pesos[i][j] * estado[i] * estado[j]
                    for i in range(N) for j in range(i + 1, N))

    def recuperar(self, entrada):
        estado = entrada[:]
        historial = [estado[:]]
        energias = [self.energia(estado)]
        for _ in range(MAX_CICLOS):
            cambios = 0
            # Actualizacion asincrona: cada cambio se usa inmediatamente.
            for i in range(N):
                campo = sum(w * x for w, x in zip(self.pesos[i], estado))
                nuevo = 1 if campo > TOL else -1 if campo < -TOL else estado[i]
                if nuevo != estado[i]:
                    estado[i] = nuevo
                    cambios += 1
            historial.append(estado[:])
            energias.append(self.energia(estado))
            if cambios == 0:
                return estado, historial, energias, True
        return estado, historial, energias, False

    def identificar(self, estado):
        # No asignar un nombre solo por ser el patron mas cercano.
        for i, patron in enumerate(self.patrones):
            if estado == patron:
                return 'P' + str(i + 1)
        return 'No almacenado'


def main():
    patrones = [crear_patron(1, 2), crear_patron(1, 4), crear_patron(3, 3)]
    redes = [Hopfield(patrones, m) for m in ('Hebb', 'Pseudoinversa')]
    print('PATRONES ALMACENADOS (coordenadas desde cero)')
    for i, patron in enumerate(patrones):
        print('\nP' + str(i + 1))
        mostrar(patron)

    # Ejemplo detallado: P2 con diez pixeles invertidos.
    entrada = agregar_ruido(patrones[1], 10, SEMILLA)
    print('\nEJEMPLO: P2 CON 10 PIXELES ALTERADOS (10%)')
    for red in redes:
        salida, historial, energias, estable = red.recuperar(entrada)
        print('\nMETODO:', red.metodo)
        for ciclo, (imagen, energia) in enumerate(zip(historial, energias)):
            print('\nCiclo', ciclo, '| Energia:', round(energia, 4))
            mostrar(imagen)
        print('Estable:', estable, '| Identificacion:', red.identificar(salida))
        print('Errores iniciales:', distancia(entrada, patrones[1]))
        print('Errores finales:', distancia(salida, patrones[1]))
        print('Ciclos (incluye confirmacion sin cambios):', len(historial) - 1)
        print('Recuperacion exacta:', salida == patrones[1])

    print('\nCOMPARACION: UNA ENTRADA POR PATRON Y NIVEL DE RUIDO')
    print('Metodo        Original Ruido Final          Errores Ciclos Estable')
    for indice, patron in enumerate(patrones):
        for ruido in (0, 10, 20, 35):
            entrada = agregar_ruido(patron, ruido, SEMILLA)
            for red in redes:
                salida, hist, energias, estable = red.recuperar(entrada)
                print(f'{red.metodo:13} P{indice + 1:<7} {ruido:>3}% '
                      f'{red.identificar(salida):14} '
                      f'{distancia(salida, patron):>7} {len(hist)-1:>6} {estable}')

    print('\nNota: pocas pruebas ilustrativas; no son una tasa general de acierto.')
    print('Recuperar una plantilla no mide el desplazamiento real del block.')


if __name__ == '__main__':
    main()
