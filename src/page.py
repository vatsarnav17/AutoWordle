from selenium.webdriver.common.by import By #locator
from selenium.webdriver.common.keys import Keys 
import time

class WordlePage:
    def __init__(self,driver):
        self.driver = driver
        self._init_dom()
    
    def _init_dom(self):

        self.game_app = self.driver.execute_script(
            "return document.querySelector('game-app')"
        )

        self.shadow_root_1 = self.driver.execute_script(
            "return arguments[0].shadowRoot",self.game_app
        )

        self.game_theme_manager = self.driver.execute_script(
            "return arguments[0].querySelector('game-theme-manager')",
            self.shadow_root_1
        )

        self.game_box = self.driver.execute_script(
            "return arguments[0].querySelector('#game')",
            self.game_theme_manager
        )

        self.game_modal = self.driver.execute_script(
            "return arguments[0].querySelector('game-modal')",
            self.game_box
        )

        if self.game_modal:
            shadow_root_close = self.driver.execute_script(
                "return arguments[0].shadowRoot",
                self.game_modal
            )
            
            game_overlay = self.driver.execute_script(
                "return arguments[0].querySelector('.overlay')",
                shadow_root_close
            )

            overlay_content = self.driver.execute_script(
                "return arguments[0].querySelector('.content')",
                game_overlay
            )

            if overlay_content:
                
                overlay_close_btn = self.driver.execute_script(
                    "return arguments[0].querySelector('.close-icon')",
                    overlay_content
                )

                time.sleep(2)

                if overlay_close_btn:

                    self.driver.execute_script(
                        "arguments[0].click()",
                        overlay_close_btn
                    )

        self.board_container = self.driver.execute_script(            #both GB methods here too   
            "return arguments[0].querySelector('#board-container')",
            self.game_box
        ) 

        self.board = self.driver.execute_script(
            "return arguments[0].querySelector('#board')",
            self.board_container
        )

        self.game_row = self.driver.execute_script(
            "return arguments[0].querySelectorAll('game-row')",
            self.board
        )

    def type_word(self,word):
        body = self.driver.find_element(By.TAG_NAME,"body")
        for letter in word:
            body.send_keys(letter)
        body.send_keys(Keys.ENTER)
        time.sleep(3)

    def read_rows(self,turn):
        # read feedback from the specific turn's row instead of always the first
        shadow_root_2 = self.driver.execute_script(
            "return arguments[0].shadowRoot",
            self.game_row[turn]
        )

        tile_row = self.driver.execute_script(
            "return arguments[0].querySelector('.row')",
            shadow_root_2
        )
        
        game_tile = self.driver.execute_script(
            "return arguments[0].querySelectorAll('game-tile')",
            tile_row
        )

        


        feedback= []
        for tile in game_tile:
            letter = tile.get_attribute("letter")
            evaluation = tile.get_attribute("evaluation")
            feedback.append((letter,evaluation))

        return feedback
    
    def get_answer(self):

        self.answer_toaster = self.driver.execute_script(
            "return arguments[0].querySelector('#game-toaster')",
            self.game_box
        )

        if not self.answer_toaster:
            return None

        game_toast = self.driver.execute_script(
            "return arguments[0].querySelector('game-toast')",
            self.answer_toaster
        )

        ans = game_toast.get_attribute("text")

        if not ans:
            return None
        
        return ans.strip().lower()

    def play_again(self):
            time.sleep(2)  # Wait for modal to appear
            
            # Reinitialize to get fresh reference
            self._init_dom()
            
            # Try to find the refresh button in the stats modal
            if self.game_modal:
                stats = self.driver.execute_script(
                    "return arguments[0].querySelector('game-stats')",
                    self.game_modal
                )
                
                if stats:
                    stats_shadow = self.driver.execute_script(
                        "return arguments[0].shadowRoot",
                        stats
                    )
                    
                    refresh_btn = self.driver.execute_script(
                        "return arguments[0].querySelector('#refresh-button') || arguments[0].querySelector('button[aria-label*=\"play\"]') || arguments[0].querySelector('button')",
                        stats_shadow
                    )
                    
                    if refresh_btn:
                        self.driver.execute_script("arguments[0].click()", refresh_btn)
                        print("Play again button clicked")
                        time.sleep(3)
                        return True
                    else:
                        print("Refresh button not found in stats shadow")
                        return False
                else:
                    print("Stats element not found")
                    return False
            else:
                print("Game modal not found")
                return False
