import subprocess
import os

# fichier utilisé par le fichier auto_calcul.py
def lancement(classe, k):
    os.chdir(
        "/home/user/store/data/calcul_zoom_"
        + str(classe)
        + "/calcul_zoom_"
        + str(classe)
        + str(k)
    )
    subprocess.run(
        "Zrun /home/user/store/data/calcul_zoom_"
        + str(classe)
        + "/calcul_zoom_"
        + str(classe)
        + str(k)
        + "/calcul_v7.inp",
        shell=True,
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 3:
        classe = sys.argv[1]
        k = sys.argv[2]
        lancement(classe, k)
