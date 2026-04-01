from deep_translator import GoogleTranslator
import speech_recognition as sr
import sys
import os
import gtts.lang
import time
from gtts import gTTS
import pygame

pygame.mixer.init()
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QInputDialog
)
from PyQt5.QtGui import QFont
recognizer = sr.Recognizer()


class SimpleGUI(QWidget):
    def __init__(self):
        super().__init__()
        # list to save the temporary audio files to
        self.audio_files = []
        self.setWindowTitle("Speech Translator")
        self.setGeometry(200, 200, 1000, 1000)

        # Set font type and size for better accesibility
        font = QFont("Arial", 16)

        # Labels
        self.intro = QLabel("Welcome to the Speech translator! Here you can translate english speech into your desired language, \n" 
        "just pick a langauge in the drop down and it will translate and say it back to you in that language! \n"
        "You can also pick some pre defined options and even save your speech as a new option.")
        self.intro.setFont(font)
        self.original_label = QLabel("Recognized text will appear here")
        self.original_label.setFont(font)
        self.translated_label = QLabel("Translated text will appear here")
        self.translated_label.setFont(font)

        # Buttons
        self.record_button = QPushButton("Start Recording")
        self.record_button.setFont(font)
        self.save_button = QPushButton("Save as Preset")
        self.save_button.setFont(font)
        
        # Dropdown for languages
        self.languages_label = QLabel("Pick your desired language from the dropdown")
        self.languages_label.setFont(font)

        # Get all the languages gtts offers
        languages = gtts.lang.tts_langs() 

        self.language_box = QComboBox()
        self.language_box.setFont(font)
        
        # add all the languages in a sorted order
        for code, name in sorted(languages.items(), key=lambda x: x[1]):
            self.language_box.addItem(name, code)

        # pre-defined options
        self.preset_layout = QHBoxLayout()
        self.preset_label = QLabel("Pick a pre-defined option by clicking on one of the buttons")
        self.preset_label.setFont(font)
        phrases = [
            "I need help",
            "Where is the nearest bus?",
            "Thank you"
        ]
        
        for phrase in phrases:
            btn = QPushButton(phrase)
            btn.setFont(QFont("Arial", 16))
            btn.clicked.connect(lambda checked, p=phrase: self.use_predefined_text(p))
            self.preset_layout.addWidget(btn)
        
        # Layouts
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.record_button)
        button_layout.addWidget(self.save_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.intro)
        main_layout.addWidget(self.languages_label)
        main_layout.addWidget(self.language_box)
        main_layout.addWidget(self.preset_label)
        main_layout.addLayout(self.preset_layout)
        main_layout.addWidget(self.original_label)
        main_layout.addWidget(self.translated_label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Store last recognized text
        self.recognized_text = ""

        # Connect buttons to their functions
        self.record_button.clicked.connect(self.handle_record)
        self.save_button.clicked.connect(self.save_preset)

    def microphone(self):
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            # use english as audio language
            text = recognizer.recognize_google(audio, language="en")
            return text
        except:
            return "Speech not understood"

    def translate(self, text):
        # language to translate to is equal to what is picked in the drop down
        target_lang = self.language_box.currentData()
        # translate from english to that language
        translator = GoogleTranslator(source="en", target=target_lang)
        translated_text = translator.translate(text)

        # create temporarily mp3 audiofile for the translation
        filename = f"audio_{int(time.time())}.mp3"
        self.audio_files.append(filename)
        # use gTTS for text to speech
        tts = gTTS(text=translated_text, lang=target_lang)
        tts.save(filename)

        # play the audio file out loud for tts
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        return translated_text

    # Button handlers
    def handle_record(self):
        self.recognized_text = self.microphone()
        self.original_label.setText(self.recognized_text)
        
        if self.recognized_text:
            translated = self.translate(self.recognized_text)
            self.translated_label.setText(translated)
        else:
            self.translated_label.setText("No text to translate!")

    def use_predefined_text(self, phrase):
        self.recognized_text = phrase
        self.original_label.setText(phrase)

        translated = self.translate(phrase)
        self.translated_label.setText(translated)
    
    def save_preset(self):
        if not self.recognized_text:
            return
        # ability to edit text and save it as predefined option
        text, ok = QInputDialog.getText(
            self,
            "Save Phrase",
            "Edit phrase:",
            text=self.recognized_text
        )
        # create the option as a new button
        if ok and text:
            btn = QPushButton(text)
            btn.setFont(QFont("Arial", 16))
            btn.clicked.connect(lambda checked, p=text: self.use_predefined_text(p))
            self.preset_layout.addWidget(btn)
    
    def closeEvent(self, event):
        # Delete the file when closing
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        time.sleep(0.1) 

        # Loop through each file
        for file in self.audio_files:
            if os.path.exists(file):
                try:
                    os.remove(file)
                    print(f"Deleted: {file}")
                except Exception as e:
                    print(f"Error deleting {file}: {e}")
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleGUI()
    window.show()
    sys.exit(app.exec_())
