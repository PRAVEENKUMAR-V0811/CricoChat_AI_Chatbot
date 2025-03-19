import os
import subprocess
import tkinter as tk
from tkinter import scrolledtext, messagebox
from gtts import gTTS
import pygame
import time
import threading
import tempfile  # Import the tempfile module

# Initialize Pygame mixer for audio
pygame.mixer.init()

# IPL Data (Unchanged)
winners = {
    2008: "Rajasthan Royals", 2009: "Deccan Chargers", 2010: "Chennai Super Kings",
    2011: "Chennai Super Kings", 2012: "Kolkata Knight Riders", 2013: "Mumbai Indians",
    2014: "Kolkata Knight Riders", 2015: "Mumbai Indians", 2016: "Sunrisers Hyderabad",
    2017: "Mumbai Indians", 2018: "Chennai Super Kings", 2019: "Mumbai Indians",
    2020: "Mumbai Indians", 2021: "Chennai Super Kings", 2022: "Gujarat Titans",
    2023: "Chennai Super Kings", 2024: "Sunrisers Hyderabad"
}

orange_caps = {
    2008: "Shaun Marsh (616 runs)", 2009: "Matthew Hayden (572 runs)", 2010: "Sachin Tendulkar (618 runs)",
    2011: "Chris Gayle (608 runs)", 2012: "Chris Gayle (733 runs)", 2013: "Michael Hussey (733 runs)",
    2014: "Robin Uthappa (660 runs)", 2015: "David Warner (562 runs)", 2016: "Virat Kohli (973 runs)",
    2017: "David Warner (641 runs)", 2018: "Kane Williamson (735 runs)", 2019: "David Warner (692 runs)",
    2020: "KL Rahul (670 runs)", 2021: "Ruturaj Gaikwad (635 runs)", 2022: "Jos Buttler (863 runs)",
    2023: "Shubman Gill (890 runs)", 2024: "Virat Kohli (741 runs)"
}

purple_caps = {
    2008: "Sohail Tanvir (22 wickets)", 2009: "RP Singh (23 wickets)", 2010: "Pragyan Ojha (21 wickets)",
    2011: "Lasith Malinga (28 wickets)", 2012: "Morne Morkel (25 wickets)", 2013: "Dwayne Bravo (32 wickets)",
    2014: "Mohit Sharma (23 wickets)", 2015: "Dwayne Bravo (26 wickets)", 2016: "Bhuvneshwar Kumar (23 wickets)",
    2017: "Bhuvneshwar Kumar (26 wickets)", 2018: "Andrew Tye (24 wickets)", 2019: "Imran Tahir (26 wickets)",
    2020: "Kagiso Rabada (30 wickets)", 2021: "Harshal Patel (32 wickets)", 2022: "Yuzvendra Chahal (27 wickets)",
    2023: "Mohammed Shami (28 wickets)", 2024: "Harshal Patel (32 wickets)"
}

ipl_teams = {
    "csk": "Chennai Super Kings", "mi": "Mumbai Indians", "kkr": "Kolkata Knight Riders",
    "srh": "Sunrisers Hyderabad", "rr": "Rajasthan Royals", "dc": "Delhi Capitals",
    "rcb": "Royal Challengers Bangalore", "pbks": "Punjab Kings", "gt": "Gujarat Titans",
    "lsg": "Lucknow Super Giants"
}


def speak(text):
    file_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            file_path = temp_file.name

        tts = gTTS(text=text, lang='en')
        tts.save(file_path)

        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

    except Exception as e:
        print("Error in speak function:", e)
        messagebox.showerror("Audio Error", f"Error playing audio: {e}")

    finally:  # Only remove the file here, leave mixer alone
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            print("File removed")


def close_after_audio():
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    root.destroy()  # Or root.quit() if you prefer

def get_team_win_count(team_name):
    """Count the number of IPL wins for a team."""
    return sum(1 for winner in winners.values() if winner.lower() == team_name.lower())

def season_to_year(season):
    """Convert Season number to corresponding year."""
    try:
        season_num = int(season)
        year = 2007 + season_num
        return year if 2008 <= year <= 2024 else None
    except ValueError:
        return None

def handle_query():
    user_input = query_entry.get().lower().strip()

    if not user_input:
        messagebox.showwarning("Input Error", "Please enter a query!")
        return

    exit_commands = ["thanks", "thank you", "bye", "stop", "exit", "end"]
    if user_input in exit_commands:
        response = "Goodbye! It was great chatting with you."
        display_response(user_input, response)
        threading.Thread(target=speak, args=(response,)).start()
        threading.Thread(target=close_after_audio).start()
        return

    season_number = None
    year = None
    team_name = None
    query_type = None
    words = user_input.split()

    # Detect numeric input for year or season
    for word in words:
        if word.isdigit():
            num = int(word)
            if 2008 <= num <= 2024:  # If it's a valid IPL year
                year = num
            elif 1 <= num <= 17:  # If it's a season number
                season_number = num

    for short, full in ipl_teams.items():
        if short in user_input or full.lower() in user_input:
            team_name = full
            break

    if "orange cap" in user_input:
        query_type = "orange_cap"
    elif "purple cap" in user_input:
        query_type = "purple_cap"
    elif "win count" in user_input or "how many times" in user_input or "titles" in user_input:
        query_type = "win_count"

    # Convert season number to year if needed
    if season_number and not year:
        year = season_to_year(season_number)

    if query_type == "win_count" and team_name:
        win_count = get_team_win_count(team_name)
        response = f"{team_name} has won {win_count} IPL titles." if win_count > 0 else f"{team_name} has not won any IPL titles yet."
    elif query_type == "orange_cap":
        response = f"IPL {year} Orange Cap: {orange_caps.get(year, 'No data')}" if year else "Specify a valid season or year."
    elif query_type == "purple_cap":
        response = f"IPL {year} Purple Cap: {purple_caps.get(year, 'No data')}" if year else "Specify a valid season or year."
    elif year:
        response = f"IPL {year} Winner: {winners.get(year, 'No data')}"
    else:
        response = "I didn't understand that. Try asking about a winner, Orange Cap, Purple Cap, or a team's win count."

    display_response(user_input, response)
    threading.Thread(target=speak, args=(response,)).start()
    query_entry.delete(0, tk.END)

def display_response(user_input, response):
    """Display user query and bot response with typing effect (with alignment)."""
    output_text.config(state=tk.NORMAL)

    output_text.insert(tk.END, f"You: {user_input}\n", "user")
    output_text.tag_configure("user", justify=tk.RIGHT)

    output_text.insert(tk.END, "Bot: ", "bot")

    def type_text():
        for char in response:
            output_text.insert(tk.END, char, "bot")
            output_text.update()
            time.sleep(0.02)
        output_text.insert(tk.END, "\n\n")
        output_text.config(state=tk.DISABLED)

    threading.Thread(target=type_text).start()


# GUI Setup (Improved styling and layout)
root = tk.Tk()
root.title("CricoChat AI")
root.geometry("600x550")
root.configure(bg="#282c34")

# Title Label
title_label = tk.Label(root, text="🏏 CricoChat AI 🏆", font=("Arial", 20, "bold"), fg="#61dafb", bg="#282c34")
title_label.pack(pady=10)

# Output Box
output_text = scrolledtext.ScrolledText(root, width=65, height=18, font=("Arial", 12), state=tk.DISABLED, bg="#3e4451", fg="#abb2bf", relief=tk.FLAT)
output_text.pack(pady=10)

# Custom Tag Styles
output_text.tag_configure("user", foreground="#98c379", font=("Arial", 12, "bold"))
output_text.tag_configure("bot", foreground="#e6c07b", font=("Arial", 12))

# Input Frame (for input box and button)
input_frame = tk.Frame(root, bg="#282c34")
input_frame.pack(pady=(0, 10))

# Input Box
query_entry = tk.Entry(input_frame, width=50, font=("Arial", 14), bg="#3e4451", fg="#abb2bf", insertbackground="#abb2bf", relief=tk.FLAT)
query_entry.pack(side=tk.LEFT)

# Ask Button
ask_button = tk.Button(input_frame, text="Ask", font=("Arial", 14, "bold"), bg="#61dafb", fg="#282c34", relief=tk.RAISED, command=handle_query)
ask_button.pack(side=tk.LEFT, padx=(5, 0))

# Enter Key Binding
root.bind("<Return>", lambda event: handle_query())

# Greeting Message
greeting = "Welcome to CricoChat AI! How can I help you?"
display_response("", greeting)
threading.Thread(target=speak, args=(greeting,)).start()

root.mainloop()
# Quit the mixer when the application closes (important!)
pygame.mixer.quit()