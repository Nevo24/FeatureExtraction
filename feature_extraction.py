import numpy as np
import pandas as pd

HC_FUN_AND_BLOCK_LIST = 0
HC_FUN_LIST = 1
HC_BLOCK_LIST = 2
TYPE_BLOCK_LIST = 3


def create_bl_hc_list(bl_type, bl_hc_list, bl_type_list):
    ans = []
    lists_len = bl_hc_list.__len__()
    for i in range(lists_len):
        if bl_type_list[i] == bl_type:
            ans.append(bl_hc_list[i])
    return ans


# table=np.genfromtxt('block_table.csv', dtype=None, delimiter=',')
data = pd.read_csv('block_table.csv')
features_table = pd.DataFrame(index=[0],
                              columns=['File Name', 'Hc_block_mean', 'Hc_block_median',
                                       'Hc_block_std', 'Hc_block_var', 'Cond_hc_block_mean', 'Cond_hc_block_std',
                                       'Cond_hc_block_median', 'Cond_hc_block_var', 'Goto_hc_block_mean',
                                       'Goto_hc_block_std', 'Goto_hc_block_median', 'Goto_hc_block_var', 'Hc_fun_mean',
                                       'Hc_fun_median', 'Hc_fun_std', 'Hc_fun_var',
                                       'Per_blocks_in_loop', 'Cond_block_num', 'Goto_block_num'])

hit_count_table = {}  # {file_name:  [(fun_hc, [bl_hc_0, bl_hc_1,...,bl_hc_n])], [fun_hc_0, fun_hc_1,...,fun_hc_n], [bl_hc_0, bl_hc_1,...,bl_hc_n], [bl_type_0, bl_type_1, bl_type_2,..., bl_type_n] }


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
        block_type = row['Block_type']
        if file_name != last_file_name:
            # finished collecting data for a file
            new_file = True
            last_file_name = file_name
            hit_count_table[file_name] = ([], [], [], [])
        if new_file or function_name != last_fun_name:
            # finished collecting data for a function
            last_fun_name = function_name
            func_hc = block_hc
            hit_count_table[file_name][HC_FUN_AND_BLOCK_LIST].append((func_hc, []))
            hit_count_table[file_name][HC_FUN_LIST].append(func_hc)
        hit_count_table[file_name][HC_FUN_AND_BLOCK_LIST][-1][1].append(block_hc)
        hit_count_table[file_name][HC_BLOCK_LIST].append(block_hc)
        hit_count_table[file_name][TYPE_BLOCK_LIST].append(block_type)
    print('Building the features...')
    global features_table
    for file_name, value in hit_count_table.items():
        num_of_blocks_in_file = value[HC_BLOCK_LIST].__len__()
        per_blocks_in_loop = 0

        hc_block_mean = np.mean(value[HC_BLOCK_LIST])
        hc_block_std = np.std(value[HC_BLOCK_LIST])
        hc_block_mid = np.median(value[HC_BLOCK_LIST])
        hc_block_var = np.var(value[HC_BLOCK_LIST])

        cond_bl_hc_list = create_bl_hc_list('cond', value[HC_BLOCK_LIST], value[TYPE_BLOCK_LIST])
        if cond_bl_hc_list.__len__() > 0:
            cond_hc_block_mean = np.mean(cond_bl_hc_list)
            cond_hc_block_std = np.std(cond_bl_hc_list)
            cond_hc_block_mid = np.median(cond_bl_hc_list)
            cond_hc_block_var = np.var(cond_bl_hc_list)
        else:
            cond_hc_block_mean = 0
            cond_hc_block_std = 0
            cond_hc_block_mid = 0
            cond_hc_block_var = 0

        goto_bl_hc_list = create_bl_hc_list('goto', value[HC_BLOCK_LIST], value[TYPE_BLOCK_LIST])
        if goto_bl_hc_list.__len__() > 0:
            goto_hc_block_mean = np.mean(goto_bl_hc_list)
            goto_hc_block_std = np.std(goto_bl_hc_list)
            goto_hc_block_mid = np.median(goto_bl_hc_list)
            goto_hc_block_var = np.var(goto_bl_hc_list)
        else:
            goto_hc_block_mean = 0
            goto_hc_block_std = 0
            goto_hc_block_mid = 0
            goto_hc_block_var = 0

        hc_fun_mean = np.mean(value[HC_FUN_LIST])
        hc_fun_std = np.std(value[HC_FUN_LIST])
        hc_fun_mid = np.median(value[HC_FUN_LIST])
        hc_fun_var = np.var(value[HC_FUN_LIST])

        for fun_hc, bl_hc_list in value[HC_FUN_AND_BLOCK_LIST]:
            num_blocks_in_a_loop = 0
            for current_bl_hc in bl_hc_list:
                if current_bl_hc > fun_hc:
                    num_blocks_in_a_loop += 1
            per_blocks_in_loop += num_blocks_in_a_loop
        per_blocks_in_loop = per_blocks_in_loop / num_of_blocks_in_file

        cond_block_num = 0
        goto_block_num = 0
        for bl_type in value[TYPE_BLOCK_LIST]:
            if bl_type == 'cond':
                cond_block_num += 1
            if bl_type == 'goto':
                goto_block_num += 1

        new_line = {'File Name': file_name,
                    'Hc_block_mean': hc_block_mean,
                    'Hc_block_std': hc_block_std,
                    'Hc_block_median': hc_block_mid,
                    'Hc_block_var': hc_block_var,

                    'Cond_hc_block_mean': cond_hc_block_mean,
                    'Cond_hc_block_std': cond_hc_block_std,
                    'Cond_hc_block_median': cond_hc_block_mid,
                    'Cond_hc_block_var': cond_hc_block_var,

                    'Goto_hc_block_mean': goto_hc_block_mean,
                    'Goto_hc_block_std': goto_hc_block_std,
                    'Goto_hc_block_median': goto_hc_block_mid,
                    'Goto_hc_block_var': goto_hc_block_var,

                    'Hc_fun_mean': hc_fun_mean,
                    'Hc_fun_std': hc_fun_std,
                    'Hc_fun_median': hc_fun_mid,
                    'Hc_fun_var': hc_fun_var,
                    'Per_blocks_in_loop': per_blocks_in_loop,
                    'Cond_block_num': cond_block_num,
                    'Goto_block_num': goto_block_num
                    }
        features_table = features_table.append(new_line, ignore_index=True)


create_block_feutures(data)
features_table = features_table.drop(features_table.index[0])
features_table.to_csv('features_table.csv', index=False)
