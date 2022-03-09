import numpy as np
from Descriptions import SexTypes
from Brain import Brain
from SynonymEngine import Synonym
from playsound import playsound
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import numpy as np
import os
import pyttsx3

def randomFileItem(fileName):
        with open(fileName, 'r') as fin:
            names = fin.readlines()[0].split(',')
            return np.random.choice(names).strip()
      
class Agent:
    def __init__(self, seed, sex=None):
        
        # Seed the RNG
        self.seed = seed
        np.random.seed(seed)
        
        # Age and sex are shared by all agents
        self.sex = sex
        if sex == None:
            self.sex = np.random.choice(list(SexTypes))
        
        # Age range depends on agent type
        self.age = None
        
class Human(Agent):
    def __init__(self, seed=np.random.randint(1000), firstName=None, sex=None):
        Agent.__init__(self, seed, sex=SexTypes.Male)
        
        # Init translation engine
        self.translator = Translator()
        
        # Handle first names
        self.firstName = firstName
        if firstName == None:
            if self.sex == SexTypes.Male:
                self.firstName = randomFileItem('Data/Countries/Italy/Names/Human/Male/List.txt')
            else:
                self.firstName = randomFileItem('Data/Countries/Italy/Names/Human/Female/List.txt')

        self.language = 'italian'
        self.abreviatedLanguage = 'it'
        self.age = np.random.randint(18, 50)
        self.origin = randomFileItem('Data/Countries/Italy/Cities/List.txt')
        self.brain = Brain()
        self.brain.learn(f"Data/Countries/Italy/Cities/{self.origin}.dat")
        
    def listen(self, speech=False):
        if speech:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print(f"*{self.firstName} is listening...")
                recognizer.pause_threshold = 0.5
                audio = recognizer.listen(source)
                
                try:
                    self.statement = recognizer.recognize_google(audio, language='it-in')
                    print(f"*{self.firstName} heard \"{self.statement}.\"")
                    self.statement = self.translate(self.statement, "english")
                    print(f"*Translated as: \"{self.statement}.\"")
                    
                    
                except Exception as e:
                    print(f"{self.firstName} didn't hear that clearly.")
                    return
        else:
            self.statement = input("type input:")
            self.statement = self.translate(self.statement, "english")
            
        # Agent made out the words
        self.interpret()
        self.respond()
        
    def interpret(self):
        statement = self.statement.lower()
        word = statement.split()[0]
        rest = ' '.join(statement.split()[1:])
        
        # where questions
        if word == "where":
            if "are you from" in rest:
                self.response = f"I am from {self.origin}."
                return
                
            word = rest.split()[0]
            rest = ' '.join(rest.split()[1:])
            if word == "is":
                if rest in self.brain.knowledge:
                    info = self.brain.knowledge[rest]['where']
                    self.response = f"{rest} is {info}."
                    return
                else:
                    self.response = f"Sorry, I don't know where {rest} is."
                    return
                    
        # how questions
        if word == "how":
            if "old are you" in rest:
                self.response = f"I am {self.age} years old."
                return
                
        # what questions
        if word == "what":
            if "is your name" in rest:
                self.response = f"My name is {self.firstName}."
                return
                
        # General statements
        if word == "hello":
            self.response = "Hello"
            return
            
        # Process knowledge updates
        if "is in" in rest:
            key = ' '.join([word.lower(), rest.split('is in')[0]]).strip()
            if not key in self.brain.knowledge:
                self.brain.knowledge[key] = {}
            self.brain.knowledge[key]['where'] = rest.split('is in')[-1]
            self.response = "Oh, okay."
            return
        
        # Agent did not understand
        self.response = "I did not understand that"
            
    def translate(self, text, toL="italian"):
        try:
            response = self.translator.translate(text, dest=toL).text
            print(response)
            return response
           
        except Exception as e:
            print("Failed to translate")
            return "Failure"
            
    def respond(self):
    
        # Translate from english (code language) to native language
        translatedResponse = self.translate(self.response)
        
        print(f"{self.firstName} said: {translatedResponse}")
        speak = gTTS(text=translatedResponse, lang=self.abreviatedLanguage, slow=False)
        speak.save('response.mp3')
        playsound('response.mp3')
        os.remove('response.mp3')