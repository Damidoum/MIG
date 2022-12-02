import pandas as pd
import sys

# traitement des tableaux fixes
LHS = pd.read_csv("LHS_points.csv")
LHS = LHS.drop("Unnamed: 0", axis=1)
col = {"epsilon 300.0": "epsilon_300", "epsilon 3630.0": "epsilon_600"}
LHS = LHS.rename(col, axis=1)
index = list(range(10)) * 10
LHS["index"] = index
LHS.set_index("index", inplace=True)


def auto_krig_csv(classe):
    col2 = {"#": "time", "time": "sig"}
    lst = [
        pd.read_csv(
            "/home/user/store/data/Krigeage/Classe"
            + str(classe)
            + "/extract_on_group"
            + str(k)
            + ".post",
            sep=" ",
        )
        .drop(["<sigmises>", "Unnamed: 3"], axis=1)
        .rename(col2, axis=1)
        .set_index("time")
        for k in range(10)
    ]
    lst_sig = [float(x.iloc[2]) for x in lst]
    df = pd.DataFrame(lst_sig, columns=["sig"])
    krig = pd.concat([LHS.iloc[10 * classe : 10 * (classe + 1)], df], axis=1)
    krig.to_csv(
        "/home/user/store/data/Krigeage/format_ok/krig_csv_" + str(classe) + ".csv"
    )


if __name__ == "__main__":
    if len(sys.argv) == 2:
        classe = int(sys.argv[1])
        auto_krig_csv(classe)
