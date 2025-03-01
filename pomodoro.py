from tkinter import* #import tkinker
from PIL import Image, ImageTk   # Ensure Pillow is installed
from tkinter import ttk
from tkinter import messagebox 



#  ----------------------------- GLOBAL VARIABLES -----------------------------

# Constants for UI design and color scheme
GREEN = "#1b5725" # Green for Font Color
DEFAULT_BACKGROUND = "#F6F6F6" # Background color for the app
FONT_NAME = "Comic Sans MS"    # Font style used throughout


running = False # Tracks if the timer is running
timer_value = 7  # Default work time in seconds
short_break_time = 5  # Short break time in seconds
timer_id = None  # Stores reference to the after() function
timer = "00:00"
global my_image  # Load image once and store in a global variable to prevent garbage collection


# ----------------------------- Setup UI Main Window -----------------------------


mainWindow = Tk() # Create main Tkinter window
mainWindow.title("Pomodoro Timer⏲️") # Set window title
mainWindow.configure(padx=50, pady=50, bg=DEFAULT_BACKGROUND) # Set padding and background color


# ----------------------------- MODULE: Setup UI -----------------------------
# Function to initializes UI components like labels, buttons, and image.
def setup_window():
    """
    Sets up all labels in main window, buttons, and an image.
    This function initializes the UI elements but does not start the timer.
    """
    global mainWindow, label_Timer, my_image, bg_img, label_1 

    def change_label():
        """Function to update the label text based on user input."""
        new_text = title_entry.get().strip() # Get the text from the entry field and remove any leading/trailing spaces.
        if new_text:  # Check if the input is not empty.
            label_1.config(text=f"🍅 Pomodoro Session: {new_text}")  # Change label_1 text instead of window title
        else:
            messagebox.showerror("Invalid Input", "Label title cannot be empty.") # Show an error message if input is empty.

    # UI Elements
    # Create a label for the Pomodoro Session with default text, large bold font, and specified colors.
    label_1 = Label(text="🍅 Pomodoro Timer", font=(FONT_NAME, 40, "bold"), fg=GREEN, bg=DEFAULT_BACKGROUND)
    label_1.grid(row=0, column=1)
    
    # Create an entry widget for user input with a specific font size.
    title_entry = Entry(font=(FONT_NAME, 14))
    title_entry.grid(row=2, column=1, pady=10)

    # Create a button that calls change_label() when clicked.
    button_change_label = Button(text="Change Label", font=(FONT_NAME, 14), command=change_label)
    button_change_label.grid(row=3, column=1, pady=10)


    #------------ Load and display image
    my_image = Image.open("tomato.png")  # Ensure the image file exists
    my_image = my_image.resize((400, 350))  # Resize image to fit window
    my_image = ImageTk.PhotoImage(my_image) # Convert to Tkinter-compatible format
    
    
    # Create Label to display the image using grid
    bg_img = Label(mainWindow, image=my_image, text=timer,bg=DEFAULT_BACKGROUND)
    bg_img.grid(row=10, column=0, columnspan=3, rowspan=3) 

    #------------ Timer Label
    label_Timer = Label(
        font=(FONT_NAME, 30, "bold"), # Set font style and size
        fg=GREEN, # Text color
        bg="#ce1417",  # Background color for the timer display
        highlightthickness=0, # Remove highlight border
        text= timer # Default timer display
    )

    label_Timer.grid(row=11, column=1) # Position label on grid
    
    #------------Create Buttons to control the timer
    # button to start the timer
    button_start = Button(
        mainWindow,
        text="   ▶  ",
        font=(FONT_NAME, 25),
        bg="#FDD133",
        fg="#9C1817",
        command= start_timer
    )
    # button to pause the timer
    button_pause = Button(
        mainWindow,
        text="  ||  ",
        font=(FONT_NAME, 20),
        bg="#faa28e",
        fg="#F5F2ED",
        command= pause_timer,
    )
    # button to reset the timer
    button_reset = Button(
        mainWindow,
        text="  ↻  ",
        font=(FONT_NAME, 20),
        bg="#e7305b",
        fg="#F5F2ED",
        command=reset_timer,
    )

    # Position buttons on the grid
    button_pause.grid(row=20, column=0, pady=10, padx=5)
    button_reset.grid(row=20, column=2, pady=10, padx=5)
    button_start.grid(row=19, column=1, pady=20) 


# ----------------------------- MODULE: Timer Logic -----------------------------

def countdown(): 
    """
    Updates the timer display and counts down every second.
    Calls itself recursively using after() to avoid UI freezing.
    """
    global running, timer_value
    
    if timer_value >-1 and running: # Ensure timer runs only when `running` is True
        
        mins, secs = divmod(timer_value, 60) # Convert seconds into MM:SS format
        timer = f"{mins:02d}:{secs:02d}" #create a variable that stores min and seconds
        label_Timer.config(text=timer) # Update label display
        timer_value -= 1 # Decrease time by 1 second
        
        # Use after() to schedule the next call (this acts as a callback)
        mainWindow.after(1000, countdown) # Wait 1 second before updating again
        
    elif (timer_value == -1):  # check if the countdown finished
        # print("pomodoro session finished")
        messagebox.showinfo("Time's Up!", f"Time's up! You've completed  work interval Take a 5-minute break.")
        countdown_short_break() # Transition to short break

# ----------------------------- MODULE: Timer Break -----------------------------       
def countdown_short_break():
    """
    Starts a short break after a work session ends.
    This function is triggered automatically when the timer reaches 0 on the function countdown().
    """
    global running, short_break_time
    
    if short_break_time >-1 and running: # Ensure timer runs only when `running` is True
        print("that is the break time")
        mins, secs = divmod(short_break_time, 60) # Convert seconds into MM:SS format
        timer = f"{mins:02d}:{secs:02d}" #create a variable that stores min and seconds
        label_Timer.config(text=f"Break\n {timer}", font=(FONT_NAME, 20, "bold")) # Update label display
        short_break_time -= 1 # Decrease time by 1 second
        
         # Use after() to schedule the next call (this acts as a callback)
        mainWindow.after(1000, countdown_short_break) # Wait 1 second before updating again
       
        
    elif (short_break_time == -1): # check if the countdown finished
        
        running = False # assigne running to false to avoid the timer not running next section
        label_Timer.config(text="00:00", font=(FONT_NAME, 30, "bold")) # Reset the timer display 
        messagebox.showinfo("Break Over", "Break is over! Time to start working again.")
        
         
       
    
# ----------------------------- MODULE: Timer Controls -----------------------------

def start_timer():
    """
    Starts the Pomodoro work session timer.
    If the timer is already running, it does nothing.
    """
    global running, timer_value, short_break_time
    
    if running == False: # If timer is not running
        
        timer_value = 25*60  # Reset timer duration 
        short_break_time = 5*60  # Reset short timer duration 
        running = True # Mark timer as running
        countdown() # Start countdown
        
 

    
    
def pause_timer(): 
    """
    Toggles between pausing and resuming the timer.
    If the timer is running, it pauses. If it's paused, it resumes.
    """
    global running
    
    if running:
        
        running = False  # Pause the timer
        messagebox.showinfo("Break Time", "Timer paused. Click OK to resume.")
        running = True  # Resume the timer after user clicks OK
        countdown()  # Restart countdown from where it left off
   

def reset_timer():
    """
    Resets the timer to its default state.
    Stops the countdown and resets the display.
    """
    global running, timer_value, short_break_time
    
    if running == True:
        
        running = False  # Stop the timer
        timer_value = 25*60 # Reset timer duration
        short_break_time = 5*60 # Reset short timer duration 
        label_Timer.config(text="00:00") # Reset label display
        messagebox.showinfo("Reset", "Timer has been reset.")  
        

# ----------------------------- MODULE: Secondary Window -----------------------------

# Create a secondary window.

def open_secondary_window():
    """Creates and opens a secondary settings window."""
    
    global bg_img,label_1, mainWindow, DEFAULT_BACKGROUND
    
    secondary_window = Toplevel() # Creates a new window (a separate pop-up window).
    secondary_window.title("Configuration 🔧")  # Sets the title of the window.
    secondary_window.config(width=500, height=600, bg=DEFAULT_BACKGROUND) # Sets the window dimensions to 500x600 pixels.
    
# ------------ Load and display image ------------
       
    newImage = "set.png"
    sec_image = Image.open(newImage)
    sec_image = sec_image.resize((50, 50))
    sec_image = ImageTk.PhotoImage(sec_image)
    

    settings_img = Label(secondary_window,image=sec_image, bg=DEFAULT_BACKGROUND) # Creates a Label widget to display the image.
    settings_img.image = sec_image  # Prevent garbage collection
    settings_img.grid(row=0, column=0)

    # secondary_window.update_idletasks()  # Force Tkinter to refresh


 # ------------ Functions to change background color ------------
    def change_colorOne():
        global bg_img,label_1, mainWindow, BACKGROUND
        
        BACKGROUND = "#3B393E"
        mainWindow.configure(bg=BACKGROUND)  # Changes the main window's background.
        bg_img.configure(bg=BACKGROUND) # Changes the background color of the tomato image
        label_1.configure(bg=BACKGROUND) # Updates the background of `label_1`.


    def change_colorTwo():
        global bg_img,label_1, mainWindow, BACKGROUND
        BACKGROUND = "#FA5B3D"
        mainWindow.configure(bg=BACKGROUND)
        bg_img.configure(bg=BACKGROUND)
        label_1.configure(bg=BACKGROUND)

    def change_colorThree():
        global bg_img,label_1, mainWindow, BACKGROUND
        BACKGROUND = "#50b848"
        mainWindow.configure(bg=BACKGROUND)
        bg_img.configure(bg=BACKGROUND)
        label_1.configure(bg=BACKGROUND)
        
    def reset_color():
        """Reset background color to original."""
    
        mainWindow.configure(bg=DEFAULT_BACKGROUND) 
        bg_img.configure(bg=DEFAULT_BACKGROUND)
        label_1.configure(bg=DEFAULT_BACKGROUND)

    # ------------ Create a frame for color selection buttons ------------
    frameButton = LabelFrame(secondary_window, text="Change Color", fg="black",bg=DEFAULT_BACKGROUND, padx=15, pady=15) 
    frameButton.grid(row=2, column=0, padx=10, pady=10) # Positions frame in the grid layout.
    
    
    # ------------ Create buttons for different colors ------------
    """Each button calls a function to change the background color of the main window."""
    button_color1 = Button(frameButton, command=change_colorOne, bg="#3B393E", width=10, height=2)
    button_color1.grid(row=3, column=2, pady=3, padx=10)

    button_color2  = Button(frameButton, command=change_colorTwo, bg="#FA5B3D",width=10, height=2)
    button_color2.grid(row=3, column=6, pady=3, padx=10)

    button_color3 = Button(frameButton, command=change_colorThree, bg="#50b848", width=10, height=2)
    button_color3.grid(row=3, column=8, pady=3, padx=10)
    
    # Reset button to restore the default background color
    button_reset = Button(frameButton, command=reset_color, bg=DEFAULT_BACKGROUND, fg="white", width=10, height=2)
    button_reset.grid(row=3, column=10, pady=3, padx=10)
    
    # create a frame for how to use instructions
    frameHelp = LabelFrame(secondary_window, text="Need Help?",bg=DEFAULT_BACKGROUND, fg="black", width=300, height=50) 
    frameHelp.grid(row=3, column=0, padx=10, pady=10)
    
    # ------------ Help Section ------------
    def open_instructions():
        """Displays usage instructions in a popup."""
        
        instructions = (
            "📌 How to Use the Pomodoro Timer:\n\n"
        "1️⃣ Click ▶ to begin a 25 minutes work session.\n"
        "2️⃣ The timer will count down until it reaches 0.\n"
        "3️⃣ When the work session ends, you'll receive a notification.\n"
        "4️⃣ After you click OK **5-minute break** will start automatically.\n"
        "5️⃣ When the break ends, you'll receive a notification.\n"
        "6️⃣Click 'Start' to begin another work session.\n\n"
        "📝✍️ Stay focused and make the most of your time! 🚀🔥"
        )
        messagebox.showinfo("Pomodoro Instructions", instructions)  # Displays instructions in a messagebox.

        
    # ------------Create a button to open the popup instructions ------------
    button_instructions = Button(
        frameHelp,
        text="📝 Instructions",
        font=(FONT_NAME, 15), # Sets the font size and style.
        bg="#4CAF50", # Sets background color of the button.
        fg="white",  # Sets text color to white.
        command=open_instructions # Calls function to open instructions.
    )
    button_instructions.grid(row=21, column=1, pady=10)

# ------------ Button to open the secondary window ------------
button_open = ttk.Button(
    mainWindow,
    text="⚙️",
    command=open_secondary_window  # Calls the function to open the secondary window.
)
# Place button in grid.
button_open.grid(row=0, column=2, pady=3, padx=10)


# ----------------------------- PROGRAM EXECUTION -----------------------------
setup_window() #Initializes UI components like labels, buttons, and image.
mainWindow.mainloop() # Run the application
