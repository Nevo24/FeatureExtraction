import xml.etree.ElementTree as ET

import pandas as pd


def add_to_table(class_path, method_name, meth_len, is_constructor, method_flags, bl_id, bl_start, bl_end, bl_count,
                 bl_opcode, bl_type, cond_true_start, cond_true_end, cond_true_count, cond_false_start, cond_false_end,
                 cond_false_count, goto_start, goto_count, can_fall_through, is_cond, is_goto, table):
    if not is_cond:
        cond_true_start = '-'
        cond_true_end = '-'
        cond_true_count = '-'
        cond_false_start = '-'
        cond_false_end = '-'
        cond_false_count = '-'
    if not is_goto:
        goto_start = '-'
        goto_count = '-'
    new_line = {'Class_path': class_path,
                'Method_name': method_name,
                'Method_len': meth_len,
                'Is_constructor': is_constructor,
                'Method_flags': method_flags,
                'Block_id': bl_id,
                'Block_start': bl_start,
                'Block_end': bl_end,
                'Block_count': bl_count,
                'Block_opcode': bl_opcode,
                'Block_type': bl_type,
                'Cond_true_start': cond_true_start,
                'Cond_true_end': cond_true_end,
                'Cond_true_count': cond_true_count,
                'Cond_false_start': cond_false_start,
                'Cond_false_end': cond_false_end,
                'Cond_false_count': cond_false_count,
                'Goto_start': goto_start,
                'Goto_count': goto_count,
                'Line_in_file': '-',
                'Can_fall_through': can_fall_through
                }
    table = table.append(new_line, ignore_index=True)
    return table


def parsing_xml(version_name, perform_new_parse=True):
    print('Parsing ' + version_name)
    table_name = 'temporaryFiles/parsing_table_' + version_name + '.csv'
    if not perform_new_parse:
        return pd.read_csv(table_name)

    CLASS_PATH = 0
    METHOD_NAME = 1
    METHOD_LEN = 2
    METHOD_FLAGS = 3
    BLOCK_ID = 4
    BLOCK_START = 5
    BLOCK_END = 6
    BLOCK_COUNT = 7
    BLOCK_OPCODE = 8
    BLOCK_TYPE = 9
    COND_TRUE_START = 10
    COND_TRUE_END = 11
    COND_TRUE_COUNT = 12
    COND_FALSE_START = 13
    COND_FALSE_END = 14
    COND_FALSE_COUNT = 15
    GOTO_START = 16
    GOTO_COUNT = 17
    LINE_IN_FILE = 18

    table = pd.DataFrame(index=[0],
                         columns=['Class_path', 'Method_name', 'Method_len', 'Is_constructor', 'Method_flags',
                                  'Block_id', 'Block_start', 'Block_end', 'Block_count', 'Block_opcode', 'Block_type',
                                  'Cond_true_start', 'Cond_true_end', 'Cond_true_count', 'Cond_false_start',
                                  'Cond_false_end', 'Cond_false_count', 'Goto_start', 'Goto_count', 'Line_in_file',
                                  'Can_fall_through'])

    block_types = {'exit', 'methenter', 'br'}

    tree = ET.parse('.\\jcov_hive\\{}.xml'.format(version_name))
    root = tree.getroot()

    for package in root:
        if 'head' in package.tag:
            continue
        class_path = package.attrib['name'] + '.'
        class_path = class_path.replace(".", "/")
        if 'package' in package.tag:
            for projectClass in package:
                current_class_path = class_path + projectClass.attrib['source']
                print(current_class_path)
                if 'class' in projectClass.tag:
                    for method in projectClass:
                        method_name = method.attrib['name']
                        if 'meth' in method.tag:
                            if 'length' in method.attrib:
                                meth_len = method.attrib['length']
                            else:
                                meth_len = '-'
                            if 'cons' in method.attrib:
                                is_constructor = 'yes'
                            else:
                                is_constructor = 'no'
                            method_flags = method.attrib['flags']
                        if method.__len__() != 0:
                            cond_true_start = '-'
                            cond_true_end = '-'
                            cond_true_id = '-'
                            cond_true_count = '-'
                            cond_false_start = '-'
                            cond_false_end = '-'
                            cond_false_id = '-'
                            cond_false_count = '-'
                            goto_start = '-'
                            goto_id = '-'
                            goto_count = '-'
                            num_of_blocks = 0
                            for method_content in method:
                                if 'bl' in method_content.tag:
                                    bl_start = method_content.attrib['s']
                                    bl_end = method_content.attrib['e']
                                    if method_content.__len__() > 0:
                                        content_exists = True
                                        bl_content = method_content[0]
                                    else:
                                        content_exists = False
                                    if content_exists and 'id' in bl_content.attrib:
                                        bl_id = bl_content.attrib['id']
                                    else:
                                        if bl_start == cond_true_start:
                                            bl_id = cond_true_id
                                        elif bl_start == cond_false_start:
                                            bl_id = cond_false_id
                                        elif bl_start == goto_start:
                                            bl_id = goto_id
                                    if content_exists and 'count' in bl_content.attrib:
                                        bl_count = bl_content.attrib['count']
                                    else:
                                        if bl_start == cond_true_start:
                                            bl_count = cond_true_count
                                        elif bl_start == cond_false_start:
                                            bl_count = cond_false_count
                                        elif bl_start == goto_start:
                                            bl_count = goto_count
                                    if content_exists and 'opcode' in bl_content.attrib:
                                        bl_opcode = bl_content.attrib['opcode']
                                    else:
                                        bl_opcode = '-'
                                    can_fall_through = 'no'
                                    goto_start = '-'
                                    goto_count = '-'
                                    is_cond = False
                                    is_goto = False
                                    bl_type = '-'
                                    for block_content in method_content:
                                        bl_type = block_content.tag.split("}", 1)[1]
                                        if bl_type in block_types:
                                            if bl_type == 'br':
                                                bl_type = 'cond'
                                                is_cond = True
                                                cond_true_start = block_content[0].attrib['s']
                                                cond_true_end = block_content[0].attrib['e']
                                                cond_true_id = block_content[0].attrib['id']
                                                cond_true_count = block_content[0].attrib['count']
                                                cond_false_start = block_content[1].attrib['s']
                                                cond_false_end = block_content[1].attrib['e']
                                                cond_false_id = block_content[1].attrib['id']
                                                cond_false_count = block_content[1].attrib['count']
                                        else:
                                            if bl_type == 'goto':
                                                is_goto = True
                                                goto_start = block_content[0].attrib['s']
                                                goto_id = block_content[0].attrib['id']
                                                goto_count = block_content[0].attrib['count']
                                            else:
                                                if bl_type == 'fall':
                                                    can_fall_through = 'yes'
                                                bl_type = '-'
                                    num_of_blocks += 1
                                    table = add_to_table(current_class_path, method_name, meth_len, is_constructor,
                                                         method_flags, bl_id, bl_start, bl_end, bl_count, bl_opcode,
                                                         bl_type, cond_true_start, cond_true_end, cond_true_count,
                                                         cond_false_start, cond_false_end, cond_false_count, goto_start,
                                                         goto_count, can_fall_through, is_cond, is_goto, table)
                                if 'lt' in method_content.tag:
                                    lines = method_content.text.split(';')
                                    del lines[-1]
                                    lines_index = 0
                                    try:
                                        for last_modified_row in range(-num_of_blocks, 0):
                                            while True:
                                                if table.values[last_modified_row][BLOCK_START] == \
                                                        lines[lines_index].split('=')[0]:
                                                    table.values[last_modified_row][LINE_IN_FILE] = \
                                                        lines[lines_index].split('=')[1]
                                                    break
                                                elif table.values[last_modified_row][BLOCK_START] > \
                                                        lines[lines_index].split('=')[0]:
                                                    table.values[last_modified_row][LINE_IN_FILE] = \
                                                        lines[lines_index - 1].split('=')[1]
                                                    break
                                                lines_index += 1
                                    except Exception:
                                        pass

    table = table.drop(table.index[0])
    table.to_csv(table_name, index=False)
    return table
