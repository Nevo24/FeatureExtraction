import os

import pandas as pd
from bs4 import BeautifulSoup

upper_table = pd.DataFrame(index=[0],
                           columns=['Class_path', 'Method_%', 'Method_fraction', 'Block_%', 'Block_fraction',
                                    'Branch_%',
                                    'Branch_fraction', 'Line_%', 'Line_fraction'])

method_table = pd.DataFrame(index=[0],
                            columns=['Class_path', 'Hit_count', 'Method_name%', 'Method_modifiers',
                                     'Method_signatures'])


def get_next_index(table, i):
    i = i + 1
    if table[i].findAll("span").__len__() == 0:
        return i + 1
    return i


def build_upper_table(soup, full_path):
    global upper_table
    table = soup.findAll("table", {"class": "percentGraph"})

    i = 0
    method_content = table[i].findAll("span")[0]
    method_percentage = method_content.contents[0].contents[0]
    method_fraction = method_content.contents[1][1:]
    i = get_next_index(table, i)

    block_content = table[i].findAll("span")[0]
    block_percentage = block_content.contents[0].contents[0]
    block_fraction = block_content.contents[1][1:]
    i = get_next_index(table, i)

    branch_content = table[i].findAll("span")[0]
    branch_percentage = branch_content.contents[0].contents[0]
    branch_fraction = branch_content.contents[1][1:]
    i = get_next_index(table, i)

    line_content = table[i].findAll("span")[0]
    line_percentage = line_content.contents[0].contents[0]
    line_fraction = line_content.contents[1][1:]

    new_line = {'Class_path': full_path,
                'Method_%': method_percentage,
                'Method_fraction': method_fraction,
                'Block_%': block_percentage,
                'Block_fraction': block_fraction,
                'Branch_%': branch_percentage,
                'Branch_fraction': branch_fraction,
                'Line_%': line_percentage,
                'Line_fraction': line_fraction}
    upper_table = upper_table.append(new_line, ignore_index=True)


def build_method_table(soup, full_path):
    global method_table
    table = soup.findAll("table", {"id": "mcoverage"})[0]
    table = table.findAll("tr")

    for i in range(1, table.__len__()):
        hit_count = table[i].contents[1].contents[0].contents[0]
        method_name = table[i].contents[3].contents[0].contents[0].contents[0]
        method_modifires = table[i].contents[5].contents[0].contents[0]
        method_signature = table[i].contents[7].contents[0].contents[0]
        new_line = {'Class_path': full_path,
                    'Hit_count': hit_count,
                    'Method_Name%': method_name,
                    'Method_modifiers': method_modifires,
                    'Method_signatures': method_signature}
        method_table = method_table.append(new_line, ignore_index=True)


def parse(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.html') and not file.__contains__("package-"):
                full_path = os.path.join(root, file)
                soup = BeautifulSoup(open(full_path), 'html.parser')
                full_path = full_path.replace(".\\jcov_hive\\report_html\\", "")
                full_path = full_path.replace(".html", "")
                print(full_path)
                build_upper_table(soup, full_path)
                build_method_table(soup, full_path)


parse(".\\jcov_hive\\report_html\\org")
method_table.to_csv('method_table.csv', index=False)
upper_table.to_csv('upper_table.csv', index=False)
