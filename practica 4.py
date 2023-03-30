# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 18:56:53 2023

@author: luis mercado
"""

# Abrimos el archivo y leemos los datos

def leer_archivo(archivo):
    datos = {}
    with open(archivo, 'r') as f:
        for line in f:
            nombre, entrada, prioridad = line.strip().split(',')
            datos[nombre] = (int(entrada), int(prioridad))
    return datos 
# sobreescribimos el archivo mediante la consola
def escribir_datos(archivo, datos):
    with open(archivo, 'w') as f:
        for nombre, valores in datos.items():
            f.write(f"{nombre},{valores[0]},{valores[1]}\n")
            
def agregar_datos(archivo):
    nombre = input("escribe el nombre del proceso: ")
    entrada = int(input("Escribe el lugar de entrada: "))
    prioridad = int(input("Escribe la prioridad (1 la mayor): "))
    datos = leer_archivo(archivo)
    datos[nombre] = (entrada, prioridad)
    escribir_datos(archivo, datos)

#algoritmo de round robin funciona con un quantum de 3
def round_robin(datos):
    quantum = 3
    
    tiempo_espera = 0
    tiempo_respuesta = 0
    total_espera = 0
    total_respuesta = 0
    proceso = len(datos)
    
    tiempo_ejecucion = {nombre: valores[1] for nombre, valores in datos.items()}
    tiempo_llegada = {nombre: valores[0] for nombre, valores in datos.items()}
    tiempo_completado = {nombre: None for nombre in datos.keys()}
    tiempo_actual = 0
    while True:
        hecho = True
        for nombre, ejecucion in tiempo_ejecucion.items():
            if ejecucion > 0:
                hecho = False
                if ejecucion > quantum:
                    tiempo_actual += quantum
                    tiempo_ejecucion[nombre] -= quantum
                else:
                    tiempo_actual += ejecucion
                    tiempo_espera = tiempo_actual - tiempo_llegada[nombre] - datos[nombre][1]
                    tiempo_respuesta = tiempo_actual - tiempo_llegada[nombre]
                    total_espera += tiempo_espera
                    total_respuesta += tiempo_respuesta
                    tiempo_ejecucion[nombre] = 0
                    tiempo_completado[nombre] = tiempo_actual
        if hecho:
            break
    
    print("\nResultados del algoritmo round robin:")
    print("proceso\t tiempo espera\t tiempo respuesta\t completado en:")
    for nombre in datos.keys():
        print(f"{nombre}\t\\\t{total_espera/proceso:.2f}\t\\\t{total_respuesta/proceso:.2f}\t\\\t{tiempo_completado[nombre]}")

    pass

# algoritmo por prioridad eñ cual terminara antes si tiene una prioridad mas alta sindo 1 y la mas baja 10
def prioridad(datos):
    espera = 0
    respuesta = 0
    total_espera = 0
    total_respuesta = 0
    proceso = len(datos)
    
    sorted_data = dict(sorted(datos.items(), key=lambda x: x[1][1]))
    
    
    completado = {}
    for nombre, valores in sorted_data.items():
        if not completado:
            espera = 0
        else:
            espera = completado[list(completado.keys())[-1]] - valores[0]
            if espera < 0:
                espera = 0
        total_espera += espera
        respuesta = espera + valores[1]
        total_respuesta += respuesta
        completado[nombre] = espera + valores[1]
    
    print("\nResultados prioridad:")
    print("proceso\t tiempo espera\t tiempo respuesta\t completado en:")
    for nombre in datos.keys():
        print(f"{nombre}\t\\\t{total_espera/proceso:.2f}\t\\\t{total_respuesta/proceso:.2f}\t\\\t{completado[nombre]}")

    pass

#agoritmo de pila el primer proceso en entrar sera el primero en terminar 
def fifo(datos):
    espera = 0
    respuesta = 0
    total_espera = 0
    total_respuesta = 0
    proceso = len(datos)
    
    completado = {}
    for nombre, valores in datos.items():
        if not completado:
            espera = 0
        else:
            espera = completado[list(completado.keys())[-1]] - valores[0]
            if espera < 0:
                espera = 0
        total_espera += espera
        respuesta = espera + valores[1]
        total_respuesta += respuesta
        completado[nombre] = espera + valores[1]
    
    print("\nResultados del algoritmo FIFO o pila:")
    print("proceso\t tiempo espera\t tiempo respuesta\t completado en:")
    for nombre in datos.keys():
        print(f"{nombre}\t\\\t{total_espera/proceso:.2f}\t\\\t{respuesta/proceso:.2f}\t\\\t{completado[nombre]}")

    pass

def sjf(datos):
    # algoritmo por sjf 
    sorted_data = sorted(datos.items(), key=lambda x: x[1][1])
    
    espera = 0
    respuesta = 0
    total_espera = 0
    total_respuesta = 0
    proceso = len(datos)
    
    # tiempo de espera, respuesta y completado del algoritmo
    completado = {sorted_data[0][0]: sorted_data[0][1][1]}
    for i in range(1, len(sorted_data)):
        nombre = sorted_data[i][0]
        espera = completado[sorted_data[i-1][0]] - sorted_data[i][1][0]
        if espera < 0:
            espera = 0
        total_espera += espera
        respuesta = espera + sorted_data[i][1][1]
        total_respuesta += respuesta
        completado[nombre] = completado[sorted_data[i-1][0]] + sorted_data[i][1][1]
    
    print("\nResultados del algoritmo sjf:")
    print("proceso\t tiempo espera\t tiempo respuesta\t completado en:")
    for nombre in datos.keys():
        print(f"{nombre}\t\\\t{total_espera/proceso:.2f}\t\\\t{total_respuesta/proceso:.2f}\t\\\t{completado[nombre]}")

    pass



def mostrar(datos):
   archivo = open("procesos.txt") 
   print(archivo.read())

def main():
    archivo = "procesos.txt"
    while True:
        print("\n1. agregar datos\t 2. Round Robin\t 3. Shortest Job First\t 4. FIFO\t 5. prioridad\t6. mostrar datos \t7. salir \t  ")

        choice = int(input("escribe tu eleccion: "))
        if choice == 1:
            agregar_datos(archivo)
        else:
            datos = leer_archivo(archivo)
            if choice == 2:
                round_robin(datos)
            elif choice == 3:
                sjf(datos)
            elif choice == 4:
                fifo(datos)
            elif choice == 5:
                prioridad(datos)
            elif choice == 6: 
                mostrar(datos)
            elif choice == 7:
                break
            else:
                print("Invalid choice")

if __name__ == '__main__':
    main()
