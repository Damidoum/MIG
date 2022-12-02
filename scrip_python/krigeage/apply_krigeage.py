import openturns as ot
import pandas as pd 
import numpy as np 

study = ot.Study()
study.setStorageManager(ot.XMLStorageManager(f'metamodel_par_classe.xml'))
study.load()
lst = [ot.Function() for _ in range(10)]
for i in range(10):
    if i != 2: 
        study.fillObject(f'metamodel_class{i}', lst[i]) 

df = pd.read_csv('../../data/krigeage/for_krigeage.csv', index_col = 'node')
dico = {}
for x in df.index : 
    dico[x] = int(x.split('_')[1])
df = df.rename(dico)
df = df.rename({'3630.0' : '600.0'}, axis = 1)
df2 = df.groupby('classe')

res = []
for k in range(10): 
    if k!=2: 
        df3 = df2.get_group(k)
        l = [lst[k]((df3.iloc[i,0],df3.iloc[i,1]))[0] for i in range(len(df3))]
        df3['sig'] = l
        res.append(pd.DataFrame(df3['sig']))
    else : 
        df3 = df2.get_group(k)
        l = [0 for _ in range(len(df3))]
        df3['sig'] = l
        res.append(pd.DataFrame(df3['sig']))
df_res = pd.concat(res)
df_res.to_csv('../../data/sig.csv')

