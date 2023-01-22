from revChatGPT.ChatGPT import Chatbot
from os import getenv
from dotenv import load_dotenv

environment = load_dotenv()

config = {
    "session_token": getenv("TOKEN"),
    "browser_exec_path": r"C:\chrome-win\chrome.exe",
    "driver_exec_path": r"C:\chromedriver_win32\chromedriver.exe",
}

chatbot = Chatbot(config, conversation_id=getenv("CONVERSATION"))

chatHistory = "Starting ChatGPT...\nYou: "

while True:
    message = input("You: ")
    response = chatbot.ask(message)
    print(response.get("message"))