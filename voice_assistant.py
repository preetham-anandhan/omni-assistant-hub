import datetime
import json
import os
import sys
import time
import webbrowser
import requests
import pyttsx3
import speech_recognition as sr

# =====================================================================
# ASSISTANT CONFIGURATION
# =====================================================================
WAKE_WORD = "nova"
WEATHER_API_KEY = "your_openweather_api_key_here"  # Optional: Add key to enable weather
NEWS_API_KEY = "your_newsapi_org_key_here"        # Optional: Add key to enable real news

class VoiceAssistant:
    def __init__(self):
        # Initialize Text-to-Speech Engine
        self.engine = pyttsx3.init()
        self._configure_voice()
        
        # Initialize Speech Recognizer
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        
        # Micro State storage
        self.reminders_file = "reminders.json"
        self.load_reminders()

    def _configure_voice(self):
        """Sets clean playback configurations for the TTS engine."""
        voices = self.engine.getProperty('voices')
        # Index 1 usually provides a clearer female voice synthesis, 0 for male.
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)
        self.engine.setProperty('rate', 180)  # Moderate talking pace (Words Per Minute)
        self.engine.setProperty('volume', 1.0) # Full system execution volume

    def speak(self, text):
        """Converts text string into natural voice synthesis line-by-line."""
        print(f"🔊 Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Listens via system microphone with dynamic ambient noise calibration."""
        with sr.Microphone() as source:
            print("\n🎙️ Listening...")
            # Adjusts sensitivity profile to accommodate structural room echoes
            self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                print("⚡ Processing acoustic matrix...")
                query = self.recognizer.recognize_google(audio, language="en-US")
                print(f"👤 User: {query}")
                return query.lower()
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                print("❌ Could not understand audio profile.")
                return ""
            except sr.RequestError:
                self.speak("Network connection to translation servers disrupted.")
                return ""

    # =====================================================================
    # TASK CAPABILITIES
    # =====================================================================
    def check_weather(self, command):
        """Fetches live weather or points to mock framework if API keys are empty."""
        if WEATHER_API_KEY == "your_openweather_api_key_here":
            self.speak("Weather API integration is structural. Currently, it's 22 degrees Celsius and partly cloudy.")
            return

        # Simple extraction logic out of voice string
        city = "New York"
        if "in " in command:
            city = command.split("in ")[-1]
            
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        try:
            res = requests.get(url).json()
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"]
            self.speak(f"The current temperature in {city} is {temp} degrees Celsius with {desc}.")
        except Exception:
            self.speak("Could not reach weather nodes at this time.")

    def read_news(self):
        """Fetches dynamic global headlines or reads standard current feed."""
        if NEWS_API_KEY == "your_newsapi_org_key_here":
            self.speak("Here is your top headline: Space exploration advancements reach a new milestone this week.")
            return

        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
        try:
            articles = requests.get(url).json().get("articles", [])[:3]
            self.speak("Here are today's top three updates.")
            for i, art in enumerate(articles, 1):
                self.speak(f"Headline {i}: {art['title']}")
        except Exception:
            self.speak("Unable to synchronize with the news wire.")

    def set_reminder(self, command):
        """Saves text-based string markers mapped directly against timelines."""
        # Parsing basic syntax patterns: "remind me to [task]"
        reminder_content = command.replace("set a reminder to", "").replace("remind me to", "").strip()
        if not reminder_content:
            self.speak("What exactly would you like me to remind you about?")
            reminder_content = self.listen()
            
        if reminder_content:
            self.reminders.append({"task": reminder_content, "timestamp": str(datetime.datetime.now())})
            self.save_reminders()
            self.speak(f"I have successfully logged a reminder to: {reminder_content}")

    def list_reminders(self):
        """Reads back active memory structural data logs."""
        if not self.reminders:
            self.speak("Your structural reminder log is completely clear.")
            return
        self.speak(f"You have {len(self.reminders)} active reminders.")
        for item in self.reminders:
            self.speak(item["task"])

    def load_reminders(self):
        if os.path.exists(self.reminders_file):
            with open(self.reminders_file, 'r') as f:
                self.reminders = json.load(f)
        else:
            self.reminders = []

    def save_reminders(self):
        with open(self.reminders_file, 'w') as f:
            json.dump(self.reminders, f)

    # =====================================================================
    # MAIN CONTROL ENGINE Loop
    # =====================================================================
    def run(self):
        self.speak(f"Voice interface online. Say '{WAKE_WORD}' to initialize commands.")
        
        while True:
            raw_input = self.listen()
            
            # Look for wake word activation state
            if WAKE_WORD in raw_input:
                self.speak("System listening. How can I assist you?")
                command = self.listen()
                
                if not command:
                    continue
                
                if "weather" in command:
                    self.check_weather(command)
                    
                elif "news" in command:
                    self.read_news()
                    
                elif "remind" in command:
                    self.set_reminder(command)
                    
                elif "what are my reminders" in command or "list reminders" in command:
                    self.list_reminders()
                    
                elif "time" in command:
                    current_time = datetime.datetime.now().strftime("%I:%M %p")
                    self.speak(f"The current internal clock reads {current_time}.")
                    
                elif "open google" in command:
                    self.speak("Opening browser pipeline.")
                    webbrowser.open("https://google.com")
                    
                elif "shutdown" in command or "stop" in command or "exit" in command:
                    self.speak("Shutting down core runtime loops. Goodbye.")
                    sys.exit()
                    
                else:
                    self.speak("Command fell outside current functional matrix. Can you rephrase?")
            
            # Short processing break to avoid resource thrashing
            time.sleep(0.2)

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()