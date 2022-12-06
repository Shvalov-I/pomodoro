from tkinter import *
import math
from pixels_graph import ProgrammingGraph
# import beepy

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = ""
graph = ProgrammingGraph()


def raise_above_all(win):
    # beepy.beep(sound=1)
    win.wm_state('normal')
    win.attributes('-topmost', 1)
    win.attributes('-topmost', 0)


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)
    title_label.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")
    check_marks.config(text="")
    global reps
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        title_label.config(text="Break", fg=RED)
        count_down(long_break_sec)
    elif reps % 2 == 0:
        title_label.config(text="Break", fg=PINK)
        count_down(short_break_sec)
    else:
        title_label.config(text="Work", fg=GREEN)
        count_down(work_sec)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = int(count // 60)
    count_sec = int(count % 60)
    if count_sec < 10:
        count_sec = "0" + str(count_sec)
    if count_min < 10:
        count_min = "0" + str(count_min)
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        if title_label["text"] == "Work" and count != WORK_MIN * 60 and count % 60 == 0:
            graph.calculate_score(1/60)
        timer = window.after(1000, count_down, count-1)
    else:
        start_timer()
        raise_above_all(window)
        marks = ""
        work_session = math.floor(reps / 2)
        for _ in range(work_session):
            marks += "✔"
            check_marks.config(text=f"{marks}")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 135, text="00:00", fill="white", font=(FONT_NAME, 40, "bold"))
canvas.grid(row=1, column=1)


# Label
title_label = Label()
title_label.config(text="Timer", font=(FONT_NAME, 40), bg=YELLOW, fg=GREEN)
title_label.grid(row=0, column=1)

check_marks = Label()
check_marks.config(bg=YELLOW, fg=GREEN)
check_marks.grid(row=3, column=1)

# Button
start_button = Button()
start_button.config(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(row=2, column=0)

reset_button = Button()
reset_button.config(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(row=2, column=2)

window.mainloop()
