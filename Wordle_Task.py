# https://wordfinder.yourdictionary.com/blog/possible-wordle-answers-with-only-three-unique-letters/
# https://wordfinder.yourdictionary.com/blog/can-letters-repeat-in-wordle-a-closer-look-at-the-rules/
# TODO: Account for TRIPLE LETTER SCENARIO

import json
import time
start_time = time.time()
with open('words_dictionary.json') as json_file:
    raw_data = json.load(json_file)
wordle_words = []  # At 5 letter 'wordle' words are in this


def filtering_raw():
    for word in raw_data:
        if len(word) == 5:
            wordle_words.append(word)


class Word:
    def __init__(self):
        self.guess = self.guess_validation()
        self.clue = self.clue_validation()
        # self.guess = 'adazy'
        # self.clue = 'ywwgy'

    def double_guess_index(self, find_letter):
        check = True
        first_index = None
        second_index = None
        for i, letter in enumerate(self.guess):
            if check and letter == find_letter:
                first_index = i
                check = False
            elif not second_index and letter == find_letter:
                second_index = i
        return first_index, second_index

    def guess_hash(self):
        guess_hash = {}
        for letter in self.guess:
            if letter in guess_hash:
                guess_hash[letter] += 1
            else:
                guess_hash[letter] = 1
        return guess_hash

    @staticmethod
    def guess_validation():
        while True:
            guess = input('(1) Enter the guessed word:\n')
            if len(guess) == 5 and guess.isalpha():
                break
            print('!Enter ONLY a 5 letter word!')
        return guess

    @staticmethod
    def clue_validation():
        colours = 'y', 'g', 'w'
        while True:
            clue = input('(2) Enter the given clue:\n')
            for letter in clue:
                if letter in colours and letter.isalpha():
                    continue
                else:
                    clue = False
            if clue and len(clue) == 5:
                break
            print('!Print only a 5 letter word!')
        return clue


def yellow(letter, guess_i):
    global wordle_words
    for index, wordle in enumerate(wordle_words):
        if wordle[guess_i] == letter or letter not in wordle:
            wordle_words[index] = None
    wordle_words = list(filter(None, wordle_words))


def green(letter, guess_i):
    global wordle_words
    for index, wordle in enumerate(wordle_words):
        if wordle[guess_i] != letter:
            wordle_words[index] = None
    wordle_words = list(filter(None, wordle_words))


def white(letter):
    global wordle_words
    for i, wordle in enumerate(wordle_words):
        if letter in wordle:
            wordle_words[i] = None
    wordle_words = list(filter(None, wordle_words))


def single_func(letter, current):
    i = current.guess.index(letter)
    clue = current.clue
    if clue[i] == 'y':
        yellow(letter, i)
    elif clue[i] == 'g':
        green(letter, i)
    elif clue[i] == 'w':
        white(letter)


def yellow_white(index_y, index_w, current):
    global wordle_words
    for index, wordle in enumerate(wordle_words):
        if wordle.count(current.guess[index_y]) > 1:
            wordle_words[index] = None
        elif wordle[index_y] == current.guess[index_y]:
            wordle_words[index] = None
        elif wordle[index_w] == current.guess[index_w]:
            wordle_words[index] = None
    wordle_words = list(filter(None, wordle_words))


def green_white(i_first, i_second, current):
    global wordle_words
    if current.clue[i_first] == 'g':
        index_g, index_w = i_first, i_second
    else:
        index_g, index_w = i_second, i_first
    for index, wordle in enumerate(wordle_words):
        if wordle.count(current.guess[index_g]) > 1:
            wordle_words[index] = None
        elif wordle[index_g] != current.guess[index_g]:
            wordle_words[index] = None
        elif wordle[index_w] == current.guess[index_w]:
            wordle_words[index] = None
    wordle_words = list(filter(None, wordle_words))


def yellow_yellow(i_first, i_second, current):
    letter = current.guess[i_first]
    global wordle_words
    for index, wordle in enumerate(wordle_words):
        if wordle.count(letter) < 2:
            wordle_words[index] = None
        elif wordle[i_first] == letter or wordle[i_second] == letter:
            wordle_words[index] = None
    wordle_words = list(filter(None, wordle_words))


def yellow_green(i_first, i_second, current):
    global wordle_words
    if current.clue[i_first] == 'y':
        index_y, index_g = i_first, i_second
    else:
        index_y, index_g = i_second, i_first
    for index, wordle in enumerate(wordle_words):
        if wordle.count(current.guess[index_y]) < 2:
            wordle_words[index] = None
        elif wordle[index_g] != current.guess[index_g]:
            wordle_words[index] = None
        elif wordle[index_y] == current.guess[index_y]:
            wordle_words[index] = None
    wordle_words = list(filter(None, wordle_words))


def double_func(letter, current):
    double_indexes = current.double_guess_index(letter)
    i_first = double_indexes[0]
    i_second = double_indexes[1]
    if current.clue[i_first] == 'y' and current.clue[i_second] == 'w':
        yellow_white(i_first, i_second, current)
    elif current.clue[i_first] == 'w' and current.clue[i_second] == 'g' or \
            current.clue[i_first] == 'g' and current.clue[i_second] == 'w':
        green_white(i_first, i_second, current)
    elif current.clue[i_first] == 'y' and current.clue[i_second] == 'g' or \
            current.clue[i_first] == 'g' and current.clue[i_second] == 'y':
        yellow_green(i_first, i_second, current)
    elif current.clue[i_first] == 'w' and current.clue[i_second] == 'w':
        white(letter)
    elif current.clue[i_first] == 'y' and current.clue[i_second] == 'y':
        yellow_yellow(i_first, i_second, current)


def game_loop():
    while True:
        print(f"Length of wordle list is: {len(wordle_words)}")
        print(wordle_words)
        current = Word()
        guess_hash = current.guess_hash()
        for letter in guess_hash:
            if guess_hash[letter] == 1:
                single_func(letter, current)
            elif guess_hash[letter] == 2:
                double_func(letter, current)
            elif guess_hash[letter] == 3:
                pass


if __name__ == '__main__':
    filtering_raw()  # Filter JSON for only 5-letter words.
    game_loop()
    end_time = time.time()
    print(f"\n\nFinished in {end_time - start_time} seconds.")