import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# from tslearn.clustering import TimeSeriesKMeans


def format_post_process(file, folder):
    """Prend le fichier du post process et le met en forme pour être mis correction dans un DataFrame pandas"""
    fichier = open(file, "r")
    char = fichier.read()
    char_split = ["# ===" + x for x in char.split("# ===")[1:]]
    time = [float(x.split("\n")[0][13:]) for x in char_split]
    time_str = ""
    for x in time:
        time_str += str(x)
    char_split = [x.split("\n", maxsplit=1) for x in char_split]
    doc = [x[1][2:] for x in char_split]

    os.mkdir(folder)
    for k in range(len(doc)):
        with open(folder + "/time" + str(k) + ".txt", "w") as f:
            f.write(doc[k])

    # Mettons les données sous forme de dataframe
    lst_df = []
    for k in range(len(os.listdir(folder))):
        lst_df.append(pd.read_csv("time" + str(k) + ".txt", sep="  "))
    df = pd.concat(lst_df)  # dataFrame global
    nodes = df["node"].unique()  # différents noeuds
    by_nodes = {}
    for node in nodes:
        aux = df[df["node"] == node].copy()
        aux["time"] = time
        aux = aux.drop(["node", "X", "Y", "Z"], axis=1)
        aux.set_index("time", inplace=True)
        aux["epsilon_" + str(node)] = (
            1
            / 2
            * (
                aux["gpeto11"]
                + aux["gpeto33"]
                + np.sqrt(
                    np.square(aux["gpeto11"] - aux["gpeto33"])
                    + 4 * np.square(aux["gpeto31"])
                )
            )
        )
        by_nodes[str(node)] = aux
    nodes_str = list(by_nodes.keys())


format_post_process(
    "/Users/damidoum/Desktop/MIG/TraitementEpsilon/epsilon_11_31_33.txt",
    "/Users/damidoum/Desktop/MIG/TraitementEpsilon/time_series2",
)
