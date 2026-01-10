from selenium import webdriver #engine that talks to browser
from selenium.webdriver.chrome.service import Service #chrome takes commands from driver, this gives location of driver.
from selenium.webdriver.chrome.options import Options #chrome opening options
from webdriver_manager.chrome import ChromeDriverManager #makes sure chrome sahi se chale
from selenium.webdriver.common.by import By #locator
from selenium.webdriver.common.keys import Keys 
import time 

options=Options()

options.add_argument("--start-maximised")

options.add_argument("--disable-blink-features=AutomationControlled") #to avoid detection as bot

service=Service(ChromeDriverManager().install()) #installs CDM, passes as Service() in variable service

driver = webdriver.Chrome(service=service,options=options) # starts chrome

driver.get("https://wordleunlimited.org/")

body = driver.find_element(By.TAG_NAME,"body")
print("Body Found:",body is not None)

game_app = driver.execute_script(
    "return document.querySelector('game-app')"
)
print("game-app found:",game_app is not None)

shadow_root_1 = driver.execute_script(
    "return arguments[0].shadowRoot",game_app
)
print("shadow root 1 found:",shadow_root_1 is not None)

game_theme_manager = driver.execute_script(
    "return arguments[0].querySelector('game-theme-manager')",
    shadow_root_1
)
print("game theme manager found:",game_theme_manager is not None)

#for game box , both these work as they are in same shadow domain as game-theme-manager 

# 1.
#  game_box = game_theme_manager.find_element(By.ID, "game")

# 2.
game_box = driver.execute_script(
    "return arguments[0].querySelector('#game')",
    game_theme_manager
)
print("game box found:",game_box is not None)

board_container = driver.execute_script(            #both GB methods here too   
    "return arguments[0].querySelector('#board-container')",
    game_box
) 
print("board container found:",board_container is not None)

board = driver.execute_script(
    "return arguments[0].querySelector('#board')",
    board_container
)
print("board found:",board is not None)

game_row = driver.execute_script(
    "return arguments[0].querySelectorAll('game-row')",
    board
)
print("Number of rows:",len(game_row))

last_row = game_row[-1]

shadow_root_2 = driver.execute_script(
    "return arguments[0].shadowRoot",
    game_row[0]
)
print("shadow root 2 found:",shadow_root_2 is not None)

tile_row = driver.execute_script(
    "return arguments[0].querySelector('.row')",
    shadow_root_2
)
print("tile_row found:",tile_row is not None)

game_tile = driver.execute_script(
    "return arguments[0].querySelectorAll('game-tile')",
    tile_row
)
print("number of tiles found:",len(game_tile))

word = "adieu"
for ch in word:
    driver.find_element(By.TAG_NAME,"body").send_keys(ch)

driver.find_element(By.TAG_NAME,"body").send_keys(Keys.ENTER)

tile_later = driver.execute_script(
    "return arguments[0].querySelectorAll('game-tile')",
    tile_row
)

for i,tile in enumerate(tile_later):
    letter = tile.get_attribute("letter")
    evaluation = tile.get_attribute("evaluation")
    print(f"Tile {i}: letter = {letter} , state = {evaluation}")

time.sleep(3)

driver.quit()