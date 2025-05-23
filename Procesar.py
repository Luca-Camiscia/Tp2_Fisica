
def process(path: str):
    with open(path, "r") as file:
        # Saltar las primeras 3 líneas
        for _ in range(3):
            next(file)
        # Voy a usar los t como clave
        Datos = {"T": [], "X": [], "Y": [], "theta": []}  # Leer línea por línea
        for linea in file:

            print(linea)
            limpio = linea.strip()
            curr = limpio.split()
            print(curr)
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
    if Id == "ALL":
        for key in ["X", "Y", "theta"]:
            plt.plot(Datos["T"], Datos[key], marker='o', label=key)
        plt.xlabel("T")
        plt.ylabel("Valor")
        plt.title("X, Y y theta vs T")
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
    plt.title(f"{Id} vs T")
    plt.grid(True)
    plt.show()
