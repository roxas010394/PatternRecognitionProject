#!/usr/bin/env python
# -*- coding: cp1252 -*-
from math import pow, cos, sin, pi
from PIL import Image, ImageOps
import matplotlib.pyplot as plt

class ImagenFacial:
    def __init__(self, nombreArchivo, K):
    #Donde self es una referencia a el mismo objeto
    #nombreArchivo es el nombre de la imagen
    #K son las regiones en las que se va a dividir la imagen
        try:
	    print "Cara\\"+nombreArchivo
            self.__ImagenCara = Image.open("Caras\\"+nombreArchivo)
            self.__ImagenCara = ImageOps.grayscale(self.__ImagenCara)
	self.mostrarImagen()
        except IOError:
            print "El archivo \" "+nombreArchivo+ "\" que usted intenta abrir no existe."
            exit()
        self.__Regiones = K

    def mostrarImagen(self):
        self.__ImagenCara.show()

    def asignarImagen(self, nombreArchivo):
        self.__ImagenCara = Image.open(nombreArchivo)

    def asignarKRegiones(self, K):
        self.__Regiones = K

    def obtenerImagen(self):
        return self.__ImagenCara

    def obtenerRegiones(self):
        return self.__Regiones

    def obtenerTamImagen(self):
        return self.__ImagenCara.size

    def crearRegiones(self):
        #crop(left, upper, right, lower)
        #AnchoImagen = right - left
        #AltoImagen = lower - upper
        #crop(AnchoImagen, AltoImagen, AnchoImagen, AltoImagen)
        tamX, tamY = self.obtenerTamImagen()
        tamX = int(round(tamX/float(self.__Regiones)))
        tamY = int(round(tamY/float(self.__Regiones)))
        izq, arr, der, ab = 0, 0, 0, 0

        #i = 1
        listaImagenes = []
        for y in range(0, self.__Regiones):
            arr = y*tamY
            ab = (y + 1) * tamY
            aux = []
            for x in range(0, self.__Regiones):
                izq = x * tamX
                der = (x + 1) * tamX
                #self.__ImagenCara.crop((izq, arr, der, ab)).save("LOL"+str(x)+str(y), "JPEG")
                #imagen = self.__ImagenCara.crop((izq, arr, der, ab)).load()
                #print imagen[1, 1]
                aux.append(self.__ImagenCara.crop((izq, arr, der, ab)))
            listaImagenes.append(aux)
                #print str(i)+".- "+str((izq, arr, der, ab))
                #i = i + 1
        return listaImagenes

    def crearHistograma(self):
        listaHistograma = []
	listaRet = []
        regiones = self.crearRegiones()
        for i in regiones:
            for j in i:
                listaHistograma.append(self.LocalBinaryPattern2(8, 1, j))
		
		for i in range(0, len(listaHistograma)):
			if listaHistograma[i][1] == "No-Uniforme":
				listaHistograma.pop(i)
			else:
				listaRet.append(listaHistograma.pop(i)[0])
        return  listaRet

    def crearHistograma2(self):
        listaHistograma = []
        regiones = self.crearRegiones()
        print regiones
        for i in regiones:
            for j in i:
                listaHistograma = listaHistograma + self.LocalBinaryPattern(j)
        return  listaHistograma


    def LocalBinaryPattern2(self, P, R, region):
        imagenLBP = region.load()
        tamX, tamY = region.size
        tamX = tamX/2 #xc
        tamY = tamY/2 #yc

        xp = []
        yp = []

        aux = []

        for i in range(0, P):
            xp.append(int(round(tamX + R*cos((2*pi*i)/P))))
            yp.append(int(round(tamY + R*sin((2*pi*i)/P))))

        grises = []
        pixCentro = imagenLBP[tamX, tamY]
        #grises.append(pixCentro)

        for i in range(0, P):
            grises.append(self.funcionS(imagenLBP[xp[i], yp[i]] - pixCentro))
        decimal = int(self.convDecimal(P, grises))
        if self.calcularTransicionesBitABit(decimal):
            return decimal, "Uniforme"
        else:
            return decimal, "No-Uniforme"

    def LocalBinaryPattern(self, region):
        imagenLBP = region.load()
        posX = 1
        posY = 1
        tamX, tamY = region.size
        pixCentro = imagenLBP[posX, posY]
        grises = []
        listaT = []
        for i in range(0, tamY - 2):
            posX = 1
            for j in range(0, tamX - 2):
                grises.append(self.funcionS(imagenLBP[posX-1, posY-1] - imagenLBP[posX, posY]))
                grises.append(self.funcionS(imagenLBP[posX, posY-1] - imagenLBP[posX, posY]))
                grises.append(self.funcionS(imagenLBP[posX+1, posY-1] - imagenLBP[posX, posY]))
                grises.append(self.funcionS(imagenLBP[posX+1, posY] - imagenLBP[posX, posY]))
                grises.append(self.funcionS(imagenLBP[posX+1, posY+1] - imagenLBP[posX, posY]))
                grises.append(self.funcionS(imagenLBP[posX, posY+1] - imagenLBP[posX, posY]))
                grises.append(self.funcionS(imagenLBP[posX-1, posY+1] - imagenLBP[posX, posY]))
                grises.append(self.funcionS(imagenLBP[posX-1, posY] - imagenLBP[posX, posY]))
                decimal = int(self.convDecimal(8,grises))
                if self.calcularTransicionesBitABit(decimal):
                    listaT.append(decimal)
                else:
                    continue #print str(decimal)+", No-Uniforme"
                posX = posX + 1
            posY = posY + 1
        return listaT

    def convDecimal(self, nBIts, lista):
        acum = 0
        lista.reverse()
        for i in range(0, nBIts):
            acum = acum + pow(2, i)*lista[i]
            #print str(acum)+"+("+str(2)+"^"+str(i)+")x("+str(lista[i])+")"
        lista.reverse()
        return acum

    def funcionS(self, x):
        return 1 if x >= 0 else 0

    def calcularTransicionesBitABit(self, numero):
        aux = numero
        bitAnterior = bin(aux)[len(bin(aux)) - 1]
        nTransiciones = 0
        while aux != 0:
            aux = aux >> 1
            bitActual = bin(aux)[len(bin(aux)) - 1]
            if bin(aux) == "0b0":
                break
            if bitAnterior != bitActual:
                nTransiciones = nTransiciones + 1
                bitAnterior = bitActual
        #print bin(numero)
        #print nTransiciones

        if nTransiciones > 2:
            return False
        else:
            return True

    def guardarVector(self):
		archivo = open("caracteristicas.dat", "a")
		archivo.write(str(self.crearHistograma())+"\n")
		archivo.close()


"""hola = ImagenFacial("rikura.jpg", 8)
hola.guardarVector()"""

def __init__():
	print "Elige una opción"
	print "1.- Entrenar"
	print "2.- Probar"
	print "Elige una opción"
	opcion = input()
	if opcion == 1:
		print "Escribe el nombre de la foto [nombre.extensión] a entrenar"
		imagen = raw_input()
		img = ImagenFacial(imagen, 8)
		img.guardarVector()
	elif opcion == 2:
		print "Escribe el nombre de la foto [nombre.extensión] a probar" 

__init__()

