import sys
import scipy
import numpy
import matplotlib
import pandas
import sklearn

from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

# Load dataset; Note - Python 3.6 upwards needed to update SSL ceritifcates to remove parse errors
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv"
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset = read_csv(url, names=names)

# Some methods to display and summarise the data loaded

print("How many rows and columns are we dealing with?")
print(dataset.shape) #(rows,columns)

print("Let's see the first 10 rows to get a look at what we're dealing with")
print(dataset.head(10))

print("Now let's see a summary of some standard values:")
print(dataset.describe())

print("How many data points do we have within each class of iris flowers?")
print(dataset.groupby('class').size())

# Visualising the data using pandas and matplotlib

print("Box and whisker plots (image):")
dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
pyplot.show()

print("Histograms (image):")
dataset.hist()
pyplot.show()

print("Scatter plot matrix (image):")
scatter_matrix(dataset)
pyplot.show()

# Moving to Evaluation

#Create validation set - 20% of original so we can compare against trained data
#using NumPy methods
array = dataset.values

# Matrix called X for obervations
X = array[:, 0:4]

# Vector called y for responses
y = array[:,4]
X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=1)


# Which algorithms to use? We are testing LR, LDA, KNN, CART, NB, SVM
# From skLearn

models = []
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))

#Accuracy of each model = (number of correctly predicted instances)/(total number of instances in the dataset) * 100)
print("The accuracy of each model is:")
results = []
names = []
for name, model in models:
	kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
	cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
	results.append(cv_results)
	names.append(name)
	print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))

print("Algorithm Comparison graph (image):")
#Compare results of all 6 methods in a box and whisker plot
pyplot.boxplot(results, labels=names)
pyplot.title('Algorithm Comparison')
pyplot.show()


# Make predictions on validation dataset using SVC model
model = SVC(gamma='auto')
model.fit(X_train, Y_train)
predictions = model.predict(X_validation)

# Evaluate and print prediction accuracy
print("Accuracy of chosen model:", (accuracy_score(Y_validation, predictions)))
print("Confusion model:") #whatever that is?
print(confusion_matrix(Y_validation, predictions))
print("Final report on classification results using chosen model:")
print(classification_report(Y_validation, predictions))


