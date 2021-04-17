import csv

result = {'0': 0, '1': 0}

count = 0
with open('/home/doyle/Me336/ME336-2021Spring/Grasping_Franka/output/result/C4_cutter7.csv') as file:
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
