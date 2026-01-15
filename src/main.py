from solver import filter_words,best_guess
from browser import create_driver
from page import WordlePage
from logger import Excel_Logger

with open("../data/wordle data.txt","r") as f:
    words = [line.strip() for line in f if line.strip()] #loading files

print(f"Total words loaded: ",len(words)) #count numbers

driver = create_driver() #driver created
driver.get("https://wordleunlimited.org/")

page = WordlePage(driver)   #page accessed, DOM traversed with all req elements

logger = Excel_Logger()
logger.start_new_game()

used = set()
MAX_TRIES = 6

for turn in range(MAX_TRIES):   #start soln

    guess = best_guess(words,used) #find best guess

    if guess is None:
        print("no new words left to try")
        break
    
    used.add(guess) #add selected word to set
    print(f"Turn{turn+1}:guess {guess}") #guess number


    page.type_word(guess)   #type selected word

    feedback = page.read_rows(turn) #post typing acquire feedback

    logger.log_turn(turn,feedback)
    

    if all(evaluation == "correct" for _,evaluation in feedback):   #analyse
        print("Solved !")
        break

    old_count = len(words) 
    words = filter_words(words,feedback)    #filter words
    print("Words reduced:",old_count,"->",len(words))   #new words

driver.quit()