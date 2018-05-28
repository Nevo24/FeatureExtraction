import xml.etree.ElementTree as ET
import pandas as pd

upper_table = pd.DataFrame(index=[0],
                           columns=['Class_Name', 'Method_Name', 'Length'])

tree = ET.parse('.\\jcov_hive\\result.xml')
root = tree.getroot()

for package in root:
    if 'head' in package.tag:
        continue
    # print('tag: {}'.format(package.tag), '###attrib###: {}'.format(package.attrib))
    package_name = package.attrib['name']
    if 'package' in package.tag:
        for projectClass in package:
            # print('tag: {}'.format(projectClass.tag), '###attrib###: {}'.format(projectClass.attrib))
            class_name = projectClass.attrib['name']
            if 'class' in projectClass.tag:
                for method in projectClass:
                    # print('tag: {}'.format(method.tag), '###attrib###: {}'.format(method.attrib))
                    method_name = method.attrib['name']
                    print(method_name)
                    if 'meth' in method.tag:
                        # print('tag: {}'.format(method.tag), '###attrib###: {}'.format(method.attrib))
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
                        print(
                            'class_name: {}, method_name: {}, meth_len: {}, meth_access: {}, bl_start: {}, bl_end: {}, bl_id: {}, bl_count: {}, bl_opcode: {}'.format(
                                class_name, method_name, meth_len, meth_access, bl_start, bl_end, bl_id, bl_count,
                                bl_opcode))
                    else:
                        for bl in method:
                            if 'bl' in bl.tag:
                                bl_start = bl.attrib['s']
                                bl_end = bl.attrib['e']
                                if bl.__len__() > 0:
                                    content_exists = True
                                    bl_content = bl[0]
                                else:
                                    content_exists = False

                                # print('tag: {}'.format(bl.tag), '###attrib###: {}'.format(bl.attrib))
                                if content_exists and 'id' in bl_content.attrib:
                                    bl_id = bl_content.attrib['id']
                                else:
                                    # print('no id')
                                    bl_id = '-'
                                if content_exists and 'count' in bl_content.attrib:
                                    bl_count = bl_content.attrib['count']
                                else:
                                    bl_count = '-'
                                    # print('no count')
                                if content_exists and 'opcode' in bl_content.attrib:
                                    bl_opcode = bl_content.attrib['opcode']
                                else:
                                    bl_opcode = '-'
                                    # print('no opcode')
                                bl_type = bl_content.tag.split("}", 1)[1]
                                print(
                                    'class_name: {}, method_name: {}, meth_len: {}, meth_access: {}, bl_start: {}, bl_end: {}, bl_id: {}, bl_count: {}, bl_opcode: {}'.format(
                                        class_name, method_name, meth_len, meth_access, bl_start, bl_end, bl_id,
                                        bl_count,
                                        bl_opcode))
