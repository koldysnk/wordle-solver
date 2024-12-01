import os.path
import logging
import requests
from datetime import datetime
from bs4 import BeautifulSoup as BS

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d - %(lineno)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

TODAY_DATE = datetime.today().strftime("%Y%m%d")

ALPHABET = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
VOWELS = ['a','e','i','o','u']

ANSWER = ''
POSSIBLE_ANSWERS = []
VALID_WORDS = []
VALID_ANSWERS = []
PAST_ANSWERS = []

def getAnswerFromWeb():
    logging.warning("Unable to get the answer from the web.")
    return False

def getAnswerFromUser():
    global ANSWER 

    ANSWER = input("Please enter todays answer (It is only used for validation): ").strip()
    while ANSWER not in POSSIBLE:
        ANSWER = input("INVALID - Answer must only include letters and must be a valid wordle answer: ").strip()

#This function gets the answer. The answer is used to validate the programs guesses.
def getAnswer():
    logging.debug("Atempting to get todays answer.")

    if not getAnswerFromWeb():
        getAnswerFromUser()

def loadPossibleWords():
    global VALID_WORDS

    with open("validWords.txt","r") as f:
        VALID_WORDS = [x.strip() for x in f.readlines()]

def loadPossibleAnswers():
    global VALID_ANSWERS

    if not os.path.exists('validAnswers.txt'):
        logging.debug("List off possible words is missing. Generating new list.")

        resp = requests.get("https://wordunscrambler.me/wordle-words-starting-with/n")
        print(resp.text)
    else:
        with open("validAnswers.txt","r") as f:
            VALID_ANSWERS = [x.strip() for x in f.readlines()]

def loadPastAnswers():
    global PAST_ANSWERS

    path = f"data/pastAnswers{TODAY_DATE}.txt"
    if not os.path.exists(path):
        url = "https://www.techradar.com/news/past-wordle-answers"
        response = requests.get(url)
        soup = BS(response.content,"lxml")
        body = soup.find("div",{"id":"article-body"})

        for p in body.find_all("p"):
            words = p.getText().split("|")
            if len(words) > 10:
                PAST_ANSWERS = [word.strip() for word in words]
        
        with open(path, "w") as f:
            f.writelines([f"{word}\n" for word in PAST_ANSWERS])
    else:
        with open(path,"r") as f:
            PAST_ANSWERS = [word.strip() for word in f.readlines()]

def filterPastAnswers():
    global POSSIBLE_ANSWERS

    POSSIBLE_ANSWERS = list(set(VALID_ANSWERS).difference(set(PAST_ANSWERS)))

def printPossible():
    POSSIBLE_ANSWERS.sort(key=lambda word: sum([letter in VOWELS for letter in word]))
    for word in POSSIBLE_ANSWERS[-10:]:
        print(word)

def verifyGood(word,good_letters):
    return sum([letter in word for letter in good_letters])==len(good_letters)

def verifyBad(word,bad_letters):
    return sum([letter in bad_letters for letter in word])==0

def verifyBadPositions(word,positions):
    for i, letter in enumerate(word):
        if letter in positions[i]:
            return False
    return True

def verifyGoodPositions(word,positions):
    for i, letter in enumerate(word):
        if letter != positions[i] and positions[i] != '':
            return False
    return True

def humanGuess():
    guess = input("Guess a 5 letter word: ").lower().strip()
    while guess not in VALID_WORDS:
        guess = input("INVALID - Guess again: ").lower().strip()
    return guess

def validateResults(results):
    if len(results) != 5:
        return True
    for letter in results:
        if letter not in ['b','y','g']:
            return True
    return False

def manualResults():
    results = input("Enter the hint provided by wordle (b|y|g): ").lower().strip()

    while validateResults(results):
        results = input("Hint must only include 'b', 'y', and 'g': ").lower().strip()

    return results

def updateInputs(guess, results, bad_letters,good_letters,bad_positions,good_positions):
    for i,letter in enumerate(guess):
        result = results[i]

        if result == "g":
            if letter not in good_letters:
                good_letters.append(letter)

            good_positions[i] = letter
    
    for i,letter in enumerate(guess):
        result = results[i]
        
        if result == "y":
            if letter not in good_letters:
                good_letters.append(letter)

            bad_positions[i].append(letter)

    for i,letter in enumerate(guess):
        result = results[i]
        
        if result == 'b':
            if letter not in bad_letters and letter not in good_letters:
                bad_letters.append(letter)

            bad_positions[i].append(letter)

    return bad_letters,good_letters,bad_positions,good_positions

def main():
    global POSSIBLE_ANSWERS

    logging.info('STARTING PROGRAM')

    loadPossibleWords()
    loadPossibleAnswers()
    loadPastAnswers()

    filterPastAnswers()
    print(len(POSSIBLE_ANSWERS))

    bad_letters = []
    good_letters = []
    bad_positions = [
        [],
        [],
        [],
        [],
        []
    ]
    good_positions = [
        '',
        '',
        '',
        '',
        ''
    ]

    guess_count = 0
    searching = True
    while searching:

        POSSIBLE_ANSWERS = list(filter(lambda word: verifyGood(word,good_letters) and \
                                                    verifyBad(word,bad_letters) and \
                                                    verifyGoodPositions(word,good_positions) and \
                                                    verifyBadPositions(word,bad_positions) , POSSIBLE_ANSWERS))
        print(len(POSSIBLE_ANSWERS))

        printPossible()
        print()

        #guess = computerGuess(POSSIBLE_ANSWERS)
        guess = humanGuess()
        print(guess)
        #results = autoResults()
        results = manualResults()

        bad_letters,good_letters,bad_positions,good_positions = updateInputs(guess, results, bad_letters,good_letters,bad_positions,good_positions)
        
        guess_count += 1
        if results == "ggggg":
            print(f"You won in {guess_count} guesses!")
            searching = False
        elif guess_count >= 6:
            print("Out of guesses. You lost...")
            searching = False

    pass

main()