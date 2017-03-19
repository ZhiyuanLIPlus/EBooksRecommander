# -*- coding: utf-8 -*-
from __future__ import division
from math import sqrt
from dataloader import loadJsonObjectToDict

def sim_euclid(prefs, personA, personB):
    si = {} #Dict for shared item
    for item in prefs[personA]:
        if item in prefs[personB]:
            si[item] = 1
    #Zero shared item -> not similar at all
    if len(si) == 0: return 0
    sum_of_squares = sum([pow(prefs[personA][item] - prefs[personB][item], 2) for item in si])
    return 1/(1+sqrt(sum_of_squares))

def sim_pearson(prefs, personA, personB):
    si = {} #Dict for shared item
    for item in prefs[personA]:
        if item in prefs[personB]:
            si[item] = 1
    n = len(si)
    if n == 0: return 0
    #sum
    sumA = sum([prefs[personA][item] for item in si])
    sumB = sum([prefs[personB][item] for item in si])
    #for item in si:
    #    print item.encode("UTF-8") + "|" + str(prefs[personA][item]) + "|" + str(prefs[personB][item])
    #sum sqrt
    sumASqrt = sum([pow(prefs[personA][item], 2) for item in si])
    sumBSqrt = sum([pow(prefs[personB][item], 2) for item in si])
    #power of sum
    pSum = sum(prefs[personA][it] * prefs[personB][it] for it in si)
    #pearson Formula 4
    num = pSum - (sumA*sumB/n)
    den = sqrt((sumASqrt - pow(sumA, 2)/n) * (sumBSqrt - pow(sumB, 2)/n))
    if den == 0: return 0
    r = num/den
    return r
#To Think over
def topMatches(prefs, person, n=5, similarity = sim_pearson):
    #scores = [(sim_pearson(prefs, person, other) * sim_euclid(prefs, person, other), other) for other in prefs if other != person]
    scores = [(sim_pearson(prefs, person, other), other) for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

def getRecommanditions(prefs, person,similarity = sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        if other == person : continue
        sim = similarity(prefs, person, other)
        if sim <= 0: continue

        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] ==0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                simSums.setdefault(item, 0)
                simSums[item] += sim
    rankings = [(total/simSums[item], item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings

def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            result[item][person] = prefs[person][item]
    return result

def calculationSimilarItem(prefs, n=10):
    result = {}
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        c+=1
        if c%100 == 0: print "%d / %d" % (c, len(itemPrefs))
        scores = topMatches(itemPrefs, item, n=n, similarity=sim_euclid)
        result[item] = scores
    return result

def getRecommandedItems(prefs, itemMatch, user):
    userRating = prefs[user]
    scores = {}
    totalSim = {}

    for (item, rating) in userRating.items():
        #print item.encode("UTF-8")
        for (similarity, itemSim) in itemMatch[item]:
            if itemSim in userRating or similarity <= 0: continue
            scores.setdefault(itemSim,0)
            scores[itemSim] += similarity*rating
            totalSim.setdefault(itemSim,0)
            totalSim[itemSim] += similarity
    rankings =[(score/totalSim[item], item) for item,score in scores.items()]
    rankings.sort()
    rankings.reverse()
    return rankings
#Test
loadedData = loadJsonObjectToDict("test.json")
'''
print sim_euclid(loadedData, u'己未癸酉', u'赤戟')
print sim_pearson(loadedData, u'己未癸酉', u'阿克夏记录')
li = getRecommanditions(loadedData, u'己未癸酉')
for tl in li:
    print str(tl[0]) + ":" + tl[1]
books = transformPrefs(loadedData)
li = topMatches(books, u'间客')
for tl in li:
    print str(tl[0]) + ":" + tl[1]
'''
li = calculationSimilarItem(loadedData)
re = getRecommandedItems(loadedData, li,  u'赤戟')
for tl in re:
    print str(tl[0]) + ":" + tl[1]