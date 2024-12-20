import numpy as np
from utils.dct import my_dct, lib_dct
from utils.dct2 import my_dct2, lib_dct2

def test_dct():
    """
    Test the 1D DCT implementation against expected results.
    """
    v = [231, 32, 233, 161, 24, 71, 140, 245]
    expected_dct = [401.9902051045522, 6.600019905532548, 109.16736544429627, -112.78557857175124, 65.40737725975556, 121.83139803666808, 116.65648855486545, 28.800407217830443]
    assert np.allclose(lib_dct(v), expected_dct)
    assert np.allclose(my_dct(v), expected_dct)

def test_dct2():
    """
    Test the 2D DCT implementation against expected results.
    """
    A = [
        [231, 32, 233, 161, 24, 71, 140, 245],
        [247, 40, 248, 245, 124, 204, 36, 107],
        [234, 202, 245, 167, 9, 217, 239, 173],
        [193, 190, 100, 167, 43, 180, 8, 70],
        [11, 24, 210, 177, 81, 243, 8, 112],
        [97, 195, 203, 47, 125, 114, 165, 181],
        [193, 70, 174, 167, 41, 30, 127, 245],
        [87, 149, 57, 192, 65, 129, 178, 228]
    ]
    expected_dct2 = [
        [1.11875000e+03, 4.40221926e+01, 7.59190503e+01, -1.38572411e+02, 3.50000000e+00, 1.22078055e+02, 1.95043868e+02, -1.01604906e+02],
        [7.71900790e+01, 1.14868206e+02, -2.18014421e+01, 4.13641351e+01, 8.77720598e+00, 9.90829620e+01, 1.38171516e+02, 1.09092795e+01],
        [4.48351537e+01, -6.27524464e+01, 1.11614114e+02, -7.63789658e+01, 1.24422160e+02, 9.55984194e+01, -3.98287969e+01, 5.85237670e+01],
        [-6.99836647e+01, -4.02408945e+01, -2.34970508e+01, -7.67320594e+01, 2.66457750e+01, -3.68328290e+01, 6.61891485e+01, 1.25429731e+02],
        [-1.09000000e+02, -4.33430857e+01, -5.55436908e+01, 8.17347083e+00, 3.02500000e+01, -2.86602437e+01, 2.44149822e+00, -9.41437025e+01],
        [-5.38783591e+00, 5.66345009e+01, 1.73021519e+02, -3.54234494e+01, 3.23878249e+01, 3.34576728e+01, -5.81167864e+01, 1.90225615e+01],
        [7.88439693e+01, -6.45924096e+01, 1.18671203e+02, -1.50904840e+01, -1.37316928e+02, -3.06196663e+01, -1.05114114e+02, 3.98130497e+01],
        [1.97882438e+01, -7.81813409e+01, 9.72311860e-01, -7.23464180e+01, -2.15781633e+01, 8.12999035e+01, 6.37103782e+01, 5.90618071e+00]
    ]
    assert np.allclose(lib_dct2(A), expected_dct2)
    assert np.allclose(my_dct2(A), expected_dct2)

def main():
    """
    Main function to run the DCT tests.
    """
    test_dct()
    test_dct2()

if __name__ == "__main__":
    main()
