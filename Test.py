from playsound import playsound
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import numpy as np
import os

outputLanguage = 'italian'
lookup = { 'italian': 'it', 'english': 'en' }
abreviatedLanguage = lookup[outputLanguage]
    
class Agent:
    def __init__(self):
        self.hunger = np.random.randint(low=0, high=100, size=1)[0]
        self.tiredness = np.random.randint(low=0, high=100, size=1)[0]
        self.unhappiness = np.random.randint(low=0, high=100, size=1)[0]
        
        self.mood = None
        self.degree = 'a little'
        
    def calculateMood(self):
        
        # Find primary mood
        self.mood = ['hungry', 'tired', 'unhappy'][np.argmax([self.hunger, self.tiredness, self.unhappiness])]
        
        # Calculate degree of primary mood
        if self.mood == 'hungry':
            val = self.hunger
        elif self.mood == 'tired':
            val = self.tiredness
        elif self.mood == 'unhappy':
            val = self.unhappiness
        if val >= 80:
            self.degree = np.random.choice(['extremely', 'exceptionally'], 1)[0]
        elif val >= 60:
            self.degree = np.random.choice(['very', 'pretty'], 1)[0]
        elif val >= 40:
            self.degree = np.random.choice(['slightly', 'rather'], 1)[0]
        else:
            self.degree = np.random.choice(['somewhat', 'a little'], 1)[0]
        
    def ask(self, question):
        self.calculateMood()
        if 'how are you' in question:
            response = np.random.choice(['How about you?', 'And how are you doing today?', 'How have you been?'], 1)[0]
            return f"I'm {self.degree} {self.mood}. {response}"
        else:
            return "Can you repeat that?"
        
def takeCommand(voice=False):
    if voice:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
            
            try:
                print("Recognizing...")
                query = r.recognize_google(audio, language='en-in')
                print(f"user said {query}\n")
            except Exception as e:
                print("Say that again please...")
                return "None"
            return query
    return input('Input:')
        
translator = Translator()

while True:
    
    # Generate new agent every time
    marco = Agent()
    
    # Get input
    userQuestion = takeCommand()
    while (userQuestion == "None"):
        userQuestion = takeCommand()
        
    botResponse = marco.ask(userQuestion)
        
    text_to_translate = translator.translate(botResponse, dest=outputLanguage)
    text = text_to_translate.text
    
    speak = gTTS(text=text, lang=abreviatedLanguage, slow=False)
    speak.save('a.mp3')
    playsound('a.mp3')
    os.remove('a.mp3')