import os
import subprocess
import shutil
import sys


def prost_process_file(classe):
    """Mise en place des fichiers de post process et de maillage"""
    for k in range(10):
        shutil.copyfile(
            "/home/user/store/data/Preparation INP/create_group.inp",
            "/home/user/store/data/calcul_zoom_"
            + str(classe)
            + "/calcul_zoom_"
            + str(classe)
            + str(k)
            + "/create_group.inp",
        )
        shutil.copyfile(
            "/home/user/store/data/Preparation INP/extract_on_group.inp",
            "/home/user/store/data/calcul_zoom_"
            + str(classe)
            + "/calcul_zoom_"
            + str(classe)
            + str(k)
            + "/extract_on_group.inp",
        )


def run_mesh(classe):
    """Création du maillage"""
    for k in range(10):
        os.chdir(
            "/home/user/store/data/calcul_zoom_"
            + str(classe)
            + "/calcul_zoom_"
            + str(classe)
            + str(k)
        )
        subprocess.call("xterm -e Zrun create_group.inp", shell=True)


def run_post(classe):
    """Lancement des posts process"""
    for k in range(10):
        os.chdir(
            "/home/user/store/data/calcul_zoom_"
            + str(classe)
            + "/calcul_zoom_"
            + str(classe)
            + str(k)
        )
        subprocess.call("xterm -e Zrun extract_on_group.inp", shell=True)


def get_post_process(classe):
    """Récupération des fichiers du post process"""
    if not os.path.exists("/home/user/store/data/Krigeage/Classe" + str(classe)):
        os.mkdir("/home/user/store/data/Krigeage/Classe" + str(classe))
    for k in range(10):
        shutil.copyfile(
            "/home/user/store/data/calcul_zoom_"
            + str(classe)
            + "/calcul_zoom_"
            + str(classe)
            + str(k)
            + "/extract_on_group.post",
            "/home/user/store/data/Krigeage/Classe"
            + str(classe)
            + "/extract_on_group"
            + str(k)
            + ".post",
        )


def main(classe):
    prost_process_file(classe)
    run_mesh(classe)
    run_post(classe)
    get_post_process(classe)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        classe = int(sys.argv[1])
        main(classe)
