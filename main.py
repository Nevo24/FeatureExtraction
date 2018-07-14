import argparse
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, accuracy_score, recall_score, roc_auc_score
import feature_extraction
import parse_results
import xml_parse
from copy import deepcopy

train_files = ['1_7_jcov', '1_7_rc2_jcov', '1_8_jcov']
test_files = ['1_8_rc2_jcov']
dic_versions = {'1_7_jcov': '1.7', '1_7_rc2_jcov': '1.7-rc2',
                '1_8_jcov': '1.8', '1_8_rc2_jcov': '1.8-rc2'}


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


parser = argparse.ArgumentParser()
parser.add_argument('--parsing', type=str, default="yes")
parser.add_argument('--feature_extraction', type=str, default="yes")
parser.add_argument('--process_data', type=str, default="yes")
args = parser.parse_args()

# When not equal to zero -  mock modules will be generated
PARSING = str2bool(args.parsing)
FEATURE_EXTRACTION = str2bool(args.feature_extraction)
PROCESS_DATA = str2bool(args.process_data)


def prepare_data(training,versions_array, bugged_paths, dic_versions):
    if not PROCESS_DATA:
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


def build_model(x_train, y_train, x_test, y_test,group_name):
    model = RandomForestClassifier()
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    # metrics
    precision = precision_score(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_pred)

    # print the results
    print("* * * * * * * Results * * * * * * *")
    print("Accuracy Score: " + str(acc))
    print("roc_auc_score: " + str(auc))
    print("Precision: " + str(precision))
    print("Recall: " + str(recall))
    print("* * * * * * * * * * * * * * * * * * \n")

    result = {'Group Name': group_name,
                'Accuracy': acc,
                'Auc Area': auc,
                'Precision': precision,
                'Recall': recall}
    return result


# create results table
results = pd.DataFrame(index=[0],
                        columns=['Group Name', 'Accuracy', 'Auc Area', 'Precision', 'Recall'])
# extract bugged files
bugged_paths = parse_results.get_bugged_files()
# get the train data
train_data = prepare_data(training=True, versions_array=train_files,
                          bugged_paths=bugged_paths, dic_versions=dic_versions)
# get the test data
test_data = prepare_data(training=False, versions_array=test_files,
                         bugged_paths=bugged_paths, dic_versions= dic_versions)

train_data.drop("File Name", axis=1, inplace=True)
test_data.drop("File Name", axis=1, inplace=True)

# all the features
x_train = train_data.iloc[:, :-1]
y_train = train_data.iloc[:, -1]
x_test = test_data.iloc[:, :-1]
y_test = test_data.iloc[:, -1]

print("\nBuild the model with all features: \n")
res = build_model(x_train, y_train, x_test, y_test,'all features')
results = results.append(res, ignore_index=True)

print("Build the model with block features: \n")
x_train_block = train_data.iloc[:, :69]
x_test_block = test_data.iloc[:, :69]
res = build_model(x_train_block, y_train, x_test_block, y_test,'block features')
results = results.append(res, ignore_index=True)

print("Build the model with function features: \n")
x_train_func = train_data.iloc[:, 69:-1]
x_test_func = test_data.iloc[:, 69:-1]
res = build_model(x_train_func, y_train, x_test_func, y_test,'function features')
results = results.append(res, ignore_index=True)

# build the model according the groups (with the group ang without the group)
group_features =[(1,8),(9,16),(17,24),(25,64),(65,69),(70,77),(78,93),(94,125)]
for interval in group_features:
    copy_train = deepcopy(x_train)
    copy_test = deepcopy(x_test)
    print("Build the model with group features "+ str(interval)+":\n")
    x_train_with = copy_train.iloc[:, interval[0]-1: interval[1]]
    x_test_with = copy_test.iloc[:, interval[0]-1: interval[1]]
    res = build_model(x_train_with, y_train, x_test_with, y_test, 'with '+str(interval))
    results = results.append(res, ignore_index=True)

    print("Build the model without group features " + str(interval) + ":\n")
    x_train_without = copy_train.drop(copy_train.columns[interval[0]-1: interval[1]], axis=1, inplace=False)
    x_test_without = copy_test.drop(copy_train.columns[interval[0]-1: interval[1]], axis=1, inplace=False)
    res = build_model(x_train_without, y_train, x_test_without, y_test, 'without' + str(interval))
    results = results.append(res, ignore_index=True)

results.to_csv('Model results.csv', index=False)