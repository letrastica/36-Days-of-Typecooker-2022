'''
Este documento genera las imágenes de promoción de las recetas diarias para el 36 Days of Typecooker 2022
'''

# Módulos requeridos para este script
import os
import csv
from collections import namedtuple

# Variables para funcionamiento
# ·····························

# Rutas relevantes
datosCarpeta = os.path.join( os.path.split(__file__)[0], 'datos' )
datos = os.path.join(datosCarpeta, 'datos36DaysOfType2022.csv')
repo = os.path.split(datosCarpeta)[0]
salida = os.path.join(repo, 'salida')
# Named tuple para generar la estructura de cada archivo de salida
FormatoDeSalida = namedtuple('FormatoDeSalida',['x','y'])
# Diccionario con los archivos de salida
formatosDeSalida = {
    'instaFeed': FormatoDeSalida(x=1080, y=1080),
    'instaStory': FormatoDeSalida(x=1080, y=1920),
}

# ·····························

# Área de diseño
# ·····························

for formato in formatosDeSalida.values():
    ancho, alto = formato.x, formato.y
    newPage(ancho, alto)
