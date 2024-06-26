import numpy as np
from utils.matrix import random_matrix
from utils.dct2 import my_dct2, lib_dct2
import matplotlib.pyplot as plt
import timeit

# Matrix sizes for benchmarking
sizes = [40, 80, 160, 320, 640]

# Theoretical times based on complexity
my_theoretical_times = [n**3 for n in sizes]
lib_theoretical_times = [n**2 * np.log(n) for n in sizes]

# Lists to store actual measured times
my_times = []
lib_times = []

def get_times():
    """
    Measure and print the execution times for custom and library DCT2 implementations.
    """
    for size in sizes:
        matrix = random_matrix(size)
        print(f'--- Matrice {len(matrix)}x{len(matrix[0])} ---')
        my_times.append(timeit.timeit(lambda: my_dct2(matrix), number=1))
        print(f'Eseguita DCT2 homemade in {my_times[-1]} sec')
        lib_times.append(timeit.timeit(lambda: lib_dct2(matrix), number=1))
        print(f'Eseguita DCT2 SciPy in {lib_times[-1]} sec')

def scale_theoretical_to_practical(theoretical, practical):
    """
    Scale theoretical times to practical times using a median-based scaling factor.

    Parameters:
    theoretical (list): Theoretical execution times.
    practical (list): Actual measured execution times.

    Returns:
    list: Scaled theoretical times.
    """
    scaling_factor = np.median(np.array(practical) / np.array(theoretical))
    return [t * scaling_factor for t in theoretical]

def plot_times():
    """
    Plot the execution times on a semilog scale.
    """
    scaled_my_theoretical_times = scale_theoretical_to_practical(my_theoretical_times, my_times)
    scaled_lib_theoretical_times = scale_theoretical_to_practical(lib_theoretical_times, lib_times)
    
    plt.figure()
    plt.semilogy(sizes, scaled_my_theoretical_times, color='darkgoldenrod', label='n^3 (scaled)', linestyle='dashed')
    plt.semilogy(sizes, my_times, color='orange', label='Tempo DCT2 homemade')
    plt.semilogy(sizes, scaled_lib_theoretical_times, color='navy', label='n^2 log n (scaled)', linestyle='dashed')
    plt.semilogy(sizes, lib_times, color='cornflowerblue', label='Tempo DCT2 SciPy')
    plt.xticks(sizes)
    plt.xlabel('Dimensione matrice')
    plt.ylabel('Tempo (s)')
    plt.title('Tempi di esecuzione DCT2 in scala semilog')
    plt.legend()
    plt.savefig('tempi_dct2.png')
    plt.close()

def main():
    """
    Main function to measure and plot execution times.
    """
    get_times()
    plot_times()

if __name__ == "__main__":
    main()
