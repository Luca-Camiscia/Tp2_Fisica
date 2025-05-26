from Procesar import process,graph, GetFrecuencia, infoGet
from matplotlib.lines import Line2D
import numpy as np
import math
import matplotlib.pyplot as plt
def Plot_frecuencias():
    """
    Grafica las frecuencias de las 15 grabaciones como un scatter plot, coloreando según el valor de infoGet()["Oscilacion"].
    En las etiquetas del eje x muestra el ID y el largo en cm.
    """
    # IDs de los videos a procesar
    lista_videos = [5924, 5925, 5926, 5933, 5934, 5936, 5939, 5940, 5941, 5942, 5943, 5944, 5946, 5947, 5948]
    color_map = {"chica": "blue", "mediana": "orange", "grande": "green"}

    frecuencias = []
    colores = []
    etiquetas = []

    for video_id in lista_videos:
        print(video_id)
        datos = process(str(video_id))
        frecuencia = GetFrecuencia(datos)
        info = infoGet(str(video_id))
        oscilacion = info.get("Oscilacion", "chica")
        largo = info.get("Largo", "N/A")
        color = color_map.get(oscilacion, "gray")

        frecuencias.append(frecuencia)
        colores.append(color)
        etiquetas.append(f"{video_id}\n{largo}cm")

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.scatter(range(len(lista_videos)), frecuencias, color=colores, s=80)

    ax.set_xticks(range(len(lista_videos)))
    ax.set_xticklabels(etiquetas, rotation=45, ha='right')
    ax.set_ylabel("Frecuencia (Hz)")
    ax.set_xlabel("Video ID y Largo (cm)")
    ax.set_title("Frecuencias de las 15 grabaciones con masa de 6g")

    # Leyenda personalizada
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Chica'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=10, label='Mediana'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Grande')
    ]
    ax.legend(handles=legend_elements, title="Oscilación")

    plt.tight_layout()
    plt.show()

def Plot_F_vs_M():
    
    lista_videos = [5917, 5918, 5920, 5921, 5922, 5923, 5924, 5925, 5926]

import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import math

# Colores fijos por tipo de oscilación
COLOR_MAP = {"chica": "green", "mediana": "orange", "grande": "blue"}

def graficar_comparativo_ordenado(lista_ids):
    grupos = defaultdict(dict)  # (peso, largo) -> oscilacion -> Datos

    for vid in lista_ids:
        datos = process(vid)
        key = (datos["Peso"], datos["Largo"])
        oscilacion = datos["Osilacion"].lower()
        grupos[key][oscilacion] = datos

    claves = sorted(grupos.keys())
    n = len(claves)
    columnas = 3
    filas = math.ceil(n / columnas)

    fig, axs = plt.subplots(filas, columnas, figsize=(4.5 * columnas, 3 * filas), sharex=True, sharey=True)

    if filas == 1:
        axs = [axs]
    if columnas == 1:
        axs = [[ax] for ax in axs]
    axs = np.array(axs)

    for i, (key, subdatos) in enumerate(grupos.items()):
        fila = i // columnas
        col = i % columnas
        ax = axs[fila, col]

        for osc in ["chica", "mediana", "grande"]:
            if osc in subdatos:
                d = subdatos[osc]
                theta0 = round(d["theta"][0], 2)
                ax.plot(d["T"], d["theta"], label=f"θ₀ = {theta0} rad")

        peso, largo = key
        ax.set_title(f"Peso: {peso}g, Largo: {largo}cm", fontsize=10)
        ax.set_xlabel("t [s]")
        ax.set_ylabel("θ [rad]")
        ax.set_xticks(np.arange(0, 8, 1))  # eje x de 0 a 7 s
        ax.grid(True)
        ax.legend(fontsize=8)

    # Eliminar subplots vacíos
    for j in range(i + 1, filas * columnas):
        fig.delaxes(axs[j // columnas, j % columnas])

    plt.tight_layout()
    plt.suptitle("Comparación de θ(t) con distintas amplitudes iniciales", fontsize=14, y=1.02)
    plt.show()


def main():
    lista = [5917, 5918, 5920, 5921, 5922, 5923, 5924, 5925, 5926, 5927, 5928, 5929, 5930, 5931, 5932, 5933, 5934, 5936]
    graficar_comparativo_ordenado(lista)
    #Plot_frecuencias()

#     res = process(5939)

#     graph(res,"ALL")

#     print(GetFrecuencia(res))
main()
    

