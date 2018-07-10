import argparse
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, accuracy_score, recall_score, roc_auc_score
import feature_extraction
import parse_results
import xml_parse

train_files = ['1_7_jcov.xml', '1_7_rc2_jcov.xml', '1_8_jcov.xml']
test_files = ['1_8_rc2_jcov.xml']
dic_versions = {'1_7_jcov.xml': '1.7', '1_7_rc2_jcov.xml': '1.7-rc2',
                '1_8_jcov.xml': '1.8', '1_8_rc2_jcov.xml': '1.8-rc2'}


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


parser = argparse.ArgumentParser()
parser.add_argument('--parsing', type=str, default="yes")
parser.add_argument('--feature_extraction', type=str, default="yes")
parser.add_argument('--processed_data', type=str, default="yes")
args = parser.parse_args()

# When not equal to zero -  mock modules will be generated
PARSING = str2bool(args.parsing)
FEATURE_EXTRACTION = str2bool(args.feature_extraction)
PROCESSED_DATA = str2bool(args.processed_data)


def prepare_data(training,versions_array, bugged_paths, dic_versions):
    if PROCESSED_DATA:
        if training:
            return pd.read_csv('temporaryFiles/data_train.csv')
        else:
            return pd.read_csv('temporaryFiles/data_test.csv')

    processed_data = []
    for version in versions_array:
        # call xml_parse
        parsing = xml_parse.parsing_xml(version, PARSING)
        # call feature_extraction and get the table
        features = feature_extraction.create_block_features(version, parsing, FEATURE_EXTRACTION)
        features['class'] = 0
        for path in bugged_paths[dic_versions[version]]:
            features.loc[features['File Name'] == path, 'class'] = 1
        processed_data.append(features)

    result = pd.concat(processed_data)
    if training:
        result.to_csv('temporaryFiles/data_train.csv', index=False)  # 2845 samples
    else:
        result.to_csv('temporaryFiles/data_test.csv', index=False)  # 573 samples
    return result


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
    print("\n* * * * * Results * * * * *\n")
    print("Accuracy Score: " + str(acc) + "\n")
    print("roc_auc_score: " + str(auc) + "\n")
    print("Precision: " + str(precision) + "\n")
    print("Recall: " + str(recall) + "\n")


bugged_paths = parse_results.get_bugged_files()
train_data = prepare_data(training=True, versions_array=train_files,
                          bugged_paths=bugged_paths, dic_versions=dic_versions)
test_data = prepare_data(training=False, versions_array=test_files,
                         bugged_paths=bugged_paths, dic_versions= dic_versions)

train_data.drop("File Name", axis=1, inplace=True)
test_data.drop("File Name", axis=1, inplace=True)

x_train = train_data.iloc[:, :-1]
y_train = train_data.iloc[:, -1]
x_test = test_data.iloc[:, :-1]
y_test = test_data.iloc[:, -1]

build_model(x_train, y_train, x_test, y_test)
