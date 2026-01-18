from solver import filter_words,best_guess
from browser import create_driver
from page import WordlePage
from logger import Excel_Logger
import time

driver = create_driver() #driver created
driver.get("https://wordleunlimited.org/")
page = WordlePage(driver)   #page accessed, DOM traversed with all req elements

while True:

    with open("../data/wordle data.txt","r") as f:
        words = [line.strip() for line in f if line.strip()] #loading files

    print(f"Total words loaded: ",len(words)) #count numbers

    logger = Excel_Logger()
    logger.start_new_game()

    used = set()
    MAX_TRIES = 6
    solved = False

    for turn in range(MAX_TRIES):   #start soln

        guess = best_guess(words,used) #find best guess

        if guess is None:
            print("no new words left to try,playing dummy guesses")
            guess = list(used)[0] #copilot
        
        used.add(guess) #add selected word to set
        print(f"Turn{turn+1}:guess {guess}") #guess number


        page.type_word(guess)   #type selected word
        feedback = page.read_rows(turn) #post typing acquire feedback
        logger.log_turn(turn,feedback)
        

        if all(evaluation == "correct" for _,evaluation in feedback):   #analyse
            print("Solved !")
            solved = True
            logger.log_answer(guess)
            break

        old_count = len(words) 
        words = filter_words(words,feedback)    #filter words
        print("Words reduced:",old_count,"->",len(words))   #new words

    while not solved and turn <MAX_TRIES -1:
        turn+=1
        if words: #copilot
            dummy=words[0]
        else:
            dummy=list(used)[0] #copilot
        print(f"Turn{turn+1}: dummy guess {dummy}")
        page.type_word(dummy)
        feedback = page.read_rows(turn)
        logger.log_turn(turn,feedback)

    exceptions = {
        "genius",
        "magnificent",
        "impressive",
        "splendid",
        "great",
        "phew"
    }

    answer = page.get_answer()
    if answer:
        logger.log_answer(answer)
        print("The answer was:",answer.upper())



        if answer not in words:
            if answer in exceptions:
                print(f"Answer : {answer} is a celebratory toast, skipping")
            else:
                print(f"New word discovered, adding {answer} to dataset.")
                with open("../data/wordle data.txt","a") as f:
                    f.write("\n"+answer.lower())

    print("Game finished")
    user = input("To stop playing, press ENTER")

    if user.strip() == "":
        break
    
    page.play_again()

driver.quit()