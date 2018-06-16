import pandas as pd
import numpy as np

HC_FUN_AND_BLOCK_LIST = 0
HC_FUN_LIST = 1
HC_BLOCK_LIST = 2


# table=np.genfromtxt('block_table.csv', dtype=None, delimiter=',')
data = pd.read_csv('block_table.csv')
features_table = pd.DataFrame(index=[0],
                              columns=['File Name', 'hc_block_mean', 'hc_block_weighted_avg', 'hc_block_median',
                                       'hc_block_std', 'hc_block_var', 'hc_block_percentage', 'hc_fun_mean',
                                       'hc_fun_weighted_avg',
                                       'hc_fun_median', 'hc_fun_std', 'hc_fun_var', 'hc_fun_percentage'])

hit_count_table = {}  # {file_name:  [(fun_hc, [bl_hc_0, bl_hc_1,...,bl_hc_n])], [fun_hc_0, fun_hc_1,...,fun_hc_n], [bl_hc_0, bl_hc_1,...,bl_hc_n] }


def create_block_feutures(data):
    global hit_count_table
    last_file_name = None
    last_fun_name = None
    print('Collecting data...')
    for index, row in data.iterrows():
        file_name = row['Class_path']
        function_name = row['Method_name']
        block_hc = int(row['Block_count'])
        if file_name != last_fun_name:
            # finished collecting data for a file
            last_file_name = file_name
            hit_count_table[file_name] = ([], [], [])
        if function_name != last_file_name:
            # finished collecting data for a function
            last_fun_name = function_name
            func_hc = block_hc
            hit_count_table[file_name][0].append((func_hc, []))
            hit_count_table[file_name][1].append(func_hc)
        hit_count_table[file_name][0][-1][1].append(block_hc)
        hit_count_table[file_name][2].append(block_hc)
    print('Building the features')
    global features_table
    for key, value in hit_count_table.items():
        hc_block_mean = np.mean(value[HC_BLOCK_LIST])
        hc_block_std = np.std(value[HC_BLOCK_LIST])
        hc_block_mid = np.median(value[HC_BLOCK_LIST])
        hc_block_avg = np.average(value[HC_BLOCK_LIST])
        hc_block_var = np.var(value[HC_BLOCK_LIST])
        hc_fun_mean = np.mean(value[HC_FUN_LIST])
        hc_fun_std = np.std(value[HC_FUN_LIST])
        hc_fun_mid = np.median(value[HC_FUN_LIST])
        hc_fun_avg = np.average(value[HC_FUN_LIST])
        hc_fun_var = np.var(value[HC_FUN_LIST])
        num_hc_fun = None
        num_hc_block = None

        if not all(x < value[HC_FUN_AND_BLOCK_LIST][0] for x in value[HC_FUN_AND_BLOCK_LIST][1]):
            # There s a loop:

            if value[HC_BLOCK_LIST][i] != 0:
                num_hc_fun += 1
        for i in range(0, value[HC_FUN_LIST].__len__()):
            if value[HC_FUN_LIST][i] != 0:
                num_hc_block += 1
        per_hc_block = num_hc_block / value[HC_BLOCK_LIST].__len__()
        per_hc_fun = num_hc_fun / value[HC_FUN_LIST].__len__()

        per_fun_with_loop = num_hc_fun / value[HC_FUN_LIST].__len__()

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


create_block_feutures(data)
