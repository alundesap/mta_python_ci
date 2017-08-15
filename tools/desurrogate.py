#!/usr/bin/python

import sys

infile = open(sys.argv[1],'r')
outfile = open(sys.argv[2],'w')

inSurrogate = False
inCustom = False

lastline = "" 

for line in infile.readlines():

    #print line,

    if lastline.startswith("#== Begin Surrogate"):
        #print "In Surrogate!"
        inSurrogate = True

    if line.startswith("#== End Surrogate"):
        #print "Out of Surrogate!"
        inSurrogate = False

    if lastline.startswith("#== Begin Custom"):
        #print "In Custom!"
        inCustom = True

    if line.startswith("#== End Custom"):
        #print "Out of Custom!"
        inCustom = False

    if inSurrogate:
        outfile.write("#")
        outfile.write(line)
    elif inCustom:
        if line.startswith("#"):
            outfile.write(line[1:])
        else:
            outfile.write(line)
    else:
        outfile.write(line)

    lastline = line

infile.close()
outfile.close()

