from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

#--------------------------------------NEXT CARD----------------------------------------#
data = pd.DataFrame()
current_card = {}
to_learn = {}

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pd.read_csv("data/french_words.csv")
    to_learn = data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

def next_card():

    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_image)
    flip_timer = window.after(3000, func=flip_card) # type: ignore

def flip_card():

    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_image)

def is_known():
    to_learn.remove(current_card)
    remained_data = pd.DataFrame(to_learn)
    remained_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

#--------------------------------------UI----------------------------------------#
#Main Window
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card) # type: ignore

#Images
card_back_image = PhotoImage(file="images/card_back.png")
card_front_image = PhotoImage(file="images/card_front.png")
check_image = PhotoImage(file="images/right.png")
unknown_image = PhotoImage(file="images/wrong.png")

#Canvas
canvas = Canvas(window, width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_background = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400, 175, font=("Arial", 40, "italic"), text="")
card_word = canvas.create_text(400, 300, font=("Arial", 60, "bold"), text="")
canvas.grid(row=0, column=0, columnspan=2)

#Buttons
check_button = Button(window, image=check_image, highlightthickness=0, command=is_known)
check_button.grid(row=1, column=1)
unknown_button = Button(window, image=unknown_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

next_card()
window.mainloop()
