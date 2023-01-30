import selenium.common
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver.v2 as uc
from time import sleep

options = webdriver.ChromeOptions()


# options.add_argument(
#     "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
# )


class ChatGPT:
    def __init__(self, token, conversation_id=None, headless=False):
        """
        Create a new ChatGPT chatbot
        :param token: the cookie token
        :param conversation_id: the conversation id
        :param headless: whether to run the browser in headless mode
        """
        if conversation_id is None or conversation_id.strip() == "":
            conversation_id = ""
        self.token = token
        self.conversation_id = conversation_id
        self.headless = headless
        self.ready = False

        # if headless then add the headless option
        if headless:
            options.add_argument("--headless")

        self.driver = uc.Chrome(options=options)
        # make window 1970x1080
        self.driver.set_window_size(1900, 1070)

        self.input_field = None
        self.input_path = r'''/html/body/div[1]/div[2]/div/main/div[2]/form/div/div[2]/textarea'''

        self.message_history = None

        self.load_page(token, conversation_id)

    def send(self, message):
        """
        Send a message to the chatbot
        :param message:
        :return:
        """
        if self.is_generating():
            return False
        try:
            self.input_field.send_keys("")
        except selenium.common.exceptions.NoSuchElementException as e:
            # reload page
            self.load_page(self.token, self.conversation_id)
            return False
        self.input_field.send_keys(message)
        self.input_field.send_keys(Keys.RETURN)
        return True

    def get_messages(self):
        """
        Get all messages in the chat
        :return:
        """
        messages = self.driver.find_elements(By.XPATH,
                                             '''//*[@id="__next"]/div[1]/div[1]/main/div[1]/div/div/div/div''')

        text_messages = []
        for message in range(1, len(messages)):
            try:
                xpath = fr'''//*[@id="__next"]/div[1]/div[1]/main/div[1]/div/div/div/div[{message}]/div/div[2]/div[1]/div/div'''
                text = self.driver.find_element(By.XPATH, xpath).text
                complete = True
                if message == len(messages) and self.is_generating():
                    complete = False
                text_messages.append({
                    "author": "OpenAI",
                    "text": text,
                    "complete": True
                })
            except selenium.common.exceptions.NoSuchElementException as e:
                xpath = fr'''//*[@id="__next"]/div[1]/div[1]/main/div[1]/div/div/div/div[{message}]/div/div[2]/div[1]/div'''
                text = self.driver.find_element(By.XPATH, xpath).get_attribute("innerHTML")
                text_messages.append({
                    "author": "user",
                    "text": text,
                    "complete": True
                })
        return text_messages

    def does_element_exist(self, by, element):
        """
        Check if an element exists
        :param by:
        :param element:
        :return:
        """
        try:
            self.driver.find_element(by, element)
            return True
        except selenium.common.exceptions.NoSuchElementException as e:
            return False

    def regenerate_response(self):
        """
        Regenerate the response
        :return:
        """
        button = r'''/html/body/div[1]/div[2]/div[1]/main/div[2]/form/div/div[1]/button'''
        text = r'''/html/body/div[1]/div[2]/div[1]/main/div[2]/form/div/div[1]/button/text()'''
        text = self.driver.find_element(By.XPATH, text).text
        if text == '"Regenerate response"':
            self.driver.find_element(By.XPATH, button).click()
            # print("Regenerating response...")
            sleep(0.5)

    def is_generating(self):
        """
        Check if the chatbot is generating a response
        :return:
        """
        button = r'''//*[@id="__next"]/div[1]/div[1]/main/div[2]/form/div/div[2]/button'''
        # check if button exists
        if self.does_element_exist(By.XPATH, button):
            button = self.driver.find_element(By.XPATH, button)
            # check if button is disabled
            if button.get_attribute("disabled") is None:
                return False
            else:
                return True
        # if the button doesn't exist, then assume it's generating
        return False

    def stop_generating(self):
        """
        Stop the chatbot from generating a response
        :return:
        """
        button = r'''/html/body/div[1]/div[2]/div[1]/main/div[2]/form/div/div[1]/button'''
        text = r'''/html/body/div[1]/div[2]/div[1]/main/div[2]/form/div/div[1]/button/text()'''
        text = self.driver.find_element(By.XPATH, text).text
        if text == "Stop generating":
            self.driver.find_element(By.XPATH, button).click()
            print("Stopping generation...")
            sleep(0.5)

    def close(self):
        """
        Close the browser
        :return:
        """
        self.driver.close()
        self.driver.quit()

    def delete_element(self, jsReference):
        """
        Delete an element from the page
        :param jsReference:
        :return:
        """
        self.driver.execute_script(fr'''elem = document.querySelector("{jsReference}"); elem.remove();''')

    def regenerate_response_error(self):
        """
        Regenerate the response if there is an error
        :return:
        """
        sleep(2)
        button1 = r'''//*[@id="__next"]/div[1]/div[1]/main/div[2]/form/div/div/button'''
        if self.does_element_exist(By.XPATH, '''//*[@id="__next"]/div[2]/div[1]/main/div[2]/form/div/div/span'''):
            self.driver.find_element(By.XPATH, button1).click()

    def load_page(self, token, conversation_id):
        """
        Load the page
        :param token:
        :param conversation_id:
        :return:
        """

        self.driver.get(f"https://chat.openai.com/chat/{conversation_id}")
        self.driver.minimize_window()

        # tries to find the element with id "__next" for 30 seconds
        WebDriverWait(self.driver, 30).until(
            ec.presence_of_element_located((By.ID, "__next"))
        )

        # print("Page is ready!")

        self.driver.add_cookie({"name": "__Secure-next-auth.session-token", "value": token})

        self.driver.get(f"https://chat.openai.com/chat/{conversation_id}")

        # tries to find the element with id "__next" for 30 seconds
        WebDriverWait(self.driver, 30).until(
            ec.presence_of_element_located((By.ID, "__next"))
        )

        # check if the login button is there
        login_button = self.does_element_exist(By.XPATH, '''//*[@id="__next"]/div[1]/div/div[4]/button[1]''')
        if login_button:
            # throw an error, invalid token
            raise Exception("Invalid token")

        # check if this element exists //*[@id="headlessui-dialog-panel-:r1:"]/div[2]/div[4]/button
        try:
            # if it does, then delete it
            self.delete_element(r'''#headlessui-portal-root > div > div''')
        except Exception as e:
            print(e)
            pass

        self.input_field = WebDriverWait(self.driver, 30).until(
            ec.presence_of_element_located((By.XPATH, self.input_path))
        )

        check_style = self.driver.find_element(By.XPATH, '''//*[@id="__next"]/div[1]''')
        if check_style.get_attribute(
                "style") == "position: fixed; top: 1px; left: 1px; width: 1px; height: 0px; padding: 0px; margin: -1px; overflow: hidden; clip: rect(0px, 0px, 0px, 0px); white-space: nowrap; border-width: 0px; display: none;":
            # print("deleting style div")
            self.delete_element("#__next > div:nth-child(2)")

        self.regenerate_response_error()
        self.ready = True

    def last_message(self):
        """
        Get the last message
        :return:
        """
        messages = self.get_messages()
        if len(messages) > 0:
            return messages[-1]
        else:
            return None

    def get_error(self):
        """
        Get the error message
        :return:
        """
        error_message = r'''//*[@id="__next"]/div[1]/div[1]/main/div[2]/form/div/div/span'''
        if self.does_element_exist(By.XPATH, error_message):
            messages = self.get_messages()
            if len(messages) > 0:
                return messages[-1]
            error_message = self.driver.find_element(By.XPATH, error_message)
            return error_message.text
        else:
            return None
