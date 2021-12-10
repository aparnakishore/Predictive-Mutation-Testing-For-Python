# Pandas is used for data manipulation
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, precision_recall_fscore_support, f1_score, roc_curve, roc_auc_score, RocCurveDisplay, auc
from collections import Counter
positive_prob = []
# Read in data and display first 5 rows
features = pd.read_csv('/Users/aparnak/Classes/Program_Analysis/Project/Data/training_pmt_12p.csv',encoding= 'unicode_escape')
print(features)
print('The shape of our features is:', features.shape)
# Use numpy to convert to arrays
# Labels are the values we want to predict
labels = np.array(features['Label'])
# Remove the labels from the features
# axis 1 refers to the columns
features= features.drop('Label', axis = 1)
# Saving feature names for later use
feature_list = list(features.columns)
# Convert to numpy array
features = np.array(features)
# Import the model we are using
from sklearn.ensemble import RandomForestClassifier
# Instantiate model with 50 decision trees
rf = RandomForestClassifier(n_estimators = 50, random_state = 5,criterion="entropy")
# Train the model on training data
#scores = cross_val_score(rf, features, labels, cv=10)
#print(scores.mean())
rf.fit(features, labels)
y_pred_train = rf.predict(features)
#print(accuracy_score(labels, y_pred_train))
#print(confusion_matrix(labels, y_pred_train))

#feature_names = [f"features {i}" for i in range(features.shape[1])]
feature_names = ["numExecuteCovered", "numTestCovered", "typeStatement", "typeOperator", "mcCabe Complexity", "LOC", "depNestedBlock", "Ca", "Ce", "Instability", "methodAssertion", "totalAssertion"]
importances = rf.feature_importances_

forest_importances = pd.Series(importances, index=feature_names).sort_values(ascending=False)

#Feature importance
fig, ax = plt.subplots()
forest_importances.plot.bar(ax=ax)
ax.set_title("Feature importances")
ax.set_ylabel("Merit")
fig.tight_layout()
plt.show()

#Input test data
test = pd.read_csv('Data/testing_pmt_5p.csv',encoding= 'unicode_escape')
print(test)
# Labels are the values we want to predict
test_labels = np.array(test['Label'])
# Remove the labels from the features
# axis 1 refers to the columns
test= test.drop('Label', axis = 1)
# Saving feature names for later use
feature_list = list(test.columns)
# Convert to numpy array
test = np.array(test)
y_pred_test = rf.predict(test)
print("Predicted labels::", y_pred_test)
#print(accuracy_score(test_labels, y_pred_test))
confusion = confusion_matrix(test_labels, y_pred_test)
print("Confusion_matrix:\n",confusion)
print(precision_recall_fscore_support(test_labels, y_pred_test, average='micro'))
print(f1_score(test_labels, y_pred_test, average='micro'))
#Get the probability of each predictions
predicted = rf.predict_proba(test)
print(predicted)
#Take the positive predictictability i.e. survived for calculating ROC AUC
for i in predicted:
    positive_prob.append(i[1])
print(positive_prob)
#Calculate ROC
fpr, tpr, thresholds = roc_curve(test_labels, positive_prob, pos_label='survived')
print(fpr, tpr, thresholds)
try:
    print("AUC: ", roc_auc_score(test_labels, positive_prob))
    roc_auc = auc(fpr, tpr)
    print(roc_auc)
except:
    pass
#display = RocCurveDisplay(fpr=fpr,tpr=tpr,roc_auc=roc_auc)
#display.plot()
#plt.show()
#Calculate absolute prediction error
test_label = list(test_labels)
print(type(test_label), test_label)
d = Counter(test_label)
count_survived = d['survived']
count_killed = d['killed']
actual_mutation_score = count_killed/(count_killed+count_survived)
print(actual_mutation_score)

pred_label = list(y_pred_test)
f = Counter(pred_label)
count_pre_survived = f['survived']
count_pre_killed = f['killed']
pre_mutation_score = count_pre_killed/(count_pre_killed+count_pre_survived)
print(pre_mutation_score)

Error = abs(actual_mutation_score - pre_mutation_score)
print("Error: ", Error)