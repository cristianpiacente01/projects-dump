import numpy as np

def random_matrix(N):
    """
    Generate a random N x N matrix with values ranging from 0 to 255.

    Parameters:
    N (int): The dimension of the matrix.

    Returns:
    np.array: The generated random matrix.
    """
    return np.random.randint(low=0, high=256, size=(N, N), dtype=np.uint8)
