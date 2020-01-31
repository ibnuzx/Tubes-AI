from random import randint
import copy, csv, os, random, numpy

def make_list(file):
    rule = []
    for l in range(len(file[0])):
        cek = []
        for k in file:
            if(k[l] not in cek):
                cek.append(k[l])
        rule.append(cek)
        
    return rule

def convert_to_binary(file, rule):

    # ubah kata ke angka
    penampung2 = []
    for k in range(len(file[0])):
        penampung1 = []
        for l in range(len(file[0][k])):
            penampung1.append(rule[l].index(file[0][k][l]))
        penampung2.append(penampung1)
        
    #ubah angka ke binner
    angka = penampung2.copy()
    binary = []
    for m in range(len(angka)):
        biner = []
        for h in range(len(angka[m])):
            for i in range(len(rule[h])):
                if len(rule[h]) != 2:
                    if i == angka[m][h]:
                        biner.append(1)
                    else:
                        biner.append(0)
                else:
                    if len(biner) < 15:
                        biner.append(angka[m][h])
                    else:
                        biner[14] = angka[m][h]
        binary.append(biner)
    return binary

def convert_ke_binary(file):
    # untuk mengubah data latih ke binary

    # mengubah rule menjadi angka
    binary = []
    for l in range(len(file[0])):
        penampung = []
        cek = []
        for k in file:
            if(k[l] not in cek):
                cek.append(k[l])
            penampung.append(cek.index(k[l]))
        binary.append(penampung)

    # mengubah angka menjadi biner
    for h in range(len(binary)):
        panjang = max(binary[h])+1
        for i in range(len(binary[h])):
            state = []
            if panjang != 2:
                for j in range(panjang):
                    if j != (binary[h][i]):
                        state.append(0)
                    else:
                        state.append(1)
                binary[h][i] = state

    # menggabungkan biner menjadi 1 baris
    finalbinary = []
    for o in range(len(file)):
        penampung = []
        for n in range(len(binary)):
            if numpy.array(binary[n]).ndim > 1:
                for m in range(len(binary[n][o])):
                    penampung.append(binary[n][o][m])
            else:
                penampung.append(binary[n][o])
        finalbinary.append(penampung)

    return finalbinary

def mencocokan_binary(binary1, binary2):
    hasil = False
    for i in range(len(binary1)):
        if(binary1[i] != binary2[i]):
            return False
        else:
            hasil = True

    return hasil


def seleksi_parent(populasi):
    # untuk melakukan parent selection
    # dengn mencari 2 kromosom terbaik

    parent = []
    fitness = []
    for i in range(len(populasi)):
        fitness.append(populasi[i]['fitness'])
    # get parent
    for j in range(2):
        for k in range(len(populasi)):
            if populasi[k]['fitness'] == min(fitness):
                parent.append(populasi[k])
                break
        fitness.pop(fitness.index(min(fitness)))
        
    return parent

def hitung_fitness(binary, data_latih):
    # Fungsi untuk menghitung fitness
    # dengan rumus 

    data_benar = 0
    for j in range(len(binary)):
        for i in range(len(data_latih)):
            if(mencocokan_binary(binary[j], data_latih[i])):
                data_benar += 1
    return data_benar/len(data_latih)

def crosover(parent1, parent2):

    child1 = []
    print(min(len(parent1), len(parent2)))
    for i in range(min(len(parent1), len(parent2))):
        child1.extend(parent1[i])
    print("1", child1)

    print(max(len(parent1), len(parent2)))
    child2 = []        
    for j in range(max(len(parent1), len(parent2))):
        # print(i)
        child2.extend(parent2[j])
    print("2", child2)

    point = random.sample(range(1, len(child1)-1), 2)
    print(point)

    # pointawl1 = (min(point[1], point[0]))
    # pointakh1 = (max(point[1], point[0]))
    # potongan1 = []
    # for i in range(pointakh1)[pointawl1:]:
    #     potongan1.append(parent1[i])
    #     del child1[pointawl1]

    # point = random.sample(range(1, len(parent2)-1), 2)
    # pointawl2 = (min(point[1], point[0]))
    # pointakh2 = (max(point[1], point[0]))
    # potongan2 = []
    # for i in range(pointakh2)[pointawl2:]:
    #     potongan2.append(parent2[i])
    #     del child2[pointawl2]

    child2[pointawl2:pointawl2] = potongan1
    child1[pointawl1:pointawl1] = potongan2

    offspring = [child1, child2]

    return offspring

def crosovers(parent1, parent2):

    child1 = []
    child2 = []
    for i in range(len(parent1)):
        child1.extend(parent1[i])
    for i in range(len(parent2)):
        child2.extend(parent2[i])

    point = random.sample(range(1, len(parent1)-1), 2)
    pointawl1 = (min(point[1], point[0]))
    pointakh1 = (max(point[1], point[0]))
    potongan1 = []
    for i in range(pointakh1)[pointawl1:]:
        potongan1.append(parent1[i])
        del child1[pointawl1]

    point = random.sample(range(1, len(parent2)-1), 2)
    pointawl2 = (min(point[1], point[0]))
    pointakh2 = (max(point[1], point[0]))
    potongan2 = []
    for i in range(pointakh2)[pointawl2:]:
        potongan2.append(parent2[i])
        del child2[pointawl2]

    child2[pointawl2:pointawl2] = potongan1
    child1[pointawl1:pointawl1] = potongan2

    offspring = [child1, child2]

    return offspring

def buat_kromosom(binary, data_latih):
    # fungsi untuk membuat kromosom
    # kromosom berisi binary, fitness

    kromosom = {'binary' : [], 'fitness' : 0, }
    kromosom['binary'] = binary
    kromosom['fitness'] = round(hitung_fitness(binary, data_latih), 3)
    return kromosom

def buat_populasi_awal(ukuran, file):
    # untuk membuat populasi dari kumpulan kromosom

    #random kromosom pertama
    daftar = make_list(file)
    data_latih = convert_ke_binary(file)

    populasi = []
    for i in range(ukuran):

        binary = []
        for i in range(5):
            penampung1 = []
            for i in range(randint(1, 5)):
                penampung2 = []
                for i in range(len(daftar)):
                    penampung2.append(daftar[i][(randint(0, (len(daftar[i])-1)))])
                penampung1.append(penampung2)
            binary.append(penampung1)
        binary = convert_to_binary(binary, daftar)

        populasi.append(buat_kromosom(binary, data_latih))

    return populasi


def decode_binary(binary):
    # fungsi untuk melakukan decode biner
    # dengan batasan -3 <= x1 <= 3  dan  -2 <= x2 <= 2

    rmax = [3,2]
    rmin = [-3,-2]
    jmlh_x = 2
    x = []

    bits = copy.deepcopy(binary)
    for i in range(jmlh_x):
        En = 0
        En2 = 0
        for j in range(0, 3):
            En = 2**(-j-1) + En #
            En2 = ( bits[0] * 2**(-j-1) ) + En2
            bits.pop(0)
        x.append(round( rmin[i] + ((rmax[i]-rmin[i])/En) * En2, 3));
    return x

def mutation(offspring):
    # untuk melakukan mutation
    # menggunakan bit-level mutation

    lajuMutasi = 0.5
    mutant = []
    for j in range(2):
        for i in range(8):
            rand = randint(0, 100)/100
            if lajuMutasi > rand:
                if offspring[j][i] == 0:
                    offspring[j][i] = 1
                else:
                    offspring[j][i] = 0
        mutant.append(buat_kromosom(offspring[j]))
    return mutant

def seleksi_survivor(populasi, mutant):
    # melakukan survivor selection
    # menggunakan fitness-based selection

    for j in range(len(mutant)):    
        populasikecil = max(populasi, key = lambda i:i['fitness'])
        populasi.pop(populasi.index(populasikecil))
        populasi.append(mutant[j])
    return populasi

def display_kromosom(populasi):
    # display kromosom

    if len(populasi) > 1:
        popul = sorted(populasi, key = lambda i:i['fitness'])
    else:
        popul = populasi

    for j in range(len(popul)):
        print('Chromosom', j+1, '=', end=' ')
        if j+1 < 10:
            print(end=' ')
        print(popul[j]['binary'], end=' ')
        print('| Fitness =', popul[j]['fitness'], end=' ')
        for i in range(5 - len(str(popul[j]['fitness']))):
            print(end=' ')
        print('| x1 =', popul[j]['x'][0], end=' ')
        for i in range(6 - len(str(popul[j]['x'][0]))):
            print(end=' ')
        print('| x2 =', popul[j]['x'][1], end=' ')
        for i in range(6 - len(str(popul[j]['x'][1]))):
            print(end=' ')
        print('| f(x1, x2) =', popul[j]['goals'], end=' ')
                  
        print()

def limit(populasi, generasi):
    # unuk menentukan berhentinya algoritma ini
    # untuk mencari Chromosom terbaik
    # berhenti ketika chromosom terbaik telah muncul sebanyak 70% atau mencapai generasi maksimal yaitu 1000

    stop = 70/100*len(populasi)
    terkecil = min(populasi, key = lambda i:i['fitness'])
    hasil = {'isloop' : True, 'terkecil' : [terkecil]}
    for k in populasi:
        if len([i for i in populasi if i['fitness'] == terkecil['fitness']]) >= stop or generasi == 1000:
            hasil['isloop'] = False
            return hasil
        else:
            return hasil
            
def main():
    # main program
    with open('Z:\Kuli ah\Semester 5\Kecerdasan Buatan\TUGAS\Tugas 2\Jawaban\data_latih_opsi_1.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter = ',')
        file = []
        for row in readCSV:
            file.append(row)

    populasi = buat_populasi_awal(3, file)

    # for g in populasi:
    #     print('binary', g['binary'], end= ' ')
    #     print('fitness', g['fitness'])

    # parent = seleksi_parent(populasi)

    print(crosover(populasi[0]['binary'], populasi[1]['binary']))    

    # daftar = make_list(file)
    # data_latih = convert_ke_binary(file)

    # #random kromosom pertama
    # binary = []
    # for i in range(5):
    #     penampung1 = []
    #     for i in range(randint(1, 5)):
    #         penampung2 = []
    #         for i in range(len(daftar)):
    #             penampung2.append(daftar[i][(randint(0, (len(daftar[i])-1)))])
    #         penampung1.append(penampung2)
    #     binary.append(penampung1)
    
    # binary = convert_to_binary(binary, daftar)

    # print(binary)
    # kromosom = buat_kromosom(binary, data_latih)
    # print("keromosom", kromosom['binary'])
    # print("fitness", kromosom['fitness'])

    # for i in range(len(binary)):
    #     print(len(binary[i]))
    #     print(binary[i])

    # print(hitung_fitness(parent[0], data_latih))

    # populasi = copy.deepcopy(buat_populasi(10))
    # islooping = True
    # generasi = 0
    # while islooping:
    #     generasi = generasi+1
    #     print()
    #     print("Generasi",generasi)
    #     print("-----------------------------------------------------------------------------------------------------------")

    #     display_kromosom(populasi)

    #     islooping = limit(populasi, generasi)['isloop']
    #     terbaik = limit(populasi, generasi)['terkecil']

    #     parent = seleksi_parent(populasi)
    #     offspring = crosover(parent)
    #     mutant = mutation(offspring)
    #     populasi = seleksi_survivor(populasi, mutant)

    # print()
    # print('Solusi terbaik adalah ')
    # print('Generasi ke ', generasi)
    # display_kromosom(terbaik)

main()
# print()
# input('Tekan ENTER untuk keluar')