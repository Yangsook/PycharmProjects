from tkinter import *
import csv
import random

BACKGROUND = "#B1DDC6"
WHITE = "#F5F5F5"
words_data = []
showed_words = []
user_words = []
display = ""
wpm_count = 0
cpm_count = 0


def count_down(count):
    if count > 0:
        window.after_id = window.after(1000, count_down, count-1)
    else:
        window.after_id = None

    if count < 10:
        count = f"0{count}"

    if count == "00":
        compare()
        restart_button["state"] = "normal"
        window.bind("<Return>", start)

    timer_text.config(text=f"{count}")


def start_timer():
    if window.after_id is not None:
        window.after_cancel(window.after_id)

    count_down(60)


def user_type(event):
    user_words.append(entry_box.get().strip())
    entry_box.delete(0, "end")
    if len(user_words) % 8 == 0:
        random_words()


# Import words list
with open("words.csv", encoding="utf-8-sig") as data_file:
    data = csv.reader(data_file)
    for row in data:
        words_data.append(''.join(row))


def random_words():
    global display
    display = ""

    for i in range(8):
        display_word = random.choice(words_data)
        showed_words.append(display_word)
        display += (display_word + ' ')

    canvas.itemconfig(word_show, text=display)


def restart():
    global showed_words, user_words, wpm_count, cpm_count
    showed_words = []
    user_words = []
    wpm_count = 0
    cpm_count = 0
    wpm_value.config(text=wpm_count)
    cpm_value.config(text=cpm_count)
    entry_box.config(state="normal")
    entry_box.delete(0, "end")
    start_timer()
    random_words()


def start(event):
    global showed_words, user_words, wpm_count, cpm_count
    showed_words = []
    user_words = []
    wpm_count = 0
    cpm_count = 0
    wpm_value.config(text=wpm_count)
    cpm_value.config(text=cpm_count)
    entry_box.config(state="normal")
    start_timer()
    random_words()
    window.unbind("<Return>")


def compare():
    # count WPM, CPM
    global wpm_count, cpm_count
    entry_box.config(state="disabled")

    for word in user_words:
        if word.lower() in showed_words:
            wpm_count += 1
            cpm_count += len(word)

    wpm_value.config(text=wpm_count)
    cpm_value.config(text=cpm_count)
    print(f"user_type: {user_words}")
    print(f"display_words: {showed_words}")




window = Tk()
window.title("Typing Speed Test")
window.config(padx=50, pady=50, bg=BACKGROUND)
window.after_id = None

canvas = Canvas(window, width=400, height=263, bg=BACKGROUND, highlightthickness=0)
word_card_img = PhotoImage(file="images/card.png")


# Creating UI
canvas.create_image(200, 132, image=word_card_img)
word_show = canvas.create_text(200, 132, text="press the space bar after each word\n*Don't need to care about upper case\n\n-press enter to start-", font=("Courier", 14, "bold"), fill="white", justify="center", width=250)
canvas.grid(row=2, column=0, columnspan=7)


title_label = Label(text="   Typing Speed Test   ", font=("Ariel", 20), fg="Green", height=2)
title_label.grid(column=0, row=0, columnspan=7)

cpm_label = Label(text="Corrected CPM: ", font=("Arial", 12), bg=BACKGROUND)
cpm_label.grid(row=1, column=0)
cpm_value = Label(text="?", font=("Arial", 12), bg=WHITE)
cpm_value.grid(row=1, column=1)

wpm_label = Label(text="   WPM: ", font=("Arial", 12), bg=BACKGROUND)
wpm_label.grid(row=1, column=2)
wpm_value = Label(text="?", font=("Arial", 12), bg=WHITE)
wpm_value.grid(row=1, column=3)

timer_label = Label(text="   time left: ", font=("Arial", 12), bg=BACKGROUND)
timer_label.grid(row=1, column=4)
timer_text = Label(text="60", font=("Arial", 12), bg=BACKGROUND)
timer_text.grid(row=1, column=5)

restart_button = Button(text=" Restart ", command=restart, font="Ariel", bg="#20bebe", fg="white", height=2, width=15)
restart_button.grid(row=1, column=6, padx=10, pady=10, sticky="W")

entry_box = Entry(window, bg=WHITE, bd=0, font=("Arial", 12), justify="center", width=30)
entry_box.focus()
entry_box.grid(row=3, column=0, columnspan=7)

window.bind("<space>", user_type)
window.bind("<Return>", start)

window.mainloop()