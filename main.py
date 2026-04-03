import tkinter as tk
from tkinter import ttk  ##use from tkinter here because we need newewer widgets and more modern that we need for menu language (combobox). That's why tk is for basic section and ttk is for more modern section

# Here this create the main app window
root = tk.Tk()

# Here we got this variable that remembers whether dark mode is on or off
is_dark = False

# We set the title shown in the top window bar
root.title("Multilingual Voice Translator")

# We set the size of the window panel
root.geometry("900x600")


# Here its a Function to switch between light mode and dark mode
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

        is_dark = True


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
    font=("Arial", 12),
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
    font=("Arial", 12),
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
    font=("Arial", 12),
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
    bg="lightgray",
    fg="black",
    command=toggle_theme
)
toggle_button.pack(pady=10)

# Create translate button
translate_button = tk.Button(
    root,
    text="Translate",
    bg="lightgray",
    fg="black"
)
translate_button.pack(pady=10)

# Set the starting window background
root.configure(bg="white")

# Keep the app running
root.mainloop()