# Import necessary modules
import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from datetime import date, datetime
from src.helpers import clear_widgets, set_background
import pygame

# Initialize the window
root = tk.Tk()
root.title('Serenity – Emotional Wellness App')
root.geometry('850x650')

# Global variables to keep track of the user, and music
current_user_id = None
current_user_name = None
instructions = None  # For activities like breathing and meditation
current_music_file = None


# Function to play background music, includes conditions to keep the same track from starting over
def play_music(filepath):
    global current_music_file
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    if not pygame.mixer.music.get_busy() or current_music_file != filepath:
        current_music_file = filepath
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play(-1)  # Loops music


# Function to create buttons, some of which use .pack, and other .place
def create_button(root, text, command, font=('Helvetica', 16), borderwidth=0, highlightthickness=0,
                  height=2, width=None, side=None, anchor=None, padx=None, pady=None, relx=None, rely=None):
    button = tk.Button(root, text=text, command=command, font=font, borderwidth=borderwidth,
                       highlightthickness=highlightthickness, height=height, width=width)
    if relx is not None and rely is not None:
        button.place(relx=relx, rely=rely)
    else:
        button.pack(side=side, anchor=anchor, padx=padx if padx is not None else 0,
                    pady=pady if pady is not None else 0)


# Function to create page titles
def create_page_title(root,
                      text,
                      font=("Helvetica bold", 20),
                      fg="black",
                      bg="white",
                      height=2,
                      pady=30):
    title_label = tk.Label(root,
                           text=text,
                           font=font,
                           fg=fg,
                           bg=bg,
                           height=height
                           )
    title_label.pack(side=tk.TOP, anchor=tk.CENTER, pady=pady)


# First page of the app
def create_homepage(root):
    clear_widgets(root)
    play_music('music/ambient.wav')
    set_background(root, "images/homepage.png", background_colour="white")

    # Navigation buttons
    create_button(root, text="🏠", command=lambda: create_homepage(root), side=tk.LEFT, anchor='ne', padx=10, pady=10)
    create_button(root, text="✖️", command=root.destroy, side=tk.RIGHT, anchor='ne', padx=10, pady=10)

    create_page_title(root, "Welcome to Serenity")

    # Login section
    userid_label = tk.Label(root,
                            text="Enter your user name",
                            font='Helvetica 16',
                            fg="black",
                            bg="white",
                            width=20,
                            height=2
                            )
    userid_label.place(relx=0.05, rely=0.35)
    username = tk.StringVar()
    username_box = tk.Entry(root,
                            textvar=username,
                            fg="black",
                            bg="white",
                            width=15,
                            highlightthickness=0,
                            highlightbackground='white'
                            )
    username_box.place(relx=0.40, rely=0.35)
    create_button(root,
                  text="Login",
                  command=lambda: check_user(root, username),
                  relx=0.65,
                  rely=0.35,
                  width=15)

    # Registration section
    registration_label = tk.Label(root,
                                  text="Don't have an account yet?",
                                  font='Helvetica 16',
                                  fg="black",
                                  bg="white",
                                  width=20,
                                  height=2
                                  )
    registration_label.place(relx=0.05, rely=0.65)

    create_button(root,
                  text="Register",
                  command=lambda: create_registration_page(root),
                  relx=0.65,
                  rely=0.65,
                  width=15)


# Registration page setup
def create_registration_page(root):
    global username, name
    clear_widgets(root)
    set_background(root, "images/registration.png", background_colour="white")

    # Navigation buttons
    create_button(root, text="🏠", command=lambda: create_homepage(root), side=tk.LEFT, anchor='ne', padx=10, pady=10)
    create_button(root, text="✖️", command=root.destroy, side=tk.RIGHT, anchor='ne', padx=10, pady=10)

    # Registration form
    create_page_title(root, "Registration")
    name_label = tk.Label(root,
                          text="Name",
                          fg="black",
                          font='Helvetica 16',
                          bg="white",
                          width=10,
                          highlightthickness=0,
                          height=2
                          )
    name_label.place(relx=0.05, rely=0.35)
    name = tk.StringVar()
    name_box = tk.Entry(root,
                        textvar=name,
                        fg="black",
                        bg="white",
                        font='Helvetica 16',
                        width=20,
                        highlightthickness=0
                        )
    name_box.place(relx=0.40, rely=0.35)
    username_label = tk.Label(root,
                              text="Username",
                              fg="black",
                              font='Helvetica 16',
                              bg="white",
                              width=10,
                              height=2
                              )
    username_label.place(relx=0.05, rely=0.65)
    username = tk.StringVar()
    username_box = tk.Entry(root,
                            textvar=username,
                            fg="black",
                            bg="white",
                            font='Helvetica 16',
                            width=20,
                            highlightthickness=0
                            )
    username_box.place(relx=0.40, rely=0.65)
    # Button to submit the registration form
    create_button(root,
                  text="Create a new user",
                  command=enter_user_data,
                  side=tk.BOTTOM,
                  anchor=tk.CENTER,
                  pady=30,
                  padx=0)


# Data submission handler
def enter_user_data():
    global current_user_id
    global current_user_name

    current_timestamp = datetime.now()

    current_user_name = name.get()
    current_user_id = username.get()

    user_data = {
        "name_of_user": name.get(),
        "user_id": username.get(),
        "created_at": current_timestamp
    }

    user_ids = list(pd.read_csv("user_data/users.csv").user_id)

    if len(username.get()) == 0 and len(name.get()) == 0:
        messagebox.showerror('Error', 'Please enter a name and username!')
    elif len(name.get()) == 0:
        messagebox.showerror('Error', 'Please enter your name!')
    elif len(username.get()) == 0:
        messagebox.showerror('Error', 'Please enter a user name!')
    else:

        if username.get() in user_ids:
            tk.messagebox.showwarning("WARNING!", "This username already exists")

        else:

            user_data_df = pd.DataFrame([user_data])

            user_data_df.to_csv("user_data/users.csv", index=False, mode='a', header=False)
            create_activities_page(root)


# Login handler – verifies the user
def check_user(root, username):
    global current_user_id
    global current_user_name
    users_data = pd.read_csv("user_data/users.csv").to_dict(orient='records')
    current_user_id = None
    for user_record in users_data:
        if username.get() == user_record['user_id']:
            current_user_name = user_record['name_of_user']
            current_user_id = user_record['user_id']
            break

    if current_user_id:
        create_activities_page(root)
    else:
        tk.messagebox.showwarning("WARNING", "User does not exist. Please check spelling and try again.")


# Breathing exercise page setup
def create_breathing_page(root):
    global instructions
    clear_widgets(root)
    set_background(root, "images/breathing.png", background_colour="white")

    # Navigation
    create_button(root, text="🏠", command=lambda: create_homepage(root), side=tk.LEFT, anchor='ne', padx=10, pady=10)
    create_button(root, text="✖️", command=root.destroy, side=tk.RIGHT, anchor='ne', padx=10, pady=10)
    create_page_title(root, "Breathing Exercise")

    # Start breathing exercise button
    create_button(root,
                  text="Start breathing exercise",
                  command=lambda: start_breathing_exercise(),
                  side=tk.TOP,
                  anchor=tk.CENTER,
                  pady=50,
                  padx=0)

    # Instructions label is initially empty
    instructions = tk.Label(root,
                            text="",
                            font='Helvetica 14',
                            bg="white",
                            fg="black")
    # Navigation
    create_button(root,
                  text="Go back",
                  command=lambda: back_to_activities_page(),
                  side=tk.BOTTOM,
                  anchor=tk.CENTER,
                  pady=30,
                  padx=0)


# Meditation practice page setup
def create_meditation_page(root):
    global instructions
    clear_widgets(root)
    set_background(root, "images/meditation.png", background_colour="white")

    # Navigation
    create_button(root, text="🏠", command=lambda: create_homepage(root), side=tk.LEFT, anchor='ne', padx=10, pady=10)
    create_button(root, text="✖️", command=root.destroy, side=tk.RIGHT, anchor='ne', padx=10, pady=10)
    create_page_title(root, 'Meditation Practice')

    # Start meditation practice button
    create_button(root,
                  text="Start meditation practice",
                  command=lambda: start_meditatation_practice(),
                  side=tk.TOP,
                  anchor=tk.CENTER,
                  pady=50,
                  padx=0)

    # Instructions label is initially empty
    instructions = tk.Label(root,
                            text="",
                            font='Helvetica 14',
                            bg="white",
                            fg="black")
    # Navigation
    create_button(root,
                  text="Go back",
                  command=lambda: back_to_activities_page(),
                  side=tk.BOTTOM,
                  anchor=tk.CENTER,
                  pady=30,
                  padx=0)


# Start breathing exercise: show instructions and play music
def start_breathing_exercise():
    global instructions
    pygame.mixer.music.stop()
    play_music('music/breathing.wav')
    instructions_text = """Sit comfortably and close your eyes
    Inhale slowly through your nose for 3 seconds
    Hold your breath for 2 seconds
    Exhale completely through your mouth for 5 seconds
    
    Repeat this breathing cycle as long as you wish"""
    instructions.config(text=instructions_text)
    instructions.pack()


# End breathing or meditation:
# play the default ambient music again,
# clear widgets and instructions
def back_to_activities_page():
    global instructions
    clear_widgets(root)
    create_activities_page(root)
    play_music('music/ambient.wav')
    instructions = None


# Start meditation practice: show instructions and play music
def start_meditatation_practice():
    global instructions
    play_music('music/singing_bowls.wav')
    instructions_text = """Welcome to your singing bowl meditation.
    
    Find comfort, close your eyes.
    Listen to the bowl's sound, breathe deeply.
    Release worries with each tone.
    Feel the vibrations, grounding you in peace.
    Let the sound lead you to relaxation,
    To inner tranquility and harmony.
    Embrace the following silence,
    Carrying serenity and clarity forward.
    """
    instructions.config(text=instructions_text)
    instructions.pack()


# Function to read past anxiety log data specific to the current user
# Displays the logs in a popup window
# It is quite complicated as I avoided using the csv module, therefore I needed to find the solution online

def view_past_logs():
    global current_user_id

    logs_window = tk.Tk()
    logs_window.title("Anxiety Logs")

    tree = ttk.Treeview(logs_window, columns=('Timestamp', 'Anxiety Level'), show='headings')
    tree.heading('Timestamp', text='Timestamp')
    tree.heading('Anxiety Level', text='Anxiety Level')

    # Open and read the file
    csv_file_path = 'user_data/anxiety_logs.csv'
    file = open(csv_file_path, mode='r', newline='')
    headers = file.readline().strip().split(',')
    user_id_idx = headers.index('user_id')
    timestamp_idx = headers.index('created_at')
    anxiety_level_idx = headers.index('anxiety_level')

    # Add the logs to the window columns
    for line in file:
        values = line.strip().split(',')
        if values[user_id_idx] == current_user_id:
            timestamp = values[timestamp_idx]
            anxiety_level = values[anxiety_level_idx]
            tree.insert('', tk.END, values=(timestamp, anxiety_level))
    file.close()

    tree.pack(expand=True, fill='both')

    logs_window.mainloop()


# Activities page setup. It is the page, where user can find the key app features:
# Log anxiety level,
# View past logs,
# Practice meditation
# Exercise breathing
def create_activities_page(root):
    today = date.today()
    date_string = today.strftime('%B %d, %Y')
    clear_widgets(root)
    set_background(root, "images/happy.png", background_colour="white")

    # Navigation
    create_button(root, text="🏠", command=lambda: create_homepage(root), side=tk.LEFT, anchor='ne', padx=10, pady=10)
    create_button(root, text="✖️", command=root.destroy, side=tk.RIGHT, anchor='ne', padx=10, pady=10)

    create_page_title(root, text='Hi ' + current_user_name + '! It is great to see you')
    date_label = tk.Label(root,
                          text='Today is ' + date_string,
                          font='Helvetica 16',
                          fg="black",
                          bg="white",
                          height=2
                          )
    date_label.pack(side=tk.TOP, anchor=tk.CENTER)

    create_button(root,
                  text="Log Anxiety Level",
                  command=lambda: show_anxiety_level_buttons(),
                  relx=0.20,
                  rely=0.4,
                  width=15)

    create_button(root,
                  text="View Past Logs",
                  command=lambda: view_past_logs(),
                  relx=0.60,
                  rely=0.4,
                  width=15)

    # The anxiety log buttons and title are initially hidden
    track_anxiety_label = tk.Label(root,
                                   text='How high is your anxiety level right now?',
                                   font='Helvetica 16',
                                   fg="black",
                                   bg="white",
                                   height=2
                                   )
    # The function create_button is not used for these buttons,
    # because they are not needed immediately & are placed by another function
    low_anxiety_button = tk.Button(text='Low 🙂',
                                   command=lambda: log_anxiety_level('Low'),
                                   fg='black',
                                   font='Helvetica 16',
                                   borderwidth=0,
                                   highlightthickness=0,
                                   height=2,
                                   width=10)
    average_anxiety_button = tk.Button(text='Average 😐',
                                       command=lambda: log_anxiety_level('Average'),
                                       fg='black',
                                       font='Helvetica 16',
                                       borderwidth=0,
                                       highlightthickness=0,
                                       height=2,
                                       width=10)
    high_anxiety_button = tk.Button(text='High 😔',
                                    command=lambda: log_anxiety_level('High'),
                                    fg='black',
                                    font='Helvetica 16',
                                    borderwidth=0,
                                    highlightthickness=0,
                                    height=2,
                                    width=10)

    create_button(root,
                  text="Meditation Practice",
                  command=lambda: create_meditation_page(root),
                  relx=0.20,
                  rely=0.5,
                  width=15)

    create_button(root,
                  text="Breathing Exercise",
                  command=lambda: create_breathing_page(root),
                  relx=0.60,
                  rely=0.5,
                  width=15)

    # Function to handle click on Log Anxiety
    def show_anxiety_level_buttons():
        low_anxiety_button.place(relx=0.30, rely=0.8, anchor="center")
        average_anxiety_button.place(relx=0.50, rely=0.8, anchor="center")
        high_anxiety_button.place(relx=0.70, rely=0.8, anchor="center")
        track_anxiety_label.place(relx=0.50, rely=0.7, anchor="center")

    # Function to handle clicks on anxiety level buttons
    def log_anxiety_level(level):
        global current_user_id
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_entry = pd.DataFrame({
            'user_id': [current_user_id],
            'anxiety_level': [level],
            'created_at': [timestamp]
        })
        file_path = 'user_data/anxiety_logs.csv'
        df = pd.read_csv(file_path)
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(file_path, index=False)

        low_anxiety_button.place_forget()
        average_anxiety_button.place_forget()
        high_anxiety_button.place_forget()
        track_anxiety_label.place_forget()


# Play ambient music and display the Homepage when the app starts
play_music('music/ambient.wav')
create_homepage(root)
root.mainloop()
