import numpy as np
from scipy.io import mmread
import os

def controlla_dominanza_righe(matrix):
    for row_index in range(matrix.shape[0]):
        row = matrix[row_index, :]
        diagonal_value = matrix[row_index, row_index]
        sum_other = np.sum(row) - diagonal_value
        if (diagonal_value <= sum_other):
            return False
    return True

def controlla_dominanza_colonne(matrix):
    for col_index in range(matrix.shape[1]):
        col = matrix[:, col_index]
        diagonal_value = matrix[col_index, col_index]
        sum_other = np.sum(col) - diagonal_value
        if (diagonal_value <= sum_other):
            return False
    return True

for filename in os.listdir('matrici'):
    f = os.path.join('matrici', filename)
    if os.path.isfile(f) and f.endswith('.mtx'):
        matrix = mmread(f).todense()
        dominanza_per_righe = controlla_dominanza_righe(matrix)
        dominanza_per_colonne = controlla_dominanza_colonne(matrix)
        print(f"Dominanza per righe in {filename}: {dominanza_per_righe}")
        print(f"Dominanza per colonne in {filename}: {dominanza_per_colonne}")
