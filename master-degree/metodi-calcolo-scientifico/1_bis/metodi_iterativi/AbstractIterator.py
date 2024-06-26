import time
from scipy.sparse.linalg import spsolve
import numpy as np
from scipy.sparse import tril
from metodi_iterativi.utils.utils import write_report_and_logs
from abc import ABC, abstractmethod

class AbstractIterator(ABC):
    def __init__(self, matrice_A, tol, max_iter=20000):
        self.matrice_A = matrice_A
        self.x_perfect = np.ones(matrice_A.shape[0])
        self.x = np.zeros(matrice_A.shape[0])
        self.b = matrice_A.dot(self.x_perfect) # A * x con x=[1,...,1]
        self.tol = tol
        self.k = 0
        self.errore_history = []
        self.t_esecuzione = 0
        self.max_iter = max(max_iter, 20000)
        self.b_norma = np.linalg.norm(self.b) # || b ||
    
    def get_residuo(self):
        # b - A * x(k)
        return self.b - self.matrice_A.dot(self.x)
    
    @abstractmethod
    def update(self):
        pass

    def relative_error(self):
        num = self.x - self.x_perfect
        return np.divide(np.linalg.norm(num), np.linalg.norm(self.x))
    
    def non_converge(self):
        return np.linalg.norm(self.get_residuo()) / self.b_norma >= self.tol 

    def solve(self):
        path_report = 'report_experiment/'
        file_report = 'report.txt'
        start = time.time()
        while self.non_converge():
            self.x = self.update()
            self.errore_history.append(self.relative_error())
            self.k += 1
            if self.k > self.max_iter:
                write_report_and_logs(path_report, file_report, "!!! Numero massimo di iterazioni raggiunte !!!!\n")
                break
        end = time.time() - start
        self.t_esecuzione = end
        write_report_and_logs(path_report, file_report, "Numero di iterazioni: " + str(self.k) + "\n")
        write_report_and_logs(path_report, file_report, "Errore relativo: " + str(self.relative_error()) + "\n")
        write_report_and_logs(path_report, file_report, "Tempo di esecuzione: " + str(round(end, 3)) + " (s)" + "\n")
        write_report_and_logs(path_report, file_report, "\n")


class Jacobi(AbstractIterator):
    def __init__(self, matrice_A, tol):
        super().__init__(matrice_A, tol)
        self.diag_inv = self.get_p_inverso(matrice_A)

    def get_p_inverso(self, matA): # P^-1 ovvero: a_ii = 1 / a_ii
        temp = matA.diagonal()
        temp = 1 / temp
        return temp
        
    def update(self):
        #        x(k) + P^-1 * r(k)
        return self.x + (self.diag_inv * self.get_residuo())


class GaussSeidel(AbstractIterator):
    def __init__(self, matrice_A, tol):
        super().__init__(matrice_A, tol)
        self.triang_inf = tril(self.matrice_A).tocsr()

    def update(self):
        #        x(k) +  risultato: P * y = r(k)
        return self.x + spsolve(self.triang_inf, self.get_residuo()) 
    
class Gradiente(AbstractIterator):
    def __init__(self, matrice_A, tol):
        super().__init__(matrice_A, tol)
    
    def get_y(self):
        # y(k) = A * r(k)
        return self.matrice_A.dot(self.get_residuo())
    
    def get_a_b(self):
        # a = r(k)^T * r(k), b = r(k)^T * y(k)
        residuo = self.get_residuo()
        return np.transpose(residuo).dot(residuo), np.transpose(residuo).dot(self.get_y())
    
    def update(self):
        a, b = self.get_a_b()
        alpha = a / b
        #       x(k)  +    alpha * r(k)
        return self.x + (alpha * self.get_residuo())
    

class GradienteConiugato(AbstractIterator):
    def __init__(self, matrice_A, tol):
        super().__init__(matrice_A, tol)
        self.d = self.get_residuo() # d(0) = r(0) cioè self.b - (self.matrice_A.dot(self.x))
        
    def update(self):
        y = self.matrice_A.dot(self.d)
        #z = self.matrice_A.dot(self.d)
        alpha = (self.d.dot(self.get_residuo())) / (self.d.dot(y))
        self.x = self.x + (alpha * self.d)
        nuovo_res = self.get_residuo()
        w = self.matrice_A.dot(nuovo_res)
        beta = (self.d.dot(w)) / (self.d.dot(y))
        self.d = nuovo_res - (beta * self.d)
        return self.x