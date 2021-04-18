import csv

result = {'0': 0, '1': 0}

count = 0
with open('/Grasping_Franka/output/result/First_round/obj1_bare.csv') as file:
    f_csv = csv.reader(file)
    for row in f_csv:
        if count != 0:
            result[row[1]] += 1
        count += 1


# previous adding
i = 0
j = 0
success_rate = float((result['1'] + i) / (result['0'] + result['1'] + j))

print(result['1'])
print(result['0'] + result['1'])
print(success_rate)
