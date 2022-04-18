# Day89 GUI - Disappearing Text Writing App

from tkinter import *
import time
import threading

BACKGROUND = "#ff7171"
count = 5
pretext = ""


def key(event):
    global pretext
    pretext = text.get("1.0", END)
    thread_start()


def timer():
    global pretext
    global count

    timer_text.config(text=f"{count} seconds")


    intext = text.get("1.0", END)
    print(f"count= {count}, pretext = {pretext}, intext = {intext}")

    if intext != "":
        time.sleep(1)
        count -= 1

        if pretext != intext:
            count = 5
        else:
            fadeaway()
            if count == 0:
                timer_text.config(text=f"{count} seconds")
                text.delete("1.0", END)
                print("delete")
            else:
                thread_start()


def thread_start():
    t = threading.Thread(target=timer)
    t.start()

def fadeaway():
    global count
    if count in [0, 5]:
        window.attributes("-alpha", 1)
    else:
        window.attributes("-alpha", count * 0.2)

def appclose():
    window.quit()




window = Tk()
window.title("Disappearing Text Writing App")
window.config(padx=50, pady=50, bg=BACKGROUND)
window.after_id = None

title_text1 = "The Most Dangerous Writing App\n"
title_label = Label(text=title_text1, font=("Arial", 30), bg=BACKGROUND, fg="white")
title_label.pack()

title_text2 = "Don’t stop writing, or all progress will be lost."
title_label2 = Label(text=title_text2, font=("Arial", 16), bg=BACKGROUND)
title_label2.pack()

timer_text = Label(text="00:00", font=("Arial", 30), fg="red", bg=BACKGROUND)
timer_text.pack()

# Text with Frame : It makes you keep main window when you write again after 5 seconds
text_frame = Frame(window, padx=10, pady=10).pack()
text = Text(text_frame, padx=10, pady=10, height=10, width=35, highlightthickness=0, font=("Courier", 20), bg="#FADBD8")
text.pack()

title_label = Label(text='\n', bg=BACKGROUND).pack()

close_btn = Button(text="close", command=appclose, padx=10, font=("Arial", 15))
close_btn.pack()



window.bind("<KeyPress>", key)
window.mainloop()