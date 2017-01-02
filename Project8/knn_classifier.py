# CS 251
# Spring 2016
#------------------------------------

# File: knn_classifier.py
# Author/Editor: Anthony Karalekas
# Collaboration: S.Parrott, J.Saul, B. Doyle
# Worked alongside S.Parrot throughout 
# Help: CP Majgaard
# Date: Apr. 24, 2016
# Assignment: Project 8

#------------------------------------

#help from CP Majgaard
# KNN CLASS TEST
# KNN CLASSIFIER CLASS


import sys
import data
import classifier
import numpy as np
import analysis as an

"""Write a python function, probably in a new file, that does the following.
-Reads in a training set and its category labels, possibly as a separate file.
-Reads a test set and its category labels, possibly as a separate file.
-Builds a classifier using the training set.
-Classifies the training set and prints out a confusion matrix.
-Classifies the test set and prints out a confusion matrix.
-Writes out a new CSV data file with the test set data and the categories as an extra column. 
Your application should be able to read this file and plot it with the categories as colors.
"""


def main(argv):
    '''Reads in a training set and a test set and builds two KNN
    classifiers.  One uses all of the data, one uses 10
    exemplars. Then it classifies the test data and prints out the
    results.
    '''

    # usage
    if len(argv) < 3:
        print 'Usage: python %s <training data file> <test data file> <optional training category file> <optional test category file>' % (argv[0])
        exit(-1)

    # read in the training set
    data_train = data.Data(argv[1])
    # read in the test set
    data_test = data.Data(argv[2])

    # compatibility check length or argv
    if len(argv) > 4:
    	# get the categories of the training data 
        train_cat_data = data.Data(argv[3])
        train_cats = train_cat_data.get_data( [train_cat_data.get_headers()[0]] )
        # get the categories of the test data 
        test_cat_data = data.Data(argv[4])
        test_cats = test_cat_data.get_data( [test_cat_data.get_headers()[0]] )
        # get the training data A and the test data B
        A = data_train.get_data( data_train.get_headers() )
        B = data_test.get_data( data_test.get_headers() )
    else:
        # just assume the categories are the last column
        train_cats = data_train.get_data( [data_train.get_headers()[-1]] )
        test_cats = data_test.get_data( [data_test.get_headers()[-1]] )
        A = data_train.get_data( data_train.get_headers()[:-1] )
        B = data_test.get_data( data_test.get_headers()[:-1] )

#----------------------------------------------------------------------- 
    # create two classifiers
    knnClass = classifier.KNN()
	print "Created Classifier, Building Now."
    # build the classifiers
    knnClass.build( A, train_cats )
    print "Built! Now classifying."

#-----------------------------------------------------------------------    
    #-Classifies the training set data and prints out a confusion matrix.    
    acats, alabels = knnClass.classify( A )
    print "Done Classifying."
   
    unique, mapping = np.unique(np.array(train_cats.T), return_inverse=True)
    unique2, mapping2 = np.unique(np.array(alabels.T), return_inverse=True)
    
    mtx = knnClass.confusion_matrix(np.matrix(mapping).T, np.matrix(mapping2).T)
    print "Training Confusion Matrix:"
    print knnClass.confusion_matrix_str(mtx)

#----------------------------------------------------------------------- 
#----------------------------------------------------------------------- 
	#-Classifies the test set data and prints out a confusion matrix.
    bcats, blabels = knnClass.classify( B )
    print "Done Classifying."
    
    unique, mapping = np.unique(np.array(test_cats.T), return_inverse=True)
    unique2, mapping2 = np.unique(np.array(blabels.T), return_inverse=True)
    
    mtx1 = knnClass.confusion_matrix(np.matrix(mapping).T, np.matrix(mapping2).T)
    print "Test Confusion Matrix:"
    print knnClass.confusion_matrix_str(mtx1)
    
#----------------------------------------------------------------------- 
	#Writes out a new CSV data file with the test set data 
	# and the categories as an extra column
    data_test.addColumn("KNN Classification", bcats)
    data_test.toFile(filename="knnClass.csv")

    return

if __name__ == "__main__":
    main(sys.argv)
