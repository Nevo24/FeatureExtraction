import xml.etree.ElementTree as ET
import pandas as pd

upper_table = pd.DataFrame(index=[0],
                           columns=['Class_Name', 'Method_Name', 'Length'])

tree = ET.parse('.\\jcov_hive\\result.xml')
root = tree.getroot()

for package in root:
    # print('tag: {}'.format(package.tag), '###attrib###: {}'.format(package.attrib))
    if 'package' in package.tag:
        for projectClass in package:
            # print('tag: {}'.format(projectClass.tag), '###attrib###: {}'.format(projectClass.attrib))
            if 'class' in projectClass.tag:
                for method in projectClass:
                    # print('tag: {}'.format(method.tag), '###attrib###: {}'.format(method.attrib))
                    if 'meth' in method.tag:
                        try:
                            method.attrib['length']
                        except Exception:
                            print('tag: {}'.format(method.tag), '###attrib###: {}'.format(method.attrib))
