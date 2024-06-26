import numpy as np
from scipy.fftpack import dct

def _w(k, N):
    """
    Calculate the cosine coefficients for the DCT.

    Parameters:
    k (int): Frequency index.
    N (int): Length of the input vector.

    Returns:
    list: Cosine coefficients for the given frequency.
    """
    # Initialize an empty list to store the coefficients
    coefficients = []
    
    # Calculate each cosine coefficient
    for i in range(N):
        # Using the formula: cos(k * pi * (2i + 1) / (2N))
        coefficient = np.cos(k * np.pi * (2 * i + 1) / (2 * N))
        coefficients.append(coefficient)
    
    return coefficients

def my_dct(v):
    """
    Compute the Discrete Cosine Transform (DCT) of a vector.

    The DCT is used to transform a sequence of values into components
    of varying frequencies.

    Parameters:
    v (list or np.array): The input vector.

    Returns:
    list: The DCT coefficients.
    """
    N = len(v)  # Length of the input vector
    result = []  # List to store DCT coefficients

    # Compute each DCT coefficient
    for k in range(N):
        # Calculate the dot product of the input vector and the cosine coefficients
        coef = np.dot(v, _w(k, N))
        
        # Normalize the result
        if k == 0:
            coef /= np.sqrt(N)
        else:
            coef /= np.sqrt(N / 2)
        
        # Append the coefficient to the result list
        result.append(coef)

    return result

def lib_dct(v):
    """
    Compute the DCT of a vector using the scipy library function.

    Parameters:
    v (list or np.array): The input vector.

    Returns:
    np.array: The DCT coefficients.
    """
    return dct(v, type=2, norm='ortho')
