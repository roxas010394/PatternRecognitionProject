#!/usr/bin/env python
# -*- coding: cp1252 -*-
from math import pow, cos, sin, pi
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
class ImagenFacial:
    def __init__(self, nombreArchivo, K, nombreIndividuo):
    #Donde self es una referencia a el mismo objeto
    #nombreArchivo es el nombre de la imagen
    #K son las regiones en las que se va a dividir la imagen
        try:
	    print "Caras/"+nombreArchivo
            self.__ImagenCara = Image.open("Caras/"+nombreArchivo)
            self.__ImagenCara = ImageOps.grayscale(self.__ImagenCara)
	#self.mostrarImagen()
        except IOError:
            print "El archivo \" "+nombreArchivo+ "\" que usted intenta abrir no existe."
            exit()
        self.__Regiones = K
        self.__nombreIndividuo = nombreIndividuo

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


    def crearHistograma(self, P, R):
        listaHistograma = []
        listaHistogramaNoUniforme = []
        regiones = self.crearRegiones()
        DiccionarioBin = {}
        
        cont = 1
        for x in range(0, 2**P):
		    if self.calcularTransicionesBitABit(x):
				DiccionarioBin[x] = []
				print str(cont)+".- "+str(bin(x))
				cont = cont + 1
        DiccionarioBin[int("0b"+"1"*(P))]
        print DiccionarioBin
        print len(DiccionarioBin)
			
        for i in regiones:
            for j in i:
                listaHistograma.append(self.LocalBinaryPattern(P, R, j)[0])
                listaHistogramaNoUniforme.append(self.LocalBinaryPattern(P, R, j)[1])
	  
        return  listaHistograma, listaHistogramaNoUniforme


    def LocalBinaryPattern(self, P, R, region):
        imagenLBP = region.load()
        tamX, tamY = region.size
        xc = R
        yc = R
	xcLimite = tamX - xc
	ycLimite = tamY - yc
	listaLBPU = []
	listaLBPNU = []
	
	for y in range(yc, ycLimite):
		for x in range(xc, xcLimite):
			#print str(x)+", "+str(y)
			xp = []
			yp = []

			aux = []

			for i in range(0, P):
				xp.append(int(round(x + R*cos((2*pi*i)/P))))
				yp.append(int(round(y + R*sin((2*pi*i)/P))))

			grises = []
			pixCentro = imagenLBP[x, y]
			#grises.append(pixCentro)

			for i in range(0, P):
				grises.append(self.funcionS(imagenLBP[xp[i], yp[i]] - pixCentro))
			decimal = int(self.convDecimal(P, grises))
			if self.calcularTransicionesBitABit(decimal):
				listaLBPU.append(decimal)
			else:
				listaLBPNU.append(decimal)

	return listaLBPU, listaLBPNU

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

        if nTransiciones == 2:
            return True

    def guardarVector(self):
		archivo = open("caracteristicas.dat", "a")
		histogramas = self.crearHistograma(8, 1)
		archivo.write(str(self.crearVectorDePropiedades(histogramas[0], histogramas[1]))+", "+self.__nombreIndividuo+"\n")
		archivo.close()
		
    def crearVectorDePropiedades(self, Lnumeros, LNumerosNU):
				      #[Spot, Spot/Flat, LineEnd, Edge, Corner, otherTextures, Non-Uniform]
		listaHist = []
		for region in Lnumeros:
		  listaVectores = [0, 0, 0, 0, 0, 0, 0]
		  for num in region:
		      if num == 0:
			listaVectores[0] = listaVectores[0] + 1
		      elif num == 255:
			listaVectores[1] = listaVectores[1] + 1
		      elif num ==249:
			listaVectores[2] = listaVectores[2] + 1
		      elif num == 60:
			listaVectores[3] = listaVectores[3] + 1
		      elif num == 248:
			listaVectores[4] = listaVectores[4] + 1
		      else:
			listaVectores[5] = listaVectores[5] + 1
		  listaVectores[6] = listaVectores[6] + len(LNumerosNU)
		  listaHist.append( listaVectores)
		return listaHist
    def muestraHistograma(self, datos):
	      plt.bar(datos)
	      plt.show()


"""hola = ImagenFacial("rikura.jpg", 8)
hola.guardarVector()"""
def sacarVectores(archivo):
  archivo = open(archivo, "r")
  Diccionario = {}
  listaHistogramas = []
  for linea in archivo:
    aux = []
    linea = linea.replace(",", "")
    linea = linea.replace("[[", "")
    linea = linea.replace("]]", "")
    linea = linea.replace("\n", "")
    linea = linea.split("] [")
    for histograma in linea:
      aux.append(histograma.split(" "))
    nombre = aux[len(aux) - 1].pop()
    aux.append(nombre)
    listaHistogramas.append(aux)
    Diccionario[nombre] = []
  
  for elemento in listaHistogramas:
	Diccionario[elemento.pop()].append(elemento)

  return Diccionario

def chiSquareStatistic(sample, model):
	acum2 = 0

	for i in range(0, len(sample)):
		acum1 = 0
		for j in range(0, len(sample[i])):
			acum1 = acum1 + ((float(sample[i][j]) - float(model[i][j]))**2)/(float(sample[i][j]) + float(model[i][j]))
		acum2 = acum2 + acum1
	print acum2

def clasificar(Diccionario, vectorMuestra):
	DiccionarioValores = {}
	llaves = Diccionario.keys()
	acumaux = 0
	for i in llaves:
		DiccionarioValores[i]=[]
	for i in llaves:
		for j in Diccionario[i]:
			DiccionarioValores[i].append(chiSquareStatistic(j, vectorMuestra))
  #print listaHistogramas[0]
  #print Diccionario
    
def __init__():
	while 1:
	  
	  print "Elige una opción"
	  print "1.- Entrenar"
	  print "2.- Probar"
	  print "3.-Salir"
	  print "Elige una opción"
	  opcion = input()
	  if opcion == 1:
		  print "Escribe el nombre de la foto [nombre.extensión] a entrenar"
		  imagen = raw_input()
		  print "Escribe el nombre del individuo"
		  nombre = raw_input()
		  img = ImagenFacial(imagen, 8, nombre)
		  img.guardarVector()
		  sacarVectores("caracteristicas.dat")
	  elif opcion == 2:
		  print "Escribe el nombre de la foto [nombre.extensión] a probar" 
		  clasificar(sacarVectores("caracteristicas.dat"))
	  elif opcion == 3:
	    exit()

__init__()
#spot 	11111111
#spot/flat 00000000
#LineEnd 11111001
#edge 	00111100
#corner 	11111000
