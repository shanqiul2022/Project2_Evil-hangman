from __future__ import annotations
from collections import defaultdict # You might find this useful
import os

"""
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************

If you worked in a group on this project, please type the EIDs of your groupmates below (do not include yourself).
Leave it as TODO otherwise.
Groupmate 1: TODO
Groupmate 2: TODO
"""

class WordMakerHuman():
    def __init__(self, words_file, verbose): # initilialize the instance of the class with two parameters
        # we need to prompt the player for a word, then clear the screen so that player 2 doesn't see the word.
        self.verbose = verbose #store verbose as an instance attribute.
        self.words = {} # Create an empty "words" dictionary to store words read from the file
        with open(words_file) as wordfile: # loop through the words file
            for line in wordfile:
                word = line.strip() #remove any leading or tailing whitespace from the line
                if len(word) > 0:
                    self.words[word] = True # If the line is not empty, store the word as the key and True as the value.

    def reset(self, word_length): #define reset method which takes one parameter "word_length"
        # Your AI code should not call input() or print().
        question = "" # initialize an empty string "question"
        while True: #repeatedly prompted to enter a word of specified length
            question = input(f"Please type in your word of length {word_length}: ") # store the input word in question
            if question in self.words and len(question) == word_length: #check if the stored word in "question" exists in self.words and it its length matches word_length
                break #if those two conditions are met, break the loop; thw word is accepted
            print("Invalid word.") #otherwise, print "invalid word" and the loop continues
        if not self.verbose: #if the verbose attribute is false, the screen is cleared by printing 100 newline characters
            print("\n" * 100) # Clear the screen
        self.word = question #the valid word entered by the user is stored in the instance attribute self.word

    def get_valid_word(self): #this method returns the valid word that has been set in the instance
        return self.word

    def get_amount_of_valid_words(self): #this method returns the number of valid words.
        return 1 # the only possible word is self.word thus it always return 1

    def guess(self, guess_letter): #this method finds all occurences of a guessed letter in the valid word
        idx = self.word.find(guess_letter) #find the ocurrence of "guess letter" in "self.word"; store the occurence in idx
        ret = [] #create an emty list ret
        while idx != -1: # run the while loop as long as idx is not -1 which indicates no more occurence
            ret.append(idx) # append idx to the list
            idx = self.word.find(guess_letter, idx + 1) # find the next occurence and update the idx
        return ret




class WordMakerAI():
    """
    A new WordMakerAI is instantiated every time you launch the game with evil_hangman.py.
    (However, the test harness can make multiple instances.)
    Between games, the reset() function is called. This should clear any internal gamestate that you have.
    The number of guesses, input gathering, winning, losing, etc. is all managed by the GameManager, so you don't
     have to prompt the user at all. All you need to do is keep track of the active dictionary of still-valid words
     in this game.

    Do not assume anything about the lengths of the words. You will be tested on dictionaries with extremely long words.
    """
    def __init__(self, words_file: str, verbose=False):
        # This initializer should read in the words into any data structures you see fit
        # The input format is a file of words separated by newlines
        # Use open() to open the file, and remember to split up words by word length!

        # Feel free to use this parameter to toggle extra print statments. Verbose mode can be turned on via the --verbose flag.
        self.verbose = verbose
        self.words_by_length = defaultdict(list)
        self.current_words = []
        self.current_pattern = []
        # Use this code if you like.
        with open(words_file) as wordfile:
            for line in wordfile:
                word = line.strip()
                # Use word
                if len(word) > 0:
                    self.words_by_length[len(word)].append(word)


    def reset(self, word_length: int) -> None:
        # This function starts a new game with a word length of `word_length`. This will always be called before guess() or get_valid_word() are called.
        # You should try to make this function should be O(1). That is, you shouldn't have to process over the entire dictionary here (find somewhere else to preprocess it)
        # Your AI code should not call input() or print().
        self.current_words = self.words_by_length[word_length]
        self.current_pattern = ['-'] * word_length

    def get_valid_word(self) -> str:
        # Get a valid word in the active dictionary, to return when you lose
        # Can return any word, as long as it satisfies the previous guesses
        if self.current_words:
            return self.current_words[0]
        return ""

    def get_amount_of_valid_words(self) -> int:
        # This function gets the total amount of possible words "remaining" (i.e., that satisfy all the guesses since self.reset was last called)
        # This should also be O(1)
        # Note: This is used extensively in the autograder! Be sure to verify that this function works
        # via the provided test cases.
        # You can see this number by running with the verbose flag, i.e. `python3 evil_hangman.py --verbose`
        return len(self.current_words)

    def get_letter_positions_in_word(self, word: str, guess_letter: str) -> tuple[int, ...]:
        # This function should return the positions of guess_letter in word. For instance:
        #  get_letter_positions_in_word("hello", "l") should return (2, 3). The list should
        #  be sorted ascending and 0-indexed.
        # You can assume that word is lowercase with at least length 1 and guess_letter has exactly length 1 and is a lowercase a-z letter.
        # Note: to convert from a list to a tuple, call tuple() on the list. For instance:
        result = [i for i, letter in enumerate(word) if letter == guess_letter]
        #returns an enumerate object that produces pairs containing the index and the corresponding item
        # from the iterable
        return tuple(result)
        

    def guess(self, guess_letter: str) -> list[int]:
        # This is the meat of the project. This function is called by the GameManager.
        # Using get_letter_positions_in_word, this function should sort all remaining words
        #  into their respective letter families. Then, it should pick the largest family,
        #  resolving ties by picking the set with fewer guess_letters. If the amount of
        #  guess_letter's are equal, then either set can be picked to become the new active
        #  dictionary.
        # This function should return the positions of where a guess_letter should appear.
        # For instance, if you want an "e" to appear in positions 0 and 2, return [0, 2].
        # Make sure the list is sorted.

        # Here is an example run of guess():
        #  If the guess is "a" and the words left are ["ah", "ai", "bo"], then we should return [0], because
        #  we are picking the family of words with an "a" in the 0th position. If this function decides that the biggest family
        #  has no a's, then we would have returned [].

        # In the case of a tie (multiple families have the same amount of words), we should pick the set of words with fewer guess_letter's.
        #  That is, if the guess is "a" and the words left are ["ah", "hi"], we should return [] (picking the set ["hi"]), 
        #  since ["hi"] and ["ah"] are equal length and "hi" has fewer a's than "ah".
        # Again, if both sets have an equal number of guess_letter's, then it is ok to pick either.
        #  For example, if the guess is "a" and the words left are ["aha", "haa"], you can return either [0, 2] or [1, 2].

        # The order of the returned list should be sorted. You can assume that 'guess_letter' has not been seen yet since the last call to self.reset(),
        #  and that guess_letter has len of 1 and is a lowercase a-z letter.

        # Create a dictionary to store letter families based on the guessed letter's positions
        families = defaultdict(list)
        # Sort words into families
        for word in self.current_words:
            # Get the positions of the guessed letter in the current word
            positions = self.get_letter_positions_in_word(word, guess_letter)
            families[positions].append(word)

        # Find the largest family (the family with the most words)
        # If there is a tie, choose the one with fewer occurrences of the guessed letter
        best_family = max(families, key=lambda k: (len(families[k]), -len(k)))

        # Update current words to the largest family
        self.current_words = families[best_family]

        # Update the current pattern based on the best family
        for index in best_family:
            self.current_pattern[index] = guess_letter

        # Return the positions of the guessed letter in the largest family (sorted list)
        return sorted(best_family)


