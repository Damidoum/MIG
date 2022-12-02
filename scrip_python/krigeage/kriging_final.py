import openturns as ot
import openturns.viewer as viewer
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
ot.Log.Show(ot.Log.NONE)

def krigeage(i):
    
    #extraction des donnees
    df = pd.read_csv(f"../../data/krigeage/krig_classe{i}.csv")

    x_train = df.loc[:,['epsilon_300', 'epsilon_600']]
    y_train = df['sig']

    x_train, y_train = np.array(x_train), np.array(y_train)

    x_train = ot.Sample(x_train)
    y_train = ot.Sample([[elt] for elt in y_train])

    #création de l'algo
    dimension = 2
    basis = ot.QuadraticBasisFactory(dimension).build()
    covarianceModel = ot.MaternModel([1.]*dimension, 1.5)
    algo = ot.KrigingAlgorithm(ot.Sample(x_train), ot.Sample(y_train), covarianceModel, basis)
    #entrainement de l'algo
    algo.run()
    result = algo.getResult()
    metamodel = result.getMetaModel()

    '''#sauvegarde du metamodel
    study = ot.Study()
    fileName = f"metamodel_class{i}.xml"
    study.setStorageManager(ot.XMLStorageManager(fileName))
    study.add("metamodel", metamodel)
    study.save()'''

    #visualisation du modèle
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    e300 = np.linspace(np.min(df['epsilon_300']), np.max(df['epsilon_300']), 100)
    e600 = np.linspace(np.min(df['epsilon_600']), np.max(df['epsilon_600']), 100)

    sig = [[metamodel((e300[i], e600[j])) for i in range (len(e300))] for j in range(len(e600))]
    e300, e600 = np.meshgrid(e300, e600)


    ax.plot_surface(e300, e600, np.array(sig)[:, :, 0], alpha = 0.5, linewidth=0, antialiased=False)
    ax.scatter(np.array(x_train)[:, 0], np.array(x_train)[:, 1], np.array(y_train)[:, 0],s = 50, color = 'red', antialiased=False)
    ax.set_xlabel('epsilon 300')
    ax.set_ylabel('epsilon 600')
    ax.set_zlabel('sigma (MPa)')
    plt.savefig(f"../../Img/krigeage/metamodel_class{i}.png")
    #plt.show()
    return metamodel

if __name__ == "__main__":
    study = ot.Study()
    fileName = "metamodel_par_classe.xml"
    study.setStorageManager(ot.XMLStorageManager(fileName))
    for i in [0,1] + list(range(3,10)):
        study.add(f"metamodel_class{i}", krigeage(i))
    study.save()