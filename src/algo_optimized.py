from itertools import chain
import numpy as np
from scipy.spatial import distance
def sort(array, sortIndex):
    """Sort the array by using quicksort."""
    less = []
    equal = []
    greater = []
    if len(array) > 1:
        pivot = array[0][sortIndex]
        for x in array:
            if x[sortIndex] < pivot:
                less.append(x)
            elif x[sortIndex] == pivot:
                equal.append(x)
            elif x[sortIndex] > pivot:
                greater.append(x)
        return sort(less, sortIndex)+equal+sort(greater, sortIndex)  # Just use the + operator to join lists
    else:
        return array
file1 = "data_scenarios_a_example.in"
file2 = "data_scenarios_b_mumbai.in"
file3 = "data_scenarios_c_metropolis.in"
file4 = "data_scenarios_d_polynesia.in"
file5 = "data_scenarios_e_sanfrancisco.in"
file6 = "data_scenarios_f_tokyo.in"

ofile1 = "data_scenarios_a_example.out"
ofile2 = "data_scenarios_b_mumbai.out"
ofile3 = "data_scenarios_c_metropolis.out"
ofile4 = "data_scenarios_d_polynesia.out"
ofile5 = "data_scenarios_e_sanfrancisco.out"
ofile6 = "data_scenarios_f_tokyo.out"

input = [file1, file2, file3, file4, file5, file6]
output = [ofile1, ofile2, ofile3, ofile4, ofile5, ofile6]
for filezz in range(len(input)):
    print(">>>>>>>>>>>>>>>>>>>>> START {}".format(input[filezz]))
    with open(input[filezz], 'r') as fin:
        iter = chain.from_iterable(line.split() for line in fin)
        listabrutta = list(iter)
        lista = list()
        for c in listabrutta:
            lista.append(int(c))
        W = int(lista[0])
        H = int(lista[1])
        Nbuildings = int(lista[2])
        Mantenas = int(lista[3])
        MaxAntennas = int(lista[4])
        lista_edifici = []
        # lista edifici
        for i in range(Nbuildings):
            edifici = np.array(lista[5 + i * 4: 5 + i * 4 + 4])
            edifici = list(edifici)
            lista_edifici.append(edifici)
        lista_antenne = []
        for i in range(Mantenas):
            antenna = np.array(lista[5 + Nbuildings * 4 + i * 2: 5 + Nbuildings * 4 + i * 2 + 2])
            antenna = list(antenna)
            antenna.insert(0,i)
            lista_antenne.append(antenna)
        lista_edifici = sort(lista_edifici,0)
        print("ORDERED LISTA EDIFICI")
        lista_antenne = sort(lista_antenne,1)
        print("ORDERED LISTA ANTENNE")
        # algo
        result = []
        count = 0
        while (len(lista_antenne) > 0 and len(lista_edifici) > 0):
            index_max = len(lista_edifici) - 1
            edificio_max = lista_edifici[index_max]
            index_best_antenna = len(lista_antenne) - 1
            antenna_max  = lista_antenne[index_best_antenna]
            result.append([lista_antenne[index_best_antenna][0] , edificio_max[0], edificio_max[1] ])
            if antenna_max[1] > 0:
                new_lista_edifici = list()
                for i in range(len(lista_edifici)):
                    edificio  = lista_edifici[i]
                    #antenna_max[1] è latency
                    dst = distance.cityblock([edificio[0],edificio[1]], [edificio_max[0],edificio_max[1]])
                    if dst > antenna_max[1]:
                        new_lista_edifici.append(edificio)
                lista_edifici = new_lista_edifici
            else:
                lista_edifici.pop(index_max)
            lista_antenne.pop(index_best_antenna)
            count+=1
            print("MAX " + str(antenna_max[1]))
            print("NUMERO ANTENNA " + str(count) + " LISTA EDIFICI MANCANTI " + str(len(lista_edifici)))
        f = open(output[filezz], 'w')
        f.write(str(len(result))+"\n")
        for item in result:
            f.write(str(item[0])+" "+str(item[1])+" "+str(item[2])+"\n")
        f.close()