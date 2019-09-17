# *-* coding: utf-8 *-*

# v0.1

import sys, os
import numpy as np
import matplotlib.pyplot as plt
from bisect import bisect_left

# Lista de prngs válidos para o benchmark
# VALID_PRNGS = ['RANDOM','RANDOM_DATE','DATE_N','DATE_AMD','SHUF','SHUF_URANDOM','URANDOM']

def plot_histogram(data, n_bins, prng_name, std_error, output_file):
    ''' Gera o histograma para os valores do arquivo de entrada '''
    count, bins, ignored = plt.hist(data, n_bins, facecolor='green')
    x_start = int(data[0])
    x_end = int(data[len(data)-1])
    x_label = "Valores gerados ({} bins)".format(n_bins)
    plt.xticks(np.arange(0, 10001, step=1000))
    # x_label = "X~U[" + str(x_start) + "," + str(x_end) + "]"
    plt.xlabel(x_label)
    plt.ylabel('Qtd. de números gerados em cada grupo') # Legenda eixo y
    plt.title("Distribuição de valores da função {}".format(prng_name)) # Legenda eixo x
    y_end = len(data) / n_bins
    y_end = int(y_end * 1.2)

    y, binEdges = np.histogram(data, bins = n_bins)
    bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
    # plt.bar(bincenters, y, width=0.05, color='black', yerr= std_deviation, joinstyle='bevel')
    plt.errorbar(bincenters, y, color='black', yerr= std_error, fmt='none', capsize=2.5)
    plt.hist(data, bins, histtype='bar', ec='black', color='green')
    plt.axis([x_start, x_end, 0, y_end]) # x_start, x_end, y_start, y_end
    plt.grid(True, linestyle='dotted', color='black') # Grade desenhada sobre o gráfico
    # plt.legend('Desvio Padrão - {}'.format(std_deviation), loc = 4, fancybox= True)
    plt.savefig(output_file)
    plt.show(block = False)


def read_data(filename):
    ''' Lê os dados do arquivo de entrada'''
    myfile = open(filename, "r")
    data = [] # Valores lidos do arquivo de números gerados
    for val in myfile.read().split():
        data.append(int(val)) # Carrega os valores lidos do arquivo pra lista 'data'
    myfile.close()
    return data


def calc_error(data, n_bins, bins):
    ''' Conta os valores em cada bin e realiza o cálculo de desvio e erro padrão '''
    idxs = [bisect_left(data, x) for x in sorted(bins)]
    bin_data = [data[x:y] for x,y in zip([0]+idxs, idxs+[len(data)]) if x!=y] # Cria uma lista onde cada sublista é um bin

    uniform_dist = len(data) / n_bins
    total_sum = 0

    for i in range(len(bin_data) - 1):
        total_sum += (len(bin_data[i]) - uniform_dist) ** 2

    std_deviation = (total_sum / n_bins) ** (1/2) # Desvio padrão
    std_error = std_deviation / (n_bins ** (1/2)) # Erro padrão (Desvio padrão dividido pela raiz quadrada do número de amostras)
    return std_deviation, std_error


def benchmark(prng, iterations):
    deviation_list = []
    error_list = []
    n_bins = 20 # Número de bins
    for i in range(iterations): # Gera um novo arquivo <iterations> vezes
        os.system('rm benchmark.txt 2> /dev/null') # Apaga o arquivo da iteração anterior
        os.system('{} >> benchmark.txt'.format(prng)) # Gera os números e salva no arquivo benchmark.txt
        data = read_data('benchmark.txt') # Lê os números gerados

        count, bins, ignored = plt.hist(data, n_bins, facecolor='green')
        data.sort(key=int)
        std_deviation, std_error = calc_error(data, n_bins, bins) # Calcula o erro pra iteração atual
        deviation_list.append(std_deviation) # Coloca o desvio atual na lista de desvios
        error_list.append(std_error) # Coloca o erro atual na lista de erros

    average_std_deviation = "{:.3f}".format(sum(deviation_list) / len(deviation_list)) # Calcula a média dos desvios
    average_std_error = "{:.3f}".format(sum(error_list) / len(error_list)) # Calcula a média dos erros

    print(15 * '-')
    print("PRNG: {}\nIterações: {}\nDesvio padrão médio: {}\nErro padrão médio: {}".format(prng, iterations, average_std_deviation, average_std_error))
    print(15 * '-')


def main():
    if len(sys.argv) != 4:
        print("[+] Read the input file and run a single time  outputting standard deviation, error and a histogram.")
        print("Usage: ./" + sys.argv[0] + " <input_file.txt> <output_file.png> <prng_name>")
        print()
        print("[+] Use the given PRNG to generate <number> files and calculate the average standard deviation and standard error.")
        print("Usage: ./" + sys.argv[0] + " benchmark <number> <prng_name>")
        raise SystemExit()

    elif sys.argv[1] == 'benchmark':
        # if sys.argv[3] in VALID_PRNGS:
        benchmark(sys.argv[3], int(sys.argv[2]))
        # else:
            # print("Please choose one of the following PRNGS: \n{}".format(", ".join(VALID_PRNGS)))

    elif len(sys.argv) == 4:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        prng_name = sys.argv[3]

        data = read_data(input_file)

        n_bins = 20 # Número de bins
        count, bins, ignored = plt.hist(data, n_bins, facecolor='green')
        data.sort(key=int)

        std_deviation, std_error = calc_error(data, n_bins, bins)
        print("Desvio padrão: {:.3f}; Erro Padrão: {:.3f}".format(std_deviation, std_error))
        print("Histograma salvo em '{}'.\n".format(output_file))

        plot_histogram(data, n_bins, prng_name, std_error, output_file)

        # for i in range(len(bin_data) - 1):
        #     print("bin {}: {}".format(i, len(bin_data[i]))) # Exibe a quantidade de valores em cada bin


if __name__ == "__main__":
    main()
