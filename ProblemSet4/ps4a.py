# The 6.00 Word Game

import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordList: list of strings
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print("  ", len(wordList), "words loaded.")
    return wordList

def getFrequencyDict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def getWordScore(word, n):
    """
    Returns the score for a word. Assumes the word is a valid word.

    The score for a word is the sum of the points for letters in the
    word, multiplied by the length of the word, PLUS 50 points if all n
    letters are used on the first turn.

    Letters are scored as in Scrabble; A is worth 1, B is worth 3, C is
    worth 3, D is worth 2, E is worth 1, and so on (see SCRABBLE_LETTER_VALUES)

    word: string (lowercase letters)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    returns: int >= 0
    """
    word = word.lower()
    score = 0
    for letter in word:
        score += SCRABBLE_LETTER_VALUES[letter]
    score *= len(word)
    if len(word) == n:
        score += 50
    return score


# Problem #2: Make sure you understand how this function works and what it does!
#
def displayHand(hand):
    """
    Displays the letters currently in the hand.

    For example:
    >>> displayHand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
    a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter,end=" ")       # print all on the same line
    print()                             # print an empty line

#
# Problem #2: Make sure you understand how this function works and what it does!
#
def dealHand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    numVowels = n // 3
    
    for i in range(numVowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(numVowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

#
# Problem #2: Update a hand by removing letters
#

def updateHand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    word = word.lower()
    newHand = hand.copy()
    for letter in word: 
        newHand[letter] = newHand.get(letter, 0) - 1
    return newHand

#
# Problem #3: Test word validity
#
def isValidWord(word, hand, wordList):
    """
    Returns True if word is in the wordList and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or wordList.

    word: string
    hand: dictionary (string -> int)
    wordList: list of lowercase strings
    """
    word = word.lower()
    handCopy = hand.copy()
    if word in wordList:
        for letter in word:
            if handCopy.get(letter, 0) > 0:
                handCopy[letter] -= 1
            else:
                return False
        return True
    else:
        return False


#
# Problem #4: Playing a hand
#

def calculateHandlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    length = 0
    for letter in hand:
        length += hand[letter]
    return length



def playHand(hand, wordList, n):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    * The user may input a word or a single period (the string ".") 
        to indicate they're done playing
    * Invalid words are rejected, and a message is displayed asking
        the user to choose another word until they enter a valid word or "."
    * When a valid word is entered, it uses up letters from the hand.
    * After every valid word: the score for that word is displayed,
        the remaining letters in the hand are displayed, and the user
        is asked to input another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when there are no more unused letters or the user
        inputs a "."

    hand: dictionary (string -> int)
    wordList: list of lowercase strings
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    
    """
    word = ''
    score = 0       
    # Keep track of the total score
    totalScore = 0
    # As long as there are still letters left in the hand:
    handLength = calculateHandlen(hand)
    while handLength > 0:
        # Display the hand
        handString = ''
        for letter in hand:
            handString += hand[letter] * letter
        print('Current Hand:', handString)
        # Ask user for input
        inputWord = input('Enter word, or a "." to indicate that you are finished: ')   
        # If the input is a single period:
        inputWord = inputWord.lower()
        if inputWord == '.':
            print('Goodbye! Total score:', totalScore, 'points.')
            break
        # Otherwise (the input is not a single period):
        else:
            # If the word is not valid:
            if not isValidWord(inputWord, hand, wordList):
                print('Invalid word, please try again.')
                print()
            # Otherwise (the word is valid):
            else:
                score = getWordScore(inputWord, n)
                totalScore += score
                print(inputWord, 'earned', score, 'points. Total:', totalScore, 'points')
                hand = updateHand(hand, inputWord)
                handLength = calculateHandlen(hand)
                print()
    # Game is over (user entered a '.' or ran out of letters), so tell user the total score
    if handLength == 0:
        print('Run out of letters. Total score:', totalScore, 'points.')
    return totalScore
            
#
# Problem #5: Playing a game
# 

def playGame(wordList):
    """
    Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
      * If the user inputs 'n', let the user play a new (random) hand.
      * If the user inputs 'r', let the user play the last hand again.
      * If the user inputs 'e', exit the game.
      * If the user inputs anything else, tell them their input was invalid.

    2) When done playing the hand, repeat from step 1    
    """
    hand = {}
    while True:
        userInput = input('Enter n to deal a new hand, r to replay the last hand, or e to end game: ')
        if userInput == 'n':
            hand = dealHand(HAND_SIZE)
            playHand(hand, wordList, HAND_SIZE)
        elif userInput == 'r':
            if hand:
                playHand(hand, wordList, HAND_SIZE)
            else:
                print('You have not played a hand yet. Please play a new hand first!')
        elif userInput == 'e':
            break
        else:
            print('Invalid command.')
    return
    

#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    wordList = loadWords()
    playGame(wordList)

class Hand(object):
    VOWELS = 'aeiou'
    CONSONANTS = 'bcdfghjklmnpqrstvwxyz'

    def __init__(self, n):
        """
        Initialize a Hand.

        n: integer, the size of the hand.
        """
        assert type(n) == int, "Hand size must be an integer."
        self.HAND_SIZE = n
        self.hand = {}
        self.dealNewHand()

    def dealNewHand(self):
        """
        Deals a new hand, and sets the hand attribute to the new hand.
        """
        self.hand = {}
        numVowels = self.HAND_SIZE // 3

        for i in range(numVowels):
            x = Hand.VOWELS[random.randrange(0, len(Hand.VOWELS))]
            self.hand[x] = self.hand.get(x, 0) + 1

        for i in range(numVowels, self.HAND_SIZE):
            x = Hand.CONSONANTS[random.randrange(0, len(Hand.CONSONANTS))]
            self.hand[x] = self.hand.get(x, 0) + 1

    def setDummyHand(self, handString):
        """
        Allows you to set a dummy hand. Useful for testing your implementation.

        handString: A string of letters you wish to be in the hand. Length of this
        string must be equal to self.HAND_SIZE.

        This method converts sets the hand attribute to a dictionary containing
        the letters of handString.
        """
        assert len(handString) == self.HAND_SIZE, "Length of handString must equal HAND_SIZE."
        self.hand = {}
        for char in handString:
            self.hand[char] = self.hand.get(char, 0) + 1

    def calculateLen(self):
        """
        Calculate the length of the hand.

        Returns: an integer equal to the total number of letters in the hand.
        """
        return sum(self.hand.values())

    def __str__(self):
        """
        Display a string representation of the hand.

        Returns: a string representation of the hand.
        """
        output = ''
        for letter in sorted(self.hand.keys()):
            output += letter * self.hand[letter]
        return output

    def update(self, word):
        """
        Updates the hand: uses up the letters in the given word
        and returns True if the hand has all the letters to make the word,
        False otherwise.

        word: string
        Returns: Boolean
        """
        handCopy = self.hand.copy()
        for letter in word:
            if handCopy.get(letter, 0) > 0:
                handCopy[letter] -= 1
            else:
                return False
        self.hand = handCopy
        return True