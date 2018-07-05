import numpy as np
import pandas as pd
import xml_parse
import feature_extraction
import parse_results
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score,accuracy_score, recall_score,roc_auc_score

train_files = ['1_7_jcov.xml','1_7_rc2_jcov.xml','1_8_jcov.xml']
test_file = '1_8_rc2_jcov.xml'
dic_versions = {'1_7_jcov.xml':'1.7', '1_7_rc2_jcov.xml':'1.7-rc2',
               '1_8_jcov.xml':'1.8', '1_8_rc2_jcov.xml': '1.8-rc2'}


def get_x_y_train(train_files,bugged_paths,dic_versions):
    x_train = []
    for file_name in train_files:
        # call xml_parse
        # parsing = xml_parse.parsing_xml(file_name)

        # call feature_extraction and get the table
        # file_paths, features = feature_extraction.get_feature_extraction(parsing,False,file_name)
        features = feature_extraction.get_feature_extraction(None, True,file_name)
        features['class'] = 0
        count = 0
        for path in bugged_paths[dic_versions[file_name]]:
            features.loc[features['File Name'] == path, 'class'] = 1
            if features.loc[features['File Name'] == path]:
                count=count+1
        a = features['class'].value_counts()
        x_train.append(features)

    result = pd.concat(x_train)
    result.to_csv('x_train.csv', index=False) # 2845 samples
    return result


def get_x_test(test_file):
    # call xml_parse
    # parsing = xml_parse.parsing_xml(test_file)

    # call feature_extraction and get the table
    # file_paths, features = feature_extraction.get_feature_extraction(parsing,False,test_file)
    features = feature_extraction.get_feature_extraction(None, True,test_file)

    features.to_csv('x_test.csv', index=False) # 573 samples
    return features


bugged_paths = parse_results.get_bugged_files()
x_train = get_x_y_train(train_files,bugged_paths,dic_versions)
y_train = 'change'
x_test = get_x_test(test_file)
y_test = 'change'


def build_model(x_train,y_train,x_test,y_test):

    model = RandomForestClassifier()
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    # metrics
    precision = precision_score(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    auc = roc_auc_score(y_test,y_pred)

    # print the results
    print("Co-training results:\n")
    print("Accuracy Score: " + str(acc) + "\n")
    print("roc_auc_score: " + str(auc) + "\n")
    print("Precision: " + str(precision) + "\n")
    print("Recall: " + str(recall) + "\n")

