import xml.etree.ElementTree as ET
import pandas as pd

table = pd.DataFrame(index=[0],
                     columns=['Class_path', 'Method_name', 'Method_len', 'Method_access', 'Block_id', 'Block_start',
                              'Block_end', 'Block_count', 'Block_opcode', 'Block_type', 'Cond_true_start',
                              'Cond_true_end', 'Cond_true_count', 'Cond_false_start', 'Cond_false_end',
                              'Cond_false_count', 'Goto_start', 'Goto_count', 'Block_line', 'Can_fall_through'])

block_types = {'exit', 'methenter', 'br'}


def add_to_table(class_path, method_name, meth_len, meth_access, bl_id='-', bl_start='-', bl_end='-', bl_count='-',
                 bl_opcode='-',
                 bl_type='-',
                 cond_true_start='-', cond_true_end='-', cond_true_count='-', cond_false_start='-', cond_false_end='-',
                 cond_false_count='-', goto_start='-', goto_count='-', can_fall_through='no'):
    global table
    new_line = {'Class_path': class_path,
                'Method_name': method_name,
                'Method_len': meth_len,
                'Method_access': meth_access,
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
                'Block_line': '-',
                'Can_fall_through': can_fall_through
                }
    table = table.append(new_line, ignore_index=True)


tree = ET.parse('.\\jcov_hive\\result.xml')
root = tree.getroot()

for package in root:
    if 'head' in package.tag:
        continue
    class_path = package.attrib['name'] + '.'
    class_path = class_path.replace(".", "\\")
    if 'package' in package.tag:
        first_iter = True
        for projectClass in package:
            if first_iter:
                class_path += projectClass.attrib['name']
                first_iter = False
            print(class_path)
            if 'class' in projectClass.tag:
                for method in projectClass:
                    method_name = method.attrib['name']
                    if 'meth' in method.tag:
                        if 'length' in method.attrib:
                            meth_len = method.attrib['length']
                        else:
                            meth_len = '-'
                        meth_access = method.attrib['access']
                    if method.__len__() == 0:
                        bl_start = '-'
                        bl_end = '-'
                        bl_id = '-'
                        bl_count = '-'
                        bl_opcode = '-'
                        add_to_table(class_path, method_name, meth_len, meth_access)
                    else:
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
                                    bl_id = '-'
                                if content_exists and 'count' in bl_content.attrib:
                                    bl_count = bl_content.attrib['count']
                                else:
                                    bl_count = '-'
                                if content_exists and 'opcode' in bl_content.attrib:
                                    bl_opcode = bl_content.attrib['opcode']
                                else:
                                    bl_opcode = '-'
                                can_fall_through = 'no'
                                for block_content in method_content:
                                    cond_true_start = '-'
                                    cond_true_end = '-'
                                    cond_true_count = '-'
                                    cond_false_start = '-'
                                    cond_false_end = '-'
                                    cond_false_count = '-'
                                    goto_start = '-'
                                    goto_count = '-'
                                    bl_type = block_content.tag.split("}", 1)[1]
                                    if bl_type in block_types:
                                        if bl_type == 'br':
                                            bl_type = 'cond'
                                            cond_true_start = block_content[0].attrib['s']
                                            cond_true_end = block_content[0].attrib['e']
                                            cond_true_count = block_content[0].attrib['count']
                                            cond_false_start = block_content[1].attrib['s']
                                            cond_false_end = block_content[1].attrib['e']
                                            cond_false_count = block_content[1].attrib['count']
                                    else:
                                        if bl_type == 'fall':
                                            can_fall_through = 'yes'
                                        if bl_type == 'goto':
                                            goto_start = block_content[0].attrib['s']
                                            goto_count = block_content[0].attrib['count']
                                        bl_type = '-'
                                add_to_table(class_path, method_name, meth_len, meth_access, bl_id, bl_start, bl_end,
                                             bl_count,
                                             bl_opcode, bl_type, cond_true_start, cond_true_end, cond_true_count,
                                             cond_false_start, cond_false_end, cond_false_count,
                                             goto_start, goto_count, can_fall_through)
                            if 'lt' in method_content.tag:
                                lines = method_content.text.split(';')
                                del lines[-1]
                                last_modified_row = -1
                                for line in reversed(lines):
                                    table.values[last_modified_row][-2] = line.split('=')[1]
                                    last_modified_row -= 1

table.to_csv('block_table.csv', index=False)
