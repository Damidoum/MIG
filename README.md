### Quelques liens :
- Time Series Classification : https://keras.io/examples/timeseries/timeseries_classification_from_scratch/
- simu en ligne : https://rep.mines-paristech.fr/home
- clustering : https://ledatascientist.com/k-means-sur-des-series-temporelles/
- https://towardsdatascience.com/hands-on-climate-time-series-clustering-using-machine-learning-with-python-6a12ce1607f9

Test-Classification -> familirisation avec la notion de classification des séries temporelles. On teste les fonctions sur des données covid. 

data -> stockage de tous les fichiers csv nécessaires et générés 

### Pour les scripts python :  
- auto_calcul.py : automatisation du lancement des calculs sur la VM
- lancement.py : dépendance de auto_calcul.py 
- auto_krig_csv.py : automatisation de la récupération des données du krigeage 
- auto_post_process.py : automatisation du lancement et de la récupération des posts process
- classification.py : mise en forme et classification des séries temporelles grâce à la librairie tslearn 


### Description du krigeage : 
kriging_final -> nécéssite les données au format krig_class{i}.csv, fait le krigeage, sauvegarde le metamodèle dans une study openturns et les courbes d'approximation du modèle en png

pour l'utilisation du fichier xml:
import openturns as ot

study = ot.Study()

study.setStorageManager(ot.XMLStorageManager(f'metamodel_par_classe.xml'))

i = 5 #numéro de la classe

study.load() #charge le fichier

metamodel = ot.Function() #crée un metamodèle vide

study.fillObject(f'metamodel_class{i}', metamodel) #metamodel est le modèle en question, il prend un tuple (espilon300, epsilon600) et renvoie la valeur de sigma
