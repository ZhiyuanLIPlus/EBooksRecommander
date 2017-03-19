# -*- coding: utf-8 -*-
import json
import time
def loadJsonObjectToDict(filename):
    f = open(filename,'r')
    totalLine, errorLine = 0, 0
    critics = {}
    start_time = time.time()
    for line in f:
        totalLine += 1
        try:
            readDict = json.loads(line)
            booklist = readDict['bookList']
            nestedDict = {}
            for book in booklist:
                nestedDict[book['name']] = book['noteInBooklist']
            if readDict['publisher'] not in critics:
                critics[readDict['publisher']] = nestedDict
            else:
                critics[readDict['publisher']].update(nestedDict)
        except ValueError as e:
            errorLine += 1
            print e.message + " @Line " + str(totalLine)

    print str(totalLine - errorLine) + "/" + str(totalLine) + " has been loaded into critics dict"
    print "Num of elements in dict:" + str(len(critics))
    print "Load time:" + str(time.time() - start_time)
    return critics

#Test
def __init__():
    testDict = loadJsonObjectToDict("test.json")
    for key, value in testDict[u'最爱小花花'].iteritems():
        print key + ":" + str(value)


