from itertools import chain
import numpy as np
from scipy.spatial import distance

def find_best_building(lista_edifici):
    max = 0
    index = 0
    for i in range(len(lista_edifici)):
        if max < lista_edifici[i][3]:
            max = lista_edifici[i][3]
            index = i
    return index


def find_best_antenna(lista_antenne):
    max = 0
    index = 0
    for i in range(len(lista_antenne)):
        if max < lista_antenne[i][2]:
            max = lista_antenne[i][2]
            index = i
    return index

file1 =  "data_scenarios_a_example.in"
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

input = [file1,file2,file3,file4,file5,file6]
output = [ofile1,ofile2,ofile3,ofile4,ofile5,ofile6]
for filezz in range(len(input)):
    print("start {}".format(filezz))
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

        # algo
        result = []
        while (len(lista_antenne) > 0 and len(lista_edifici) > 0):

            index_max = find_best_building(lista_edifici)
            edificio_max = lista_edifici[index_max]

            index_best_antenna = find_best_antenna(lista_antenne)
            antenna_max  = lista_antenne[index_best_antenna]

            result.append([lista_antenne[index_best_antenna][0] , edificio_max[0], edificio_max[1] ])

            new_lista_edifici = list()

            for i in range(len(lista_edifici)):
                edificio  = lista_edifici[i]
                #antenna_max[1] è latency
                if distance.cityblock([edificio[0],edificio[1]], [edificio_max[0],edificio_max[1]] ) > antenna_max[1]:
                    new_lista_edifici.append(edificio)

            lista_edifici = new_lista_edifici
            lista_antenne.pop(index_best_antenna)

        f = open(output[filezz], 'w')
        f.write(str(len(result))+"\n")
        for item in result:
            f.write(str(item[0])+" "+str(item[1])+" "+str(item[2])+"\n")
        f.close()


