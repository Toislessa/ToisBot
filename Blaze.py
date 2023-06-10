from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class Bot:
    BASE_URL = "https://blaze.com/pt/games/double"

    def __init__(self):
        self.driver = None
        self.account_balance = None

    def Start(self):
        print("Starting Bot")
        chrome_options = Options()
        # Use add_argument("--headless") instead of headless property
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1300,1000")
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--log-level=3")
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; X64) AppleWebKit/537.36 (KHTML, Like Gecko) Chrome/113.0.0.0 Safari/537.36"
        chrome_options.add_argument(f"user-agent={user_agent}")

        # Adicione os novos argumentos aqui
        chrome_options.add_argument("--disable-blink-features")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.set_window_position(500, 0, windowHandle="current")
        self.driver.get(self.BASE_URL)
        print("Bot started")


    def Stop(self):
        print("Bot is stopping")
        self.driver.quit()
        print("Bot stopped")

    def Login(self, email, password):
        error = None
        try:
            wait = WebDriverWait(self.driver, 30)
            LOGIN_BUTTON = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="header"]/div[2]/div/div[2]/div/div/div[1]/a')))
            LOGIN_BUTTON.click()

            time.sleep(1)
            EMAIL_INPUT = self.driver.find_elements(By.CLASS_NAME, 'input-wrapper')[0].find_element(By.TAG_NAME, 'input')
            EMAIL_INPUT.send_keys(email)

            PASSWORD_INPUT = self.driver.find_elements(By.CLASS_NAME, 'input-wrapper')[1].find_element(By.TAG_NAME, 'input')
            PASSWORD_INPUT.send_keys(password)

            SUBMIT_BUTTON = self.driver.find_element(By.CLASS_NAME, 'submit')
            SUBMIT_BUTTON.click()

            time.sleep(10)  # Wait some time for the page to load

            if self.driver.current_url != self.BASE_URL:  # If we are not redirected to the base URL, login has failed
                error = "Login failed"
            else:
                self.Get_Balance()

        except Exception as e:
            error = [False, e]
        finally:
            if error:
                print("Error", error)
                return error
            else:
                print("Login successful")
                return [True, None]

    def Get_Balance(self):
        error = None
        result = None
        try:
            balance_description = self.driver.find_element(By.CLASS_NAME, 'wallet').get_attribute("textContent")
            print(f'Balance description: {balance_description}')  # Print the balance description

            result = balance_description
            print(result)
        except:
            error = True
            print("Something went wrong")
            return error
        finally:
            if error == None:
                self.account_balance = result
                return result

if __name__ == "__main__":
    bot = Bot()
    bot.Start()
    bot.Login("toislessa5@gmail.com", "Perola2010@")
    bot.Stop()
