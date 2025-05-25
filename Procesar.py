import json
import numpy as np

def infoGet(id: str):
    with open("Data/datos_oscilacion.json", "r") as f:
        data = json.load(f)
    return data.get(id)

def GetFrecuencia(Datos: dict):
    """
    Calcula la frecuencia del péndulo a partir de los datos de 'theta' y 'T'.
    Utiliza los cruces por -90 grados para estimar el período y la frecuencia.
    """

    theta = np.array(Datos["theta"])
    T = np.array(Datos["T"])

    # Buscar los índices donde theta cruza por -90 (cambio de signo respecto a -90)
    cruces = np.where(np.diff(np.sign(theta + 90)))[0]

    # Necesitamos al menos dos cruces para calcular un período
    if len(cruces) < 2:
        print("No se detectaron suficientes cruces por -90 para calcular la frecuencia.")
        return None

    # Calcular los tiempos de cruce por -90
    tiempos_cruce = T[cruces]

    # Calcular los períodos entre cruces alternos (un ciclo completo)
    periodos = np.diff(tiempos_cruce[::2])

    if len(periodos) == 0:
        print("No se detectaron períodos completos.")
        return None

    periodo_medio = np.mean(periodos)
    frecuencia = 1 / periodo_medio

    return frecuencia

def process(id: str):
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
            Datos["theta"].append(float(curr[3].replace(',', '.')))

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

