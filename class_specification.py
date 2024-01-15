# Atributos: 
# ID: número identificador de auto (3 dígitos numéricos)
# posición p en metros
# t tiempo en segundos
# v velocidad, metros/segundo
# a aceleración 
# p_ant posicion en el tiempo anterior
# color del auto

import random 
import numpy as np


class Auto:
    def __init__(self, id:int, p:int, t:int, v:int, a:int, p_ant, color):
        self.id = id
        self.pos = p
        self.t_inicio = t # guardamos tiempo de entrada porque el de salida es el que queda guardado
        self.t = t
        self.vel = v
        self.acel = a 
        self.fin = 0 # si ya salio de la autopista
        self.pos_ant = p_ant
        self.choque = 0 # si choca es 1 
        self.multas = 0 # cantidad de multas
        self.color = color # color del auto

        #randomizamos la personalidad (proba de que acelere o se mantenga)
        rand1 = random.randint(0, 5)
        if rand1 == 1:
            self.media_acel = 0.3 #lento
        elif rand1 == 2:
            self.media_acel = 1 #rapido
        else: 
            self.media_acel = 0.5 #promedio

        # distraccion
        rand2 = random.randint(0, 5)
        if rand2 == 1 or rand2 == 2:
            self.distraido = 0.6
        else: 
            self.distraido = 0 #promedio
        

    def __repr__ (self):
        return str(self.__dict__)
    

    def final_recorrido(self):
        self.fin = 1
    

    def acelerar(self, pos_adel, vel_adel, time_scale):
        '''un auto puede acelerar entre -4 y 2'''

        distancia = pos_adel - self.pos
        val_aceleracion = 0
        
        # dif < 0 : me estoy acercando
        # dif > 0 : me estoy alejando
        if (self.vel == 0):
            if (distancia < 70):
                self.vel = 0
            else: 
                self.vel =  20/3.6*time_scale  #avanzo poco 
        
        else: 
            dif = distancia / self.vel 

            if(distancia > 300):
                # esta lejos
                if (self.vel < 80/3.6*time_scale):
                    val_aceleracion = random.normalvariate(self.media_acel+0.5, 0.5) 
                else:
                    val_aceleracion = random.normalvariate(self.media_acel-0.6, 0.4)

            elif(distancia > 200): # distancia por encima de lo recomendado
                if (self.vel < 80/3.6*time_scale):
                    val_aceleracion = random.normalvariate(self.media_acel+0.3, 0.2)
                else:
                    val_aceleracion = random.normalvariate(self.media_acel-1, 0.1)

            elif (distancia > 80):
                if (self.vel < vel_adel):
                    val_aceleracion = random.normalvariate(self.media_acel-0.55, 0.3)
                else:
                    val_aceleracion = random.normalvariate(self.media_acel-2, 0.1)
            
            elif (distancia > 40):
                if (self.vel < vel_adel):
                    val_aceleracion = random.normalvariate(self.media_acel-1.2, 0.2)
                else:
                    val_aceleracion = random.normalvariate(self.media_acel-3.9, 0.1)

                
            else: # distancia por debajo de lo recomendado                 
                # se distrajo?...
                azar = random.randint(0, 1)
                if azar <= self.distraido:
                #     #si
                    val_aceleracion = 0 
                else:
                #     #no
                    if (self.vel < vel_adel):
                        val_aceleracion = random.normalvariate(self.media_acel-3, 0.2)
                    else:
                        val_aceleracion = random.normalvariate(self.media_acel-3.7, 0.05)
                
            if(self.vel > 77/3.6*time_scale):   
                # hay camaras 
                if int(self.pos) in range(5400, 5510) or int(self.pos) in range(10400, 10510):
                    val_aceleracion = random.normalvariate(-2.7,0.3)


            self.acel = val_aceleracion * time_scale
            ruido = random.normalvariate(0,0.005)
            self.vel = self.vel + self.acel + ruido

            if self.vel < 0:
                self.vel = 0

            
            

class Carril:
    def __init__(self, autos:list[Auto]):
        self.autos = autos
        self.multas = {} # por cada hora la cantidad de multas que hubo
        self.tiempos = {} # cuanto tardaron los autos en promedio en c/ hora
        self.choques =  {} # por cada hora la cantidad de choques que hubo
        self.velocidades = {} # por cada hora la velocidad promedio
        self.vel_cam = {} # por cada hora la velocidad promedio de las camaras
        self.cant_autos = {} # cantidad de autos que ingresan por hora    
        self.updates = {} # contamos la cantidad de veces que los autos actualizaron (para dps dividir)