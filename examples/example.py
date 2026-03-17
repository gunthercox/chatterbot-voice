from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import speech_recognition
import subprocess
import platform
import datetime
import random

class VoiceChatBot(ChatBot):

    def speak(self, text):
        if platform.system() == 'Darwin':
            cmd = ['say', str(text)]
            subprocess.call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            subprocess.run('echo "' + str(text) + '" | festival --tts', shell=True)

    def get_response(self, statement=None, **kwargs):
        response = super().get_response(statement, **kwargs)
        self.speak(response.text)
        return response.text  # return the text for logging or command handling

# Initialize bot
bot = VoiceChatBot('Example ChatBot')
trainer = ChatterBotCorpusTrainer(bot)
trainer.train('chatterbot.corpus.english')

# Randomized greeting
greetings = ["Hello!", "Hi there!", "Hey! How can I help you?"]
bot.speak(random.choice(greetings))

# Initialize speech recognizer
recognizer = speech_recognition.Recognizer()

# File to log conversation
log_file = "chat_log.txt"

# List of simple jokes
jokes = [
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I told my computer I needed a break, and it said no problem—it needed one too!",
    "Why do bees have sticky hair? Because they use honeycombs!"
]

while True:
    try:
        with speech_recognition.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            audio = recognizer.listen(source)

            result = recognizer.recognize_google(audio)
            print(f"You said: {result}")

            # Basic commands
            if "time" in result.lower():
                response_text = f"The current time is {datetime.datetime.now().strftime('%H:%M')}"
                bot.speak(response_text)
            elif "joke" in result.lower():
                response_text = random.choice(jokes)
                bot.speak(response_text)
            else:
                response_text = bot.get_response(statement=result)

            # Log conversation
            with open(log_file, "a") as f:
                f.write(f"User: {result}\nBot: {response_text}\n")

    except speech_recognition.UnknownValueError:
        bot.speak("I am sorry, I could not understand that.")
    except speech_recognition.RequestError as e:
        message = 'My speech recognition service has failed. {0}'
        bot.speak(message.format(e))
    except (KeyboardInterrupt, EOFError, SystemExit):
        bot.speak("Goodbye!")
        break
