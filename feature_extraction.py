import pandas as pd
import numpy as np

# table=np.genfromtxt('block_table.csv', dtype=None, delimiter=',')
data = pd.read_csv('block_table.csv')
features_table = pd.DataFrame(index=[0],
                              columns=['File Name', 'hc_block_mean', 'hc_block_weighted_avg', 'hc_block_median',
                                       'hc_block_std', 'hc_block_var', 'hc_block_percentage', 'hc_fun_mean',
                                       'hc_fun_weighted_avg',
                                       'hc_fun_median', 'hc_fun_std', 'hc_fun_var', 'hc_fun_percentage'])


def create_block_feutures(data):
    table = {}
    last_fun_name = None
    new_fun = False
    print('Data collection')
    for index, row in data.iterrows():
        file_name = row['Class_path']
        function_name = row['Method_name']
        if function_name != last_fun_name:
            new_fun = True
            last_fun_name = function_name
        hc = int(row['Block_count'])
        if file_name not in table:
            table[file_name] = [[hc], [hc]]
        else:
            hc_fun_list = list(table.get(file_name)[1])
            if new_fun:
                hc_fun_list.append(hc)
            hc_block_list = list(table.get(file_name)[0])
            hc_block_list.append(hc)
            table[file_name] = [hc_block_list, hc_fun_list]
            new_fun = False
    print('Building the features')
    global features_table
    for key, value in table.items():
        hc_block_mean = np.mean(value[0])
        hc_block_std = np.std(value[0])
        hc_block_mid = np.median(value[0])
        hc_block_avg = np.average(value[0])
        hc_block_var = np.var(value[0])
        hc_fun_mean = np.mean(value[1])
        hc_fun_std = np.std(value[1])
        hc_fun_mid = np.median(value[1])
        hc_fun_avg = np.average(value[1])
        hc_fun_var = np.var(value[1])
        num_hc_fun = None
        num_hc_block = None
        for i in range(0, value[0].__len__()):
            if value[0][i] != 0:
                num_hc_fun += 1
        for i in range(0, value[1].__len__()):
            if value[1][i] != 0:
                num_hc_block += 1
        per_hc_block = num_hc_block / value[0].__len__()
        per_hc_fun = num_hc_fun / value[1].__len__()

        new_line = {'File Name': key,
                    'hc_block_mean': hc_block_mean,
                    'hc_block_weighted_avg': hc_block_avg,
                    'hc_block_median': hc_block_mid,
                    'hc_block_std': hc_block_std,
                    'hc_block_var': hc_block_var,
                    'hc_block_percentage': per_hc_block,
                    'hc_fun_mean': hc_fun_mean,
                    'hc_fun_weighted_avg': hc_fun_avg,
                    'hc_fun_median': hc_fun_mid,
                    'hc_fun_std': hc_fun_std,
                    'hc_fun_var': hc_fun_var,
                    'hc_fun_percentage': per_hc_fun
                    }
        features_table = features_table.append(new_line, ignore_index=True)

    print('keren')


create_block_feutures(data)
print('keren')
