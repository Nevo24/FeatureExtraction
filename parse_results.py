import pandas as pd


def get_bugged_files():
    data = pd.read_csv('tables/tika_bugged_files.csv')
    files_per_version = {}

    for index, row in data.iterrows():
        version_name = row[0]
        files_paths = row[1]
        split_pahts = files_paths.split(';')
        real_path=[]
        for path in split_pahts:
            if path =='tika-parsers/pom.xml' or path=='.gitignore' or path=='NOTICE.txt' or path=='CHANGES.txt' or \
                    path=='tika-parent/pom.xml' or path=='tika-bundle/pom.xml' or path=='tika-example/pom.xml' or path=='tika-server/pom.xml':
                continue
            if 'resources' in path:
                if '.java' in path:
                    real_path.append(path.split('resources/')[1])
            else:
                if '.java' in path:
                    real_path.append(path.split('java/')[1])
        files_per_version[version_name] = real_path
    return files_per_version


