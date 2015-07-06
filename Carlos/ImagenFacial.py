#!/usr/bin/env python
# -*- coding: cp1252 -*-
from math import pow, cos, sin, pi
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import Tkinter
import tkMessageBox
class ImagenFacial:
    def __init__(self, nombreArchivo, K, nombreIndividuo):
    #Donde self es una referencia a el mismo objeto
    #nombreArchivo es el nombre de la imagen
    #K son las regiones en las que se va a dividir la imagen
        self.__histogramas = []
        try:
	    self.__rutaArchivo = "Caras/"+nombreArchivo
            self.__ImagenCara = Image.open(self.__rutaArchivo)
            self.__ImagenMostrar = Image.open(self.__rutaArchivo)
            self.__ImagenCara = ImageOps.grayscale(self.__ImagenCara)
	#self.mostrarImagen()
        except IOError:
            print "The file \" "+nombreArchivo+ "\" doesn't exist."
            exit()
        self.__Regiones = K
        self.__nombreIndividuo = nombreIndividuo.lower()

    def mostrarImagen(self):
        self.__ImagenMostrar.show()

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
        regiones = self.crearRegiones()
        for i in regiones:
            for j in i:
                listaHistograma.append(self.LocalBinaryPattern(P, R, j))
        return listaHistograma

	  
        return  listaHistograma, listaHistogramaNoUniforme
    
    def crearDiccionarios(self, P):
      DiccionarioBin = dict()
      DiccionarioBin["No-Uniformes"] = 0
      for x in range(0, 2**P):
	if self.calcularTransicionesBitABit(x) or x == int("0b"+"1"*(P), 2) or x == 0:
	  DiccionarioBin[x] = 0
	else:
	  DiccionarioBin["No-Uniformes"] = 0
      return DiccionarioBin


    def LocalBinaryPattern(self, P, R, region):
        imagenLBP = region.load()
        tamX, tamY = region.size
        xc = R
        yc = R
	xcLimite = tamX - xc
	ycLimite = tamY - yc
	listaLBPU = []
	listaLBPNU = []
	DiccionarioBin = self.crearDiccionarios(P)
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
			if self.calcularTransicionesBitABit(decimal) or decimal == int("0b"+"1"*(P), 2) or decimal == 0:
				DiccionarioBin[decimal] = DiccionarioBin[decimal] + 1
			else:
				DiccionarioBin["No-Uniformes"] = DiccionarioBin["No-Uniformes"] + 1
	return DiccionarioBin

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
		#self.__histogramas = self.crearHistograma(8, 1)
		archivo.write(self.__nombreIndividuo+"\t"+self.__rutaArchivo+"\n")
		archivo.close()
		
    def muestraHistograma(self, datos):
	      plt.bar(datos)
	      plt.show()


"""hola = ImagenFacial("rikura.jpg", 8)
hola.guardarVector()"""
def sacarVectores(nfile):
  Diccionario = crearDiccionariosIndividuos(nfile)
  archivo = open(nfile, "r")
  DicHistogramas = []
  
  for linea in archivo:
    linea = linea.replace("\n", "")
    linea = linea.replace("Caras/", "")
    linea = linea.split("\t")    
    nombre = linea[0]
    Diccionario[nombre].append(linea[1])
  archivo.close()
  DicHistogramas = calcularVectores(Diccionario, nfile)
  return DicHistogramas
    
def calcularVectores(Diccionario, archivo):
  llaves = Diccionario.keys()
  DiccionarioHistogramas = crearDiccionariosIndividuos(archivo)
  for llave in llaves:
    for listaDir in Diccionario[llave]:
      Imagenes = ImagenFacial(listaDir, 8, llave)
      DiccionarioHistogramas[llave].append(Imagenes.crearHistograma(8, 1))
  return DiccionarioHistogramas

def crearDiccionariosIndividuos(archivo):
  archivo = open(archivo, "r")
  Diccionario = {}
  for linea in archivo:
    aux = []
    linea = linea.replace("\n", "")
    linea = linea.split("\t")    
    nombre = linea[0]
    Diccionario[nombre] = []
  return Diccionario

def chiSquareStatistic(sample, model):
  if len(sample) != len(model):
    print "Error: the number of region does not have coincidence"
    exit()
  tamRegiones = len(model)
  acum = 0
  for x in range(0, tamRegiones):
    llaves = sample[x].keys()
    acum2 = 0
    for y in llaves:
      if sample[x][y] == 0 and model[x][y] == 0:
	continue
      acum2 = acum2 + ((sample[x][y] - model[x][y])**2)/float(sample[x][y] + model[x][y])
    acum = acum + acum2
  return acum

def clasificar(DiccionarioModelos, DiccionarioMuestra):
  personas = DiccionarioModelos.keys()
  DicResultados = {}
  for nombres in personas:
    DicResultados[nombres] = []
    for imagen in DiccionarioModelos[nombres]:
      DicResultados[nombres].append(chiSquareStatistic(DiccionarioMuestra, imagen))
  tkMessageBox.showinfo("Results", "This photo belongs to: "+obtenerClaseperteneciante(DicResultados))
  print DicResultados
  #print "This photo belongs to : "+ obtenerClaseperteneciante(DicResultados)
  #print DiccionarioModelos["aaron"][0][0]#[71]
  #print listaHistogramas[0]
  #print Diccionario
def obtenerClaseperteneciante(DicResultados):
  menor = DicResultados[DicResultados.keys()[0]]
  auxPersona = ""
  for persona in DicResultados:
    for resultado in DicResultados[persona]:
      if resultado < menor:
	menor = resultado
	auxPersona = persona
  return auxPersona
def __init__():
	while 1:
	  
	  print "Choose an option"
	  print "1.- Train"
	  print "2.- Test a photo"
	  print "3.-Exit"
	  opcion = input()
	  if opcion == 1:
		  print "Write the name of the file [name.ext] which the program is going to train."
		  imagen = raw_input()
		  print "Write the name of the person"
		  nombre = raw_input()
		  img = ImagenFacial(imagen, 8, nombre)
		  img.guardarVector()
	  elif opcion == 2:
		  print "Write the name of the file [name.ext] which the program is going to testr" 
		  imagenEntrada = raw_input()
		  img = ImagenFacial(imagenEntrada, 8, "")
		  DatosPrueba = img.crearHistograma(8, 1)
		  img.mostrarImagen()
		  DatosModelos = sacarVectores("caracteristicas.dat")
		  clasificar(DatosModelos, DatosPrueba)
	  elif opcion == 3:
	    exit()

__init__()
#spot 	11111111
#spot/flat 00000000
#LineEnd 11111001
#edge 	00111100
#corner 	11111000
