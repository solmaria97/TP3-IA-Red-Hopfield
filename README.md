# TP3 – Inteligencia Artificial: Red de Hopfield

**Alumna:** Sol María Rodríguez García  
**Carrera:** Licenciatura en Informática  
**Universidad:** Universidad Siglo 21  
**Año:** 2026

## Descripción

Prototipo desarrollado en Python para recuperar imágenes de 10 × 10 píxeles mediante una red de Hopfield.

Se utilizan tres patrones con un contorno cuadrado en distintas posiciones y una escuadra fija como referencia. Se comparan los entrenamientos mediante la regla de Hebb y pseudoinversa.

## Archivo principal

`TP3-IA-PUNTO3.py`: contiene la implementación y las pruebas del prototipo.

## Requisitos

Python 3.6 o posterior. No requiere instalar librerías externas.

## Ejecución en OnlineGDB

1. Ingresar a https://www.onlinegdb.com/online_python_compiler.
2. Copiar el contenido de `TP3-IA-PUNTO3.py`.
3. Pegarlo en el editor, reemplazando el código de ejemplo.
4. Presionar Run.

El programa no solicita datos por teclado.

## Ejecución local

Desde una terminal ubicada en la carpeta del archivo:

```bash
python TP3-IA-PUNTO3.py
```

En sistemas donde el intérprete se invoca como `python3`, utilizar ese comando en lugar de `python`.

## Pruebas realizadas

Se evalúan tres patrones con 0, 10, 20 y 35 píxeles alterados mediante ambos entrenamientos: 24 pruebas en total.

El programa muestra los patrones originales, la evolución de un ejemplo con ruido y una comparación final que incluye el patrón identificado, los errores, los ciclos y la estabilidad.

## Resultados y alcance

En las pruebas incluidas, pseudoinversa recuperó correctamente los patrones en 12 de 12 condiciones y Hebb en 2 de 12.

Estos resultados corresponden únicamente a las imágenes y alteraciones utilizadas. Un estado estable no garantiza una recuperación correcta.

El prototipo tiene fines educativos: no procesa fotografías del motor, no mide coordenadas físicas y no controla un robot.
