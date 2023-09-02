# Quant-S9
# Made by Justin Lee 
# @jlee.ai 

from curses.textpad import Textbox, rectangle
import curses
import json
import datetime
import time
import random
import re

#rainbow tier
#bot v bot functionality 
# ['┼', '┤', '╶', '╴', '─', '╰', '╭', '╮', '╯', '│']


# Define window height and width
h, w = 30, 81

def generate_question(difficulty):
    op_list = ['+', '-', '*', '/']
    operation = random.choice(op_list)
    
    # Difficulty
    if difficulty == 1:
        operand1, operand2 = random.randint(1, 10), random.randint(1, 10)
    elif difficulty == 2:
        operand1, operand2 = random.randint(1, 50), random.randint(1, 50)
    elif difficulty == 3:
        operand1, operand2 = random.randint(1, 100), random.randint(1, 100)
    elif difficulty == 4:
        operand1, operand2 = random.randint(1, 500), random.randint(1, 500)
    elif difficulty == 5:
        operand1, operand2 = random.randint(1, 1000), random.randint(1, 1000)
    
    # Handle division to avoid non-integer solutions
    if operation == '/':
        operand1 = operand1 * operand2

    question = f"{operand1} {operation} {operand2} = "
    
    if operation == '+':
        answer = operand1 + operand2
    elif operation == '-':
        answer = operand1 - operand2
    elif operation == '*':
        answer = operand1 * operand2
    elif operation == '/':
        answer = operand1 // operand2  # Integer division

    return question, answer
    # use eval 

def add_skill_bars(stdscr):
    # Skill Level (thes ecan lash maybe)
    # Make this a function, refresh after every session. 
    # Simply the average of 3 best scores for each one

    # Zeta bar
    # Get the skill level from the json or something; should be computed when this is displayed? maybe? 
    skill_range = 17

    #Zeta
    zeta_skill = 13
    stdscr.addstr(3, 40, "▓" * (zeta_skill-1), curses.color_pair(2))
    stdscr.addstr(3, 40+zeta_skill-1, "▓", curses.color_pair(2) | curses.A_BLINK)
    stdscr.addstr(3, 40+zeta_skill, "▒" * (skill_range-zeta_skill), curses.color_pair(2))

    stdscr.addstr(4, 40, "▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒", curses.color_pair(2))
    stdscr.addstr(5, 40, "▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒", curses.color_pair(2))
    stdscr.addstr(6, 40, "▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒", curses.color_pair(2))
    stdscr.addstr(7, 40, "▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒", curses.color_pair(2))
    stdscr.addstr(8, 40, "▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒", curses.color_pair(2))

    stdscr.addstr(11, 40, "▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒", curses.color_pair(2))
    stdscr.addstr(12, 40, "▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒", curses.color_pair(2))
    stdscr.addstr(13, 40, "▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒", curses.color_pair(2))
    stdscr.addstr(14, 40, "▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒", curses.color_pair(2))

def draw_box(stdscr, y, x, height, width):
    h_max, w_max = stdscr.getmaxyx()
    if y + height >= h_max or x + width >= w_max:
        return  
    
    # Draw the top and bottom
    stdscr.addch(y, x, curses.ACS_ULCORNER)
    stdscr.addch(y, x + width, curses.ACS_URCORNER)
    stdscr.addch(y + height, x, curses.ACS_LLCORNER)
    stdscr.addch(y + height, x + width, curses.ACS_LRCORNER)

    # Draw the sides
    for i in range(y+1, y + height):
        stdscr.addch(i, x, curses.ACS_VLINE)
        stdscr.addch(i, x + width, curses.ACS_VLINE)

    # Draw the top and bottom
    for i in range(x+1, x + width):
        stdscr.addch(y, i, curses.ACS_HLINE)
        stdscr.addch(y + height, i, curses.ACS_HLINE)

def start_zeta(stdscr, game_time, difficulty):
    # Data science - track literally everything 
    stdscr.nodelay(True)  # set getch() non-blocking
    stdscr.addstr(5, 3, f"Starting: {game_time} seconds, difficulty {difficulty}")
    stdscr.refresh()
    #countdown(stdscr)
    time.sleep(1)
    stdscr.addstr(5, 3, "                                                       ")
    # stdscr.addstr(5, 40, "Live", curses.color_pair(4) | curses.A_BLINK)
    stdscr.refresh()
    
    start_time = time.time()
    elapsed_time = 0
    time_left = True
    score = 0 

    while time_left:
        question, correct_answer = generate_question(difficulty)
        stdscr.addstr(6, 3, f"> {question}           ")
        stdscr.refresh()
        
        answer_str = ''
        while True:
            stdscr.addstr(5, 3, f"⏲: {int(game_time - elapsed_time)+1}s  ") 
            elapsed_time = time.time() - start_time

            if elapsed_time >= game_time:
                time_left = False
                break  # Exit inner while loop
            
            key = stdscr.getch()
            
            if key in [curses.KEY_BACKSPACE, ord('\b'), ord('\x7f')]:
                if len(answer_str) > 0:
                    answer_str = answer_str[:-1]
                    stdscr.addstr(6, 5 + len(question) + len(answer_str), ' ')
                    stdscr.refresh()

            elif key != -1 and len(answer_str)+1 < 10:
                answer_str += chr(key)
            
            stdscr.addstr(6, 5 + len(question), answer_str)
            stdscr.refresh()
            
            # Check whether answer is correct 
            try:
                if float(answer_str) == correct_answer:
                    score += 1
                    stdscr.addstr(6, 45, "           ")
                    stdscr.refresh()
                    break  # Go to the next question

            except ValueError:  # Handle the case where answer_str cannot be converted to float
                continue

    # print your final score was
    # Standardise score: divide by time in seconds (so it's per second), and then multiply by difficulty
    # To reward longer games
    stnd_score = int((score / (game_time ** 0.75)) * 100)
    stdscr.addstr(5, 3, f"⏲: 0s") 
    stdscr.addstr(6, 3, f"Program finished") 
    stdscr.addstr(7, 3, f"  Raw Score:          {score}") 
    stdscr.addstr(8, 3, f"  Standardized Score: {stnd_score}") 
    stdscr.addstr(10, 3, f"  Saved", curses.color_pair(4) | curses.A_BLINK) 
    stdscr.refresh()
    stdscr.nodelay(False)
    key = stdscr.getch()
    # Save to profile, show a flashing 'saved'
    game_event = {
        "date_of_attempt": datetime.now().strftime('%d/%m/%Y'), 
        "score": stnd_score,
    }

def countdown(stdscr):
    for count in reversed(range(1, 4)):
        stdscr.addstr(6, 3, f"Game starting in {count}...")
        stdscr.refresh()
        time.sleep(1)
    stdscr.refresh()
    time.sleep(0.4)
    return 

def draw_home(stdscr):
    # Clear Screen
    stdscr.clear()
    # Draw the square and rectangle beneath the top menu bar
    draw_box(stdscr, 0, 0, 16, w-20-2)
    draw_box(stdscr, 0, w-20-1, 10, 20)
    draw_box(stdscr, 11, w-20-1, 5, 20)

    # Draw the long row at the bottom
    draw_box(stdscr, 17, 0, 13, w - 1)

    # Add line
    for i in range(1, w-20-2): 
        stdscr.addch(2, i, curses.ACS_HLINE) 
    stdscr.addch(2, 0, curses.ACS_LTEE) 
    stdscr.addch(2, w-20-2, curses.ACS_RTEE) 

    # Add line
    for i in range(1, w-20-2): 
        stdscr.addch(10, i, curses.ACS_HLINE) 
    stdscr.addch(10, 0, curses.ACS_LTEE) 
    stdscr.addch(10, w-20-2, curses.ACS_RTEE) 
    
    
    # Titles
    stdscr.addstr(0, 2, " 𝞼-Quant ", curses.A_STANDOUT)
    stdscr.addstr(2, 2, " Exercises ")
    stdscr.addstr(10, 2, " Sims ")
    stdscr.addstr(17, w//2-4, " Progress ")


    # Game Names
    # Displaying numbers and brackets in regular style
    stdscr.addstr(3, 2, "[0] ", curses.A_NORMAL)
    stdscr.addstr(4, 2, "[1] ", curses.A_NORMAL)
    stdscr.addstr(5, 2, "[3] ", curses.A_NORMAL)
    stdscr.addstr(6, 2, "[4] ", curses.A_NORMAL)
    stdscr.addstr(7, 2, "[5] ", curses.A_NORMAL)
    stdscr.addstr(8, 2, "[6] ", curses.A_NORMAL)
    stdscr.addstr(11, 2, "[A] ", curses.A_NORMAL)
    stdscr.addstr(12, 2, "[B] ", curses.A_NORMAL)
    stdscr.addstr(13, 2, "[C] ", curses.A_NORMAL)
    stdscr.addstr(14, 2, "[D] ", curses.A_NORMAL)

    # Displaying game names in bold style
    stdscr.addstr(3, 6, "Zetamac", curses.A_BOLD)
    stdscr.addstr(4, 6, "24", curses.A_BOLD)
    stdscr.addstr(5, 6, "Sequences", curses.A_BOLD)
    stdscr.addstr(6, 6, "Probability", curses.A_BOLD)
    stdscr.addstr(7, 6, "Approximation", curses.A_BOLD)
    stdscr.addstr(8, 6, "Approximation", curses.A_BOLD)
    stdscr.addstr(11, 6, "Type Speed", curses.A_BOLD)
    stdscr.addstr(12, 6, "Live Problems", curses.A_BOLD)
    stdscr.addstr(13, 6, "Trading/Gambling", curses.A_BOLD)
    stdscr.addstr(14, 6, "Full Interview", curses.A_BOLD)


    add_skill_bars(stdscr)

    for i in range(w-20, w-1):
        for j in range(1,10):
            stdscr.addstr(j, i, ".")

    # Profile Stats
    stdscr.addstr(11, w-20+4, " STATISTICS ")
    stdscr.addstr(13, w-19, "Rank:")
    stdscr.addstr(14, w-19, "XP:")

    stdscr.addstr(13, w-12, "Tom", curses.color_pair(3))
    stdscr.addstr(14, w-12, "29438")

    # Graph
    for i in range(18, 30):
        stdscr.addstr(i, 4, "┤")


        curses.curs_set(0)

    # Home Screen Event Logic
    while True:
        key = stdscr.getch()
        
        if key == ord('H') or key == ord('h'):
            continue
        elif key == ord('0'):
            return 'game0_zeta'
        elif key == ord('1'):
            game_mode1(stdscr, h, w)
        # ... (Add more elif blocks for other game modes) ...

        stdscr.refresh()

    return 'home'

def game0_zeta(stdscr):
    presets = {'a': [60, 3], 'b': [120, 2], 'c': [100, 5]}
    stdscr.clear()
    while True:
        for i in range(3, 15):
            stdscr.addstr(i, 2, "                                                       ") # same operation
        stdscr.refresh()
        stdscr.keypad(True)

        # Draw Layout (GUI) 
        draw_box(stdscr, 0, 0, h, w-1)
        for i in range(1, w-1): 
            stdscr.addch(2, i, curses.ACS_HLINE) 
        stdscr.addch(2, 0, curses.ACS_LTEE) 
        stdscr.addch(2, w-1, curses.ACS_RTEE) 

        for i in range(1, w-1): 
            stdscr.addch(h-3, i, curses.ACS_HLINE) 
        stdscr.addch(h-3, 0, curses.ACS_LTEE) 
        stdscr.addch(h-3, w-1, curses.ACS_RTEE) 

        stdscr.addstr(0, 2, " 𝞼-Quant ", curses.A_STANDOUT)
        stdscr.addstr(0, 13, " Zetamac ", curses.A_STANDOUT)
        stdscr.addstr(2, 2, " Welcome to zetamac ")

        #draw_box(stdscr, 3, 58, 23, 20)
        for j in range(2, 27):
            stdscr.addch(j, 58, curses.ACS_VLINE)
        stdscr.addch(2, 58, curses.ACS_TTEE) 
        stdscr.addch(27, 58, curses.ACS_BTEE) 
        
        # Filling in text 
        stdscr.addstr(h-3, 2, " COMMANDS ")
        stdscr.addstr(h-2, 3, "'home' to exit                           |    ")
        stdscr.addstr(h-1, 3, "'game [time in seconds] [difficulty 1-5] |    ")



        y, x = 3, 3  # Position of the text field
        input_str = ""
        
        stdscr.addstr(y, x, "> ")
        
        while True:
            # Capture key press
            key = stdscr.getch()
            
            # If 'Enter' is pressed, break the loop
            if key == ord('\n'):
                break
            
            # Handle backspace
            elif key in [curses.KEY_BACKSPACE, ord('\b'), ord('\x7f')]:
                if len(input_str) > 0:
                    input_str = input_str[:-1]
                    stdscr.addstr(y, x + 2 + len(input_str), " ")
                    stdscr.refresh()
            
            # Handle other printable characters
            elif (32 <= key <= 126) and len(input_str) <= 50:
                input_str += chr(key)
            
            # Display the updated input string
            stdscr.addstr(y, x + 2, input_str)
            stdscr.refresh()
        
        # Do something with input_str here (e.g., analyze or store it)
        if (input_str == 'home'):
            return 'home'
        
        # Now, match against input_str   
        pattern = r"game (\d{1,3}) (\d) ?(p?)"
        match = re.fullmatch(pattern, input_str)

        pattern2 = r"game ([a-f])"
        match2 = re.fullmatch(pattern2, input_str)

        if (match):
            # Start game 
            time_val = int(match.group(1))
            difficulty_val = int(match.group(2))
            optional_p = match.group(3)
            start_zeta(stdscr, time_val, difficulty_val)

        elif (match2):
            time_val = presets[match2.group(1)][0]
            difficulty_val = presets[match2.group(1)][1]
            optional_p = 'p'
            start_zeta(stdscr, time_val, difficulty_val)

        else: 
            stdscr.addstr(5, 3, f"'{input_str}'")
            stdscr.addstr(6, 3, "is not a valid command")
            stdscr.addstr(7, 3, "Press ↳ to try again")
            stdscr.getch()  # Wait for another key press to exit, currently just resets 
            stdscr.refresh()
            
        
        '''
        # Add game logic here
        key = stdscr.getch()
        stdscr.refresh()
        if key == ord('H') or key == ord('h'):
            return 'home'
        '''
        
        # Type: game [time] [difficulty] [p (optional)]’
        # e.g 'game 120 3 p

    return 'game0_zeta'

def game_mode1(stdscr):
    # use QWAS to select the boxes and then 7-0 to select operations or just mouse 
    while True:
        stdscr.clear()
        draw_box(stdscr, 0, 0, h, w)
        stdscr.addstr(2, 2, "24. Press 'H' to exit.")
        # Add game logic here
        key = stdscr.getch()
        stdscr.refresh()
        if key == ord('H') or key == ord('h'):
            break

# Add more game_mode functions...

def main(stdscr):
    # Initialize color support
    curses.start_color()
    
    # Initialize color pair (Foreground: White, Background: Black)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)  
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE) 
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)

    # Apply the color pair to stdscr
    stdscr.bkgd(' ', curses.color_pair(1))

    # Make cursor invisible
    curses.curs_set(0)  
    
    # Screen dimensions
    h_min, w_min = h, w

    #get to, tomtxt,addscreen,somethin bout her face ___? mum

    while True:
        stdscr.clear()
        h_curr, w_curr = stdscr.getmaxyx()
        if h_curr <= h_min or w_curr <= w_min:
            # Show a live read of the screen size 
            stdscr.addstr(0, 0, "Please resize the window to at least 30 x 80")
            stdscr.addstr(1, 0, f"Currently: {h_curr:3} x {w_curr:3}")
            stdscr.addstr(2, 0, "You may use ⌘- / ⌘+")
        else:
            break

        # Refresh the screen
        stdscr.refresh()


    # CENTRAL LOOP 
    current_mode = 'home'

    while True:
        if current_mode == 'home':
            current_mode = draw_home(stdscr)
        elif current_mode == 'game0_zeta':
            current_mode = game0_zeta(stdscr)
    draw_home(stdscr)
    
if __name__ == "__main__":
    curses.wrapper(main)

    '''
    while True:
        key = stdscr.getch()
        
        # Navigation
        if key in range(ord("1"), ord("9") + 1):
            stdscr.clear()
            if key == ord("1"):
                stdscr.addstr(square_side // 2, (square_side // 2) - 2, "Mode 1")
            elif key == ord("2"):
                stdscr.addstr(square_side // 2, (square_side // 2) - 2, "Mode 2")
            # ... handle other keys accordingly

        elif key == ord("q"):
            break
    '''



    
    '''
    while True:
        key = stdscr.getch()
        
        # Navigate to different pages based on number keys
        if key in [ord(str(i)) for i in range(1, 10)]:
            stdscr.clear()
            stdscr.addstr(0, 0, f"Welcome to Game Mode {chr(key)}")
            stdscr.refresh()
            stdscr.getch()  # Wait for another key press
            
            # Refresh layout
            topbar.refresh()
            square.refresh()
            rectangle.refresh()
            bottomrow.refresh()
        
        elif key == ord('q'):
            break
            '''


'''

def add_to_json(game, date, time, score):
    
    with open('game_data.json', 'r') as file:
            game_data = json.load(file)

    game_data["player_info"][game]["num_played"] += 1
    game_data["player_info"][game]["history"].append({
            "date_of_attempt": date, # date
            "time_taken": time , # time in seconds
            "score": score, 
    })
    

while True: 
    print(f'Quant_S9 | {datetime.datetime.now().date()} | ')
    print()
    next = input("Enter: ")
    
    
    

    with open('game_data.json', 'w') as file:
            json.dump(game_data, file, indent=4)

'''
    # ▐░▒▓▔▕▖	▗	▘	▙	▚	▛	▜	▝	▞	▟ ┤










'''
Sample JSON 
{
  "player_profile": {
    "Name": "",
    "Ranking": "",
    "QXP": "",
    "Activity": {
        "2023-08-30": 150,
        "2023-08-31": 200,
        "2023-09-01": 120
    }
  },
  "games": {
    "24": {
      "num_played": 0,
      "history": [],
      "best_score": {
        "time": "",
        "score": ""
      }
    },
    "zetamac": {
      "num_played": 0,
      "history": [],
      "best_score": {
        "time": "",
        "score": ""
      }
    }
  }
}
'''
