"""
    T-test between groups
"""
import os, glob
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt

def plot_groups(data):
    """Cumulative bars of pairwise groups
    """
    groups = data.groupby('DX_Group').size()
    labels = ['AD/Normal', 'AD/MCI', 'MCI/Normal', 'MCI/LMCI']
    
    p1 = [groups.AD, groups.AD, groups.MCI, groups.MCI]
    p2 = [groups.Normal, groups.MCI, groups.Normal, groups.LMCI]
    width = .35
    plt.bar(range(len(p1)), p1, width, color='g')    
    plt.bar(range(len(p2)), p2, width, color='y', bottom=p1)
    plt.ylabel('Individuals')
    plt.title('Population repartition')
    plt.xticks(np.arange(len(p1))+width/2., labels )
    plt.yticks(np.arange(0,81,10))
    fname = 'population_repartition_adni_baseline_'
    plt.savefig(os.path.join('figures', fname))



BASE_DIR = '/disk4t/mehdi/data/pet_fdg_baseline_processed_ADNI'
data = pd.read_csv(os.path.join('description_file.csv'))
Y = np.zeros(len(data))
Y[data[data.DX_Group=='AD'].index.values]=1

if os.path.exists('features.npy'):
    X = np.load('features.npy')
    


#AD/MCI, AD/Normal, MCI/LMCI, MCI/Normal
pairwise_groups = [['AD', 'Normal'],
                   ['AD', 'MCI'],
                   ['MCI', 'Normal'],
                   ['MCI', 'LMCI']]
                   
pg = pairwise_groups[0]

print pg

