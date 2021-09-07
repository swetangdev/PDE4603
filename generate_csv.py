import csv
from datetime import datetime

class generate_csv:
    def __init__(self, algorithm_name, environment_name, epsilon_array, short_rows, long_rows, time_rows, head_qTable_fields, q_table_rows):
        date = datetime.now().strftime("%Y_%m_%d-%I_%M%p")
        filename = algorithm_name+"_analysis_"+ environment_name +"_"+date+".csv"
        epsilon_array.insert(0, 'X-X-X-X')

        with open(filename, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            writer.writerow(['', '' , algorithm_name+' Learning Algorithm', '', environment_name])
            writer.writerow('')

            # print shortest path table
            writer.writerow(['','Shortest Path'])
            writer.writerow(epsilon_array)
            writer.writerows(short_rows)
            writer.writerow('')

            # print longest path table 
            writer.writerow(['','Longest Path'])
            writer.writerow(epsilon_array)
            writer.writerows(long_rows)
            writer.writerow('')

            # print 'time' table
            writer.writerow(['','Total time'])
            writer.writerow(epsilon_array)
            writer.writerows(time_rows)
            writer.writerow('')

            # print Q table
            writer.writerow(['','Q Table'])
            writer.writerow(head_qTable_fields)
            writer.writerows(q_table_rows)