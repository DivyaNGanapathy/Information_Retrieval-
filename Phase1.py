import sys
import codecs
import os
import nltk
from string import punctuation
from nltk.corpus import stopwords
import urllib
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time

# Read input path from sysstem arguemnts amd list out the file names present
def readFromDirectory(inputPath):
    print("Reading from Directory...")
    fileNameList = []
    for filename1 in os.listdir(inputPath):
        #print("filename1", filename1)
        #print("Path", os.path)
        filename = inputPath + "\\" + filename1
       # print("filename2", filename)
        fileNameList.append(filename)
    return fileNameList


# Read every file from the input path directory using ISO-8859-1 encoding and then pass it through Beautifulsoup to
#convert html to text file.

def htmlParser(listOfFiles):
    print("Parsing html files...")
    textSoupList = []
    for filename in listOfFiles:
        INP = codecs.open(filename, 'r', 'ISO-8859-1', errors='ignore')
        #print(filename)
        soup = BeautifulSoup(INP, 'html.parser')
        text_soup = soup.get_text()
        textSoupList.append(text_soup)
    return textSoupList

#Function to build custom stopwords which would include the stopwords from nltk and the punctuations in english language
def buildCustomeStopwords():
    StopWords = set(nltk.corpus.stopwords.words('English') + list(punctuation))
    return StopWords

#Whole text obtained from beautiful soup is then tokenized to separate out each and evry component of the text
#Numbers are removed
#Stopwords are removed
#Length of the word is kept to greate than 1
def wordTokenizer(textSoupList,stopWords):
    print('Tokenizing the list of words...')

    wordTokenList = []
    for text_soup in textSoupList:
        words = nltk.word_tokenize(text_soup)

        words = [word for word in words if len(word) > 1]
        words = [word for word in words if not word.isnumeric()]
        words = [word.lower() for word in words]
        words = [word for word in words if word not in stopWords]
        wordTokenList.append(words)
    return wordTokenList


#Output tokens of every file is written onto a separate text document,


def generateOutput(wordTokenizerList,dest,inputPath):
    print("write")
    if not os.path.exists(dest):
        os.mkdir(dest, 0o755)

    lsitofFielsnMawse = os.listdir(inputPath)



    for x , y  in zip(lsitofFielsnMawse,wordTokenizerList):


        completeName = dest + "\\" + x.replace(".html", ".txt")
        newfile = open(completeName, 'w')
        print("Writing : ", completeName)

        newfile.write(str(y))
        #print(y)
        newfile.close()

#Word frequency is calculated using fredist function of nltk,which does a word count of every word present in the list of tokens
#Op2.txt has sorted(words) , frequency
#Op.txt has word,sorted(frequency)

import itertools
def freqDistribution(wordTokenizerList):
    print("Frequ")
    words=list(itertools.chain(*wordTokenizerList))

    fdist = nltk.FreqDist(words)
    #print(wordTokenizerList)

    outputfile = open("C:\\Users\divya\Desktop\OutputDir2\Op.txt", "w+")
    Outputfile2 = open("C:\\Users\divya\Desktop\OutputDir2\op2.txt", "w+")
    for word, frequency in fdist.items():
        #  print(u'{};{}'.format(word, frequency))
        ans = (word, frequency)
        ansstring=str(ans)
        first50=ansstring[:50]
        last50=ansstring[-50:]
        #print(ans)
        #outputfile.write(str(ans))
        outputfile.write(first50 + last50)
# concatinate the first 50 and the last 50 before putting into the outputfile


    ans2 = []
    for word, frequency in fdist.items():
        ans3 = word, frequency
        ans2.append(ans3)
        #print (ans2)
    #print("sorted words with frequency")
    #print(sorted(ans2))
    #print(len(ans2))
    sortedans2=str(sorted(ans2))


    sortedans2first50=sortedans2[:50]
    sortedlast50=sortedans2[-50 :]
    print(sortedans2first50)
    Outputfile2.write(sortedans2first50 + sortedlast50 )





################################################################################################33
start_time = time.time()

listOfFiles = ""
inputpa = sys.argv[1]
dest= sys.argv[2]

listOfFiles = readFromDirectory(inputpa)

buildCustomeStopwords()

textSoupList = htmlParser(listOfFiles)
stopWords= buildCustomeStopwords()
wordTokenizerList=wordTokenizer(textSoupList,stopWords)
print("length1 :", len(listOfFiles))
print("length2 :", len(wordTokenizerList))
freqDistribution(wordTokenizerList)
generateOutput(wordTokenizerList,dest,inputpa)

print("end")


#



print("Total Time Enlapsed in Seconds : ", (time.time() - start_time))