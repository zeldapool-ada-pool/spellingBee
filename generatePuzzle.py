# This is a sample Python script.

from english_words import get_english_words_set
import string
import random
import requests
import argparse
from pathlib import Path
import params
import inflect
from params import MAX_GERUNDS,MAX_PLURALS,MAX_WORD_COUNT,MAX_TOTAL_SCORE,MIN_PANAGRAM_COUNT,MIN_WORD_COUNT,MIN_TOTAL_SCORE


def generate_random_letters():
    length_of_string = 7
    randstring="".join(random.choice(string.ascii_lowercase) for i in range(length_of_string))
    return [*randstring]

def charCount(word):
    dict = {}
    for i in word:
        dict[i] = dict.get(i, 0) + 1
    return dict

def isPanagram(word,charSet):
    return len(charCount(word))==len(charSet)



def possible_words(lwords, charSet):
    wordslist = dict()
    for word in lwords:
        flag = 1 #default - all word has all the letters
        chars = charCount(word)

        # First entry in charset is the mandatory word. If that is not present then loop
        if charSet[0] in word:
            for key in word:
                if key not in charSet:
                    #print("found entry not in charset")
                    flag = 0
                    break
                else:
                    flag=1
                    #print("Letter "+key+" in "+word)

            if flag == 1 and len(word)>3:
                score = len(word)
                if isPanagram(word,charSet):
                    score=len(word)+7
                wordslist[word] = score
    return wordslist

def generateSpellingBeePuzzle(englishdictionary):
    validGame = False
    while not validGame:
        charSet=generate_random_letters()
        answers = possible_words(englishdictionary, charSet)
        validGame = checkValidGame(answers)
        if validGame:
            for key in answers:
                print(key + " | score |"+str(answers[key]))
    return answers

def generateMultipleSpellingBeePuzzles(englishdictionary,numPuzzle):
    spellingBeePuzzles=list()
    for i in range(numPuzzle):
        print("Loading Puzzle "+str(i))
        spellingBeePuzzles.append(generateSpellingBeePuzzle(englishdictionary))
    return spellingBeePuzzles

def loadDictionary():
    # load badwords
    file_path = Path('blacklistwords.txt')
    with open(file_path) as f:
        data = f.read()
    badwords=data.split()

    # load dictionary
    url="http://www.mieliestronk.com/corncob_lowercase.txt"
    response = requests.get(url)
    allwords = response.text.split()

    # filter out profane words
    result = [x for x in allwords if x not in badwords]
    return result

import matplotlib.pyplot as plt


def drawHexagon(page):
    # define the vertices of the hexagon
    vertices = [[0, 0], [1, 0], [1.5, 0.866], [1, 1.732], [0, 1.732], [-0.5, 0.866]]

    # plot the hexagon
    plt.plot([vertices[i][0] for i in range(6)], [vertices[i][1] for i in range(6)], 'b-')

    # show the plot
    plt.show()
    return

def checkValidGame(game):
    # initialize plural detection engine
    p = inflect.engine()

    # calculate panagrams
    panagramCount=0
    maxScore = 0
    gerunds=0
    pluralCount=0
    # gather data concerning the game
    for key in game:
        is_plural = p.plural(key) == key
        if game[key] >= 14: panagramCount += 1 #count panagrams
        if key.endswith('ing'): gerunds+=1 #count gerunds
        if is_plural: pluralCount+=1 #count plural
        maxScore+=game[key] #count score

    return (panagramCount>=MIN_PANAGRAM_COUNT) and \
           (gerunds<=MAX_GERUNDS) and \
           (maxScore<=MAX_TOTAL_SCORE) and \
           (maxScore>=MIN_TOTAL_SCORE) and \
           (pluralCount<=MAX_PLURALS) and \
           (len(game)>=MIN_WORD_COUNT) and \
           (len(game)<=MAX_WORD_COUNT)






if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('arg1', type=int, help='A required integer argument')
    args = parser.parse_args()
    generateMultipleSpellingBeePuzzles(loadDictionary(),args.arg1)






