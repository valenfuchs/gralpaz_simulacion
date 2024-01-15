from class_specification import Carril, Auto
import random
import time
import csv
import matplotlib.pyplot as plt
import pygame
import pygame.mixer
import sys
from data import recopilar_data

 # iniciamos la simulacion ingresando de a 1 auto
 # t = 0
 # son 15 km

########################## 
# Inicializa Pygame
pygame.init()
pygame.mixer.init()

# Configuración de la ventana
window_width = 1000
window_height = 200
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("General Paz")

# Colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
verde = (0, 255, 0)
rojo = (255, 0, 0)
naranja = (255, 128, 0)
gris = (77, 77, 77)

# Autos
auto_azul = pygame.image.load("media/blue_car.png")
auto_azul = pygame.transform.scale(auto_azul, (30,20))
auto_blanco = pygame.image.load("media/white_car.png")
auto_blanco = pygame.transform.scale(auto_blanco, (30,20))
auto_rojo = pygame.image.load("media/red_car.png")
auto_rojo = pygame.transform.scale(auto_rojo, (30,20))
cam = pygame.image.load("media/cam.png")
cam = pygame.transform.scale(cam, (27,27))

# Fuente
font = pygame.font.SysFont("trebuchet ms", 24)

# Imagen de fondo
fondo = pygame.image.load('media/background.jpg')
fondo = pygame.transform.scale(fondo, (window_width, window_height))  # Ajusta la imagen al tamaño de la ventana

# Sonido
beep = pygame.mixer.Sound('media/beep.mp3')

############################# SIMULACION

# Armamos la simulación...
vel1 = random.normalvariate(80/3.6, 15/3.6)
auto1 = Auto(0, 0, 0, vel1*60, 0, 0, auto_rojo)
autos: list[Auto] = [auto1]
i: int = 0
# obs: el primer auto de la lista es el mas cercano a llegar a destino (id = 0)

escala = window_width / 2500
posicion_actual = 0

# Iniciamos la simulacion (con un auto)
carril = Carril(autos)
tiempo_total = 86400  # Tiempo total que queremos que dure la simulación (en segundos)

# Reloj para controlar la velocidad de actualización
reloj = pygame.time.Clock()

simulated_time = 0 # Tiempo "dentro" de la simulacion
real_time = pygame.time.get_ticks()  # Tiempo real en milisegundos
time_scale = 60
seg = 0

# Inicializamos variables
hora = 0
carril.tiempos[0] = 0
carril.cant_autos[0] = 1
carril.velocidades[0] = 0
carril.choques[0] = 0  
carril.multas[0] = 0
carril.updates[hora] = 0
carril.vel_cam[hora] = 0

# GRAFICO
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                posicion_actual -= 2500  # Mueve 2500 metros a la izquierda
            elif event.key == pygame.K_RIGHT:
                posicion_actual += 2500  # Mueve 2500 metros a la derecha
                
    # Actualizamos el tiempo (simulado)
    dt = (pygame.time.get_ticks() - real_time) / 1000.0  # Diferencia de tiempo en segundos
    real_time = pygame.time.get_ticks()
    simulated_time += dt * time_scale
    seg_ant = seg
    seg = int(simulated_time)
    
    if simulated_time >= tiempo_total:
        carril.tiempos[hora] /= carril.cant_autos[hora]
        carril.velocidades[hora] /= (carril.cant_autos[hora] * 3600)
        recopilar_data(carril.multas, carril.tiempos, carril.choques, carril.velocidades, carril.cant_autos)
        pygame.quit()
        sys.exit()

    # Chequea si la posicion esta dentro de los limites del tramo
    posicion_actual = max(0, min(15000 - 2500, posicion_actual)) 
    # Actualiza el ancho de la ventana segun la posición actual
    tramo_visible = (posicion_actual, posicion_actual + 2500)

    # "Limpia" la pantalla
    window.fill(blanco)
    # Fondo
    window.blit(fondo, (0,0))
    
    # Dibuja el carril
    pygame.draw.line(window, gris, (0, window_height // 2), (window_width, window_height // 2), 34)

    # Posicion de las camaras
    camara = cam.get_rect()
    camara.center = (int(5500- tramo_visible[0])*escala, window_height // 2) 
    window.blit(cam, camara.topleft)
    camara = cam.get_rect()
    camara.center = (int(10500- tramo_visible[0])*escala, window_height // 2)  
    window.blit(cam, camara.topleft)


    if seg > seg_ant:
        if (seg % 3600 == 0 and seg > 0): 
            carril.tiempos[hora] /= carril.cant_autos[hora]
            carril.velocidades[hora] /= (carril.updates[hora])
            carril.vel_cam[hora] /= (carril.multas[hora])
            hora +=1
            carril.tiempos[hora] = 0
            carril.cant_autos[hora] = 0
            carril.velocidades[hora] = 0
            carril.vel_cam[hora] = 0
            carril.choques[hora] = 0
            carril.multas[hora] = 0
            carril.updates[hora] = 0

    i = 0
    for auto in carril.autos:
            
        if (auto.fin == 0): # el auto todavia no termino
            if (i == 0): 
                # es el ultimo auto (no tiene adelante)
                auto.acelerar(20000, 100, time_scale)
                auto.pos_ant = auto.pos
                auto.pos += (auto.vel) * dt 
                # el auto salio
                if (auto.pos) >= 15000:
                    auto.fin = 1

            elif (i < len(carril.autos)):
                if carril.autos[i-1].fin == 1:
                    # el de adelante ya salio
                    # (id del de adelante es i-1)
                    pos_adel = 20000
                    vel_adel = 200 * time_scale
                else: 
                    pos_adel = carril.autos[i-1].pos 
                    vel_adel = carril.autos[i-1].vel
                auto.acelerar(pos_adel, vel_adel, time_scale)
                auto.pos_ant = auto.pos 

                #si los indices lo permiten...
                if i < len(autos)-3:
                    for i_cercano in [i+1, i+2]:
                        # si alguno adelante choco, toma precaucion!
                        cercano = carril.autos[i_cercano]
                        if cercano.choque == 1:
                            if abs(cercano.pos - auto.pos) < 70:
                                auto.vel = min(40/3.6*60, auto.vel)

                auto.pos += (auto.vel) * dt 
                
                carril.updates[hora] += 1
                carril.velocidades[hora] += auto.vel *3.6/time_scale 

                # el auto salio
                if (auto.pos) >= 15000:
                    auto.fin = 1
                    carril.tiempos[hora] += auto.t - auto.t_inicio

                if auto.pos >= pos_adel and pos_adel < 15000:
                    # Chequeamos que el de adelante todavia no haya salido de la autopista
                    beep.play()
                    auto.vel = 0
                    if auto.choque == 0:
                        auto.choque = seg
                        if (carril.autos[i-1].choque == 0):
                            # si el de adelante no choco en este mismo segundo
                            carril.choques[hora] += 1
                            print("____________________________________________")
                            print("CHOQUE en p =", auto.pos,",en t=", seg, ", auto=", auto.id)
                            print("____________________________________________")

                # CHOQUE
                if (auto.choque > 0):
                    if seg > auto.choque:
                        auto.choque = 0

                # MULTAS
                if auto.vel > 81/3.6*time_scale and ((auto.pos_ant < 5500 and auto.pos >= 5500) or (auto.pos_ant < 10500 and auto.pos >= 10500)): 
                    auto.multas +=1
                    carril.multas[hora] += 1
                    print("multa", auto.vel*3.6/time_scale)
                    carril.vel_cam[hora] += auto.vel *3.6/time_scale
                    
            auto.t = seg
                
            # Graficamos los puntos
            if tramo_visible[0] <= auto.pos <= tramo_visible[1]:
                pos_en_ventana = int(auto.pos - tramo_visible[0]) * escala
                if auto.choque > 0:
                    auto_rect = auto.color.get_rect()
                    auto_rect.center = (pos_en_ventana, window_height // 2)
                    window.blit(auto.color, auto_rect.topleft)
                    pygame.draw.circle(window, rojo, (pos_en_ventana, window_height // 2), 3)
                else:
                    auto_rect = auto.color.get_rect()
                    auto_rect.center = (pos_en_ventana, window_height // 2)
                    window.blit(auto.color, auto_rect.topleft)
        i+=1

    # Por cuestiones de implementacion de la simulacion, chequeamos que se haya cumplido un segundo entero
    if seg > seg_ant:
        # Regulamos la densidad del trafico (metemos nuevos autos)
        if (seg % 10 == 0 and carril.autos[len(carril.autos)-1].pos > 70): 
            # No hora pico
            i_nuevo = len(carril.autos)

            if carril.autos[len(carril.autos)-1].pos > 200:
                vel = random.normalvariate(80/3.6, 15/3.6)
            else:
                vel = random.normalvariate(60/3.6, 10/3.6)
            color_random = random.randint(0, 3)
            if color_random == 1:
                nuevo_color = auto_azul
            elif color_random == 2:
                nuevo_color = auto_rojo
            else: 
                nuevo_color = auto_blanco
            nuevo_auto = Auto(i_nuevo, 0, seg, vel*time_scale, 0, 0, nuevo_color)
            carril.autos.append(nuevo_auto)
            carril.cant_autos[hora] += 1
            carril.velocidades[hora] += auto.vel *3.6/time_scale
            carril.updates[hora] += 1

            auto_rect = auto.color.get_rect()
            auto_rect.center = (pos_en_ventana, window_height // 2)  # Posición del automóvil
            # Dibujar la imagen del automóvil en la ventana
            window.blit(auto.color, auto_rect.topleft)
            pygame.draw.circle(window, (255, 0, 0), (int(nuevo_auto.pos- tramo_visible[0]), window_height // 2), 3)

        elif (((seg in range(7*3600, 8*3600) or seg in range(9*3600, 11*3600) or seg in range(16*3600, 19*3600)) and seg % 1 == 0) or ((seg in range(8*3600, 9*3600) or seg in range(19*3600, 20*3600)) and seg % 1 == 0)): 
            # Hora pico
            i_nuevo = len(carril.autos)

            if carril.autos[len(carril.autos)-1].pos > 50:
                vel = random.normalvariate(50/3.6, 5/3.6)
                color_random = random.randint(0, 3)
                if color_random == 1:
                    nuevo_color = auto_azul
                elif color_random == 2:
                    nuevo_color = auto_rojo
                else: 
                    nuevo_color = auto_negro
                nuevo_auto = Auto(i_nuevo, 0, seg, vel*time_scale, 0, 0, nuevo_color)
                carril.autos.append(nuevo_auto)
                carril.cant_autos[hora] += 1
                carril.velocidades[hora] += auto.vel *3.6/time_scale
                carril.updates[hora] += 1

                auto_rect = auto.color.get_rect()
                auto_rect.center = (pos_en_ventana, window_height // 2)  
                window.blit(auto.color, auto_rect.topleft)
                pygame.draw.circle(window, (255, 0, 0), (int(nuevo_auto.pos- tramo_visible[0]), window_height // 2), 3)

            elif carril.autos[len(carril.autos)-1].pos > 20:
                vel = random.normalvariate(30/3.6, 5/3.6)
                color_random = random.randint(0, 3)
                if color_random == 1:
                    nuevo_color = auto_azul
                elif color_random == 2:
                    nuevo_color = auto_rojo
                else: 
                    nuevo_color = auto_blanco
                nuevo_auto = Auto(i_nuevo, 0, seg, vel*time_scale, 0, 0, nuevo_color)
                carril.autos.append(nuevo_auto)
                carril.cant_autos[hora] += 1
                carril.velocidades[hora] += auto.vel *3.6/time_scale
                carril.updates[hora] += 1

                auto_rect = auto.color.get_rect()
                auto_rect.center = (pos_en_ventana, window_height // 2)  # Posición del automóvil
                window.blit(auto.color, auto_rect.topleft)
                pygame.draw.circle(window, (255, 0, 0), (int(nuevo_auto.pos- tramo_visible[0]), window_height // 2), 3)


    # GRAFICAMOS
    # Dibujamos bordes
    pygame.draw.line(window, blanco, (0, window_height // 2 + 20), (window_width, window_height // 2 + 20), 3)
    pygame.draw.line(window, blanco, (0, window_height // 2 - 19), (window_width, window_height // 2 - 19), 3)

    # Textos
    metros = f"[{tramo_visible[0]}m, {tramo_visible[1]}m]"
    text = font.render(metros, True, blanco)
    size = text.get_rect()
    window.blit(text, ((window_width - size.width) // 2, 130))

    minutos = (seg // 60) % 60
    hora_formato = f"{hora:02d}:{minutos:02d}hs"    
    text2 = font.render(hora_formato, True, blanco)
    size2 = text2.get_rect()
    window.blit(text2, ((window_width - size2.width) // 2, 155)) 

    # Actualiza la pantalla
    pygame.display.update()

    # Limita la velocidad de la animación en fotogramas por segundo
    reloj.tick(0)