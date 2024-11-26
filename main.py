import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d - %(lineno)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

ANSWER = ''
POSSIBLE = []

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
        


def main():
    logging.info('STARTING PROGRAM')
    
    pass

main()