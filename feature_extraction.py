import numpy as np
import pandas as pd

HC_FUN_AND_BLOCK_LIST = 0
HC_FUN_LIST = 1
HC_BLOCK_LIST = 2
TYPE_BLOCK_LIST = 3
LENGTH_BLOCK_LIST = 4
LENGTH_FUN_LIST = 5
FLAG_FUN_LIST = 6


def create_filtered_list(filt, source_list, factor_list):
    ans = []
    lists_len = source_list.__len__()
    for i in range(lists_len):
        if filt in factor_list[i]:
            ans.append(source_list[i])
    return ans


def create_inner_bl_hc_list(bl_hc_list, bl_type_list):
    ans = []
    lists_len = bl_hc_list.__len__()
    for i in range(lists_len):
        if bl_type_list[i] != 'methenter' and bl_type_list[i] != 'exit':
            ans.append(bl_hc_list[i])
    return ans


def create_block_features(file_name, data, perform_new_feature_extraction):
    table_name = 'features_table_' + file_name + '.csv'
    if not perform_new_feature_extraction:
        return pd.read_csv(table_name)

    features_table = pd.DataFrame(index=[0],
                                  columns=['File Name', 'Hc_block_mean', 'Hc_block_std', 'Hc_block_median',
                                           'Hc_block_var', 'Hc_block_min', 'Hc_block_max', 'Hc_block_unique',
                                           'Hc_block_per_zero', 'Weight_hc_block_mean', 'Weight_hc_block_std',
                                           'Weight_hc_block_median', 'Weight_hc_block_var', 'Weight_hc_block_min',
                                           'Weight_hc_block_max', 'Weight_hc_block_unique', 'Weight_hc_block_per_zero',
                                           'Normalized_hc_block_mean', 'Normalized_hc_block_std',
                                           'Normalized_hc_block_mid', 'Normalized_hc_block_var',
                                           'Normalized_hc_block_min', 'Normalized_hc_block_max',
                                           'Normalized_hc_block_unique', 'Normalized_hc_block_per_zero',
                                           'Cond_hc_block_mean', 'Cond_hc_block_std', 'Cond_hc_block_median',
                                           'Cond_hc_block_var', 'Cond_hc_block_min', 'Cond_hc_block_max',
                                           'Cond_hc_block_unique', 'Cond_hc_block_per_zero', 'Goto_hc_block_mean',
                                           'Goto_hc_block_std', 'Goto_hc_block_median', 'Goto_hc_block_var',
                                           'Goto_hc_block_min', 'Goto_hc_block_max', 'Goto_hc_block_unique',
                                           'Goto_hc_block_per_zero', 'Methenter_hc_block_mean',
                                           'Methenter_hc_block_std', 'Methenter_hc_block_median',
                                           'Methenter_hc_block_var', 'Methenter_hc_block_min', 'Methenter_hc_block_max',
                                           'Methenter_hc_block_unique', 'Methenter_hc_block_per_zero',
                                           'Exit_hc_block_mean', 'Exit_hc_block_std', 'Exit_hc_block_median',
                                           'Exit_hc_block_var', 'Exit_hc_block_min', 'Exit_hc_block_max',
                                           'Exit_hc_block_unique', 'Exit_hc_block_per_zero', 'Inner_hc_block_mean',
                                           'Inner_hc_block_std', 'Inner_hc_block_median', 'Inner_hc_block_var',
                                           'Inner_hc_block_min', 'Inner_hc_block_max', 'Inner_hc_block_unique',
                                           'Inner_hc_block_per_zero', 'Hc_fun_mean', 'Hc_fun_std', 'Hc_fun_median',
                                           'Hc_fun_var', 'Hc_fun_min', 'Hc_fun_max', 'Hc_fun_unique', 'Hc_fun_per_zero',
                                           'Public_hc_fun_mean', 'Public_hc_fun_std', 'Public_hc_fun_mid',
                                           'Public_hc_fun_var', 'Public_hc_fun_min', 'Public_hc_fun_max',
                                           'Public_hc_fun_unique', 'Public_hc_fun_per_zero', 'Private_hc_fun_mean',
                                           'Private_hc_fun_std', 'Private_hc_fun_mid', 'Private_hc_fun_var',
                                           'Private_hc_fun_min', 'Private_hc_fun_max', 'Private_hc_fun_unique',
                                           'Private_hc_fun_per_zero', 'Protected_hc_fun_mean', 'Protected_hc_fun_std',
                                           'Protected_hc_fun_mid', 'Protected_hc_fun_var', 'Protected_hc_fun_min',
                                           'Protected_hc_fun_max', 'Protected_hc_fun_unique',
                                           'Protected_hc_fun_per_zero', 'Fun_len_weight_hc_block_mean',
                                           'Fun_len_weight_hc_block_std', 'Fun_len_weight_hc_block_mid',
                                           'Fun_len_weight_hc_block_var', 'Fun_len_weight_hc_block_min',
                                           'Fun_len_weight_hc_block_max', 'Fun_len_weight_hc_block_unique',
                                           'Fun_len_weight_hc_block_per_zero', 'Num_of_bl_weight_hc_fun_mean',
                                           'Num_of_bl_weight_hc_fun_std', 'Num_of_bl_weight_hc_fun_mid',
                                           'Num_of_bl_weight_hc_fun_var', 'Num_of_bl_weight_hc_fun_min',
                                           'Num_of_bl_weight_hc_fun_max', 'Num_of_bl_weight_hc_fun_unique',
                                           'Num_of_bl_weight_hc_fun_per_zero', 'Per_blocks_in_loop',
                                           'Cond_per_blocks_in_loop', 'Goto_per_blocks_in_loop',
                                           'Methenter_per_blocks_in_loop', 'Exit_per_blocks_in_loop'])

    hit_count_table = {}  # {file_name:  [(fun_hc, [bl_hc_0, bl_hc_1,...,bl_hc_n])], [fun_hc_0, fun_hc_1,...,fun_hc_n], [bl_hc_0, bl_hc_1,...,bl_hc_n], [bl_type_0, bl_type_1, bl_type_2,..., bl_type_n], [bl_length_0, bl_length_1, bl_length_2,..., bl_length_n], [fun_length_0, fun_length_1, fun_length_2,..., fun_length_n],  [fun_flag_0, fun_flag_1, fun_flag_2,..., fun_flag_n]}
    last_file_name = None
    last_fun_name = None
    count = 0
    print('Collecting data...')
    for index, row in data.iterrows():
        new_file = False
        file_name = row['Class_path']
        function_name = row['Method_name']
        block_hc = int(row['Block_count'])
        block_type = row['Block_type']
        block_length = row['Block_end'] - row['Block_start'] + 1
        if file_name != last_file_name:
            # finished collecting data for a file
            new_file = True
            last_file_name = file_name
            hit_count_table[file_name] = ([], [], [], [], [], [], [])
            count = count + 1
        if new_file or function_name != last_fun_name:
            # finished collecting data for a function
            last_fun_name = function_name
            func_hc = block_hc
            hit_count_table[file_name][HC_FUN_AND_BLOCK_LIST].append((func_hc, []))
            hit_count_table[file_name][HC_FUN_LIST].append(func_hc)
            hit_count_table[file_name][LENGTH_FUN_LIST].append(row['Method_len'])
            hit_count_table[file_name][FLAG_FUN_LIST].append(row['Method_flags'])
        hit_count_table[file_name][HC_FUN_AND_BLOCK_LIST][-1][1].append(block_hc)
        hit_count_table[file_name][HC_BLOCK_LIST].append(block_hc)
        hit_count_table[file_name][TYPE_BLOCK_LIST].append(block_type)
        hit_count_table[file_name][LENGTH_BLOCK_LIST].append(block_length)
    print('Building the features...')
    for file_name, value in hit_count_table.items():
        num_of_blocks_in_file = value[HC_BLOCK_LIST].__len__()
        num_of_funcs_in_file = value[HC_FUN_LIST].__len__()
        per_blocks_in_loop = 0
        cond_per_blocks_in_loop = 0
        goto_per_blocks_in_loop = 0
        methenter_per_blocks_in_loop = 0
        exit_per_blocks_in_loop = 0

        hc_block_mean = np.mean(value[HC_BLOCK_LIST])
        hc_block_std = np.std(value[HC_BLOCK_LIST])
        hc_block_mid = np.median(value[HC_BLOCK_LIST])
        hc_block_var = np.var(value[HC_BLOCK_LIST])
        hc_block_min = min(value[HC_BLOCK_LIST])
        hc_block_max = max(value[HC_BLOCK_LIST])
        hc_block_unique = len(set(value[HC_BLOCK_LIST]))
        hc_block_per_zero = value[HC_BLOCK_LIST].count(0) / num_of_blocks_in_file

        max_bl_len = max(value[LENGTH_BLOCK_LIST])
        if max_bl_len != 0:
            weight_bl_hc_list = [a * b / max_bl_len for a, b in zip(value[HC_BLOCK_LIST], value[LENGTH_BLOCK_LIST])]
            weight_hc_block_mean = np.mean(weight_bl_hc_list)
            weight_hc_block_std = np.std(weight_bl_hc_list)
            weight_hc_block_mid = np.median(weight_bl_hc_list)
            weight_hc_block_var = np.var(weight_bl_hc_list)
            weight_hc_block_min = min(weight_bl_hc_list)
            weight_hc_block_max = max(weight_bl_hc_list)
            weight_hc_block_unique = len(set(weight_bl_hc_list))
            weight_hc_block_per_zero = weight_bl_hc_list.count(0) / num_of_blocks_in_file
        else:
            weight_hc_block_mean = 0
            weight_hc_block_std = 0
            weight_hc_block_mid = 0
            weight_hc_block_var = 0
            weight_hc_block_min = 0
            weight_hc_block_max = 0
            weight_hc_block_unique = 1
            weight_hc_block_per_zero = 1

        normalized_bl_hc_list = []
        for hc_fun_and_block in value[HC_FUN_AND_BLOCK_LIST]:
            first_bl_hc = hc_fun_and_block[1][0]
            if first_bl_hc != 0:
                normalized_bl_hc_list.extend([x / first_bl_hc for x in hc_fun_and_block[1]])
            else:
                normalized_bl_hc_list.extend(hc_fun_and_block[1])
        normalized_hc_block_mean = np.mean(normalized_bl_hc_list)
        normalized_hc_block_std = np.std(normalized_bl_hc_list)
        normalized_hc_block_mid = np.median(normalized_bl_hc_list)
        normalized_hc_block_var = np.var(normalized_bl_hc_list)
        normalized_hc_block_min = min(normalized_bl_hc_list)
        normalized_hc_block_max = max(normalized_bl_hc_list)
        normalized_hc_block_unique = len(set(normalized_bl_hc_list))
        normalized_hc_block_per_zero = normalized_bl_hc_list.count(0) / num_of_blocks_in_file

        cond_bl_hc_list = create_filtered_list('cond', value[HC_BLOCK_LIST], value[TYPE_BLOCK_LIST])
        if cond_bl_hc_list.__len__() > 0:
            cond_hc_block_mean = np.mean(cond_bl_hc_list)
            cond_hc_block_std = np.std(cond_bl_hc_list)
            cond_hc_block_mid = np.median(cond_bl_hc_list)
            cond_hc_block_var = np.var(cond_bl_hc_list)
            cond_hc_block_min = min(cond_bl_hc_list)
            cond_hc_block_max = max(cond_bl_hc_list)
            cond_hc_block_unique = len(set(cond_bl_hc_list))
            cond_hc_block_per_zero = cond_bl_hc_list.count(0) / num_of_blocks_in_file
        else:
            cond_hc_block_mean = 0
            cond_hc_block_std = 0
            cond_hc_block_mid = 0
            cond_hc_block_var = 0
            cond_hc_block_min = 0
            cond_hc_block_max = 0
            cond_hc_block_unique = 0
            cond_hc_block_per_zero = 0

        goto_bl_hc_list = create_filtered_list('goto', value[HC_BLOCK_LIST], value[TYPE_BLOCK_LIST])
        if goto_bl_hc_list.__len__() > 0:
            goto_hc_block_mean = np.mean(goto_bl_hc_list)
            goto_hc_block_std = np.std(goto_bl_hc_list)
            goto_hc_block_mid = np.median(goto_bl_hc_list)
            goto_hc_block_var = np.var(goto_bl_hc_list)
            goto_hc_block_min = min(goto_bl_hc_list)
            goto_hc_block_max = max(goto_bl_hc_list)
            goto_hc_block_unique = len(set(goto_bl_hc_list))
            goto_hc_block_per_zero = goto_bl_hc_list.count(0) / num_of_blocks_in_file
        else:
            goto_hc_block_mean = 0
            goto_hc_block_std = 0
            goto_hc_block_mid = 0
            goto_hc_block_var = 0
            goto_hc_block_min = 0
            goto_hc_block_max = 0
            goto_hc_block_unique = 0
            goto_hc_block_per_zero = 0

        methenter_bl_hc_list = create_filtered_list('methenter', value[HC_BLOCK_LIST], value[TYPE_BLOCK_LIST])
        if methenter_bl_hc_list.__len__() > 0:
            methenter_hc_block_mean = np.mean(methenter_bl_hc_list)
            methenter_hc_block_std = np.std(methenter_bl_hc_list)
            methenter_hc_block_mid = np.median(methenter_bl_hc_list)
            methenter_hc_block_var = np.var(methenter_bl_hc_list)
            methenter_hc_block_min = min(methenter_bl_hc_list)
            methenter_hc_block_max = max(methenter_bl_hc_list)
            methenter_hc_block_unique = len(set(methenter_bl_hc_list))
            methenter_hc_block_per_zero = methenter_bl_hc_list.count(0) / num_of_blocks_in_file
        else:
            methenter_hc_block_mean = 0
            methenter_hc_block_std = 0
            methenter_hc_block_mid = 0
            methenter_hc_block_var = 0
            methenter_hc_block_min = 0
            methenter_hc_block_max = 0
            methenter_hc_block_unique = 0
            methenter_hc_block_per_zero = 0

        exit_bl_hc_list = create_filtered_list('exit', value[HC_BLOCK_LIST], value[TYPE_BLOCK_LIST])
        if exit_bl_hc_list.__len__() > 0:
            exit_hc_block_mean = np.mean(exit_bl_hc_list)
            exit_hc_block_std = np.std(exit_bl_hc_list)
            exit_hc_block_mid = np.median(exit_bl_hc_list)
            exit_hc_block_var = np.var(exit_bl_hc_list)
            exit_hc_block_min = min(exit_bl_hc_list)
            exit_hc_block_max = max(exit_bl_hc_list)
            exit_hc_block_unique = len(set(exit_bl_hc_list))
            exit_hc_block_per_zero = exit_bl_hc_list.count(0) / num_of_blocks_in_file
        else:
            exit_hc_block_mean = 0
            exit_hc_block_std = 0
            exit_hc_block_mid = 0
            exit_hc_block_var = 0
            exit_hc_block_min = 0
            exit_hc_block_max = 0
            exit_hc_block_unique = 0
            exit_hc_block_per_zero = 0

        inner_bl_hc_list = create_inner_bl_hc_list(value[HC_BLOCK_LIST], value[TYPE_BLOCK_LIST])
        if inner_bl_hc_list.__len__() > 0:
            inner_hc_block_mean = np.mean(inner_bl_hc_list)
            inner_hc_block_std = np.std(inner_bl_hc_list)
            inner_hc_block_mid = np.median(inner_bl_hc_list)
            inner_hc_block_var = np.var(inner_bl_hc_list)
            inner_hc_block_min = min(inner_bl_hc_list)
            inner_hc_block_max = max(inner_bl_hc_list)
            inner_hc_block_unique = len(set(inner_bl_hc_list))
            inner_hc_block_per_zero = inner_bl_hc_list.count(0) / num_of_blocks_in_file
        else:
            inner_hc_block_mean = 0
            inner_hc_block_std = 0
            inner_hc_block_mid = 0
            inner_hc_block_var = 0
            inner_hc_block_min = 0
            inner_hc_block_max = 0
            inner_hc_block_unique = 0
            inner_hc_block_per_zero = 0

        type_block_list_index = 0
        cond_block_num = 0
        goto_block_num = 0
        methenter_block_num = 0
        exit_block_num = 0
        for fun_hc, bl_hc_list in value[HC_FUN_AND_BLOCK_LIST]:
            num_blocks_in_a_loop = 0
            cond_num_blocks_in_a_loop = 0
            goto_num_blocks_in_a_loop = 0
            methenter_num_blocks_in_a_loop = 0
            exit_num_blocks_in_a_loop = 0
            for current_bl_hc in bl_hc_list:
                if current_bl_hc > fun_hc:
                    num_blocks_in_a_loop += 1
                    if value[TYPE_BLOCK_LIST][type_block_list_index] == 'cond':
                        cond_block_num += 1
                        cond_num_blocks_in_a_loop += 1
                    if value[TYPE_BLOCK_LIST][type_block_list_index] == 'goto':
                        goto_block_num += 1
                        goto_num_blocks_in_a_loop += 1
                    if value[TYPE_BLOCK_LIST][type_block_list_index] == 'methenter':
                        methenter_block_num += 1
                        methenter_num_blocks_in_a_loop += 1
                    if value[TYPE_BLOCK_LIST][type_block_list_index] == 'exit':
                        exit_block_num += 1
                        exit_num_blocks_in_a_loop += 1
                type_block_list_index += 1
            per_blocks_in_loop += num_blocks_in_a_loop
            cond_per_blocks_in_loop += cond_num_blocks_in_a_loop
            goto_per_blocks_in_loop += goto_num_blocks_in_a_loop
            methenter_per_blocks_in_loop += methenter_num_blocks_in_a_loop
            exit_per_blocks_in_loop += exit_num_blocks_in_a_loop
        per_blocks_in_loop = per_blocks_in_loop / num_of_blocks_in_file
        cond_per_blocks_in_loop = cond_per_blocks_in_loop / num_of_blocks_in_file
        goto_per_blocks_in_loop = goto_per_blocks_in_loop / num_of_blocks_in_file
        methenter_per_blocks_in_loop = methenter_per_blocks_in_loop / num_of_blocks_in_file
        exit_per_blocks_in_loop = exit_per_blocks_in_loop / num_of_blocks_in_file

        # ******** Function features: ********

        hc_fun_mean = np.mean(value[HC_FUN_LIST])
        hc_fun_std = np.std(value[HC_FUN_LIST])
        hc_fun_mid = np.median(value[HC_FUN_LIST])
        hc_fun_var = np.var(value[HC_FUN_LIST])
        hc_fun_min = min(value[HC_FUN_LIST])
        hc_fun_max = max(value[HC_FUN_LIST])
        hc_fun_unique = len(set(value[HC_FUN_LIST]))
        hc_fun_per_zero = value[HC_FUN_LIST].count(0) / num_of_funcs_in_file

        public_bl_hc_list = create_filtered_list('public', value[HC_FUN_LIST], value[FLAG_FUN_LIST])
        if public_bl_hc_list.__len__() > 0:
            public_hc_fun_mean = np.mean(public_bl_hc_list)
            public_hc_fun_std = np.std(public_bl_hc_list)
            public_hc_fun_mid = np.median(public_bl_hc_list)
            public_hc_fun_var = np.var(public_bl_hc_list)
            public_hc_fun_min = min(public_bl_hc_list)
            public_hc_fun_max = max(public_bl_hc_list)
            public_hc_fun_unique = len(set(public_bl_hc_list))
            public_hc_fun_per_zero = public_bl_hc_list.count(0) / num_of_funcs_in_file
        else:
            public_hc_fun_mean = 0
            public_hc_fun_std = 0
            public_hc_fun_mid = 0
            public_hc_fun_var = 0
            public_hc_fun_min = 0
            public_hc_fun_max = 0
            public_hc_fun_unique = 0
            public_hc_fun_per_zero = 0

        private_bl_hc_list = create_filtered_list('private', value[HC_FUN_LIST], value[FLAG_FUN_LIST])
        if private_bl_hc_list.__len__() > 0:
            private_hc_fun_mean = np.mean(private_bl_hc_list)
            private_hc_fun_std = np.std(private_bl_hc_list)
            private_hc_fun_mid = np.median(private_bl_hc_list)
            private_hc_fun_var = np.var(private_bl_hc_list)
            private_hc_fun_min = min(private_bl_hc_list)
            private_hc_fun_max = max(private_bl_hc_list)
            private_hc_fun_unique = len(set(private_bl_hc_list))
            private_hc_fun_per_zero = private_bl_hc_list.count(0) / num_of_funcs_in_file
        else:
            private_hc_fun_mean = 0
            private_hc_fun_std = 0
            private_hc_fun_mid = 0
            private_hc_fun_var = 0
            private_hc_fun_min = 0
            private_hc_fun_max = 0
            private_hc_fun_unique = 0
            private_hc_fun_per_zero = 0

        protected_bl_hc_list = create_filtered_list('protected', value[HC_FUN_LIST], value[FLAG_FUN_LIST])
        if protected_bl_hc_list.__len__() > 0:
            protected_hc_fun_mean = np.mean(protected_bl_hc_list)
            protected_hc_fun_std = np.std(protected_bl_hc_list)
            protected_hc_fun_mid = np.median(protected_bl_hc_list)
            protected_hc_fun_var = np.var(protected_bl_hc_list)
            protected_hc_fun_min = min(protected_bl_hc_list)
            protected_hc_fun_max = max(protected_bl_hc_list)
            protected_hc_fun_unique = len(set(protected_bl_hc_list))
            protected_hc_fun_per_zero = protected_bl_hc_list.count(0) / num_of_funcs_in_file
        else:
            protected_hc_fun_mean = 0
            protected_hc_fun_std = 0
            protected_hc_fun_mid = 0
            protected_hc_fun_var = 0
            protected_hc_fun_min = 0
            protected_hc_fun_max = 0
            protected_hc_fun_unique = 0
            protected_hc_fun_per_zero = 0

        max_fun_len = max(value[LENGTH_FUN_LIST])
        if max_fun_len != 0:
            fun_len_weight_bl_hc_list = [a * b / hc_fun_max for a, b in zip(value[HC_FUN_LIST], value[LENGTH_FUN_LIST])]
            fun_len_weight_hc_fun_mean = np.mean(fun_len_weight_bl_hc_list)
            fun_len_weight_hc_fun_std = np.std(fun_len_weight_bl_hc_list)
            fun_len_weight_hc_fun_mid = np.median(fun_len_weight_bl_hc_list)
            fun_len_weight_hc_fun_var = np.var(fun_len_weight_bl_hc_list)
            fun_len_weight_hc_fun_min = min(fun_len_weight_bl_hc_list)
            fun_len_weight_hc_fun_max = max(fun_len_weight_bl_hc_list)
            fun_len_weight_hc_fun_unique = len(set(fun_len_weight_bl_hc_list))
            fun_len_weight_hc_fun_per_zero = fun_len_weight_bl_hc_list.count(0) / num_of_funcs_in_file
        else:
            fun_len_weight_hc_fun_mean = 0
            fun_len_weight_hc_fun_std = 0
            fun_len_weight_hc_fun_mid = 0
            fun_len_weight_hc_fun_var = 0
            fun_len_weight_hc_fun_min = 0
            fun_len_weight_hc_fun_max = 0
            fun_len_weight_hc_fun_unique = 1
            fun_len_weight_hc_fun_per_zero = 1

        fun_num_of_bl_list = []
        for hc_fun_and_block in value[HC_FUN_AND_BLOCK_LIST]:
            fun_num_of_bl_list.extend(hc_fun_and_block[1].__len__())
        max_num_of_bl = max(fun_num_of_bl_list)

        if max_num_of_bl != 0:
            num_of_bl_weight_bl_hc_list = [a * b / max_num_of_bl for a, b in
                                           zip(value[HC_FUN_LIST], fun_num_of_bl_list)]
            num_of_bl_weight_hc_fun_mean = np.mean(num_of_bl_weight_bl_hc_list)
            num_of_bl_weight_hc_fun_std = np.std(num_of_bl_weight_bl_hc_list)
            num_of_bl_weight_hc_fun_mid = np.median(num_of_bl_weight_bl_hc_list)
            num_of_bl_weight_hc_fun_var = np.var(num_of_bl_weight_bl_hc_list)
            num_of_bl_weight_hc_fun_min = min(num_of_bl_weight_bl_hc_list)
            num_of_bl_weight_hc_fun_max = max(num_of_bl_weight_bl_hc_list)
            num_of_bl_weight_hc_fun_unique = len(set(num_of_bl_weight_bl_hc_list))
            num_of_bl_weight_hc_fun_per_zero = num_of_bl_weight_bl_hc_list.count(0) / num_of_funcs_in_file
        else:
            num_of_bl_weight_hc_fun_mean = 0
            num_of_bl_weight_hc_fun_std = 0
            num_of_bl_weight_hc_fun_mid = 0
            num_of_bl_weight_hc_fun_var = 0
            num_of_bl_weight_hc_fun_min = 0
            num_of_bl_weight_hc_fun_max = 0
            num_of_bl_weight_hc_fun_unique = 1
            num_of_bl_weight_hc_fun_per_zero = 1

        new_line = {'File Name': file_name,
                    'Hc_block_mean': hc_block_mean,
                    'Hc_block_std': hc_block_std,
                    'Hc_block_median': hc_block_mid,
                    'Hc_block_var': hc_block_var,
                    'Hc_block_min': hc_block_min,
                    'Hc_block_max': hc_block_max,
                    'Hc_block_unique': hc_block_unique,
                    'Hc_block_per_zero': hc_block_per_zero,

                    'Weight_hc_block_mean': weight_hc_block_mean,
                    'Weight_hc_block_std': weight_hc_block_std,
                    'Weight_hc_block_median': weight_hc_block_mid,
                    'Weight_hc_block_var': weight_hc_block_var,
                    'Weight_hc_block_min': weight_hc_block_min,
                    'Weight_hc_block_max': weight_hc_block_max,
                    'Weight_hc_block_unique': weight_hc_block_unique,
                    'Weight_hc_block_per_zero': weight_hc_block_per_zero,

                    'Normalized_hc_block_mean': normalized_hc_block_mean,
                    'Normalized_hc_block_std': normalized_hc_block_std,
                    'Normalized_hc_block_mid': normalized_hc_block_mid,
                    'Normalized_hc_block_var': normalized_hc_block_var,
                    'Normalized_hc_block_min': normalized_hc_block_min,
                    'Normalized_hc_block_max': normalized_hc_block_max,
                    'Normalized_hc_block_unique': normalized_hc_block_unique,
                    'Normalized_hc_block_per_zero': normalized_hc_block_per_zero,

                    'Cond_hc_block_mean': cond_hc_block_mean,
                    'Cond_hc_block_std': cond_hc_block_std,
                    'Cond_hc_block_median': cond_hc_block_mid,
                    'Cond_hc_block_var': cond_hc_block_var,
                    'Cond_hc_block_min': cond_hc_block_min,
                    'Cond_hc_block_max': cond_hc_block_max,
                    'Cond_hc_block_unique': cond_hc_block_unique,
                    'Cond_hc_block_per_zero': cond_hc_block_per_zero,

                    'Goto_hc_block_mean': goto_hc_block_mean,
                    'Goto_hc_block_std': goto_hc_block_std,
                    'Goto_hc_block_median': goto_hc_block_mid,
                    'Goto_hc_block_var': goto_hc_block_var,
                    'Goto_hc_block_min': goto_hc_block_min,
                    'Goto_hc_block_max': goto_hc_block_max,
                    'Goto_hc_block_unique': goto_hc_block_unique,
                    'Goto_hc_block_per_zero': goto_hc_block_per_zero,

                    'Methenter_hc_block_mean': methenter_hc_block_mean,
                    'Methenter_hc_block_std': methenter_hc_block_std,
                    'Methenter_hc_block_median': methenter_hc_block_mid,
                    'Methenter_hc_block_var': methenter_hc_block_var,
                    'Methenter_hc_block_min': methenter_hc_block_min,
                    'Methenter_hc_block_max': methenter_hc_block_max,
                    'Methenter_hc_block_unique': methenter_hc_block_unique,
                    'Methenter_hc_block_per_zero': methenter_hc_block_per_zero,

                    'Exit_hc_block_mean': exit_hc_block_mean,
                    'Exit_hc_block_std': exit_hc_block_std,
                    'Exit_hc_block_median': exit_hc_block_mid,
                    'Exit_hc_block_var': exit_hc_block_var,
                    'Exit_hc_block_min': exit_hc_block_min,
                    'Exit_hc_block_max': exit_hc_block_max,
                    'Exit_hc_block_unique': exit_hc_block_unique,
                    'Exit_hc_block_per_zero': exit_hc_block_per_zero,

                    'Inner_hc_block_mean': inner_hc_block_mean,
                    'Inner_hc_block_std': inner_hc_block_std,
                    'Inner_hc_block_median': inner_hc_block_mid,
                    'Inner_hc_block_var': inner_hc_block_var,
                    'Inner_hc_block_min': inner_hc_block_min,
                    'Inner_hc_block_max': inner_hc_block_max,
                    'Inner_hc_block_unique': inner_hc_block_unique,
                    'Inner_hc_block_per_zero': inner_hc_block_per_zero,

                    'Hc_fun_mean': hc_fun_mean,
                    'Hc_fun_std': hc_fun_std,
                    'Hc_fun_median': hc_fun_mid,
                    'Hc_fun_var': hc_fun_var,
                    'Hc_fun_min': hc_fun_min,
                    'Hc_fun_max': hc_fun_max,
                    'Hc_fun_unique': hc_fun_unique,
                    'Hc_fun_per_zero': hc_fun_per_zero,

                    'Public_hc_fun_mean': public_hc_fun_mean,
                    'Public_hc_fun_std': public_hc_fun_std,
                    'Public_hc_fun_mid': public_hc_fun_mid,
                    'Public_hc_fun_var': public_hc_fun_var,
                    'Public_hc_fun_min': public_hc_fun_min,
                    'Public_hc_fun_max': public_hc_fun_max,
                    'Public_hc_fun_unique': public_hc_fun_unique,
                    'Public_hc_fun_per_zero': public_hc_fun_per_zero,

                    'Private_hc_fun_mean': private_hc_fun_mean,
                    'Private_hc_fun_std': private_hc_fun_std,
                    'Private_hc_fun_mid': private_hc_fun_mid,
                    'Private_hc_fun_var': private_hc_fun_var,
                    'Private_hc_fun_min': private_hc_fun_min,
                    'Private_hc_fun_max': private_hc_fun_max,
                    'Private_hc_fun_unique': private_hc_fun_unique,
                    'Private_hc_fun_per_zero': private_hc_fun_per_zero,

                    'Protected_hc_fun_mean': protected_hc_fun_mean,
                    'Protected_hc_fun_std': protected_hc_fun_std,
                    'Protected_hc_fun_mid': protected_hc_fun_mid,
                    'Protected_hc_fun_var': protected_hc_fun_var,
                    'Protected_hc_fun_min': protected_hc_fun_min,
                    'Protected_hc_fun_max': protected_hc_fun_max,
                    'Protected_hc_fun_unique': protected_hc_fun_unique,
                    'Protected_hc_fun_per_zero': protected_hc_fun_per_zero,

                    'Fun_len_weight_hc_fun_mean': fun_len_weight_hc_fun_mean,
                    'Fun_len_weight_hc_fun_std': fun_len_weight_hc_fun_std,
                    'Fun_len_weight_hc_fun_mid': fun_len_weight_hc_fun_mid,
                    'Fun_len_weight_hc_fun_var': fun_len_weight_hc_fun_var,
                    'Fun_len_weight_hc_fun_min': fun_len_weight_hc_fun_min,
                    'Fun_len_weight_hc_fun_max': fun_len_weight_hc_fun_max,
                    'Fun_len_weight_hc_fun_unique': fun_len_weight_hc_fun_unique,
                    'Fun_len_weight_hc_fun_per_zero': fun_len_weight_hc_fun_per_zero,

                    'Num_of_bl_weight_hc_fun_mean': num_of_bl_weight_hc_fun_mean,
                    'Num_of_bl_weight_hc_fun_std': num_of_bl_weight_hc_fun_std,
                    'Num_of_bl_weight_hc_fun_mid': num_of_bl_weight_hc_fun_mid,
                    'Num_of_bl_weight_hc_fun_var': num_of_bl_weight_hc_fun_var,
                    'Num_of_bl_weight_hc_fun_min': num_of_bl_weight_hc_fun_min,
                    'Num_of_bl_weight_hc_fun_max': num_of_bl_weight_hc_fun_max,
                    'Num_of_bl_weight_hc_fun_unique': num_of_bl_weight_hc_fun_unique,
                    'Num_of_bl_weight_hc_fun_per_zero': num_of_bl_weight_hc_fun_per_zero,

                    'Per_blocks_in_loop': per_blocks_in_loop,
                    'Cond_per_blocks_in_loop': cond_per_blocks_in_loop,
                    'Goto_per_blocks_in_loop': goto_per_blocks_in_loop,
                    'Methenter_per_blocks_in_loop': methenter_per_blocks_in_loop,
                    'Exit_per_blocks_in_loop': exit_per_blocks_in_loop,
                    }
        features_table = features_table.append(new_line, ignore_index=True)
    features_table = features_table.drop(features_table.index[0])
    features_table.to_csv(table_name, index=False)
    return features_table
