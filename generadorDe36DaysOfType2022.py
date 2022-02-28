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
repo = os.path.split(os.path.abspath(__file__))[0]
recursos = os.path.join(repo, 'recursos')
fuentesCarpeta = os.path.join(recursos, 'fuentes')
fuentes = dict([[fuente[:fuente.index('.')], os.path.join(fuentesCarpeta, fuente)] \
    for fuente in os.listdir(fuentesCarpeta) if fuente != '.DS_Store'])
datosCarpeta = os.path.join(recursos, 'datos')
datos = os.path.join(datosCarpeta, 'datos36DaysOfType2022.csv')
salida = os.path.join(repo, 'salida')
# Named tuple para generar la estructura de cada archivo de salida
FormatoDeSalida = namedtuple('FormatoDeSalida',['x','y'])
# Diccionario con los archivos de salida
formatosDeSalida = {
    'instaFeed': FormatoDeSalida(x=1080, y=1080),
    'instaStory': FormatoDeSalida(x=1080, y=1920),
}
# Datos de CSV a un namedtuple
dias = dict()
with open(datos, 'r', encoding='utf-8') as datosCSV:
    datosCSVreader = csv.reader(datosCSV)
    for i, linea in enumerate(datosCSVreader):
        if i == 0:
            RecetaDiaria = namedtuple('RecetaDiaria',linea)
        else:
            dias[f'{i:0>2d}'] = RecetaDiaria(*linea)

# ·····························

# Utilidades
# ·····························

def lerp(v1,v2,f): return v1 + (v2 - v1) * f

# ·····························

# Área de diseño
# ·····························

# Función de diseñador
def disenador(dia,info,formatos):
    tituloStr = '36 Days of Typecooker'
    titulo = FormattedString('', fontSize = 1, align = 'left', fill = (1), font = fuentes['SansNomVF'])
    for i, letra in enumerate(tituloStr):
        titulo.append(letra.upper(), fontVariations = dict(wght=lerp(200,600,i/len(tituloStr))))
    for nombre, formato in formatos.items():
        ancho, alto = formato.x, formato.y
        margen = max([ancho, alto])*.1
        newPage(ancho, alto)
        # Fondo definido por el valor hex del día
        diaint = sum([int(n) for n in str(int(f'0x{dia*16}',16))])
        diaColor = [int(n)/9 for n in str(diaint)]
        y, divs = 0, 50
        while y <= alto:
            grad = [lerp(c,1-c,y/alto) for c in diaColor]
            with savedState():
                fill(*tuple(grad))
                stroke(*tuple(grad)),strokeWidth(0.1)
                rect(0,y,ancho,alto/divs)
            y += alto/divs
        escalaTitulo = (alto-margen*2)/titulo.size()[0]
        # Receta
        receta = FormattedString('D', fontSize = alto*.15, align = 'left', fill = (0),
            font = fuentes['SansNomVF'], fontVariations = dict(wght=600)
            )
        receta.append(dia, fill=diaColor)
        receta.append('\nCooker:',
            fontSize = alto*.038, font = fuentes['Brujula-Regular'], lineHeight = alto*.045,
            fontVariations=dict(resetVariations=True), fill=(0)
            ), receta.append(f'{info.autor}', fill=diaColor)
        receta.append('\nCountry: ', fill=(0)), receta.append(f'{info.pais}', fill=diaColor)
        receta.append('\nSocial: ', fill=(0)), receta.append(f'{info.contacto}\n', fill=diaColor)
        receta.append('\nStyle: ', fill=(0)), receta.append(f'{info.estilo}', fill=diaColor)
        receta.append('\nWeight: ', fill=(0)), receta.append(f'{info.peso}', fill=diaColor)
        receta.append('\nContrast: ', fill=(0)), receta.append(f'{info.contraste}', fill=diaColor)
        receta.append('\nWidth: ', fill=(0)), receta.append(f'{info.ancho}', fill=diaColor)
        receta.append('\nEndings: ', fill=(0)), receta.append(f'{info.terminacion}', fill=diaColor)
        receta.append('\nOptional: ', fill=(0)), receta.append(f'{info.opcional}', fill=diaColor)
        receta.append('\nEffects: ', fill=(0)), receta.append(f'{info.efectos}', fill=diaColor)
        anchoCaja, altoCaja = ancho*.7, alto*.83
        caja = (0,-margen,anchoCaja,altoCaja)
        with savedState():
            translate(ancho-anchoCaja, alto-altoCaja)
            fill(1)
            with savedState():
                translate(-margen*.5, margen*.25)
                blendMode('overlayq')
                rect(*caja)
            textBox(receta, caja)
        # Legales
        with savedState(): fill(0), rect(0,0,margen*1.4,alto)
        with savedState():
            translate(margen,margen)
            rotate(90)
            scale(escalaTitulo)
            text(titulo,(0,0))

# Bucle diseñador
for dia, info in dias.items():
    disenador(dia,info,formatosDeSalida)
    
# ·····························
