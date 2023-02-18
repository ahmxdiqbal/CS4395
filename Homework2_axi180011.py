import sys                              # import necessary packages and functions
import nltk
import random
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

nltk.download('punkt')                  # downloading necessary packages from nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


def guessing_game(word_arg):
    user_points = 5

    # initializing the dict of correct guesses with underscores
    correct_guesses = {}
    for x in range(len(word_arg)):
        correct_guesses.update({x: "_"})

    # while loop until player either wins or runs out of points
    while user_points > -1 and "_" in correct_guesses.values():
        for ltr in correct_guesses.values():
            print(ltr, end=" ")
        print()

        guess = input("Guess a letter: ")

        if guess == "!":            # exiting program if guess is exclamation mark
            exit()

        if guess in correct_guesses.values():       # not allowing user to enter same guess
            print("You can't guess the same letter twice.")
            print("Score is still ", user_points)
            continue

        if len(guess) != 1 or not guess.isalpha():  # making sure the user only enters a single letter
            print("You can only guess a single letter of the alphabet")
            print("Score is still ", user_points)
            continue

        # finding all indices in which the guess appears in the word
        indexes_list = [k for k, ltr in enumerate(word_arg) if ltr == guess]

        if len(indexes_list) > 0:       # updating the user's points
            user_points += 1
            print("Right! Score is ", user_points)
        else:
            user_points -= 1
            if user_points > -1:
                print("Sorry, guess again. Score is", user_points)

        for index in indexes_list:      # updating the dict with the correct guess
            correct_guesses[index] = guess

    if "_" not in correct_guesses.values():         # if the user wins, print final word and score
        for ltr in correct_guesses.values():
            print(ltr, end=" ")
        print()

        print("You solved it!")
        print("\nCurrent Score:", user_points)
    else:                                           # inform user of failure
        print("You failed. The word was", word_arg)

    print("\nGuess another word")                   # Prompt for new game


def preprocess(tokens_arg):
    stop_words = set(stopwords.words('english'))
    wnl = WordNetLemmatizer()

    # processing the list of tokens in specified way
    tokens_arg = [t for t in tokens_arg if t not in stop_words and t.isalpha() and len(t) > 5]
    tokens_arg = [t.lower() for t in tokens_arg]

    # getting a list of unique lemmas
    lemmas = [wnl.lemmatize(t) for t in tokens_arg]
    lemmas_set = set(lemmas)

    # tagging and printing out some lemmas
    pos_lemmas = pos_tag(lemmas_set)
    for k in range(20):
        print(pos_lemmas[k])

    # creating a list of nouns from the tagged lemmas
    nouns_list = []
    noun_tuples = [t for t in pos_lemmas if t[1] == "NN" or t[1] == "NNS" or t[1] == "NNP" or t[1] == "NNPS"]
    for noun_tuple in noun_tuples:
        nouns_list.append(noun_tuple[0])

    # printing number of tokens and nouns
    print()
    print("Number of tokens: " + str(len(tokens_arg)))
    print("Number of nouns: " + str(len(nouns_list)))
    print()

    return tokens_arg, nouns_list


if __name__ == '__main__':
    if sys.argv[1] != "anat19.txt":             # making sure filename is given
        print("error. must pass filename anat19.txt as argument")
        exit()

    filename = sys.argv[1]

    f = open(filename, "r")                     # opening file and reading in a list
    tokens = word_tokenize(f.read())

    # calculating and printing lexical diversity
    unique_tokens = Counter(tokens).keys()
    print("\nlexical diversity: ", "%.2f" % (len(unique_tokens) / len(tokens)))
    print()

    new_tokens, new_nouns = preprocess(tokens)  # getting a list of processed tokens and nouns

    nouns_dict = {}                             # creating a dict of all nouns and their # of occurrences in tokens list
    word_counts = Counter(new_tokens)
    for noun in new_nouns:
        nouns_dict.update({noun: word_counts[noun]})

    top50_dict = {}                             # creating a dict of 50 most commonly occurring nouns
    sorted_tuple = sorted(nouns_dict.items(), key=lambda x: x[1], reverse=True)
    for i in range(50):
        top50_dict.update({sorted_tuple[i][0]: sorted_tuple[i][1]})
        print(sorted_tuple[i][0], sorted_tuple[i][1])
    print()

    # getting random word from top 50 list and playing until user enters an exclamation mark
    while True:
        word = random.choice(list(top50_dict.keys()))
        guessing_game(word)
