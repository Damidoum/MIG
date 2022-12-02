from string import Template
import pandas as pd
import os
import subprocess
import shutil
import sys

with open("calcul_v7.inp", "r") as f:
    content = f.read()
    f.close()

t = Template(content)
out = t.substitute({"VALEUR1": 10, "VALEUR2": 11})


def auto_calcul(classe):
    # Création des fichiers inp (le nom des fichiers correspond à l'organisation de la machine virtuelle)
    lst = []
    df = pd.read_csv("LHS points.csv")
    df = df.drop("Unnamed: 0", axis=1)
    df = df.iloc[10 * classe : 10 * (classe + 1)] * 4
    for k in range(10):
        dico = {}
        dico["VALEUR1"] = df.iloc[k, 0]
        dico["VALEUR2"] = df.iloc[k, 1]
        lst.append(dico)
    if not os.path.exists("classe_inp_" + str(classe)):
        os.mkdir("classe_inp_" + str(classe))
    for k in range(10):
        t = Template(content)
        out = t.substitute(lst[k])
        with open(
            "classe_inp_" + str(classe) + "/calcul_v7_" + str(classe) + str(k) + ".inp",
            "w",
        ) as f:
            f.write(out)
            f.close()
    if not os.path.exists("classe_inp_" + str(classe)):
        os.mkdir("calcul_zoom_" + str(classe))

    # Création des dossiers de calcul
    for k in range(10):
        if not os.path.exists(
            "/home/user/store/data/calcul_zoom_"
            + str(classe)
            + "/calcul_zoom_"
            + str(classe)
            + str(k),
        ):
            shutil.copytree(
                "/home/user/store/data/calcul_zoom_model",
                "/home/user/store/data/calcul_zoom_"
                + str(classe)
                + "/calcul_zoom_"
                + str(classe)
                + str(k),
            )
        shutil.copyfile(
            "/home/user/store/data/Preparation INP/classe_inp_"
            + str(classe)
            + "/calcul_v7_"
            + str(classe)
            + str(k)
            + ".inp",
            "/home/user/store/data/calcul_zoom_"
            + str(classe)
            + "/calcul_zoom_"
            + str(classe)
            + str(k)
            + "/calcul_v7.inp",
        )

    # Lancement des calculs
    commande = ""
    for k in range(9):
        commande += (
            "xterm -hold -e python lancement.py " + str(classe) + " " + str(k) + " & "
        )
    commande += "xterm -hold -e python lancement.py " + str(classe) + " 9"
    subprocess.call(commande, shell=True)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        classe = int(sys.argv[1])
        auto_calcul(classe)
