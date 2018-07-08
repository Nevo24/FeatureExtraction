import argparse

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, accuracy_score, recall_score, roc_auc_score

import feature_extraction
import parse_results
import xml_parse

train_files = ['1_7_jcov.xml', '1_7_rc2_jcov.xml', '1_8_jcov.xml']
test_file = '1_8_rc2_jcov.xml'
dic_versions = {'1_7_jcov.xml': '1.7', '1_7_rc2_jcov.xml': '1.7-rc2',
                '1_8_jcov.xml': '1.8', '1_8_rc2_jcov.xml': '1.8-rc2'}


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


parser = argparse.ArgumentParser()
parser.add_argument('--parsing', type=str, default="yes")
parser.add_argument('--feature_extraction', type=str, default="yes")
parser.add_argument('--classified_data', type=str, default="yes")
args = parser.parse_args()

# When not equal to zero -  mock modules will be generated
PARSING = str2bool(args.parsing)
FEATURE_EXTRACTION = str2bool(args.feature_extraction)
CLASSIFIED_DATA = str2bool(args.classified_data)


def prepar_training_data(train_files, bugged_paths, dic_versions):
    if not CLASSIFIED_DATA:
        return pd.read_csv('data_train.csv')
    data_train = []
    for file_name in train_files:
        # call xml_parse
        parsing = xml_parse.parsing_xml(file_name, PARSING)
        # call feature_extraction and get the table
        features = feature_extraction.create_block_features(file_name, parsing, FEATURE_EXTRACTION)
        features['class'] = 0
        for path in bugged_paths[dic_versions[file_name]]:
            features.loc[features['File Name'] == path, 'class'] = 1
        a = features['class'].value_counts()
        data_train.append(features)

    result = pd.concat(data_train)
    result.to_csv('data_train.csv', index=False)  # 2845 samples
    return result


def prepar_testing_data(test_file, bugged_paths, dic_versions):
    if not CLASSIFIED_DATA:
        return pd.read_csv('data_test.csv')
    # call xml_parse
    parsing = xml_parse.parsing_xml(test_file, PARSING)
    # call feature_extraction and get the table
    features = feature_extraction.create_block_features(test_file, parsing, FEATURE_EXTRACTION)
    features['class'] = 0
    for path in bugged_paths[dic_versions[test_file]]:
        features.loc[features['File Name'] == path, 'class'] = 1
    a = features['class'].value_counts()

    features.to_csv('data_test.csv', index=False)  # 573 samples
    return features


def build_model(x_train, y_train, x_test, y_test):
    model = RandomForestClassifier()
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    # metrics
    precision = precision_score(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_pred)

    # print the results
    print("Results:\n")
    print("Accuracy Score: " + str(acc) + "\n")
    print("roc_auc_score: " + str(auc) + "\n")
    print("Precision: " + str(precision) + "\n")
    print("Recall: " + str(recall) + "\n")


bugged_paths = parse_results.get_bugged_files()
train_data = prepar_training_data(train_files, bugged_paths, dic_versions)
test_data = prepar_testing_data(test_file, bugged_paths, dic_versions)

train_data.drop("File Name", axis=1, inplace=True)
test_data.drop("File Name", axis=1, inplace=True)

x_train = train_data.iloc[:, :-1]
y_train = train_data.iloc[:, -1]
x_test = test_data.iloc[:, :-1]
y_test = test_data.iloc[:, -1]

build_model(x_train, y_train, x_test, y_test)
