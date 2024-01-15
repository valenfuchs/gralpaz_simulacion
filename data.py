import csv
import matplotlib.pyplot as plt

def recopilar_data(multas, tiempos, choques, velocidades, cant_autos):  
    # Nombre del archivo CSV en el que deseas guardar el diccionario
    filename = 'simulacion10.csv'
    diccionarios = [multas, tiempos, choques, velocidades, cant_autos]

    # Abre el archivo CSV en modo escritura
    with open(filename, mode='w', newline='') as archivo_csv:
        # Define los nombres de las columnas (cabecera)
        
        campos = ['hora', 'multas', 'tiempos', 'choques', 'velocidades', 'cant_autos']
        titulos = ['multas', 'tiempos', 'choques', 'velocidades', 'cant_autos']
        # Crea un objeto DictWriter
        escritor_csv = csv.DictWriter(archivo_csv, fieldnames=campos)
        
        # Escribe la cabecera
        escritor_csv.writeheader()
        
        # Itera a través de las horas
        for hora in range(len(multas)):  # asumiendo que tienes horas de 0 a 24
            fila = {'hora': hora}
            i = 0
            for titulo in titulos:
                fila[titulo] = diccionarios[i].get(hora, '')  # Obtén el valor o un valor vacío si no existe
                i += 1
            escritor_csv.writerow(fila)

    print(f'Se han guardado los datos en "{filename}"')
