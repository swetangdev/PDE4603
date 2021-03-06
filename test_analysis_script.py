# test analysis script that runs for multiple tuples of [gamma, epsilon]
# to store analysis of each tuple 

'''import csv

# open the file in the write mode
test_file = open('test_csv_file', 'w')

# create CSV writer
csv_writer = csv.writer(test_file)

#write row in csv file
csv_writer.writerow(row) '''

import numpy as np
import csv
from datetime import datetime

from numpy.lib.function_base import average
    
obstacle_coord = [23.0, 43.0, 37.0, 57.0]
if [23.0, 43.0] in obstacle_coord:
    print('aaa')   
exit()
# csv header
fieldnames = ['name', 'area', 'country_code2', 'country_code3']

# csv data
rows = np.array([
    ['Albania', 28748, 'AL', 'ALB'],
    ['Algeria', 2381741, 'DZ', 'DZA'],
    ['American Samoa', 199, 'AS', 'ASM']
])

newaa =  [[0.9, 197, 101], [0.9, 101, 101], [0.9, 101, 101], '', [0.8, 101, 101], [0.8, 101, 96], [0.8, 96, 96], '']
newbb = np.array(list(filter(None,(newaa))))

print(newaa)
converted = newbb.transpose()
average_a = (np.mean(converted, axis=1)).tolist()
average_a[0] = 'Avg'
print(average_a)
exit()

date = str(datetime.now().strftime("%d_%m_%Y-%I_%M_%p"))
with open(str('countries_'+date+'.csv'), 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(fieldnames)
    writer.writerows(rows)

exit()

gamma_epsilon = [[0.9, 0.9], [0.4, 0.6], [0.4, 0.65], [0.5, 0.6], [0.5, 0.5]]
for iter in range(len(gamma_epsilon)):
    print(gamma_epsilon[iter][0])
exit()

gammaa = 0.9
epsilona = 0.9
gamma_epsilon = [[gammaa, epsilona]]
for iter in range(3):
    gammaa -= 0.1
    epsilona -= 0.1
    gamma_epsilon += [[round(gammaa,1), round(epsilona,1)]]

print(gamma_epsilon)
exit()

import csv

    

# csv header
fieldnames = ['name', 'area', 'country_code2', 'country_code3']

# csv data
rows = [
    {'name': 'Albania',
    'area': 28748,
    'country_code2': 'AL',
    'country_code3': 'ALB'},
    {'name': 'Algeria',
    'area': 2381741,
    'country_code2': 'DZ',
    'country_code3': 'DZA'},
    {'name': 'American Samoa',
    'area': 199,
    'country_code2': 'AS',
    'country_code3': 'ASM'}
]

with open('countries.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)