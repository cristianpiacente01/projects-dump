import numpy as np
from scipy.fftpack import dctn
from utils.dct import my_dct

def my_dct2(A):
    """
    Compute the 2D Discrete Cosine Transform (DCT) of a matrix.

    The 2D DCT is applied first on the columns and then on the rows
    of the input matrix.

    Parameters:
    A (np.array): The input matrix.

    Returns:
    np.array: The DCT-transformed matrix.
    """
    res = np.array(A, dtype=float)  # Convert input to float type matrix
    N, M = res.shape  # Get the dimensions of the matrix

    # Apply DCT to each column
    for j in range(M):
        res[:, j] = my_dct(res[:, j])

    # Apply DCT to each row
    for i in range(N):
        res[i, :] = my_dct(res[i, :])

    return res

def lib_dct2(A):
    """
    Compute the 2D DCT of a matrix using the scipy library function.

    Parameters:
    A (np.array): The input matrix.

    Returns:
    np.array: The DCT-transformed matrix.
    """
    return dctn(A, type=2, norm='ortho')
