import json
import numpy as np

def infoGet(id: str):
    with open("Data/datos_oscilacion.json", "r") as f:
        data = json.load(f)
    return data.get(id)

from scipy.signal import find_peaks
import numpy as np
from scipy.signal import argrelextrema

def estimar_periodo(t, theta):
    # Buscar máximos locales
    peaks, _ = find_peaks(theta)
    
    # Si hay menos de 2 picos no se puede estimar
    if len(peaks) < 2:
        return None
    
    # Tiempos en los que ocurren los picos
    tiempos_picos = t[peaks]
    
    # Diferencias entre tiempos de picos consecutivos
    diferencias = np.diff(tiempos_picos)
    
    # Promedio de diferencias → período estimado
    periodo_estimado = np.mean(diferencias)
    return periodo_estimado

def GetMaxlib(lista: list):
    """
    Devuelve una lista de índices de los máximos locales usando scipy.signal.find_peaks.
    """
    arr = np.array(lista)
    peaks, _ = find_peaks(arr)
    return peaks.tolist()


def GetFrecuencia(Datos: dict):
    """
    Calcula la frecuencia del péndulo a partir de los datos de 'theta' y 'T'.
    Utiliza los máximos locales de theta para estimar el período y la frecuencia.
    """
    theta = np.array(Datos["theta"])
    T = np.array(Datos["T"])

    # Obtener los índices de los máximos locales usando GetMaxs
    #idx_maximos = GetMaxs(theta)
    idx_maximos = GetMaxlib(theta)

    # Necesitamos al menos dos máximos para calcular un período
    if len(idx_maximos) < 2:
        print("No se detectaron suficientes máximos para calcular la frecuencia.")
        return None

    # Tiempos en los que ocurren los máximos
    tiempos_maximos = T[idx_maximos]

    # Calcular los períodos entre máximos consecutivos
    periodos = np.diff(tiempos_maximos)

    if len(periodos) == 0:
        print("No se detectaron períodos completos.")
        return None

    periodo_medio = np.mean(periodos)
    frecuencia = 1 / periodo_medio

    return frecuencia

def process(id: str):
    """
    Procesa un archivo de datos experimentales y retorna un diccionario con la información extraída.
    Args:
        id (str): Identificador del archivo de datos a procesar. El archivo debe estar en la ruta "Data/Datos_<id>.txt".
    Returns:
        dict: Un diccionario con las siguientes claves:
            - "T": Lista de tiempos (float).
            - "X": Lista de posiciones X (float).
            - "Y": Lista de posiciones Y (float).
            - "theta": Lista de ángulos theta (float).
            - "Peso": Peso extraído de la función infoGet (float/int).
            - "Largo": Largo extraído de la función infoGet (float/int).
            - "Osilacion": Tipo de oscilación extraído de la función infoGet (str).
    Notas:
        - El archivo de datos debe tener al menos 3 líneas de encabezado, que serán ignoradas.
        - Los valores numéricos pueden estar separados por comas o puntos decimales.
        - La función infoGet debe estar definida y retornar un diccionario con las claves "Peso", "Largo" y "Oscilacion".
    """
    path = "Data/Datos_" + str(id) + ".txt"
    with open(path, "r") as file:
        # Saltar las primeras 3 líneas
        for _ in range(3):
            next(file)
        # Voy a usar los t como clave
        Datos = {"T": [], "X": [], "Y": [], "theta": [],"Peso":0,"Largo":0,"Osilacion":""}  # Leer línea por línea
        datos_json = infoGet(str(id))
        Datos["Peso"] = datos_json["Peso"]
        Datos["Largo"] = datos_json["Largo"]
        Datos["Osilacion"] = datos_json["Oscilacion"]
        for linea in file:
            limpio = linea.strip()
            curr = limpio.split()
            # Reemplazar comas por puntos para conversión a float
            Datos["T"].append(float(curr[0].replace(',', '.')))
            Datos["X"].append(float(curr[1].replace(',', '.')))
            Datos["Y"].append(float(curr[2].replace(',', '.')))

             #  Sumamos 90 grados a theta
            angulo_original = float(curr[3].replace(',', '.'))
            Datos["theta"].append(angulo_original + 90)

        return Datos

import matplotlib.pyplot as plt

def graph(Datos: dict, Id: str):
    """
    Le paso los Datos y le digo que grafico quiero.
    En el eje x va a poner el T y en el eje Y el id.
    Si Id es 'ALL', grafica X, Y y theta vs T.
    """
    info = f"Peso: {Datos['Peso']}, Largo: {Datos['Largo']}, Oscilacion: {Datos['Osilacion']}"
    if Id == "ALL":
        for key in ["X", "Y", "theta"]:
            plt.plot(Datos["T"], Datos[key], marker='o', label=key)
        plt.xlabel("T")
        plt.ylabel("Valor")
        plt.title(f"X, Y y theta vs T\n{info}")
        plt.legend()
        plt.grid(True)
        plt.show()
        return

    if Id not in Datos:
        print(f"'{Id}' no es una clave válida. Opciones: {list(Datos.keys())}")
        return
    plt.plot(Datos["T"], Datos[Id], marker='o')
    plt.xlabel("T")
    plt.ylabel(Id)
    plt.title(f"{Id} vs T\n{info}")
    plt.grid(True)
    plt.show()

