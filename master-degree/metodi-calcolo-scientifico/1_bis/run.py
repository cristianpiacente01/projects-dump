from metodi_iterativi.AbstractIterator import Jacobi, GaussSeidel, Gradiente, GradienteConiugato
from metodi_iterativi.utils.utils import read, write_report_and_logs
import os

def build_matrix_paths_list(directory):
    matrici = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f) and f.endswith('.mtx'):
            matrici.append(f)
    return matrici

def main():
    output_path = "report_experiment/"
    output_file = "report.txt"
    matrices = build_matrix_paths_list('matrici')
    tols = [0.0001, 10 ** -6, 10 ** -8, 10 ** -10]

    write_report_and_logs(output_path, output_file, "               RESOCONTO DELLE ESECUZIONI\n")
    for m in matrices:
        write_report_and_logs(output_path, output_file, "******************************************************\n")
        mat = str(m.split("\\")[-1])
        temp = mat
        write_report_and_logs(output_path, output_file, "                    "+mat+"\n")
        write_report_and_logs(output_path, output_file, "******************************************************\n")
        for t in tols:
            mat = read(m)
            write_report_and_logs(output_path, output_file, "******************************************************\n")
            write_report_and_logs(output_path, output_file, "                 tolleranza:"+str(t)+"\n")
            write_report_and_logs(output_path, output_file, "******************************************************\n")
            write_report_and_logs(output_path, output_file, "Algoritmo utilizzato: Jacobi\n")

            jacobi = Jacobi(mat, t)
            jacobi.solve()

            write_report_and_logs(output_path, output_file, "Algoritmo utilizzato: Gauss-Seidel\n")
            gs = GaussSeidel(mat, t)
            gs.solve()

            write_report_and_logs(output_path, output_file, "Algoritmo utilizzato: Gradiente\n")
            gr = Gradiente(mat, t)
            gr.solve()

            write_report_and_logs(output_path, output_file, "Algoritmo utilizzato: Gradiente coniugato\n")
            gr_con = GradienteConiugato(mat, t)
            gr_con.solve()

if __name__ == "__main__":
    main()