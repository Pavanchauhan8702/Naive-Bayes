# -*- coding: utf-8 -*-
"""Telecom attempt .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15VT8WwgteCq3OX0B3vwLkWGimleDsIS4
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LassoCV
from sklearn.feature_selection import SelectKBest, chi2

d1 = pd.read_excel('/content/test.xlsx')
df = pd.read_excel('/content/train.xlsx')

df

df.info()

df.isnull().sum()

df.describe()

df=df.drop('customerID',axis=1)

df.head()

def ohe(df):
    x=pd.get_dummies(df)
    x=x.iloc[:,:-1]
    return x

x=ohe(df['gender'])
df.drop('gender',axis=1,inplace=True)
df=pd.concat([df,x],axis=1)

df['Partner']=df['Partner'].replace(['Yes','No'],[1,0])

df['Dependents'].unique()

df['Dependents']=df['Dependents'].replace(['Yes','No'],[1,0])

df['MultipleLines'].unique()

from sklearn import preprocessing
 
# label_encoder object knows how to understand word labels.
label_encoder = preprocessing.LabelEncoder()
 
# Encode labels in column 'species'.
df['MultipleLines']= label_encoder.fit_transform(df['MultipleLines'])
 
df['MultipleLines'].unique()

df['InternetService'].unique()

df['InternetService']= label_encoder.fit_transform(df['InternetService'])

df['OnlineSecurity'].unique()

df['OnlineSecurity']= label_encoder.fit_transform(df['OnlineSecurity'])

df['OnlineBackup'].unique()

df['OnlineBackup']= label_encoder.fit_transform(df['OnlineBackup'])

df

df['PhoneService'].unique()

df['PhoneService']=df['PhoneService'].replace(['Yes','No'],[1,0])

df.head()

df['DeviceProtection'].unique()

df['DeviceProtection']= label_encoder.fit_transform(df['DeviceProtection'])

df['TechSupport'].unique()

df['TechSupport']= label_encoder.fit_transform(df['TechSupport'])

df['StreamingTV'].unique()

df['StreamingTV']= label_encoder.fit_transform(df['StreamingTV'])

df['Contract'].unique()

df['Contract']= label_encoder.fit_transform(df['Contract'])

df['PaperlessBilling'].unique()

df['PaperlessBilling']=df['PaperlessBilling'].replace(['Yes','No'],[1,0])

df.head()

df['Churn'].unique()

df['Churn']=df['Churn'].replace(['Yes','No'],[1,0])

df['PaymentMethod'].unique()

df['PaymentMethod']= label_encoder.fit_transform(df['PaymentMethod'])

df['StreamingMovies'].unique()

df['StreamingMovies']= label_encoder.fit_transform(df['StreamingMovies'])

df.head(50)

df.info()

df['TotalCharges'].unique()

X=df.drop('Churn',axis=1)
X.head()

y=df["Churn"]
y=pd.DataFrame(y)
y.head()

X.info()

X['Female'] = X['Female'].astype('int')
X['MonthlyCharges'] = X['MonthlyCharges'].astype('int')

X['TotalCharges'] = pd.to_numeric(X['TotalCharges'],errors='coerce')
median = X['TotalCharges'].median()
X['TotalCharges'].fillna(median,inplace=True)

reg = LassoCV()
reg.fit(X, y)
print("Best alpha using built-in LassoCV: %f" % reg.alpha_)
print("Best score using built-in LassoCV: %f" %reg.score(X,y))
coef = pd.Series(reg.coef_, index = X.columns)
print("Lasso picked " + str(sum(coef != 0)) + " variables and eliminated the other " + str(sum(coef == 0)) + " variables")

from sklearn.preprocessing import MinMaxScaler
names=X.columns
indexes=X.index
X=MinMaxScaler().fit_transform(X)
X=pd.DataFrame(X,columns=names,index=indexes)
X.head()

kmodel=SelectKBest(score_func=chi2,k=8)
x_clf_new=kmodel.fit_transform(X,y)
mask=kmodel.get_support()
important=X.columns[mask]
print(important,len(important))

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y)

#alpha= []
class NaiveBayes:
    
    def fit(self, X, y):
        self.classes = np.unique(y)
        self.mean = np.zeros((len(self.classes), X.shape[1]))
        self.variance = np.zeros((len(self.classes), X.shape[1]))
        self.prior = np.zeros(len(self.classes))
        for i, c in enumerate(self.classes):
            X_c = X[y==c]
            self.mean[i, :] = X_c.mean(axis=0)
            self.variance[i, :] = X_c.var(axis=0)
            self.prior[i] = X_c.shape[0] / X.shape[0]
            
    def predict(self, X):
        posterior = np.zeros((X.shape[0], len(self.classes)))
        for i, c in enumerate(self.classes):
            likelihood = np.exp(-(X - self.mean[i, :]) ** 2 / (2 * self.variance[i, :])) / np.sqrt(2 * np.pi * self.variance[i, :])
            posterior[:, i] = np.log(likelihood).sum(axis=1) + np.log(self.prior[i])
        return self.classes[np.argmax(posterior, axis=1)]

nb=NaiveBayes()
nb.fit(X_train,y_train)

# Checking Accuracy
def accuracy(y_true, y_pred):
        accuracy = np.sum(y_true == y_pred) / len(y_true)
        return accuracy

"""The error is happening because the accuracy function is expecting two numpy arrays as inputs, but y_test and predictions are both pandas DataFrames. To fix the error, you can convert these DataFrames to numpy arrays using the .values attribute.

Note that we also used the .ravel() method to flatten the y_test array, as the accuracy function expects a 1D array as input.
"""

nb = NaiveBayes()
nb.fit(X_train, y_train)
predictions = nb.predict(X_test)

print("Naive Bayes classification test data accuracy:", 
      accuracy(y_test.values.ravel(), predictions)*100)

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Train the Naive Bayes classifier
nb = NaiveBayes()
nb.fit(X_train, y_train)

# Make predictions on the test data
predictions = nb.predict(X_test)

# Calculate the evaluation metrics
acc = accuracy_score(y_test, predictions)
prec = precision_score(y_test, predictions, average='weighted')
rec = recall_score(y_test, predictions, average='weighted')
f1 = f1_score(y_test, predictions, average='weighted')

# Print the evaluation metrics
print("Accuracy:", acc)
print("Precision:", prec)
print("Recall:", rec)
print("F1 score:", f1)

import itertools
import numpy as np
from collections import Counter


class NaiveBayes:
    def __init__(self):
        self.class_priors = None
        self.feature_likelihoods = None

    def train(self, X, y):
        # Compute class priors
        self.class_priors = Counter(y)
        total_samples = len(y)
        for c in self.class_priors:
            self.class_priors[c] /= total_samples

        # Compute feature likelihoods
        n_samples, n_features = X.shape
        self.feature_likelihoods = np.zeros((n_features, 2))
        for feature_idx in range(n_features):
            for feature_value in [0, 1]:
                for c in self.class_priors:
                    X_c = X[y == c]
                    self.feature_likelihoods[feature_idx, feature_value] += (
                        (X_c[:, feature_idx] == feature_value).sum()
                        / float(self.class_priors[c] * total_samples)
                    )

    def predict(self, X):
        y_pred = []
        for x in X:
            probs = []
            for c in self.class_priors:
                likelihoods = self.feature_likelihoods[np.arange(len(x)), x]
                log_prob = np.log(self.class_priors[c]) + np.log(likelihoods).sum()
                probs.append(log_prob)
            y_pred.append(np.argmax(probs))
        return np.array(y_pred)

    def accuracy(self, X, y):
        y_pred = self.predict(X)
        return (y_pred == y).mean()


def grid_search(X, y, param_grid):
    best_accuracy = 0
    best_params = None

    for params in itertools.product(*param_grid.values()):
        # Train Naive Bayes classifier
        nb = NaiveBayes()
        nb.train(X, y)

        # Evaluate accuracy
        accuracy = nb.accuracy(X, y)

        # Check if current params are better than previous ones
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_params = params

    return best_params, best_accuracy

# Generate example data
X = np.random.randint(0, 2, size=(100, 10))
y = np.random.randint(0, 2, size=100)

# Define hyperparameter search space
param_grid = {"alpha": [0.1, 1.0, 10.0], "fit_prior": [True, False]}

# Perform grid search
best_params, best_accuracy = grid_search(X, y, param_grid)

print("Best hyperparameters:", best_params)
print("Best accuracy:", best_accuracy*100)

def accuracy(y_true, y_pred):
    correct_predictions = np.sum(y_true == y_pred)
    return correct_predictions / len(y_true)

def precision(y_true, y_pred):
    true_positives = np.sum((y_true == 1) & (y_pred == 1))
    false_positives = np.sum((y_true == 0) & (y_pred == 1))
    if true_positives + false_positives == 0:
        return 0
    return true_positives / (true_positives + false_positives)

def recall(y_true, y_pred):
    true_positives = np.sum((y_true == 1) & (y_pred == 1))
    false_negatives = np.sum((y_true == 1) & (y_pred == 0))
    if true_positives + false_negatives == 0:
        return 0
    return true_positives / (true_positives + false_negatives)

def f1_score(y_true, y_pred):
    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    if p + r == 0:
        return 0
    return 2 * (p * r) / (p + r)

# Train Naive Bayes classifier
nb = NaiveBayes()
nb.train(X, y)

# Predict labels
y_pred = nb.predict(X)

# Compute accuracy, precision, recall, and F1 score
acc = accuracy(y, y_pred)
prec = precision(y, y_pred)
rec = recall(y, y_pred)
f1 = f1_score(y, y_pred)

print("Accuracy:", acc*100)
print("Precision:", prec*100)
print("Recall:", rec)
print("F1 Score:", f1*100)

