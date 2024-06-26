import numpy as np
from scipy.io import mmread
import os

def controlla_simmetrica(matrix):
    return np.allclose(matrix, matrix.T)

def controlla_definita_positiva(matrix):
    try:
        res = np.all(np.linalg.eigvals(matrix) > 0)
    except np.linalg.LinAlgError:
        res = False
    return res

for filename in os.listdir('matrici'):
    f = os.path.join('matrici', filename)
    if os.path.isfile(f) and f.endswith('.mtx'):
        matrix = mmread(f).todense()
        simmetrica = controlla_simmetrica(matrix)
        definita_positiva = controlla_definita_positiva(matrix)
        print(f"{filename} - Simmetrica: {simmetrica}")
        print(f"{filename} - Definita Positiva: {definita_positiva}")
