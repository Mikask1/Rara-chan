from chatterbot import ChatBot
from random import choice

default_response = ["I'm sorry darling~, I can't understand you", "Wakaranai", "I don't understand you :<", "Rara chan ga wakaranai",
                    "Sore tte doiu imi??", "Moo~~ imi wo wakanai", "Nani o itteru no ka??~ Wakaranai wa", "Atama ga okashi yo ne?"]

chatbot = ChatBot('rara chan',
                  database_uri='sqlite:///src\chatbot\db.sqlite3',
                  preprocessors=['chatterbot.preprocessors.clean_whitespace'],
                  logic_adapters=[{'import_path': 'chatterbot.logic.BestMatch',
                                   'default_response': default_response, 'maximum_similarity_threshold': 0.90}]
                  )


def answer(message):
    if message[:9].strip().lower() == "rara chan":
        return choice(["Yes darling?", "What is it master~", "H-hi", "...", "Who are you?", "What is it darling?~"])

    return chatbot.get_response(message)


# For debugging purposes
if __name__ == "__main__":
    from chatterbot.trainers import ChatterBotCorpusTrainer
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train(
        r"C:\Users\darre\Desktop\Projects\Rara-chan\src\chatbot\dataset2\conversation.yml")

    while True:
        print(chatbot.get_response(input("> ")))
