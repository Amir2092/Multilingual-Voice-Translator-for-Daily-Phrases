import tkinter as tk
from tkinter import ttk  ##use from tkinter here because we need newewer widgets and more modern that we need for menu language (combobox). That's why tk is for basic section and ttk is for more modern section
from googletrans import Translator  #used to translate eng to another languages...
import speech_recognition as sr     #this listens to microphone to convert speech to text
import pyttsx3                      #from text to speech... so users can listen to voice speech from pc.. sound 
import threading                #we use threading in order to run speech(sound) in background so we have thread of gui and speech so app dont slow,crash
import pythoncom                #Needed for audio system(windows)

# Here this create the main app window
root = tk.Tk()

# Here we got this variable that remembers whether dark mode is on or off, where false means dark mode is off
is_dark = False

# We create recognizer that listens and converts speech to text..
recognizer = sr.Recognizer()    

# We set the title shown in the top window bar
root.title("Multilingual Voice Translator")

# We set the size of the window panel
root.geometry("900x600")


# Here its a Function to switch between light mode and dark mode(aka dark mode function that we need here )
def toggle_theme():
    global is_dark

    if is_dark:
        root.configure(bg="white")
        title_label.configure(bg="white", fg="black")  ##here we do for thing on the panel, dark light mode
        language_label.configure(bg="white", fg="black")
        original_label.configure(bg="white", fg="black")
        translated_label.configure(bg="white", fg="black")

        original_text.configure(bg="white", fg="black")
        translated_text.configure(bg="white", fg="black")

        toggle_button.configure(bg="lightgray", fg="black", text="Switch to Dark Mode")
        translate_button.configure(bg="lightgray", fg="black")

        
        start_button.configure(bg="lightgray", fg="black")
        stop_button.configure(bg="lightgray", fg="black")
        status_label.configure(bg="white", fg="black")

        is_dark = False
    else:
        root.configure(bg="black")
        title_label.configure(bg="black", fg="white")
        language_label.configure(bg="black", fg="white")
        original_label.configure(bg="black", fg="white")
        translated_label.configure(bg="black", fg="white")

        original_text.configure(bg="gray", fg="white")
        translated_text.configure(bg="gray", fg="white")

        toggle_button.configure(bg="gray", fg="white", text="Switch to Light Mode")
        translate_button.configure(bg="gray", fg="white")

        
        start_button.configure(bg="gray", fg="white")
        stop_button.configure(bg="gray", fg="white")
        status_label.configure(bg="black", fg="white")

        is_dark = True


# Function for Start button
def start_listening():
    try:
        status_label.config(text="Listening...")           #we get text "listning" as status
        root.update()               #forces the gui to refresh immediatly, or status label will not update automatically

        with sr.Microphone(device_index=48) as source:   ##choosing 48 input of my mic, depends on the pc, choose 48 for testing. this here open micriphone
            
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)   #there here record voice, it waits 5sec for us to start speaking, records our voice and stops after 5 sec max

        status_label.config(text="Recognizing...")  #it updates status again when it recognize/detects a voice
        root.update()

        text = recognizer.recognize_google(audio, language="en-US") #sends recored auido to google speech recognition, and returns text

        original_text.delete("1.0", tk.END) #deletes everything in the inpit box, so when we insert new words, we dont have first and second speech combined, like hello how u doing+whast u eating on same voice..
        original_text.insert(tk.END, text) #inserts text at the end, we use tk, because we dont know where the text end, tinkter know and handles it automatically. where "1:0" corresponds to first page, first letter, END laste page so its like we erase from first page to laste page in order to write a new sentence 

        status_label.config(text="Speech recognized")
    #all of this excpetions(errors) are defined in SpeechRecognition library, so all this errors such as waittimeouterror,unknownvalueerror are build in this lib.
    except sr.WaitTimeoutError:     
        status_label.config(text="No speech detected")
    except sr.UnknownValueError:
        status_label.config(text="Could not understand speech")
    #here any other error that wasnt caught, get caught here and it stores it inside "e", so it shows acttual message error that we got 
    except Exception as e:
        status_label.config(text=f"Error: {e}") 

# Function for Stop button, but stop button is useless just for look in app to have better ui look, bcz voic speech after clicking on start listing, it automatically stops after 5 sec
def stop_listening():
    status_label.config(text="Stopped")


# this function is responslibe abt taking the translated text, choosing a voice, and then making the pc speak it alout.(Text-To-Speech)
def speak_translation(text, selected_language):  #"text" is translated text I want the pc to say, where "selected language", is the drop down main menu for language choose.
    def run_speech(): #here we create new function insde speack_translation in order to run the speech in background in another thread, so without the inside function everything freezes if we use the main one: "speak_translation"
        pythoncom.CoInitialize()    #this is as windows specipc setup, without it speech may fail or work only wonce, because pyttsx3 often uses windows speech engine features that depends on COM.

        try:
            new_engine = pyttsx3.init() #we create new engine for text-to-speech engine, becuase I noticed sometimes after first sentence it dont work anymore instead of reusing same engine and then speech only work 1 time and thats it.. So instead of putting this line of code as global(outside this function), we write it here, so with each time this function runs(when translate button exactly clicks) so a new engien is created
        

            # slower speech for better understanding
            new_engine.setProperty("rate", 135)   ##for sound better, 135 so he speaks slower instead of super fast

            voices = new_engine.getProperty('voices')   #here we get the list of voices that exists on the pc
            new_engine.setProperty('voice', voices[0].id) #here we just use the system default voice, because the language voice packages were anyway 0mb so the extra matching logic was not helping in real way

            new_engine.say(text)   #here the engine gets the translated text and prepares to say it
            new_engine.runAndWait()   #here it actually speaks and waits until speech is finished
        finally:
            pythoncom.CoUninitialize()      #here after we started pythoncom.CouInitialize at top, we need to close it if we dont close it so we get bugs in speeching etc.. and we use try,finally to keep them safe instead of having issues and break

    threading.Thread(target=run_speech, daemon=True).start()  #here we start the background thread so speech runs without freezing the gui


# This function is for: first it takes input(text), translate, show translated text(result) and then speak it. 
def translate_text():
    translator = Translator()   #here we create translator object from googletrans lib, this obj is connected to google translate and does the translation

    # Get text from the original text box
    text = original_text.get("1.0", tk.END).strip() #here we again, start fromn line 1, character 0 in page and go until the end, where strip remove empty spaces bcz tinker add spaces automatically at end of sentence

    # if text box is empty, do not try to translate, so if user didnt speak anything so we get this on screen:
    if not text:
        status_label.config(text="Please enter or speak text first")    
        return

    # Get selected language from dropdown
    selected_language = language_menu.get() #it get information from what user selected from language main menu.

    # Convert language names into translator codes
    language_codes = {
        "Norwegian": "no",
        "Spanish": "es",
        "French": "fr"
    }

    target_code = language_codes.get(selected_language, "no")

    try:
        # Translate the text
        translated = translator.translate(text, dest=target_code)   #"text" what user said or typed. dest=target_Code: is the language we wish to translate to

        # Clear old translated text
        translated_text.delete("1.0", tk.END)

        # Insert new translated text
        translated_text.insert(tk.END, translated.text)

        # Update status
        status_label.config(text="Translation complete")

        # Speak translated text aloud
        speak_translation(translated.text, selected_language)

    except Exception as e:
        status_label.config(text=f"Translation error: {e}")


# It create the title text inside the app
title_label = tk.Label(
    root,
    text="Multilingual Voice Translator",
    font=("Arial", 20, "bold"),
    bg="white",
    fg="black"
)
title_label.pack(pady=20)

# We create label for language dropdown (create here the text "choose language" )
language_label = tk.Label(
    root,
    text="Choose target language:",
    font=("Arial", 15),
    bg="white",
    fg="black"
)
language_label.pack(pady=5)

# Create dropdown menu to decide which language
language_menu = ttk.Combobox(
    root,
    values=["Norwegian", "Spanish", "French"],
    state="readonly"
)
language_menu.pack(pady=5)
language_menu.set("Norwegian")

# Create label for original text (same thing, we create "orgiinal text here")
original_label = tk.Label(
    root,
    text="Original English text:",
    font=("Arial", 15),
    bg="white",
    fg="black"
)
original_label.pack(pady=5)

# Create text box for original text so we can write into it
original_text = tk.Text(
    root,
    height=5,
    width=60,
    bg="white",
    fg="black"
)
original_text.pack(pady=5)

# Create label for translated text
translated_label = tk.Label(
    root,
    text="Translated text:",
    font=("Arial", 15),
    bg="white",
    fg="black"
)
translated_label.pack(pady=5)

# Create text box for translated text
translated_text = tk.Text(
    root,
    height=5,
    width=60,
    bg="white",
    fg="black"
)
translated_text.pack(pady=5)

# Create dark mode button
toggle_button = tk.Button(
    root,
    text="Switch to Dark Mode",
    font=("Arial", 16, "bold"),
    bg="lightgray",
    fg="black",
    command=toggle_theme
)
toggle_button.pack(pady=10)

# Create translate button
translate_button = tk.Button(
    root,
    text="Translate Text",
    font=("Arial", 16, "bold"),
    bg="lightgray",
    fg="black",
    command=translate_text
)
translate_button.pack(pady=10)

# 🔹 NEW BUTTONS

# Create Start button
start_button = tk.Button(
    root,
    text="Start Listening",
    font=("Arial", 16, "bold"),
    bg="lightgray",
    fg="black",
    command=start_listening
)
start_button.pack(pady=5)

# Create Stop button
stop_button = tk.Button(
    root,
    text="Stop",
    font=("Arial", 16, "bold"),
    bg="lightgray",
    fg="black",
    command=stop_listening
)
stop_button.pack(pady=5)

# 🔹 STATUS LABEL
status_label = tk.Label(
    root,
    text="Ready",
    font=("Arial", 14,"bold"),
    
    bg="lightgray",
    fg="black"
)
status_label.pack(pady=10)

# Set the starting window background
root.configure(bg="white")

# Keep the app running
root.mainloop()