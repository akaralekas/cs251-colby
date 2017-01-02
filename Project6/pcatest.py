# Bruce A. Maxwell
# Spring 2015
# CS 251 Project 6
#
# PCA test function
#
import numpy as np
import data
import analysis
import sys

if __name__ == "__main__":
#   if len(sys.argv) < 2:
#         print 'Usage: python %s <data file>' % (sys.argv[0])
#         exit()

    data = data.Data( "pcatest.csv" )
    pcadata = analysis.pca( data, data.get_headers(), False )

    print "\nOriginal Data Headers"
    print pcadata.get_data_headers()
    print "\nOriginal Data", 
    print data.get_data( data.get_headers() )
    print "\nOriginal Data Means"
    print pcadata.get_data_means()
    print "\nEigenvalues"
    print pcadata.get_eigenvalues()
    print "\nEigenvectors"
    print pcadata.get_eigenvectors()
    print "\nProjected Data"
    print pcadata.get_data(pcadata.get_data_headers())
