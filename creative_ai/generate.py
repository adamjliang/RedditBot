#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True # Suppress .pyc files

import random
import praw
import pdb
import re
import os

# Create the Reddit instance
reddit = praw.Reddit('bot1')


import spacy
nlp = spacy.load("en_core_web_sm")

from creative_ai.utils.menu import Menu
from creative_ai.data.dataLoader import *
from creative_ai.models.musicInfo import *
from creative_ai.models.languageModel import LanguageModel

# FIXME Add your team name
TEAM = 'Lets Git This Bread'
LYRICSDIRS = ['headlinesagain']
TESTLYRICSDIRS = ['headlines']

def output_models(val, output_fn = None):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  outputs the dictionary val to the given filename. Used
              in Test mode.

    This function has been done for you.
    """
    from pprint import pprint
    if output_fn == None:
        print("No Filename Given")
        return
    with open('TEST_OUTPUT/' + output_fn, 'wt') as out:
        pprint(val, stream=out)

def sentenceTooLong(desiredLength, currentLength):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  returns a bool indicating whether or not this sentence should
              be ended based on its length.

    This function has been done for you.
    """
    STDEV = 1
    val = random.gauss(currentLength, STDEV)
    return val > desiredLength

def printHeadline(verseOne):
    """
    Requires: verseOne, verseTwo, and chorus are lists of lists of strings
    Modifies: nothing
    Effects:  prints the song.

    This function is done for you.
    """
    myString = ""
    for line in verseOne:
        myString += ((' '.join(line)).capitalize())
    return myString

def trainHeadlineModels(headlineDirs, test=False):
    """
    Requires: lyricDirs is a list of directories in data/headlines/
    Modifies: nothing
    Effects:  loads data from the folders in the lyricDirs list,
              using the pre-written DataLoader class, then creates an
              instance of each of the NGramModel child classes and trains
              them using the text loaded from the data loader. The list
              should be in tri-, then bi-, then unigramModel order.
              Returns the list of trained models.

    This function is done for you.
    """
    model = LanguageModel()

    for hdir in headlineDirs:
        headline = prepData(loadLyrics(hdir))
        model.updateTrainedData(headline)

    return model


def runHeadlineGenerator(models):
    """
    Requires: models is a list of a trained nGramModel child class objects
    Modifies: nothing
    Effects:  generates a verse one, a verse two, and a chorus, then
              calls printSongLyrics to print the song out.
    """
    verseOne = []
    myBool = True

    while (myBool):
        verseOne = []
        for _ in range(1):
            verseOne.append(generateTokenSentence(models, 12))
        myString = ''
        for line in verseOne:
            myString += ((' '.join(line)).capitalize())
        doc = nlp(myString)
        i = len(doc)
        if checkToSeeIfHeadlineIsUsed(myString):
            if doc[i - 1].pos_ != 'DET' and doc[i - 1].pos_ != 'ADJ' and doc[i - 1].pos_ != 'ADP':
                myString2 = printHeadline(verseOne)
                myBool = False
            else:
                myBool = True
    return myString2


###############################################################################
# Begin Core >> FOR CORE IMPLEMENTION, DO NOT EDIT OUTSIDE OF THIS SECTION <<
###############################################################################

def generateTokenSentence(model, desiredLength):
    """
    Requires: model is a single trained languageModel object.
              desiredLength is the desired length of the sentence.
    Modifies: nothing
    Effects:  returns a list of strings where each string is a word in the
              generated sentence. The returned list should NOT include
              any of the special starting or ending symbols.
              For more details about generating a sentence using the
              NGramModels, see the spec.
    """
    sentence = ['^::^', '^:::^']
    while not sentenceTooLong(desiredLength, len(sentence) - 2):
        sentence.append(model.getNextToken(sentence))
        if '$:::$' in sentence:
            return sentence[2:-1]
    return sentence[2:]

###############################################################################
# End CORE
###############################################################################

###############################################################################
# Begin REACH
###############################################################################


def checkToSeeIfHeadlineIsUsed(string):
    ifstream = open('allHeadlines.txt')
    lines = ifstream.readlines()
    ifstream.close()
    i = 0
    count = 0
    while i < len(lines):
        if lines[i][:-1] == string:
            count += 1
        i += 1
    if count == 0:
        return True
    else:
        return False

def printHighScores():
    # Read file contents
    ifstream = open('leaderboardData.txt')
    lines = ifstream.readlines()
    ifstream.close()

    for i in range(0, 10):
        print((str(i+1)) + ') ' + lines[i])


def printRankBasedOnTotalPlayers(userName):
    # Read file contents
    count = 0
    aUserName = ""
    ifstream = open('leaderboardData.txt')
    lines = ifstream.readlines()
    ifstream.close()
    # print(len(lines)) prints the amount of lines in the the txt file
    i = 0
    rank = 0
    # for letters in lines[0]: this does one letter per line
    # for words in lines: this does one line of words per line
    #  words in lines:
    # print(words[0]) This prints the first letter of each line
    while i < len(lines):
        if count == 0:
            aUserName = ''
            while '|' not in aUserName:
                for letters in lines[i]:
                    if '|' not in aUserName:
                        aUserName = aUserName + letters
            aUserName = aUserName[:-1]
            if aUserName == userName:
                count += 1
                # length of how many lines - current rank all divided by length of how many lines
                rank = ((((len(lines) - 1 - i) / (len(lines) - 1))) * 100)
                print('You are better than ' + str('{:.1f}'.format(rank)) + '% of people who have played this game')
                print()
        i += 1
    if count == 0:
        print('You have never played before using this unique username!')
        print()

def playGame(userName):
    # Create the Reddit instance
    reddit = praw.Reddit('bot1')

    # posting generated text in reddit
    subreddit = reddit.subreddit('eecs183')

    subreddit.submit('Commit to the Fake', 'Welcome to "Commit to the Fake"')

    print('Would you like to play with a short, medium, long, or very long game?')
    print()
    typeOfGame = input('Type of game: ')
    typeOfGame = typeOfGame.lower()
    if typeOfGame == 'short' or typeOfGame == 's':
        numOfHeadlines = 10
    elif typeOfGame == 'medium' or typeOfGame == 'm':
        numOfHeadlines = 25
    elif typeOfGame == 'long' or typeOfGame == 'l':
        numOfHeadlines = 50
    elif typeOfGame == 'very long' or typeOfGame == 'v':
        numOfHeadlines = 100
    else:
        numOfHeadlines = 0
    while not (numOfHeadlines == 10 or numOfHeadlines == 25 or numOfHeadlines == 50 or numOfHeadlines == 100):
        print('Input must be short, s, medium, m, long, l, very long, or v')
        print()
        typeOfGame = input("Type of game: ")
        typeOfGame = typeOfGame.lower()
        if typeOfGame == 'short' or typeOfGame == 's':
            numOfHeadlines = 10
        if typeOfGame == 'medium' or typeOfGame == 'm':
            numOfHeadlines = 25
        if typeOfGame == 'long' or typeOfGame == 'l':
            numOfHeadlines = 50
        if typeOfGame == 'very long' or typeOfGame == 'v':
            numOfHeadlines = 100
    print()
    print('What difficulty mode would you like to play on?')
    print()
    dMode = input('Type 1 for Beginner, 2 for Easy, 3 for Medium, 4 for Hard, 5 for Impossible: ')
    while not (dMode == '1' or dMode == '2' or dMode == '3' or dMode == '4' or dMode == '5'):
        print()
        print('That is not a valid mode! Input must be 1, 2, 3, 4, or 5. Try again.')
        print()
        dMode = input('Type 1 for Beginner, 2 for Easy, 3 for Medium, 4 for Hard, 5 for Impossible: ')
    if dMode == '1':
        beginnerMode(userName, numOfHeadlines)
    elif dMode == '2':
        easyMode(userName, numOfHeadlines)
    elif dMode == '3':
        mediumMode(userName, numOfHeadlines)
    elif dMode == '4':
        hardMode(userName, numOfHeadlines)
    else:
        impossibleMode(userName, numOfHeadlines)


def beginnerMode(userName, numHeadlines):
    print()
    numUserRight = 0
    # n represent the number of headlines that we went through
    n = 0
    numAIRight = 0
    percentChanceOfAIGettingItRight = 1.0 / 10.0
    while n < numHeadlines:
        myString = ''
        # Possibly include myRandomInt
        realLeft = 2
        fakeLeft = 1
        gameList = ['', '', '']
        gameListCount = 0
        count = 0
        i = 0
        ifstream = open('allHeadlines.txt')
        lines = ifstream.readlines()
        ifstream.close()
        # populate gameList with one fake and two real headlines, random order
        while gameListCount < 3:
            myString = lines[random.randint(0, len(lines) - 1)]
            if realLeft > 0 and fakeLeft > 0:
                randomInt = random.randint(1, 2)
                if randomInt == 1:
                    gameList[gameListCount] = myString[:-1]
                    realLeft -= 1
                elif randomInt == 2:
                    headlineTrained = False
                    if not headlineTrained:
                        headlineModel = trainHeadlineModels(TESTLYRICSDIRS)
                        headlineTrained = True
                    gameList[gameListCount] = runHeadlineGenerator(headlineModel)
                    fakeLeft -= 1
            elif realLeft > 0 and fakeLeft == 0:
                gameList[gameListCount] = myString[:-1]
                realLeft -= 1
            elif fakeLeft > 0 and realLeft == 0:
                headlineTrained = False
                if not headlineTrained:
                    headlineModel = trainHeadlineModels(TESTLYRICSDIRS)
                    headlineTrained = True
                gameList[gameListCount] = runHeadlineGenerator(headlineModel)
                fakeLeft -= 1
            gameListCount += 1
        # here the reddit bot will output the titles but ill just do it here for testing
        print(gameList)
        print('Choose which one is the fake!! (1/2/3)')
        choice = input('Choice: ')
        while not (choice == '1' or choice == '2' or choice == '3'):
            print('Invalid choice! Choice must be 1, 2, or 3')
            choice = input('Choice: ')

        while i < len(lines):
            if gameList[int(choice) - 1] == lines[i][:-1]:
                count += 1
            i += 1

        if count == 0:
            print()
            print('Correct!!')
            numUserRight += 1
        else:
            print()
            print('Incorrect!!')

        randomIntForAI = random.randint(1, 10)
        if randomIntForAI == 1:
            numAIRight += 1
            print('The bot got it right!')
            print()
        else:
            print('The bot got it wrong!')
            print()

        n += 1
    print('Amount you got right: ' + str(numUserRight))
    print('Amount bot got right: ' + str(numAIRight))
    if numUserRight > numAIRight:
        multiplier = 1
        if numHeadlines == 10:
            multiplier = 1
        if numHeadlines == 25:
            multiplier = 3
        if numHeadlines == 50:
            multiplier = 7
        if numHeadlines == 100:
            multiplier = 15
        totalPointsAdded = 0 * multiplier
        print('Congratulations, you beat the bot! We have added ' + str(
            totalPointsAdded) + ' points to your total score!')
        # Read file contents
        count = 0
        aUserName = ''
        ifstream = open('leaderboardData.txt')
        lines = ifstream.readlines()
        ifstream.close()
        # print(len(lines)) prints the amount of lines in the the txt file
        i = 0
        while i < len(lines):
            # not needed but might wack up the indent
            if count == 0:
                aUserName = ''
                while '|' not in aUserName:
                    for letters in lines[i]:
                        if '|' not in aUserName:
                            aUserName = aUserName + letters
                aUserName = aUserName[:-1]
                if aUserName == userName:
                    count += 1
            i += 1
        if count == 0:
            f = open('leaderboardData.txt', 'a')  # Open file
            f.write(
                userName + '| Beginner Wins: 1 Easy Wins: 0 Medium Wins: 0 Hard Wins: 0 Impossible Wins: 0 Total Wins: 0 Total Score: ' + str(
                    totalPointsAdded) + '|' + '\n')  # Write string
            f.close()  # Close the file
            while not isLeaderboardSorted():
                sortLeaderboard()
        else:
            # Read file contents
            count = 0
            aUserName = ''
            ifstream = open('leaderboardData.txt')
            lines = ifstream.readlines()
            ifstream.close()
            # print(len(lines)) prints the amount of lines in the the txt file
            i = 0
            f = open('leaderboardData.txt', 'w')  # Open file
            while i < len(lines):
                # not needed but might wack up the indent
                if count == 0:
                    aUserName = ''
                    while '|' not in aUserName:
                        for letters in lines[i]:
                            if '|' not in aUserName:
                                aUserName = aUserName + letters
                    aUserName = aUserName[:-1]
                    if aUserName == userName:
                        origTotalScore = ''
                        amountOfBeginnerWinsForThisUser = int(lines[i][len(userName) - 1 + 18])
                        amountOfBeginnerWinsForThisUser += 1
                        for letters in lines[i][-8:]:
                            if letters == '0' or letters == '1' or letters == '2' or letters == '3' or letters == '4' \
                                    or letters == '5' or letters == '6' or letters == '7' or letters == '8' or letters == '9':
                                origTotalScore += letters
                        intOrigTotalScore = int(origTotalScore)
                        intTotalPointsAdded = int(totalPointsAdded)
                        intTotalPointsAdded += intOrigTotalScore
                        f.write(userName + '| Beginner Wins: ' + str(amountOfBeginnerWinsForThisUser) + ' Easy Wins: 0 Medium Wins: 0 Hard Wins: 0 Impossible Wins: 0 Total Wins: 0 Total Score: ' + str(
                            intTotalPointsAdded) + '|' + '\n')  # Write string
                    else:
                        f.write(lines[i])
                i += 1
            f.close()
            while not isLeaderboardSorted():
                sortLeaderboard()
    elif numUserRight == numAIRight:
        print('Sorry, you have tied the bot. No points have been added to your total score.')
    else:
        print('Sorry, you lost to the bot. No points have been added to your total score')

def easyMode(userName, numHeadlines):
    print()
    numUserRight = 0
    #n represent the number of headlines that we went through
    n = 0
    numAIRight = 0
    percentChanceOfAIGettingItRight = 1.0/3.0
    while n < numHeadlines:
        theFakeIndex = 0
        myString = ''
        #Possibly include myRandomInt
        realLeft = 2
        fakeLeft = 1
        gameList = ['', '', '']
        gameListCount = 0
        count = 0
        i = 0
        ifstream = open('allHeadlines.txt')
        lines = ifstream.readlines()
        ifstream.close()
        #populate gameList with one fake and two real headlines, random order
        while gameListCount < 3:
            myString = lines[random.randint(0, len(lines) - 1)]
            if realLeft > 0 and fakeLeft > 0:
                randomInt = random.randint(1, 2)
                if randomInt == 1:
                    gameList[gameListCount] = myString[:-1]
                    realLeft -= 1
                elif randomInt == 2:
                    headlineTrained = False
                    if not headlineTrained:
                        headlineModel = trainHeadlineModels(TESTLYRICSDIRS)
                        headlineTrained = True
                    gameList[gameListCount] = runHeadlineGenerator(headlineModel)
                    fakeLeft -= 1
                    theFakeIndex = gameListCount
            elif realLeft > 0 and fakeLeft == 0:
                gameList[gameListCount] = myString[:-1]
                realLeft -= 1
            elif fakeLeft > 0 and realLeft == 0:
                headlineTrained = False
                if not headlineTrained:
                    headlineModel = trainHeadlineModels(TESTLYRICSDIRS)
                    headlineTrained = True
                gameList[gameListCount] = runHeadlineGenerator(headlineModel)
                fakeLeft -= 1
                theFakeIndex = gameListCount
            gameListCount += 1
        #here the reddit bot will output the titles but ill just do it here for testing
        # Get the top 5 values from our subreddit
        subreddit = reddit.subreddit('eecs183')
        for submission in subreddit.hot(limit=10):

            if re.search("Commit to the Fake", submission.title, re.IGNORECASE):
                # Reply to the post
                verses = ['1', '2', '3', '4']
                submission.reply('1) "' + gameList[0] + '",' + '\n' + ' 2) "' + gameList[1] + '",' + '\n' + ' 3) "' + gameList[2] + '"')
        #print(gameList)
        print('Choose which one is the fake!! (1/2/3)')
        choice = input('Choice: ')
        while not (choice == '1' or choice == '2' or choice == '3'):
            print('Invalid choice! Choice must be 1, 2, or 3')
            choice = input('Choice: ')

        while i < len(lines):
            if gameList[int(choice) - 1] == lines[i][:-1]:
                count += 1
            i += 1

        if count == 0:
            print()
            print('Correct!!')
            numUserRight += 1
        else:
            print()
            print('Incorrect!!')
            print()
            print('The correct answer was: ' + gameList[theFakeIndex][:-1])

        randomIntForAI = random.randint(1, 3)
        if randomIntForAI == 1:
            numAIRight += 1
            print('The bot got it right!')
            print()
        else:
            print('The bot got it wrong!')
            print()

        n += 1
    print('Amount you got right: ' + str(numUserRight))
    print('Amount bot got right: ' + str(numAIRight))
    if numUserRight > numAIRight:
        multiplier = 1
        if numHeadlines == 10:
            multiplier = 1
        if numHeadlines == 25:
            multiplier = 3
        if numHeadlines == 50:
            multiplier = 7
        if numHeadlines == 100:
            multiplier = 15
        totalPointsAdded = 1 * multiplier
        print('Congratulations, you beat the bot! We have added ' + str(totalPointsAdded) +' points to your total score!')
        # Read file contents
        count = 0
        aUserName = ''
        ifstream = open('leaderboardData.txt')
        lines = ifstream.readlines()
        ifstream.close()
        # print(len(lines)) prints the amount of lines in the the txt file
        i = 0
        while i < len(lines):
            # not needed but might wack up the indent
            if count == 0:
                aUserName = ''
                while '|' not in aUserName:
                    for letters in lines[i]:
                        if '|' not in aUserName:
                            aUserName = aUserName + letters
                aUserName = aUserName[:-1]
                if aUserName == userName:
                    count += 1
            i+=1
        if count == 0:
            f = open('leaderboardData.txt', 'a')  # Open file
            f.write(userName +  '| Beginner Wins: 0 Easy Wins: 1 Medium Wins: 0 Hard Wins: 0 Impossible Wins: 0 Total Wins: 0 Total Score: ' + str(totalPointsAdded) + '|' + '\n')  # Write string
            f.close()  # Close the file
            while not isLeaderboardSorted():
                sortLeaderboard()
        else:
            # Read file contents
            count = 0
            aUserName = ''
            ifstream = open('leaderboardData.txt')
            lines = ifstream.readlines()
            ifstream.close()
            # print(len(lines)) prints the amount of lines in the the txt file
            i = 0
            f = open('leaderboardData.txt', 'w')  # Open file
            while i < len(lines):
                # not needed but might wack up the indent
                if count == 0:
                    aUserName = ''
                    while '|' not in aUserName:
                        for letters in lines[i]:
                            if '|' not in aUserName:
                                aUserName = aUserName + letters
                    aUserName = aUserName[:-1]
                    if aUserName == userName:
                        origTotalScore = ''
                        amountOfEasyWinsForThisUser = int(lines[i][len(userName) - 1 + 31])
                        amountOfEasyWinsForThisUser += 1
                        for letters in lines[i][-8:]:
                            if letters == '0' or letters == '1' or letters == '2' or letters == '3' or letters == '4'\
                            or letters == '5' or letters == '6' or letters == '7' or letters == '8' or letters == '9':
                                    origTotalScore += letters
                        intOrigTotalScore = int(origTotalScore)
                        intTotalPointsAdded = int(totalPointsAdded)
                        intTotalPointsAdded += intOrigTotalScore
                        f.write(userName + '| Beginner Wins: 0 Easy Wins: ' + str(amountOfEasyWinsForThisUser) + ' Medium Wins: 0 Hard Wins: 0 Impossible Wins: 0 Total Wins: 0 Total Score: ' + str(intTotalPointsAdded) + '|' + '\n')  # Write string
                    else:
                        f.write(lines[i])
                i+=1
            f.close()
            while not isLeaderboardSorted():
                sortLeaderboard()
    elif numUserRight == numAIRight:
        print('Sorry, you have tied the bot. No points have been added to your total score.')
    else:
        print('Sorry, you lost to the bot. No points have been added to your total score')

def mediumMode(userName, numHeadlines):
    print()
    numUserRight = 0
    numHeadLinesWentThrough = 0
    numAIRight = 0
    percentChanceOfAIGettingItRight = 0
    print('Medium Mode in progress...')

def hardMode(userName, numHeadlines):
    print()
    numUserRight = 0
    numHeadLinesWentThrough = 0
    numAIRight = 0
    percentChanceOfAIGettingItRight = 0
    print('Hard Mode in progress...')

def impossibleMode(userName, numHeadlines):
    print()
    numUserRight = 0
    numHeadLinesWentThrough = 0
    numAIRight = 0
    percentChanceOfAIGettingItRight = 0
    print('Impossible Mode in progress...')

def userNamePrompt():
    print()
    userName = input('User name: ')
    print()

    # Read file contents
    count = 0
    aUserName = ''
    ifstream = open('usernamesAndPasswords.txt')
    linesBeginning = ifstream.readlines()
    ifstream.close()
    # print(len(lines)) prints the amount of lines in the the txt file
    i = 0
    while i < len(linesBeginning):
        if count == 0:
            aUserName = ''
            while ':' not in aUserName:
                for letters in linesBeginning[i]:
                    if ':' not in aUserName:
                        aUserName = aUserName + letters
            aUserName = aUserName[:-1]
            if aUserName == userName:
                count += 1
                print('Enter your password so we know it is really you!')
                password = input('Password (type "escape" to go back): ')
                if password.lower() == 'escape':
                    userName = userNamePrompt()
                else:
                    authenticatePassword(userName, password)
                    print()
                    print('Welcome back, ' + userName + '!')
                    NEWUSERNAME = 0
        i += 1
    if count == 0:
        print('Wow, a new user! Welcome, ' + userName + '!')
        NEWUSERNAME = 1
        print()
        print('Enter a password for this user name for later use')
        password = input('Password (type "escape" to go back): ')
        if password.lower() == 'escape':
            userName = userNamePrompt()
        else:
            f = open('usernamesAndPasswords.txt', 'a')  # Open file
            f.write('\n' + userName + ':' + password + '|')  # Write string
            f.close()  # Close the file

    print()
    return userName


def authenticatePassword(userName, password):
    # Read file contents
    personalCount = 0
    count = 0
    i = 0
    wrongTimesEntered = 0
    timesLeftBeforeExit = 10
    aUserName = ''
    aPassword = '1$%d8cds823jr'
    count = 0
    ifstream = open('usernamesAndPasswords.txt')
    linesPasswords = ifstream.readlines()
    ifstream.close()
    while i < len(linesPasswords):
        personalCount = 0
        if count == 0:
            aUserName = ''
            while ':' not in aUserName:
                for letters in linesPasswords[i]:
                    if ':' not in aUserName:
                        aUserName = aUserName + letters
            aUserName = aUserName[:-1]
            if aUserName == userName:
                aPassword = ''
                for letters in linesPasswords[i]:
                    if ':' not in aPassword and personalCount == 0:
                        aPassword = aPassword + letters
                    if ':' in aPassword and personalCount == 0:
                        personalCount = 1
                    if ':' in aPassword and personalCount == 1:
                        aPassword = ''
                        personalCount = 2
                    if personalCount == 2 and '|' not in aPassword:
                        aPassword = aPassword + letters
                aPassword = aPassword[1:-1]
                if aPassword == password:
                    count += 1
                else:
                    while not (password == aPassword):
                        timesLeftBeforeExit -= 1
                        if (timesLeftBeforeExit == 0):
                            print('You have entered your password incorrectly too many times, goodbye!')
                            sys.exit()
                        print('Your password is incorrect. Please retry! You have ' + str(timesLeftBeforeExit) + ' times left (case sensitive!!)')
                        password = input('Password: ')

        i += 1

def welcomeMessage():
    print()
    print('Welcome to: "Commit to the Fake"! Please input your username and select an option to continue.'.format(TEAM))

def endMessage():
    print('Thank you for playing "Commit to the Fake"!'.format(TEAM))

def __gen_colors(n):
    possible_foreground = list(range(30, 38)) + list(range(90, 98))
    possible_background = list(range(40, 48)) + list(range(100, 108))
    fx = n % len(possible_foreground)
    bx = (n * 2 - 17 * 3029) % len(possible_background)
    f_hsh = possible_foreground[fx]
    b_hsh = possible_background[bx]

    fmt = '\033[{0};{1}m'
    if n == 68: return fmt.format(103, 96)
    if n == 118: return fmt.format(43, 37)
    return fmt.format(f_hsh, b_hsh)

def __reset_colors(n):
    # default \e[49m \e[39m
    return '\033[49;39m'

def sortLeaderboard():
    '''
     Requires: leaderboardData.txt is in the proper format
     Modifies: leaderboardData.txt
     Effects: returns a new list of a sorted leaderboard and then overwrites the current file
     Sorts so that highest score is on top and the lowest total score
     is on the bottom and the data is maintained while sorting
     '''
    i = 0
    temp = ''
    ifstream = open('leaderboardData.txt')
    linesToSeeTotalScore = ifstream.readlines()
    ifstream.close()
    while i < len(linesToSeeTotalScore) - 1:
        stringTotalScore = ''
        stringTotalScorePlusOne = ''
        stringLine = ''
        stringLinePlusOne = ''
        for letters in linesToSeeTotalScore[i][-8:]:
            if letters == '0' or letters == '1' or letters == '2' or letters == '3' or letters == '4'\
                    or letters == '5' or letters == '6' or letters == '7' or letters == '8' or letters == '9':
                stringTotalScore += letters
        for letters in linesToSeeTotalScore[i+1][-8:]:
            if letters == '0' or letters == '1' or letters == '2' or letters == '3' or letters == '4'\
                    or letters == '5' or letters == '6' or letters == '7' or letters == '8' or letters == '9':
                stringTotalScorePlusOne += letters
        if int(stringTotalScorePlusOne) > int(stringTotalScore):
            for letters in linesToSeeTotalScore[i]:
                stringLine += letters
            for letters in linesToSeeTotalScore[i + 1]:
                stringLinePlusOne += letters
            #reversing the lines
            temp = stringLine
            stringLine = stringLinePlusOne
            stringLinePlusOne = temp
            linesToSeeTotalScore[i] = stringLine
            linesToSeeTotalScore[i+1] = stringLinePlusOne
        i += 1
    i = 0
    print(len(linesToSeeTotalScore))
    f = open('leaderboardData.txt', 'w')  # Open file
    while i < len(linesToSeeTotalScore):
        f.write(linesToSeeTotalScore[i])  # Write string
        i += 1
    f.close()  # Close the file



def isLeaderboardSorted():
    '''
    Requires: leaderboardData.txt is in the proper format
    Modifies: Nothing
    Effects: returns true if the leaderboard is sorted and returns false if the leaderboard is not sorted
    '''
    i = 0
    check = 0
    stringTotalScore = ''
    stringTotalScorePlusOne = ''
    ifstream = open('leaderboardData.txt')
    linesToSeeTotalScore = ifstream.readlines()
    ifstream.close()
    while i < len(linesToSeeTotalScore) - 1:
        stringTotalScore = ''
        stringTotalScorePlusOne = ''
        for letters in linesToSeeTotalScore[i][-8:]:
            if letters == '0' or letters == '1' or letters == '2' or letters == '3' or letters == '4'\
                    or letters == '5' or letters == '6' or letters == '7' or letters == '8' or letters == '9':
                stringTotalScore += letters
        for letters in linesToSeeTotalScore[i+1][-8:]:
            if letters == '0' or letters == '1' or letters == '2' or letters == '3' or letters == '4'\
                    or letters == '5' or letters == '6' or letters == '7' or letters == '8' or letters == '9':
                stringTotalScorePlusOne += letters
        if int(stringTotalScorePlusOne) > int(stringTotalScore):
            check += 1
        i += 1
    if check == 0:
        return True
    else:
        return False

###############################################################################
# End REACH FUNCTIONS
###############################################################################

###############################################################################
# BEGIN Main FUNCTION FOR REACH
###############################################################################

PROMPT1 = __gen_colors(350) + 'Print Instructions'


PROMPT = [
    'Print Instructions',
    'Print High Scores',
    'Print Rank Based on UserName',
    'Play the Game',
    'Change User',
    'Quit the game'
]

INSTRUCTIONS = 'Welcome to Commit the Fake. To play the game, please selection option 4.\n\
You will have the option to play a short, medium, long, or very long game.\n\
A short game will consist of 10 headlines, a medium game will consist of 25 headlines,\n\
a long game will consist of 50 headlines, and a very long game will consist of 100 headlines.\n\
The whole goal of the game is to pick the fake headline more often than the bot does.\n\
There are five difficulty levels for the bot: Beginner, Easy, Medium, Hard, and Impossible.\n\
Your total score is calculated using the formula below: \n\
Beginner Mode wins will increase your total score by 0 points. \n\
Easy Mode wins will increase your total score by 1 point. \n\
Medium Mode wins will increase your total score by 3 points. \n\
Hard Mode wins will increase your total score by 5 points. \n\
Impossible Mode wins will increase your total score by 10000 points. \n\
Note that you must BEAT the bot in order for it to count as a win. \n\
BONUS: Depending on the length of the game, your score will get multiplied as follows: \n\
Short games will multiply the amount of points you receive for that game by 1. \n\
Medium games will multiply the amount of points you receive for that game by 3. \n\
Long games will multiply the amount of points you receive for that game by 7. \n\
Very long games will multiply the amount of points you receive for that game by 15. \n\
'



def main():
    """
    Requires: Nothing
    Modifies: Nothing
    Effects:  This is your main function, which is done for you. It runs the
              entire generator program for both the reach and the core.

              It prompts the user to choose to generate either headlines or music.
    """

    mainMenu = Menu(PROMPT)
    welcomeMessage()
    userName = userNamePrompt()
    while True:
        userInput = mainMenu.getChoice()
        if userInput == 1:
            print(INSTRUCTIONS)
        elif userInput == 2:
            printHighScores()
        elif userInput == 3:
            printRankBasedOnTotalPlayers(userName)
        elif userInput == 4:
            playGame(userName)
        elif userInput == 5:
            userName = userNamePrompt()
        elif userInput == 6:
            endMessage()
            sys.exit()

if __name__ == '__main__':
    main()
    # note that if you want to individually test functions from this file,
    # you can comment out main() and call those functions here. Just make
    # sure to call main() in your final submission of the project!
