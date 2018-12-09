#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True # Suppress .pyc files

import random

from creative_ai.pysynth import pysynth
from creative_ai.utils.menu import Menu
from creative_ai.data.dataLoader import *
from creative_ai.models.musicInfo import *
from creative_ai.models.languageModel import LanguageModel

# FIXME Add your team name
TEAM = 'YOUR NAME HERE'
LYRICSDIRS = ['the_beatles']
TESTLYRICSDIRS = ['the_beatles_test']
MUSICDIRS = ['gamecube']
WAVDIR = 'wav/'

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

def printSongLyrics(verseOne, verseTwo, chorus):
    """
    Requires: verseOne, verseTwo, and chorus are lists of lists of strings
    Modifies: nothing
    Effects:  prints the song.

    This function is done for you.
    """
    verses = [verseOne, chorus, verseTwo, chorus]

    print()
    for verse in verses:
        for line in verse:
            print((' '.join(line)).capitalize())
        print()

def trainLyricModels(lyricDirs, test=False):
    """
    Requires: lyricDirs is a list of directories in data/lyrics/
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

    for ldir in lyricDirs:
        lyrics = prepData(loadLyrics(ldir))
        model.updateTrainedData(lyrics)

    return model

def trainMusicModels(musicDirs):
    """
    Requires: musicDirs is a list of directories in data/midi/
    Modifies: nothing
    Effects:  works exactly as trainLyricsModels, except that
              now the dataLoader calls the DataLoader's loadMusic() function
              and takes a music directory name instead of an artist name.
              Returns a list of trained models in order of tri-, then bi-, then
              unigramModel objects.

    This function is done for you.
    """
    model = LanguageModel()

    for mdir in musicDirs:
        music = prepData(loadMusic(mdir))
        model.updateTrainedData(music)

    return model

def runLyricsGenerator(models):
    """
    Requires: models is a list of a trained nGramModel child class objects
    Modifies: nothing
    Effects:  generates a verse one, a verse two, and a chorus, then
              calls printSongLyrics to print the song out.
    """
    verseOne = []
    verseTwo = []
    chorus = []

    for _ in range(4):
        verseOne.append(generateTokenSentence(models, 7))
        verseTwo.append(generateTokenSentence(models, 7))
        chorus.append(generateTokenSentence(models, 9))

    printSongLyrics(verseOne, verseTwo, chorus)

def runMusicGenerator(models, songName):
    """
    Requires: models is a list of trained models
    Modifies: nothing
    Effects:  uses models to generate a song and write it to the file
              named songName.wav
    """

    verseOne = []
    verseTwo = []
    chorus = []

    for i in range(4):
        verseOne.extend(generateTokenSentence(models, 7))
        verseTwo.extend(generateTokenSentence(models, 7))
        chorus.extend(generateTokenSentence(models, 9))

    song = []
    song.extend(verseOne)
    song.extend(verseTwo)
    song.extend(chorus)
    song.extend(verseOne)
    song.extend(chorus)

    pysynth.make_wav(song, fn=songName)

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
                rank = ((((len(lines) - (i + 1)) / len(lines))) * 100)
                print('You are better than ' + str('{:.1f}'.format(rank)) + '% of people who have played this game')
                print()
        i += 1
    if count == 0:
        print('You have never played before using this unique username!')
        print()

def playGame():
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
        beginnerMode(numOfHeadlines)
    elif dMode == '2':
        easyMode(numOfHeadlines)
    elif dMode == '3':
        mediumMode(numOfHeadlines)
    elif dMode == '4':
        hardMode(numOfHeadlines)
    else:
        impossibleMode(numOfHeadlines)


def beginnerMode(numHeadlines):
    print()
    numUserRight = 0
    numHeadLinesWentThrough = 0
    numAIRight = 0
    percentChanceOfAIGettingItRight = 0
    print('Beginner Mode in progress...')

def easyMode(numHeadlines):
    print()
    numUserRight = 0
    numHeadLinesWentThrough = 0
    numAIRight = 0
    percentChanceOfAIGettingItRight = 0
    print('Easy Mode in progress...')

def mediumMode(numHeadlines):
    print()
    numUserRight = 0
    numHeadLinesWentThrough = 0
    numAIRight = 0
    percentChanceOfAIGettingItRight = 0
    print('Medium Mode in progress...')

def hardMode(numHeadlines):
    print()
    numUserRight = 0
    numHeadLinesWentThrough = 0
    numAIRight = 0
    percentChanceOfAIGettingItRight = 0
    print('Hard Mode in progress...')

def impossibleMode(numHeadlines):
    print()
    numUserRight = 0
    numHeadLinesWentThrough = 0
    numAIRight = 0
    percentChanceOfAIGettingItRight = 0
    print('Impossible Mode in progress...')

def __gen_colors(n):
    possible_foreground = list(range(30, 38)) + list(range(90, 98))
    possible_background = list(range(40, 48)) + list(range(100, 108))
    fx = n % len(possible_foreground)
    bx = (n * 2 - 17 * 3029) % len(possible_background)
    f_hsh = possible_foreground[fx]
    b_hsh = possible_background[bx]

    fmt = '\033[{0};{1}m'
    # \e[103m with \e[96m is elixir
    if n == 68: return fmt.format(103, 96)
    #\e[43m  with \e[37m is felix
    if n == 118: return fmt.format(43, 37)
    return fmt.format(f_hsh, b_hsh)

def __reset_colors(n):
    # default \e[49m \e[39m
    return '\033[49;39m'

###############################################################################
# End Core
###############################################################################

###############################################################################
# Main
###############################################################################

PROMPT1 = __gen_colors(350) + 'Print Instructions'


PROMPT = [
    'Print Instructions',
    'Print High Scores',
    'Print Rank Based on UserName',
    'Play the Game',
    'Change Username',
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

              It prompts the user to choose to generate either lyrics or music.
    """

    mainMenu = Menu(PROMPT)

    print()
    print('Welcome to: "Commit to the Fake"! Please input your username and select an option to continue.'.format(TEAM))
    print()
    userName = input('User name: ')
    print()
    print('Hello, ' + userName + '!')
    print()
    while True:
        userInput = mainMenu.getChoice()
        print ()
        if userInput == 1:
            print(INSTRUCTIONS)
        elif userInput == 2:
            printHighScores()
        elif userInput == 3:
            printRankBasedOnTotalPlayers(userName)
        elif userInput == 4:
            playGame()
        elif userInput == 5:
            print('Enter in your new user name.')
            userName = input('User name: ')
            print('Hello, ' + userName + '!')
            print()
        elif userInput == 6:
            print('Thank you for playing "Commit to the Fake"!'.format(TEAM))
            sys.exit()

if __name__ == '__main__':
    main()
    # note that if you want to individually test functions from this file,
    # you can comment out main() and call those functions here. Just make
    # sure to call main() in your final submission of the project!
