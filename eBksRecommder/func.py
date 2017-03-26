# -*- coding: utf-8 -*-
from __future__ import division
from math import sqrt
from dataloader import loadJsonObjectToDict
import pickle
import os

SHAREDITEM_AJUSTNUM = 50

def sim_euclid(prefs, personA, personB):
    si = {} #Dict for shared item
    for item in prefs[personA]:
        if item in prefs[personB]:
            si[item] = 1
    #Zero shared item -> not similar at all
    if len(si) == 0: return 0
    sum_of_squares = sum([pow(prefs[personA][item] - prefs[personB][item], 2) for item in si])
    r = 1/(1+sqrt(sum_of_squares))
    return r

def sim_euclid_ajust(prefs, personA, personB):
    si = {} #Dict for shared item
    for item in prefs[personA]:
        if item in prefs[personB]:
            si[item] = 1
    #Zero shared item -> not similar at all
    if len(si) == 0: return 0
    sum_of_squares = sum([pow(prefs[personA][item] - prefs[personB][item], 2) for item in si])
    r = 1/(1+sqrt(sum_of_squares))
    r *= len(si)/SHAREDITEM_AJUSTNUM
    return r

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

def sim_pearson_ajust(prefs, personA, personB):
    si = {} #Dict for shared item
    for item in prefs[personA]:
        if item in prefs[personB]:
            si[item] = 1
    n = len(si)
    if n == 0: return 0
    #sum
    sumA = sum([prefs[personA][item] for item in si])
    sumB = sum([prefs[personB][item] for item in si])

    #sum sqrt
    sumASqrt = sum([pow(prefs[personA][item], 2) for item in si])
    sumBSqrt = sum([pow(prefs[personB][item], 2) for item in si])
    #power of sum
    pSum = sum(prefs[personA][it] * prefs[personB][it] for it in si)
    #pearson Formula 4
    num = pSum - (sumA*sumB/n)
    den = sqrt((sumASqrt - pow(sumA, 2)/n) * (sumBSqrt - pow(sumB, 2)/n))
    if den == 0: return 0
    r = (num/den) * (n/SHAREDITEM_AJUSTNUM)
    return r
#To Think over
def topMatches(prefs, person, n=5, similarity = sim_pearson):
    #scores = [(sim_pearson(prefs, person, other) * sim_euclid(prefs, person, other), other) for other in prefs if other != person]
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
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

def calculationSimilarItem(prefs, dumpedfilePath, n=10):
    result = {}
    if os.path.exists(dumpedfilePath):
        print('find preprocessed data, loading directly...')
        with open(dumpedfilePath, 'rb') as f:
            result = pickle.load(f)
        return result
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        c+=1
        if c%100 == 0: print('%d/%d'%(c,len(itemPrefs)))
        scores = topMatches(itemPrefs, item, n=n, similarity=sim_euclid_ajust)
        result[item] = scores
    with open(dumpedfilePath, 'wb') as f:
        pickle.dump(result,f)
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

def calculateAverageSharedItemForPrefs(prefs):
    length_prefs = len(prefs) #Total Number
    sumOneUser = 0
    sumAll = 0
    i = 0
    for user in prefs:
        i += 1
        for other in prefs:
            if user == other: continue
            si = {}
            for item in prefs[user]:
                if item in prefs[other]:
                    si[item] = 1
            sumOneUser += len(si)
        sumOneUser /= length_prefs
        sumAll += sumOneUser
        if i%100 == 0: print('%d/%d Users Done. SumAll: %d ' %(i,length_prefs,sumAll))
    return sumAll/length_prefs

#LocalTest
def main():
    loadedData = loadJsonObjectToDict("./data/test.json")
    #n = calculateAverageSharedItemForPrefs(loadedData)
    li = calculationSimilarItem(loadedData, "./data/CalculatedItemSim" +"Distance" + ".pkl")
    re = getRecommandedItems(loadedData, li,  u'赤戟')
    for tl in re:
        print (str(tl[0]) + ":" + tl[1])

if __name__ == '__main__':
    main()