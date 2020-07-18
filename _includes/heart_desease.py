#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 15:49:39 2020

@author: arley
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import scale
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score


##########################Data analysis#######################################
##############################################################################

#-------------------------Imput dataset--------------------------------#
dataset= pd.read_csv('Heart_desease.csv')
print("")
print("=============================Dataset==================================")
print(dataset.head(20))


#------------------------Initial information------------------------------#
print("")
print("=============================Correlation Matrix==================================")
print(dataset.corr())


print("")
print("=============================Descriptive statistics==================================")
print(dataset.describe())


#-----------------------------New_dataset--------------------------------#
X= dataset.drop(columns=['DEATH_EVENT'])
X2= scale(X) #For KNN
Y= dataset['DEATH_EVENT']
X_treino, X_teste, Y_treino, Y_teste= train_test_split(X, Y, test_size= 0.3, 
                                                       random_state= 115)

X_treino2, X_teste2, Y_treino2, Y_teste2= train_test_split(X2, Y, test_size= 0.3, 
                                                       random_state= 115)


###########################-Machine learning##################################
##############################################################################

clf= DecisionTreeClassifier(random_state= 115)
clf2= GradientBoostingClassifier(random_state= 115)
clf3= RandomForestClassifier(random_state= 115)
clf4= KNeighborsClassifier()

#-------------------------Parameters----------------------------------------#
param_dist= {'max_depth':[1, 2, 3, 4, 5, 6, 7, 8, 9, 12, None],
             'criterion': ['entropy', 'gini'],
             'max_leaf_nodes':[2, 3, 4, 5, None],
             'min_samples_split': [8, 10, 11, 14, 16, 19],
             'min_samples_leaf':[1, 2, 3, 4, 5, 6, 7]}


param_dist2= {'max_depth':[1, 2, 3, 4, 5, 6, 7, 8, 9, 12, None],
              'learning_rate':[0.1, 0.5, 1.0, 2.0, 5.0, 10.0],
              'n_estimators':[1, 5, 10, 20, 50, 100, 150, 200],
              'max_leaf_nodes':[2, 3, 4, 5, None],
              'min_samples_split': [8, 10, 11, 14, 16, 19],
              'min_samples_leaf':[1, 2, 3, 4, 5, 6, 7]}


param_dist3= {'n_estimators':[2, 3, 4, 5, 10, 15, 30, 50, 55, 63, 100, 120, 150],
             'bootstrap': [True, False],
             'max_depth':[1, 2, 3, 4, 5, 6, 7, 8, 9, 12, None],
             'criterion':['gini', 'entropy'],
             'max_leaf_nodes':[2, 3, 4, 5, 6, 7, None],
             'min_samples_split': [8, 10, 11, 14, 16, 19],
             'min_samples_leaf':[1, 2, 3, 4, 5, 6, 7]}


param_dist4= {'n_neighbors':list(range(1, 40))}


#--------------------------Randomized Search-------------------------------#
rsearch= RandomizedSearchCV(clf, param_distributions= param_dist, n_iter= 60, 
                            return_train_score= True)

rsearch2= RandomizedSearchCV(clf2, param_distributions= param_dist2, n_iter= 60, 
                            return_train_score= True)

rsearch3= RandomizedSearchCV(clf3, param_distributions= param_dist3, n_iter= 60, 
                            return_train_score= True)

rsearch4= RandomizedSearchCV(clf4, param_distributions= param_dist4, n_iter= 30, 
                            return_train_score= True)


#-------------------------Fit and prediction-------------------------------#
rsearch.fit(X_treino, Y_treino)
bestclf= rsearch.best_estimator_
predicao= bestclf.predict(X_teste)

rsearch2.fit(X_treino, Y_treino)
bestclf2= rsearch2.best_estimator_
predicao2= bestclf2.predict(X_teste)

rsearch3.fit(X_treino, Y_treino)
bestclf3= rsearch3.best_estimator_
predicao3= bestclf3.predict(X_teste)

rsearch4.fit(X_treino2, Y_treino2)
bestclf4= rsearch4.best_estimator_
predicao4= bestclf4.predict(X_teste2)


#----------------------Accuracy of models-------------------------#
acuracia= accuracy_score(Y_teste, predicao) #Decision Tree
acuracia2= accuracy_score(Y_teste, predicao2) #GBClassifier
acuracia3= accuracy_score(Y_teste, predicao3) #Random Forest
acuracia4= accuracy_score(Y_teste, predicao4) #KNN
resultados=[acuracia, acuracia2, acuracia3, acuracia4]

#-------------------Accuracy horizontal bar plot------------------------------------#
modelos= ['Decision Tree', 'GBClassifier', 'Random Forest', 'KNN']
fig= plt.figure(figsize=(11,7))
ax= fig.add_subplot(1,1,1)
ax.barh(range(len(resultados)), resultados, align= 'center')
ax.set_yticks(range(len(resultados)))
ax.set_yticklabels(modelos, fontsize=14)
ax.set_title("Peformance of models", fontsize=16)
ax.set_xlabel("Accuracy", fontsize=14)
plt.show()

