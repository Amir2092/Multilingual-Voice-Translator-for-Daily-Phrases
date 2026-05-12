from googletrans import Translator
import speech_recognition as sr
import sys
import threading
import pygame
import pyttsx3
from PyQt5.QtCore import Qt
translator = Translator()
pygame.mixer.init()

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QInputDialog, QMessageBox, QScrollArea, QWidget
)
from PyQt5.QtGui import QFont

recognizer = sr.Recognizer()
recognizer.energy_threshold = 250   
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 1.0   
recognizer.non_speaking_duration = 0.5

class SimpleGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.is_recording = False
        #only one of each preset is needed
        self.presets = set()
        self.setWindowTitle("Speech Translator")
        self.setGeometry(200, 200, 1000, 1000)
        #fullscreen
        self.showMaximized()

        #font set to 22 to ensure better readability
        font = QFont("Arial", 22)

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

        #languages to translate to
        languages = {
            "Norwegian": "no",
            "Spanish": "es"
        }

        for name, code in languages.items():
            self.language_box.addItem(name, code)

        # Presets
        self.preset_container = QWidget()
        self.preset_layout = QVBoxLayout(self.preset_container)
        self.preset_layout.setAlignment(Qt.AlignTop)

        #Scroll area so presets dont go off screen when there are a lot of presets
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.preset_container)
        
        # Layout
        layout = QVBoxLayout()
        
        layout.addWidget(self.intro)
        layout.addWidget(self.language_box)
        layout.addWidget(scroll_area)
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
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                self.original_label.setText("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            self.original_label.setText("Processing...")
            return recognizer.recognize_google(audio, language="en-US")
        
        except sr.WaitTimeoutError:
            return "Speech not understood"
        except sr.UnknownValueError:
            return "Speech not understood"
        except Exception as e:
            print(e)
            return "Speech not understood"

    def speak(self, text):
        if not text:
            return

        def run():
            #text to speech 
            try:
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
                engine.stop()

            except Exception as e:
                print("Speech error:", e)

        threading.Thread(target=run, daemon=True).start()

    def translate(self, text):
        #translate into desired language
        target_lang = self.language_box.currentData()
        result = translator.translate(text, dest=target_lang)
        translated_text = result.text 
        return translated_text

    def handle_record(self):
        if self.is_recording:
            return
        self.is_recording = True
        #record button should be disabled during recording to avoid error
        self.record_button.setEnabled(False)
        self.original_label.setText("Listening...")
        self.translated_label.setText("")

        threading.Thread(target=self.record_and_translate, daemon=True).start()
        
    def record_and_translate(self):
        text = self.microphone()

        self.recognized_text = text
        self.original_label.setText(text)

        if text and text != "Speech not understood":
            #translate speech if speech is understood
            self.original_label.setText(text)
            self.translated_label.setText("Translating...")
            translated = self.translate(text)
            self.translated_label.setText(translated)
            self.speak(translated) 
        else:
            self.original_label.setText("Could not understand speech")
            self.translated_label.setText("")

        self.is_recording = False
        #stop recording afterwards
        self.record_button.setEnabled(True)
        #enable the record button after the previous recording is finished

    def use_predefined_text(self, phrase):
        if self.is_recording:
            return
        self.handle_preset(phrase)

    def handle_preset(self, phrase):
        self.recognized_text = phrase
        self.original_label.setText(phrase)

        self.translated_label.setText("Translating...")
        translated = self.translate(phrase)

        self.translated_label.setText(translated)
        self.speak(translated)

    def save_preset(self):
        #fontsize to 20 for better readability
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        if not self.recognized_text:
            return
        if self.recognized_text=="Speech not understood":
            #to avoid speech not understood being set as a preset
            msg = QMessageBox()
            msg.resize(800, 500)
            msg.setFont(font)
            msg.setWindowTitle("Alert")
            msg.setText("You can't set this as a predefined option")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()
        else:
            app = QApplication.instance()
            app.setFont(font)
            dialog = QInputDialog()
            dialog.setFont(font)
            text, ok = dialog.getText(
            self,
            "Save Phrase",
            "Edit phrase:",
            text=self.recognized_text
            )
            if ok and text:
                if text in self.presets:
                    #only allow one of each preset
                    QMessageBox.warning(self, "Duplicate", "This preset already exists!")
                    return
                btn = QPushButton(text)
                #better readability for the preset buttons
                btn.setFont(QFont("Arial", 22))
                btn.clicked.connect(lambda checked, p=text: self.use_predefined_text(p))
                self.preset_layout.addWidget(btn)
                self.presets.add(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleGUI()
    window.show()
    sys.exit(app.exec_())
