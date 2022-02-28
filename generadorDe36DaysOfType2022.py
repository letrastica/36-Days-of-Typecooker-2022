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
imagenesCarpeta = os.path.join(recursos,'imagenes')
imagenes = dict([[imagen[:imagen.index('.')], os.path.join(imagenesCarpeta, imagen)] \
    for imagen in os.listdir(imagenesCarpeta) if imagen != '.DS_Store'])
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
def vaciarDirectorio(carpeta,vaciar):
    if vaciar:
        for archivo in os.listdir(carpeta):
            os.remove(os.path.join(carpeta, archivo))
    return vaciar

# ·····························

# Área de diseño
# ·····························

# Función de diseñador
def disenador(dia,info,formatos,salida):
    tituloStr = '36 Days of Typecooker'
    titulo = FormattedString('', fontSize = 1, align = 'left', fill = (1), font = fuentes['SansNomVF'])
    for i, letra in enumerate(tituloStr):
        titulo.append(letra.upper(), fontVariations = dict(wght=lerp(200,600,i/len(tituloStr))))
    for nombreFormato, formato in formatos.items():
        newDrawing()
        ancho, alto = formato.x, formato.y
        margen = max([ancho, alto])*.1
        newPage(ancho, alto)
        # Fondo definido por el valor hex del día
        diaint = sum([int(n) for n in str(int(f'0x{dia*16}',16))])
        diaColor = [int(n)/9 for n in str(diaint)]
        y, divs = 0, 50
        with savedState(): fill(*tuple(diaColor)), rect(0,0,ancho,alto)
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
        receta.append('\nCooker: ',
            fontSize = alto*.038, font = fuentes['Brujula-Regular'], lineHeight = alto*.045,
            fontVariations=dict(resetVariations=True), fill=(0)
            ), receta.append(f'{info.autor}', fill=diaColor)
        receta.append('\nCountry: ', fill=(0)), receta.append(f'{info.pais}', fill=diaColor)
        receta.append('\nSocial: ', fill=(0)), receta.append(f'{info.contacto}\n', fill=diaColor)
        receta.append('\nStyle: ', fill=(0)), receta.append(f'{info.estilo}', fill=diaColor)
        receta.append('\nWeight: ', fill=(0)), receta.append(f'{info.peso}', fill=diaColor)
        receta.append('\nContrast: ', fill=(0)), receta.append(f'{info.contraste}', fill=diaColor)
        receta.append('\nWidth: ', fill=(0)), receta.append(f'{info.ancho}', fill=diaColor)
        receta.append('\nSerif: ', fill=(0)), receta.append(f'{info.terminacion}', fill=diaColor)
        receta.append('\nOptional: ', fill=(0)), receta.append(f'{info.opcional}', fill=diaColor)
        receta.append('\nEffects: ', fill=(0)), receta.append(f'{info.efectos}', fill=diaColor)
        anchoCaja, altoCaja = ancho*.7, alto*.83
        caja, desfase = (0,-margen,anchoCaja,altoCaja), 50
        anchoLogo, altoLogo = imageSize(imagenes['logo'])
        escalaLogo = (alto*.2)/anchoLogo
        with savedState():
            translate(ancho-anchoCaja, alto-altoCaja)
            fill(1,1,1,.25)
            with savedState():
                translate(-margen*.5, margen*.25)
                blendMode('overlay')
                rect(*caja)
                for i in range(8):
                    inc = desfase*i
                    translate(randint(-inc,inc),randint(-inc,inc))
                    rect(*caja)
            textBox(receta, caja)
        with savedState(): fill(0), rect(0,0,margen*1.4,alto)
        with savedState():
            translate(margen,margen)
            rotate(90)
            scale(escalaTitulo*.7)
            text(titulo,(0,0))
        with savedState():
            rotate(90,(anchoLogo*.5*escalaLogo,altoLogo*.5*escalaLogo))
            scale(escalaLogo)
            translate((alto*.95-margen-anchoLogo)/escalaLogo,(margen*.25)/escalaLogo)
            image(imagenes['logo'],(0,0))
        # Exportación
        carpetaDia = f'D{dia}'
        carpetaDiaPath = os.path.join(salida,carpetaDia)
        diaPNG = f'D{dia}-{ancho}X{alto}PX-{nombreFormato.upper()}.png'
        if carpetaDia not in os.listdir(salida):
            os.mkdir(carpetaDiaPath)
        '''En caso de cambiar estructura del nombre,
        vaciar directorios antes de exportar cambiando vaciar a True'''
        vaciar = vaciarDirectorio(carpetaDiaPath, vaciar=False)
        if not vaciar:
            saveImage(os.path.join(carpetaDiaPath,diaPNG))
            
# Bucle diseñador
for dia, info in dias.items():
    disenador(dia,info,formatosDeSalida,salida)
    
# ·····························
