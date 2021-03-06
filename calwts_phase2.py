import shutil
import sys
import os
import nltk
from string import punctuation
import urllib
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import itertools
import re
import math



#######################################################################################################################
# List out the files in the input directory and read each one of them separately. It returns the list of filenames
#######################################################################################################################


def readFromDirectory():
    # print("\nReading from Directory...")
    fileNameList = []
    for filename1 in os.listdir(inputPath):
        filename = inputPath + "\\" + filename1
        fileNameList.append(filename)
    # print("--> Total files processed : ",len(fileNameList))
    return fileNameList


#######################################################################################################################
# Every file from the list is passed into an html parser to get the plain text without any html tags
#######################################################################################################################


def htmlParser(eachFile):
    textSoupList = []
    INP = open(eachFile, encoding="utf8", errors='ignore')
    soup = BeautifulSoup(INP, 'html.parser')
    text_soup = soup.get_text()
    textSoupList.append(text_soup)
    # print("--> Parsing of", len(textSoupList), "files complete")
    return textSoupList


#######################################################################################################################
# The list of stopwords is read from the given location and punctuations are added to it.
# These two together form the custom stopwords
#######################################################################################################################

def buildCustomStopwords():
    url = "https://www.csee.umbc.edu/courses/graduate/676/term%20project/stoplist.txt"
    httpfile = urlopen(url).read()
    container = httpfile.decode("utf8")
    punck=list(punctuation)
    StopWords = container + ','.join(punck)
    return StopWords

# Read stopwords from a local folder
# def buildCustomStopwords():
#     f=open("C:\\Users\divya\Dropbox\Study\IR\Stopwords.txt","r")
#
#     customstopwords=f.read()
#
#     punck=list(punctuation)
#     StopWords = customstopwords+ ','.join(punck)
#     return StopWords

#######################################################################################################################
# The plain text obtained from the html parser is now cleaned by removing the stopwords,
# removing the words of length one and the ones that occur just once
#######################################################################################################################

def cleanText(textSoupList,stopWords):
    textSoupListString = " ".join(textSoupList)
    words = nltk.word_tokenize(textSoupListString)
    words = [word for word in words if len(word) > 1]
    words = [word for word in words if not word.isnumeric()]
    words = [word for word in words if not re.search('^[0-9]+\\.[0-9]+$', word)]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in stopWords]
    return words



#######################################################################################################################
# A dictionary is formed of every (document name[k]: [v] , token[k]:[v] ,Frequency[k] : [v]
#######################################################################################################################



def freqdictionary(theWords):

    freqdicList=[]
    freq_dict={}

    textSoupListString = " ".join(theWords)
    words = nltk.word_tokenize(textSoupListString)

    for word in words:
        if word in freq_dict:
            freq_dict[word]+=1
        else:
            freq_dict[word]=1
        temp={'id':i,'freq_dict':freq_dict}

    freqdicList.append(temp)

    return freqdicList
#######################################################################################################################
# Term Frequency of every token is calculated with respect to the particular document using the formula below
#  (Number of times term t appears in a document)/ (Total number of terms in the document)
#######################################################################################################################
def getTermFreq(freqdicList):

    counter=0
    theTF = []
    for eachDoc in freqdicList:

        # print("The each Doc : ",eachDoc)
        for k in eachDoc['freq_dict']:
            # print("The freqdist of the doc : ",i)

            temp={'id':i,'term':k, 'TF': eachDoc['freq_dict'][k]/theWordsLength}
            # print("The TF of the term : ",temp)
            theTF.append(temp)

    return theTF


######################################################################################################################
# Inverse Document Frequency of every word is calculated and normalised taking into account the whole document length
# using the formula below.
# log_e(Total number of documents / Number of documents with term t in it)
#######################################################################################################################


def getIDF(allFreqDist):

    # total docs / number of docs it comes in

    print("\nGetting IDF")
    print("The total number of documents : ",numOfDocs)

    allIDF = []
    counter = 0


    # print("allfreqdicList : ",allfreqdicList)

    for eachfreqdicList in allFreqDist:
        # print("eachfreqdicList : ",eachfreqdicList)
        # print("The keys : ",eachfreqdicList['freq_dict'].keys())
        oneMore = []
        counter+=1
        for k in eachfreqdicList['freq_dict'].keys():
            count = 0
            for firstList in allFreqDist:
                if (k in firstList['freq_dict']):
                        count+=1

            temp = {'id': counter, 'term': k, 'IDF': math.log(numOfDocs/count)}
            # print("The IDF Temp : ",temp)
            oneMore.append(temp)
        allIDF.append(oneMore)
        outputdict= k + '\n' + str(count)
        writeOutput(outputdict ,"DicOut.txt")
    # print("The total IDF : ",allIDF)
    return allIDF


#################################################################
# A final TF-IDF score is calculated by the product of TF and IDF
#################################################################



def calculateTFIDF(allTFs,allIDF):

    # print("\nCalculating TFIDF")
    allTFIDF = []
    listWrite= []

    idfCounter = 0

    for x,y in zip(allTFs,allIDF):
        # print("x : ",x)
        # print("y : ",y)
        TFIDF = x['TF'] * y['IDF']
        writeStr = x['term'] + "," + str(TFIDF)
        listWrite.append(writeStr)


    writeOutput("\n".join(listWrite),str(x['id']))

    return TFIDF



#######################################################################################################################
# Output of every token in every document is written to the corresponding wts text file
# Therefore at the end of this function we have 503 files containing tokens and their TFIDF scores
#######################################################################################################################



def writeOutput(listWrite,filename):

    #filename='{:03}'.format(int(filename))

    output = Output + "\\" + filename + ".txt";
    with open(Output, "a", encoding="utf-8",errors='ignore') as f:
        f.write(listWrite)

#######################################################################################################################
# Delete the Output folder if it already exits
#######################################################################################################################

def clearOutput(path):

    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)
    else:
        raise ValueError("Error.".format(path))
    os.mkdir(path, 0o755)


#######################################################################################################################
# Input files' location are taken as Sys.argv[1] and output files location as sys.argv[2].
# A timer is started at the beginning of the preprocessing of the document and ends when all the tokens and the weights
# are written to respective output files
#######################################################################################################################



import time

startTime = time.time()

listOfFiles = ""
inputPath = "C:\\Users\divya\Dropbox\Study\IR\IRHW1\Inputfiles\\files"
Output ="C:\\Users\divya\Desktop\OutputC"
listOfFiles = readFromDirectory()
numOfDocs = len(listOfFiles)

if not os.path.exists(Output):
    os.mkdir(Output, 0o755)
else:
    clearOutput(Output)
# print("List of files : ",listOfFiles)

i=0

allTFs = []
allfreqdicList=[]

for eachFile in listOfFiles:
    i+=1
    textSoupList = htmlParser(eachFile)
    stopWords = buildCustomStopwords()
    theWords = cleanText(textSoupList,stopWords)
    # print("The words : ",theWords)
    theWordsLength = len(theWords)
    # print("The number of words : ",theWordsLength)
    freqdicList = freqdictionary(theWords)
    allfreqdicList.append(freqdicList)
    theTF = getTermFreq(freqdicList)
    allTFs.append(theTF)


# print("Freqs : ",allTFs)
allFreqDistTG = list(itertools.chain.from_iterable(allfreqdicList))
allTFsTG = list(itertools.chain.from_iterable(allTFs))


allIDF = getIDF(allFreqDistTG)
# print("All IDF : ",allIDF)



for oneTF,oneIDF in zip(allTFs,allIDF):
    allTFIDF = calculateTFIDF(oneTF,oneIDF)

endTime = time.time()
total = endTime-startTime

print("The Total time : ",total)