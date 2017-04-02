# -*- coding: utf-8 -*-
from __future__ import division
from math import sqrt
from dataloader import loadJsonObjectToDict
import pickle
import os
import json

PENALTY_RATIO = 9

def sim_tanimoto(prefs, personA, personB):
    keys_a = set(prefs[personA])
    keys_b = set(prefs[personB])
    intersection = keys_a & keys_b
    unionDict = dict(prefs[personA], **prefs[personB])
    return len(intersection)/len(unionDict)

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

def sim_combine(prefs, personA, personB):
    return (sim_euclid(prefs, personA, personB) + sim_tanimoto(prefs, personA, personB) * PENALTY_RATIO)/(PENALTY_RATIO + 1)

def topMatches(prefs, person, n=5, similarity = sim_pearson):
    #scores = [(sim_pearson(prefs, person, other) * sim_euclid(prefs, person, other), other) for other in prefs if other != person]
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

def getRecommandations(prefs, person,similarity = sim_pearson):
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

def calculationSimilarItem(prefs, simFunction, dumpedfilePath, n=10):
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
        scores = topMatches(itemPrefs, item, n=n, similarity=simFunction)
        result[item] = scores
    with open(dumpedfilePath, 'wb') as f:
        pickle.dump(result,f)
    return result

def getRecommandedItems(prefs, itemMatch, userRating):
    userRating = userRating
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

def readUserPrefs(userRatingPath):
    userRating = {}
    if os.path.exists(userRatingPath):
        f = open(userRatingPath, 'r')
        for line in f:
            txtSeg = line.split()
            userRating[txtSeg[0]] = float(txtSeg[1])
    return userRating

#TestCode
def ItemBasedReco():
    #Load scrapy data into {User -> Book -> Note} Dict
    loadedData = loadJsonObjectToDict("./data/test.json")

    # Read User prefs
    userRatingPath = "./UserPrefs.txt"
    userRating = readUserPrefs(userRatingPath)

    #Using Euclid for Calculating Similarity
    #Calculate Top10 Matche book for each book with similarity point
    li = calculationSimilarItem(loadedData, sim_euclid, "./data/CalculatedItemSim" +"Euclid" + ".pkl")
    #Get the Recommandations
    re = getRecommandedItems(loadedData, li,  userRating)
    #Print recommandation
    print("------------------ Item Based: Sim Euclid --------------------")
    for tl in re[0:15]:
        print (str(tl[0]) + ":" + tl[1])

    #Using Euclid for Calculating Similarity
    #Calculate Top10 Matche book for each book with similarity point
    li = calculationSimilarItem(loadedData, sim_tanimoto, "./data/CalculatedItemSim" +"Tanimoto" + ".pkl")
    #Get the Recommandations
    re = getRecommandedItems(loadedData, li,  userRating)
    #Print recommandation
    print("------------------ Item Based: Sim Tanimoto --------------------")
    for tl in re[0:15]:
        print (str(tl[0]) + ":" + tl[1])

    #Using Euclid for Calculating Similarity
    #Calculate Top10 Matche book for each book with similarity point
    li = calculationSimilarItem(loadedData, sim_pearson,"./data/CalculatedItemSim" +"Pearson" + ".pkl")
    #Get the Recommandations
    re = getRecommandedItems(loadedData, li,  userRating)
    #Print recommandation
    print("------------------ Item Based: Sim Pearson --------------------")
    for tl in re[0:15]:
        print (str(tl[0]) + ":" + tl[1])

    #Using Euclid for Calculating Similarity
    #Calculate Top10 Matche book for each book with similarity point
    li = calculationSimilarItem(loadedData,sim_combine, "./data/CalculatedItemSim" +"Combine" + ".pkl")
    #Get the Recommandations
    re = getRecommandedItems(loadedData, li,  userRating)
    #Print recommandation
    print("------------------ Item Based: Sim Tanimoto * 10 + Sim Euclid --------------------")
    for tl in re[0:15]:
        print (str(tl[0]) + ":" + tl[1])

def UserBasedReco():
    #Load scrapy data into {User -> Book -> Note} Dict
    loadedData = loadJsonObjectToDict("./data/test.json")
    # Read User prefs
    userRatingPath = "./UserPrefs.txt"
    userRating = readUserPrefs(userRatingPath)
    loadedData['Me'] = userRating

    re = getRecommandations(loadedData,'Me',sim_euclid)
    print("------------------ User Based: Sim Euclid --------------------")
    for tl in re[0:15]:
        print (str(tl[0]) + ":" + tl[1])

    re = getRecommandations(loadedData,'Me',sim_pearson)
    print("------------------ User Based: Sim Pearson --------------------")
    for tl in re[0:15]:
        print (str(tl[0]) + ":" + tl[1])

    re = getRecommandations(loadedData,'Me',sim_tanimoto)
    print("------------------ User Based: Sim Tanimoto --------------------")
    for tl in re[0:15]:
        print (str(tl[0]) + ":" + tl[1])

    re = getRecommandations(loadedData,'Me',sim_combine)
    print("------------------ User Based: Sim Tanimoto * 10 + Sim Euclid --------------------")
    for tl in re[0:15]:
        print (str(tl[0]) + ":" + tl[1])


if __name__ == '__main__':
    UserBasedReco()
    ItemBasedReco()