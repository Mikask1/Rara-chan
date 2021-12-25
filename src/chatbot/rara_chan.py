from chatterbot import ChatBot
from random import choice
import os

default_response = ["I'm sorry darling~, I can't understand you", "Wakaranai", "I don't understand you :<", "Rara chan ga wakaranai", "Sore tte doiu imi??", "Moo~~ imi wo wakanai", "Nani o itteru no ka??~ Wakaranai wa", "Atama ga okashi yo ne?"]

chatbot = ChatBot('rara chan', 
    database_uri='sqlite:///src\chatbot\db.sqlite3', 
    preprocessors=['chatterbot.preprocessors.clean_whitespace'],
    logic_adapters=[{'import_path': 'chatterbot.logic.BestMatch', 'default_response': default_response, 'maximum_similarity_threshold': 0.90}]
    )

def answer(message):
    if message[:9] == "rara chan":
        return choice(["Yes darling?", "What is it master~", "H-hi", "...", "Who are you?", "What is it darling?~"])

    return chatbot.get_response(message)

if __name__ == "__main__":
    while True:
        print(chatbot.get_response(input("> ")))