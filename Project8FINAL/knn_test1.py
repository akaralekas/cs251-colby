# Bruce Maxwell
# Spring 2015
# CS 251 Project 8
#
# KNN class test
#

import sys
import data
import classifier

def main(argv):
    '''Builds two KNN classifiers and prints them out.  The first uses all
    of the exemplars, the second uses only 10.

    '''

    # usage
    if len(argv) < 2:
        print 'Usage: python %s <data file> <optional category file>' % (argv[0])
        exit(-1)

    # read the data
    d = data.Data(argv[1])

    # get the categories and data matrix
    if len(argv) > 2:
        catdata = data.Data(argv[2])
        cats = catdata.get_data( [catdata.get_headers()[0]] )
        A = d.get_data( d.get_headers() )
    else:
        # assume the categories are the last column
        cats = d.get_data( [d.get_headers()[-1]] )
        A = d.get_data( d.get_headers()[:-1] )

    # create a new classifier
    knnc = classifier.KNN()

    # build the classifier using all exemplars
    knnc.build( A, cats )

    # print the classifier
    # requires a __str__ method
    print knnc


    # build and print the classifier using 10 exemplars per class
    knnc2 = classifier.KNN()
    knnc2.build( A, cats, 10 )
    print knnc2

    return

if __name__ == "__main__":
    main(sys.argv)    
