from tkinter import* #import tkinker
from PIL import Image, ImageTk   # Ensure Pillow is installed
import time

PINK = "#faa28e"
RED = "#e7305b"
GREEN = "#1b5725"
BACKGROUND = "#F5F2ED"
FONT_NAME = "Comic Sans MS"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None


#create main window

mainWindow = Tk()
mainWindow.title("Pomodoro Timer⏲️")
mainWindow.config(padx=50, pady=50, bg=BACKGROUND)



label_1 = Label(
    text="🍅 Pomodoro Timer",
    font=(FONT_NAME, 40, "bold"),
    fg=GREEN,
    bg=BACKGROUND,
    highlightthickness=0,
)
label_1.grid(row=0, column=1)

my_image = Image.open("tomato.png")  # Ensure the image file exists
my_image = my_image.resize((400, 350))  # Resize image to fit window
my_image = ImageTk.PhotoImage(my_image)

# Create Label to display the image using grid
bg_img = Label(mainWindow, image=my_image, text="00:00",
    bg=BACKGROUND)
bg_img.grid(row=10, column=0, columnspan=3, rowspan=3)  # Span multiple rows and columns
label_Timer = Label(
    
    font=(FONT_NAME, 30, "bold"),
    fg=GREEN,
    bg="#ce1417",
    highlightthickness=0,
)
label_Timer.grid(row=11, column=1)


# function to count down
def countdown(): 
    t = 120
    while t >-1: 
        mins, secs = divmod(t, 60) 
        timer = f"{mins:02d}:{secs:02d}"
        label_Timer.config(text=timer)
        t -= 1
        mainWindow.update()
        time.sleep(1)

#create buttons

button_start = Button(
    mainWindow,
    text="Start",
    font=(FONT_NAME, 25),
    bg=GREEN,
    fg=BACKGROUND,
    command= countdown,
)

button_pause = Button(
    mainWindow,
    text="Pause",
    font=(FONT_NAME, 20),
    bg=PINK,
    fg=BACKGROUND,
    # command=pause_timer,
)

button_reset = Button(
    mainWindow,
    text="Reset",
    font=(FONT_NAME, 20),
    bg=RED,
    fg=BACKGROUND,
    # command=reset_timer,
)

# Place buttons in grid
button_pause.grid(row=20, column=0, pady=10, padx=5)
button_reset.grid(row=20, column=2, pady=10, padx=5)
button_start.grid(row=19, column=1, pady=20) 








mainWindow.mainloop()