from scipy.fftpack import idctn

def lib_idct2(A):
    """
    Compute the inverse 2D Discrete Cosine Transform (IDCT) of a matrix using the scipy library function.

    Parameters:
    A (np.array): The DCT-transformed matrix.

    Returns:
    np.array: The original matrix after applying IDCT.
    """
    return idctn(A, type=2, norm='ortho')
