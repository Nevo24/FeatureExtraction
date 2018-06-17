import pandas as pd
import numpy as np

HC_FUN_AND_BLOCK_LIST = 0
HC_FUN_LIST = 1
HC_BLOCK_LIST = 2

# table=np.genfromtxt('block_table.csv', dtype=None, delimiter=',')
data = pd.read_csv('block_table.csv')
features_table = pd.DataFrame(index=[0],
                              columns=['File Name', 'Hc_block_mean', 'Hc_block_weighted_avg', 'Hc_block_median',
                                       'Hc_block_std', 'Hc_block_var', 'Hc_block_percentage', 'Hc_fun_mean',
                                       'Hc_fun_weighted_avg',
                                       'Hc_fun_median', 'Hc_fun_std', 'Hc_fun_var', 'Hc_fun_percentage',
                                       'Per_blocks_in_loop'])

hit_count_table = {}  # {file_name:  [(fun_hc, [bl_hc_0, bl_hc_1,...,bl_hc_n])], [fun_hc_0, fun_hc_1,...,fun_hc_n], [bl_hc_0, bl_hc_1,...,bl_hc_n] }


def create_block_feutures(data):
    global hit_count_table
    last_file_name = None
    last_fun_name = None
    print('Collecting data...')
    for index, row in data.iterrows():
        new_file = False
        file_name = row['Class_path']
        function_name = row['Method_name']
        block_hc = int(row['Block_count'])
        if file_name != last_file_name:
            # finished collecting data for a file
            new_file = True
            last_file_name = file_name
            hit_count_table[file_name] = ([], [], [])
        if new_file or function_name != last_fun_name:
            # finished collecting data for a function
            last_fun_name = function_name
            func_hc = block_hc
            hit_count_table[file_name][HC_FUN_AND_BLOCK_LIST].append((func_hc, []))
            hit_count_table[file_name][HC_FUN_LIST].append(func_hc)
        hit_count_table[file_name][HC_FUN_AND_BLOCK_LIST][-1][1].append(block_hc)
        hit_count_table[file_name][HC_BLOCK_LIST].append(block_hc)
    print('Building the features...')
    global features_table
    for file_name, value in hit_count_table.items():
        num_of_func_in_file = value[HC_FUN_LIST].__len__()
        num_of_blocks_in_file = value[HC_BLOCK_LIST].__len__()
        num_hc_fun = sum(value[HC_FUN_LIST])
        num_hc_block = sum(value[HC_BLOCK_LIST])
        per_blocks_in_loop = 0

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

        for fun_hc, bl_hc_list in value[HC_FUN_AND_BLOCK_LIST]:
            num_blocks_in_a_loop = 0
            for current_bl_hc in bl_hc_list:
                if current_bl_hc > fun_hc:
                    num_blocks_in_a_loop += 1
            per_blocks_in_loop += num_blocks_in_a_loop
        per_blocks_in_loop = per_blocks_in_loop / num_of_blocks_in_file

        per_hc_block = num_hc_block / num_of_blocks_in_file
        per_hc_fun = num_hc_fun / num_of_func_in_file

        new_line = {'File Name': file_name,
                    'Hc_block_mean': hc_block_mean,
                    'Hc_block_std': hc_block_std,
                    'Hc_block_median': hc_block_mid,
                    'Hc_block_weighted_avg': hc_block_avg,
                    'Hc_block_var': hc_block_var,
                    'Hc_fun_mean': hc_fun_mean,
                    'Hc_fun_std': hc_fun_std,
                    'Hc_fun_median': hc_fun_mid,
                    'Hc_fun_weighted_avg': hc_fun_avg,
                    'Hc_fun_var': hc_fun_var,
                    'Hc_block_percentage': per_hc_block,
                    'Hc_fun_percentage': per_hc_fun,
                    'Per_blocks_in_loop': per_blocks_in_loop
                    }
        features_table = features_table.append(new_line, ignore_index=True)


create_block_feutures(data)
features_table = features_table.drop(features_table.index[0])
features_table.to_csv('features_table.csv', index=False)
