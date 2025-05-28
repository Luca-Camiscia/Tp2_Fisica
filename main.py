from Procesar import process,graph, GetFrecuencia, infoGet, estimar_periodo
from matplotlib.lines import Line2D
import numpy as np
import math
import matplotlib.pyplot as plt
def Plot_frecuencias():
    """
    Grafica las frecuencias de las 15 grabaciones como un scatter plot, usando la longitud (Largo) en el eje x.
    Colorea según el valor de infoGet()["Oscilacion"].
    Agrega barras de error en las longitudes de 0.1 cm.
    """
    # IDs de los videos a procesar
    lista_videos = [5924, 5925, 5926, 5933, 5934, 5936, 5939, 5940, 5941, 5942, 5943, 5944, 5946, 5947, 5948]
    lista_videos.reverse()
    color_map = {"chica": "#AED6F1", "mediana": "#5DADE2", "grande": "#21618C"}

    frecuencias = []
    colores = []
    longitudes = []
    etiquetas = []

    for video_id in lista_videos:
        datos = process(str(video_id))
        frecuencia = GetFrecuencia(datos)
        info = infoGet(str(video_id))
        oscilacion = info.get("Oscilacion", "chica")
        largo = info.get("Largo", "N/A")
        color = color_map.get(oscilacion, "gray")

        frecuencias.append(frecuencia)
        colores.append(color)
        longitudes.append(largo)
        etiquetas.append(f"{video_id}")

    _, ax = plt.subplots(figsize=(10, 6))
    # Agregar barras de error en x (longitud) de 0.1 cm
    ax.errorbar(longitudes, frecuencias, xerr=0.1, fmt='o', color='black', ecolor="#FF0000", elinewidth=2, capsize=5, alpha=0.8, zorder=2)
    # Dibujar los puntos encima con sus colores
    ax.scatter(longitudes, frecuencias, color=colores, s=10, zorder=3)

    ax.set_xticks(sorted(set(longitudes)))
    ax.set_xticklabels(sorted(set(longitudes)))
    ax.set_ylabel("Frecuencia (Hz)")
    ax.set_xlabel("Longitud (cm)")
    ax.set_title("Frecuencias vs Longitud de las 15 grabaciones (masa 6g)")

    # Leyenda personalizada
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map["chica"], markersize=10, label='Chica'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map["mediana"], markersize=10, label='Mediana'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map["grande"], markersize=10, label='Grande')
    ]
    ax.legend(handles=legend_elements, title="Oscilación")

    plt.tight_layout()
    plt.show()

def Plot_frecuencia_vs_M():
    """
    Grafica la frecuencia en función de la masa para L = 35 cm.
    El eje x es la masa (g), el eje y la frecuencia (Hz), y el color depende de la oscilación.
    Agrega barras de error en la masa de 0.1g.
    """
    # IDs de videos con L = 35 cm
    Masas = [5924, 5925, 5926, 5921, 5922, 5923, 5917, 5918, 5920]
    color_map = {"chica": "#AED6F1", "mediana": "#5DADE2", "grande": "#21618C"}

    masas_x = []
    frecuencias_y = []
    colores = []

    for vid in Masas:
        datos = process(str(vid))
        frecuencia = GetFrecuencia(datos)
        info = infoGet(str(vid))
        masa = info.get("Masa", info.get("Peso", None))
        oscilacion = info.get("Oscilacion", "chica")
        color = color_map.get(oscilacion, "gray")

        masas_x.append(masa)
        frecuencias_y.append(frecuencia)
        colores.append(color)

    fig, ax = plt.subplots(figsize=(8, 5))
    # Agregar barras de error en x (masa) de 0.1g
    ax.errorbar(masas_x, frecuencias_y, xerr=0.1, fmt='o', color='black', ecolor="#FF0000", elinewidth=2, capsize=5, alpha=0.8, zorder=2)
    # Dibujar los puntos encima con sus colores
    ax.scatter(masas_x, frecuencias_y, color=colores, s=10, zorder=3)

    ax.set_xlabel("Masa (g)")
    ax.set_ylabel("Frecuencia (Hz)")
    ax.set_title("Frecuencia vs Masa para L = 35 cm")

    # Leyenda personalizada
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map["chica"], markersize=10, label='Chica'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map["mediana"], markersize=10, label='Mediana'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map["grande"], markersize=10, label='Grande')
    ]
    ax.legend(handles=legend_elements, title="Oscilación")

    plt.tight_layout()
    plt.show()




import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import math

# Colores fijos por tipo de oscilación
COLOR_MAP = {"chica": "green", "mediana": "orange", "grande": "blue"}

def Plot_comparativo_ordenado(lista_ids):
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

    fig, axs = plt.subplots(filas, columnas, figsize=(4 * columnas, 3 * filas), sharex=False, sharey=False)

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
                t = np.array(d["T"])
                theta = np.array(d["theta"])
                
               # periodo = estimar_periodo(t, theta)
                #if periodo is None:
                    #continue  # saltar si no se puede estimar el período

               # T_max = 4 * periodo
                #mask = t <= T_max
               # t_cortado = t[mask]
                #theta_cortado = theta[mask]
                 # Recortar a los primeros T_max segundos
                T_max = 5
                mask = t <= T_max
                t = t[mask]
                theta = theta[mask]

                theta0 = round(theta[0], 2)
                ax.plot(t, theta, label=f"θ₀ = {theta0}")
                ax.legend(loc='lower right', fontsize=4)
                

        peso, largo = key
        ax.set_title(f"Peso: {peso}g, Largo: {largo}cm", fontsize=8)
        ax.set_xlabel("t [s]")
        ax.set_ylabel("θ [rad]")
        ax.set_xticks(np.arange(0, 6, 1))  # eje x de 0 a 7 s
        ax.grid(True)
        ax.legend(fontsize=8)

        # Ajuste del eje Y en base al valor máximo de theta
        if len(theta) > 0:
            max_theta = np.max(np.abs(theta))
            ax.set_ylim(-max_theta * 1.1, max_theta * 1.1)

    # Eliminar subplots vacíos
    for j in range(i + 1, filas * columnas):
        fig.delaxes(axs[j // columnas, j % columnas])

    
    plt.tight_layout()
    plt.suptitle("Comparación de θ(t) con distintas amplitudes iniciales", fontsize=9, y=1)
    plt.show()

def Plot_theta_vs_t_con_armonica():
    """
    Compara θ(t) medido con la solución armónica ideal A cos(√(g/L) t + φ), 
    para amplitud chica y grande, en condiciones de masa y largo fijos.
    """
    import matplotlib.pyplot as plt
    import numpy as np

    ids = {"chica": 5941, "grande": 5939} #ESTO HAY QUE REVISAR QUE SEA EL MÄS MÄS CHICO Y EL MÄS MÄS GRANDE
    g = 9.81  # m/s²

    for tipo, vid in ids.items():
        datos = process(str(vid))
        T = np.array(datos["T"])
        theta = np.array(datos["theta"])
        A = theta[0]
        #A_deg = np.rad2deg(A)
        L_cm = datos["Largo"]
        L = L_cm / 100  # convertir a metros
        omega_teorica = np.sqrt(g / L)

        # Estimación de fase
        t0 = T[0]
        phi = np.arccos(theta[0] / A) - omega_teorica * t0

        # Solución armónica ideal
        theta_armonica = A * np.cos(omega_teorica * T + phi)

        plt.figure(figsize=(8, 4))
        plt.plot(T, theta, '-', color='blue', label=r"$\theta$ real")
        plt.plot(T, theta_armonica, '--', color='orange', label=r"$\theta$ armónica (pequeñas oscilaciones)")
        plt.xlabel("t [s]")
        plt.ylabel(r"$\theta$ [rad]")
        plt.title(f"Comparación entre solución exacta y armónica\nAmplitud inicial: {A:.1f}°") #DAN RARO LOS ANGULOS
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()



def main():
    lista = [5917, 5918, 5920, 5921, 5922, 5923, 5924, 5925, 5926, 5927, 5928, 5929, 5930, 5931, 5932, 5933, 5934, 5936]
    
    Plot_frecuencias()
    Plot_frecuencia_vs_M()
    # Plot_comparativo_ordenado(lista)
    #Plot_theta_vs_t_con_armonica()

    
    #res = process(5926)

    #graph(res,"theta")

#     print(GetFrecuencia(res))
main()
    

