import pandas as pd
import numpy as np

#table=np.genfromtxt('block_table.csv', dtype=None, delimiter=',')
data = pd.read_csv('block_table.csv')
features_table = pd.DataFrame(index=[0],
                              columns=['File Name', 'hc_fun_mean', 'hc_fun_weighted_avg', 'hc_fun_median',
                                       'hc_fun_std', 'hc_fun_var'])



def create_block_feutures(data):

    table = {}
    print('Data collection')
    for index, row in data.iterrows():
        file_name = row['Class_path']
        function_name = row['Method_name']
        hc = int(row['Block_count'])
        if (file_name, function_name) not in table:
            table[(file_name, function_name)] = [1, hc, [hc]]
        else:
            num_of_blocks = int(table.get((file_name, function_name))[0])+1
            hc_sum = int(table.get((file_name, function_name))[1])+hc
            hc_list = list(table.get((file_name, function_name))[2])
            hc_list.append(hc)
            table[(file_name, function_name)] = [num_of_blocks, hc_sum,hc_list]
    print('Building the features')
    for key, value in table.items():
        hc_mean = np.mean(value[2])
        hc_std = np.std(value[2])
        hc_mid = np.median(value[2])
        hc_avg = np.average(value[2])
        hc_var = np.var(value[2])
        file_name = key[0]
        new_line = {'File Name': file_name,
                'hc_fun_mean': hc_mean,
                'hc_fun_weighted_avg':hc_avg,
                'hc_fun_median':hc_mid,
                'hc_fun_std':hc_std,
                'hc_fun_var':hc_var }
        features_table = features_table.append(new_line, ignore_index=True)

    print('keren')





create_block_feutures(data)
print('keren')