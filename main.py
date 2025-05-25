from Procesar import process,graph, GetFrecuencia, infoGet
from matplotlib.lines import Line2D

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
    



def main():
    Plot_frecuencias()

#     res = process(5939)

#     graph(res,"ALL")

#     print(GetFrecuencia(res))
main()
    

