# ZETA MATRIX
# Created by Justin Lee on the 14th of September, 2023 
# Occupation
# Have you completed or recieved an internship from a trading company 
# Should measure something deeper than 'are quant traders better at ____' 
# but... should measure learning curve. yes. How about each cell is a stack. It measures the average increment 
# Could investigate learning curve...
# Investigate learnings curves and use an index. yes. okay gonna have to keep their speed score and an index. 
# i create fun minigames that are disguised tools to prove economic theories such as risk aversion, or behavioral biases, or just other interesting data insights - e.g what is the hardest combination of sum. 
# Time complexity
# Interestingly: this is a good data structure problem
# I'm thinking since I need to construct the zeta matrix but also have timestamped questions... 
# A .csv of timestamp, num1, operator, num2, timetaken
# Then iterate down this list and construct the zetamatrix 
# Then it will be one continuous... time series. 
# Lets say you have n questions complete. 
# hypothesis test: the previous one taking long results in the next one.
# Could implement an enter button... nah that's not zetamac. 
# Best settings are ______ and you can scale terminal up
# sessions should be easy to compute... make like a zen mode with a sleeping cat. It should be used as focus

# 1 = +, 2 = -, 3 = *, 4 = /
#  ⣿

# Cache the matrix for computation. (save the timestamp that it got up to.) No even easier - the zetamatrix itself is simply the best time... yeah

from curses.textpad import Textbox, rectangle
import curses
import json
import datetime
import random
import re
import csv
import time
import pandas as pd
from math import ceil

csv_path = 'data.csv'

garden_str = """     `!,
    -( )-
    /'|\`                        /
      | \ `                     //
                               ///
             ###              /[_]
            #####              [][
          #{##{####       o~   [_]
         ###\#}#}###      /`\  [][
          ###\{/###      [ /%\ [_]
           # }}{ #       [_|_\_[][
       ###   }}{           [_][__]
      #\#}#} }}{@  @       [___][]
      ##\/## }}{|@@|/      [_][__]
,ejm,,,,}{,,,}{{||||_______[___][]"""
# × ÷
oper_dict = {'+': '+', '-': '-', '*': '×', '/': '÷'}

class CSVAppender:
    def __init__(self, filename=csv_path):
        self.filename = filename
        self.file = open(filename, 'a', newline='')
        self.writer = csv.writer(self.file)

        # Check if the file already has content
        # If not, write headers
        if self.file.tell() == 0:
            self.writer.writerow(["timestamp", "num1", "operator", "num2", "timetaken", "got_wrong", "timed"])

    def append(self, timestamp, num1, operator, num2, timetaken, got_wrong, ranked, game_time):
        self.writer.writerow([timestamp, num1, operator, num2, timetaken, got_wrong, ranked, game_time])
        # If you want to ensure data is written immediately (not buffered), uncomment next line:
        # self.file.flush()

    def calculate_exp_std(self):
        # Returns as (string, string) tuple
        try:
            df = pd.read_csv(self.filename)
            
            # Check if dataframe is empty or the column 'timetaken' is not present
            if df.empty or 'timetaken' not in df.columns:
                return "n/a", "n/a"
            
            df = df.tail(200)

            # Calculate the average
            exp = str(round(df['timetaken'].mean(), 3))

            # Calculate the variance of the data
            std = str(round(df['timetaken'].std(ddof=0), 3))

            return exp, std

        except Exception as e:
            return "n/a", "n/a"
        
    def create_zm(self):

        # Filter the DataFrame based on operation
        operation_df = df[df['operator'] == operation]
        
        # If there's no data for this operation, just return
        if operation_df.empty:
            print(f"No data available for operation: {operation}")
            return
        
        # Create an empty matrix filled with NaNs, depending on dimensions of operation
        if operation in ['+', '-']:
            matrix = np.full((99, 99), np.nan)
        else: 
            matrix = np.full((11, 99), np.nan)
        
        # Populate the matrix using the data from the DataFrame
        # MUST AMEND THIS SO THAT IT ONLY UPDATES WITH FASTER TIMES
        # Also store a counter for how many unique combos have been tried 
        for index, row in operation_df.iterrows():
            matrix[int(row['num1'])-2][int(row['num2'])-2] = row['timetaken'] 

    def close(self):
        self.file.close()
    
class Button:
    def __init__(self, text):
        self.text = text
        self.selected = False

    def render(self, win, y, x):
        """Render the button on the window."""
        if self.selected:
            win.attron(curses.A_REVERSE)
        win.addstr(y, x, "[ " + self.text + " ]")
        if self.selected:
            win.attroff(curses.A_REVERSE)

def show_stats(stdscr): 
    """
    Calculates user E(X) and Var(X) and displays to screen 
    """

    # Lay out TUI
    draw_box(stdscr, 5, 1, 19, 28)
    draw_box(stdscr, 5, 30, 19, 29)

    draw_line(stdscr, 9, 2, 27)
    draw_line(stdscr, 11, 31, 28)

    # Profile
    stdscr.addstr(5, 2, " Profile ", curses.A_BOLD)
    stdscr.addstr(6, 2, " User ID:  ")

    # Statistics 
    stdscr.addstr(7, 2, " E[S]:        ")
    stdscr.addstr(8, 2, " Var[S]:      ")
    appender = CSVAppender()
    exp, std = appender.calculate_exp_std()
    appender.close()
    stdscr.addstr(7, 12, f"{exp}s     ")
    stdscr.addstr(8, 12, f"{std}s     ")


    stdscr.addstr(10, 54, " ᓚᘏᗢ ")

    # Leaderboard / ASCII art 

    # Zetamatrix 
    
    for w in range(31, 59):
        for h in range(12, 24):
           stdscr.addch(h, w, "░") #⣿
    

    # add other line structures. 
    return 


def generate_question(decimals = False):
    op_list = ['+', '-', '*', '/']
    oper = random.choice(op_list)

    #if difficulty == 1:  # One decimal place

    if not decimals: 
        add_range = [(2, 100), (2, 100)]
        mult_range = [(2, 12), (2, 100)]
        
        # fill in here 
        if oper in ['+', '-']:
            num1 = random.randint(add_range[0][0], add_range[0][1])
            num2 = random.randint(add_range[1][0], add_range[1][1])

        elif oper == "*": 
            num1 = random.randint(mult_range[0][0], mult_range[0][1])
            num2 = random.randint(mult_range[1][0], mult_range[1][1])
            answer = eval(f"{num1} {oper} {num2}")

        elif oper == "/": 
            num2 = random.randint(mult_range[0][0], mult_range[0][1])
            num1 = random.randint(mult_range[1][0], mult_range[1][1])
            product = num1 * num2
            answer = num1
            num1 = product

    return num1, oper, num2

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

def draw_line(stdscr, y, x, l): 
        for i in range(x, x+l):
            stdscr.addch(y, i, curses.ACS_HLINE) 
        stdscr.addch(y, x-1, curses.ACS_LTEE) 
        stdscr.addch(y, x+l, curses.ACS_RTEE) 

def draw_home(stdscr):
    

    # Start zeta-matrix
    while True: 
        # Set up TUI 
        stdscr.clear()
        draw_box(stdscr, 0, 0, 25, 60)

        '''
        # Draws the garden, cat home screen
        k=7 # start line
        for line in garden_str.split('\n'): 
            stdscr.addstr(k, 4, (line)) 
            k+=1
        '''

        draw_line(stdscr, 4, 1, 59)
        stdscr.addstr(0, 2, " ζ-ZetaMatrix ", curses.A_STANDOUT)
        stdscr.refresh()            
        show_stats(stdscr)
        curses.curs_set(0)  # Hide the cursor

        # Define the buttons
        buttons = [Button("Practice"), Button("60s"), Button("120s"), Button("Ranked")]
        buttons[0].selected = True  # The first button is selected initially

        current_index = 0
        while True:
            # Draw buttons
            buttons[0].render(stdscr, 2, 11)
            buttons[1].render(stdscr, 2, 24)
            buttons[2].render(stdscr, 2, 32)
            buttons[3].render(stdscr, 2, 41)

            # Get user input
            key = stdscr.getch()

            # Handle arrow keys for navigation
            if key == curses.KEY_RIGHT and current_index < len(buttons) - 1:
                buttons[current_index].selected = False
                current_index += 1
                buttons[current_index].selected = True
            elif key == curses.KEY_LEFT and current_index > 0:
                buttons[current_index].selected = False
                current_index -= 1
                buttons[current_index].selected = True
            elif key in [curses.KEY_ENTER, ord('\n')]:
                if current_index == 0: 
                    stdscr.addstr(2, 5, "                                                  ")
                    play_zeta_prac(stdscr)
                elif current_index == 1: 
                    stdscr.addstr(2, 5, "                                                  ")
                    play_zeta(stdscr, game_time=60)
                break
        
def play_zeta(stdscr, game_time, ranked=False):
    # Implement: typing speed test. Need to identify when they've figured it out and the only limitation is typing speed - 
    # Waits for '_' space to start 
    # 1 second pause and then the first question
    stdscr.addstr(0, 17, " Timed ", curses.A_STANDOUT)
    timeout_duration = 100
    stdscr.timeout(timeout_duration)
    curses.curs_set(0)
    appender = CSVAppender()
    stdscr.addstr(2, 15, " Ready? ")
    stdscr.refresh()
    time.sleep(1)
    elapsed_time = 0
    time_left = True
    score = 0
    start_time = time.time()
    while time_left: 
        time_recent = time.time()
        got_wrong = False
        answer_str = ''
        
        # Assuming generate_question() returns num1, oper, num2 in that order.
        num1, oper, num2 = generate_question()
        question = f"{num1} {oper_dict[oper]} {num2}"
        ans = eval(f"{num1} {oper} {num2}")

        stdscr.addstr(2, 15, f"> {question} =      ")
        stdscr.move(2, 20 + len(question))
        
        while True: 
            stdscr.addstr(2, 3, f"⏲: {ceil(game_time - elapsed_time)}s  ") 
            stdscr.refresh()
            elapsed_time = time.time() - start_time
            if elapsed_time >= game_time:
                time_left = False
                break  # Exit inner while loop

            key = stdscr.getch()

            if key == -1: 
                pass
            elif key == curses.KEY_ENTER or key == 10 or key == 13:
                pass
            elif key in [curses.KEY_BACKSPACE, ord('\b'), ord('\x7f')]:
                if len(answer_str) > 0:
                    answer_str = answer_str[:-1]
                    stdscr.addstr(2, 20 + len(question) + len(answer_str), ' ')
                    stdscr.refresh()
            elif len(answer_str) + 1 < 10 and (chr(key).isdigit() or chr(key) in ['-', '.']):
                answer_str += chr(key)
            
            stdscr.addstr(2, 20 + len(question), answer_str)
            stdscr.refresh()
            
            # Check whether the answer is correct 
            try:
                if int(answer_str) == 9999:
                    appender.close()
                    stdscr.addstr(1, 40, "               ")
                    stdscr.addstr(2, 5, "                                                  ")
                    return
                
                if int(answer_str) == ans:
                    score += 1
                    time_taken = round(time.time() - time_recent, 3)
                    if time_taken < 90:  # Anything over 90 seconds is considered errenous (sorry)
                        appender.append(time.time(), num1, oper, num2, time_taken, got_wrong, ranked, game_time)
                    # Print to screen for diagnostics
                    
                    # stdscr.addstr(1, 59, f"⏲")

                    stdscr.refresh()
                    time_recent = time.time()
                    break  # Go to the next question
                if len(answer_str) >= len(str(ans)):
                    got_wrong = True

                

            except ValueError:
                continue 
    
    stdscr.addstr(1, 40, "               ")
    stdscr.addstr(2, 2, "                                                  ")
    stdscr.addstr(2, 10, f"Score: {score}")
    stdscr.refresh()
    stdscr.getch()
    curses.curs_set(1)
    return 

def play_zeta_prac(stdscr, ranked=False, game_time=0):
    # Implement: typing speed test. Need to identify when they've figured it out and the only limitation is typing speed - 
    # Waits for '_' space to start 
    # 1 second pause and then the first question 
    stdscr.addstr(0, 17, " Practice ", curses.A_STANDOUT)
    appender = CSVAppender()
    stdscr.addstr(2, 15, " Ready? ")
    stdscr.refresh()
    time.sleep(1)
    
    score = 0
    # Make cursor visible
    curses.curs_set(0)    
    while True: 
        time_recent = time.time()
        got_wrong = False
        stdscr.addstr(1, 40, f"Score: {score}")
        stdscr.addstr(1, 40, f"Score: {score}")
        answer_str = ''
        
        # Assuming generate_question() returns num1, oper, num2 in that order.
        num1, oper, num2 = generate_question()
        question = f"{num1} {oper_dict[oper]} {num2}"
        ans = eval(f"{num1} {oper} {num2}")

        stdscr.addstr(2, 15, f"> {question} =      ")
        stdscr.move(2, 20 + len(question))
        stdscr.refresh()
        
        while True: 
            elapsed_time = time.time() - time_recent

            key = stdscr.getch()

            if key == curses.KEY_ENTER or key == 10 or key == 13:
                pass
            elif key in [curses.KEY_BACKSPACE, ord('\b'), ord('\x7f')]:
                if len(answer_str) > 0:
                    answer_str = answer_str[:-1]
                    stdscr.addstr(2, 20 + len(question) + len(answer_str), ' ')
                    stdscr.refresh()
            elif len(answer_str) + 1 < 10 and (chr(key).isdigit() or chr(key) in ['-', '.']):
                answer_str += chr(key)
            
            stdscr.addstr(2, 20 + len(question), answer_str)
            stdscr.refresh()
            
            # Check whether the answer is correct 
            try:
                if int(answer_str) == 9999:
                    appender.close()
                    stdscr.addstr(1, 40, "               ")
                    stdscr.addstr(2, 5, "                                                  ")
                    return
                
                if int(answer_str) == ans:
                    score += 1
                    time_taken = round(time.time() - time_recent, 3)
                    if time_taken < 90:  # Anything over 90 seconds is considered errenous (sorry)
                        appender.append(time.time(), num1, oper, num2, time_taken, got_wrong, ranked, game_time)
                    # Print to screen for diagnostics
                    
                    # stdscr.addstr(1, 59, f"⏲")

                    stdscr.refresh()
                    time_recent = time.time()
                    break  # Go to the next question
                if len(answer_str) >= len(str(ans)):
                    got_wrong = True

                

            except ValueError:
                continue 

    return 

def draw_zetaMatrix(stdscr, type='add'):

    # First, clear the area (just to be safe) 
    # Now, draw the corresponding 
    # for _ in 
    return 

def main(stdscr):
    # Initialize color support
    curses.start_color()
    
    # Initialize color pairs (Foreground: White, Background: Black)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)  
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE) 
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)

    # Apply the color pair to stdscr
    stdscr.bkgd(' ', curses.color_pair(1))  
    
    # Screen dimensions
    h, w = 25, 60
    h_min, w_min = h, w

    # Screen sizing loop
    while True:
        stdscr.clear()
        h_curr, w_curr = stdscr.getmaxyx()
        if h_curr <= h_min or w_curr <= w_min:
            # Show a live read of the screen size 
            stdscr.addstr(0, 0, "Please resize the window to at least 25x60")
            stdscr.addstr(1, 0, f"Currently: {h_curr:3} x {w_curr:3}")
            stdscr.addstr(2, 0, "You may use ⌘- / ⌘+")
        else:
            break

        # Refresh the screen
        stdscr.refresh()
    
    draw_home(stdscr)

    # CENTRAL LOOP 
    
    
# Start 
if __name__ == "__main__":
    curses.wrapper(main)


# Refresht he screen buttonso beautiful. How do they do it. 