from scipy.io import mmread
import numpy as np
import os

for filename in os.listdir('matrici'):
    f = os.path.join('matrici', filename)
    if os.path.isfile(f) and f.endswith('.mtx'):
        matrix = mmread(f).todense()
        eigenvalues = np.linalg.eigvalsh(matrix)
        print(f"{filename} - Autovalore min: {np.min(eigenvalues)}")
        print(f"{filename} - Autovalore max: {np.max(eigenvalues)}")