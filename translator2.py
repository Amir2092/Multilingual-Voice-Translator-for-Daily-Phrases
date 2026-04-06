from googletrans import Translator
import speech_recognition as sr
import sys
import threading
import pygame
import pyttsx3

translator = Translator()
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

        self.setWindowTitle("Speech Translator")
        self.setGeometry(200, 200, 1000, 1000)

        font = QFont("Arial", 16)

        # Labels
        self.intro = QLabel(
            "Welcome to the Speech translator!\n"
            "Speak English and get it translated and spoken back to you\n"
        )
        self.intro.setFont(font)

        self.original_label = QLabel("Recognized english text will appear here")
        self.original_label.setFont(font)

        self.translated_label = QLabel("Translated text will appear here")
        self.translated_label.setFont(font)

        # Buttons
        self.record_button = QPushButton("Start Recording")
        self.record_button.setFont(font)

        self.save_button = QPushButton("Save as Preset")
        self.save_button.setFont(font)

        # Dropdown
        self.language_box = QComboBox()
        self.language_box.setFont(font)

        languages = {
            "Norwegian": "no",
            "Spanish": "es"
        }

        for name, code in languages.items():
            self.language_box.addItem(name, code)

        # Presets
        self.preset_layout = QHBoxLayout()

        phrases = [
            "I need help",
            "Where is the nearest bus?",
            "Thank you"
        ]

        for phrase in phrases:
            btn = QPushButton(phrase)
            btn.setFont(font)
            btn.clicked.connect(lambda checked, p=phrase: self.use_predefined_text(p))
            self.preset_layout.addWidget(btn)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.intro)
        layout.addWidget(self.language_box)
        layout.addLayout(self.preset_layout)
        layout.addWidget(self.original_label)
        layout.addWidget(self.translated_label)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.record_button)
        btn_layout.addWidget(self.save_button)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.recognized_text = ""

        self.record_button.clicked.connect(self.handle_record)
        self.save_button.clicked.connect(self.save_preset)

    def microphone(self):
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            return recognizer.recognize_google(audio, language="en")
        except Exception as e:
            print(e)
            return "Speech not understood"

    def speak(self, text):
        def run():
            try:
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
                engine.stop()
            except Exception as e:
                print("Speech error:", e)

        threading.Thread(target=run, daemon=True).start()

    def translate(self, text):
        target_lang = self.language_box.currentData()

        result = translator.translate(text, dest=target_lang)
        translated_text = result.text 

        self.speak(translated_text)

        return translated_text

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

        text, ok = QInputDialog.getText(
            self,
            "Save Phrase",
            "Edit phrase:",
            text=self.recognized_text
        )

        if ok and text:
            btn = QPushButton(text)
            btn.setFont(QFont("Arial", 16))
            btn.clicked.connect(lambda checked, p=text: self.use_predefined_text(p))
            self.preset_layout.addWidget(btn)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleGUI()
    window.show()
    sys.exit(app.exec_())
