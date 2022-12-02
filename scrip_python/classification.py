import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
from tslearn.clustering import TimeSeriesKMeans


def format_post_process(file, folder):
    """Prend le fichier du post process et le met dans un DataFrame"""
    fichier = open(file, "r")
    char = fichier.read()
    fichier.close()
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
            f.close()

    # Mettons les données sous forme de dataframe
    lst_df = []
    for k in range(len(os.listdir(folder))):
        lst_df.append(pd.read_csv(folder + "/time" + str(k) + ".txt", sep="  "))
    df = pd.concat(lst_df)  # dataFrame global
    nodes = df["node"].unique()  # différents noeuds
    by_nodes = {}
    for node in nodes:
        aux = df[df["node"] == node].copy()
        aux["time"] = time
        aux = aux.drop(["node", "X", "Y", "Z"], axis=1)
        aux.set_index("time", inplace=True)
        aux[str(node)] = (
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
    lst_eps = []
    for node in nodes_str:
        lst_eps.append(
            by_nodes[node]
            .copy()
            .drop(["gpeto11", "gpeto31", "gpeto33"], axis=1)
            .transpose()
        )
    df_eps = pd.concat(lst_eps)
    df_eps.to_csv(folder + "/epsilon.csv")

    # pour les coordonnées :
    coord = pd.read_csv(folder + "/time0.txt", sep=" ")
    coord = coord[["node", "X", "Y", "Z"]]
    coord.set_index("node", inplace=True)
    coord.to_csv(folder + "/coord.csv")


def classification(timeSeries_file, coord_file, classe_file, number_of_cluster):
    """Fais la classification des séries temporelles"""
    # Séries temporelles par noeud
    timeSeries = pd.read_csv(timeSeries_file).rename({"Unnamed: 0": "node"}, axis=1)
    timeSeries.set_index("node", inplace=True)

    # Liste des noeuds
    node = list(timeSeries.index)

    # Coordonnées de chaque noeud
    coord = pd.read_csv(coord_file)
    coord.set_index("node", inplace=True)

    model = TimeSeriesKMeans(n_clusters=number_of_cluster, metric="dtw", max_iter=10)
    prediction = model.fit_predict(timeSeries)

    df = pd.DataFrame(node, columns=["node"])
    df["classe"] = prediction
    df.set_index(["node"], index=True)
    df.to_csv(classe_file)
