# Quant-S9
from curses.textpad import Textbox, rectangle
import curses
import json
import datetime
import time
import random

# Every question you complete gives you a QXP, with multipliers for streaks etc. 
# It needs a... Scraper. 
# 'QXP earned: ' 
    

    # :-( :-| :-) 𝝈 - whil eyou're playing. The sigma is multicoloured
    # Main loop
    # approximation game
    # ranking mode
    # need a json list of q's and a's under certain categories. 

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

def draw_menu(stdscr, selected_row_idx):
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(["Zetamac", "24", "Sequences", "Probability"]):
        x = 2
        y = idx+4
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)

def main(stdscr):
    # Initialize color support
    curses.start_color()
    
    # Initialize color pair (Foreground: White, Background: Black)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE) 

    # Apply the color pair to stdscr
    stdscr.bkgd(' ', curses.color_pair(1))

    curses.curs_set(0)  # Make cursor invisible
    
    # Screen dimensions
    h_min, w_min = 30, 80

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        if h < h_min or w < w_min:
            stdscr.addstr(0, 0, "Please resize the window to at least 30x80.")
        else:
            # Code to draw your interface here, e.g., draw_box(stdscr, 0, 0, 2, w - 1)
            stdscr.addstr(0, 0, "Window resized successfully. Press 'q' to quit.")
            
            # Listen for 'q' key to break the loop
            key = stdscr.getch()
            if key == ord('q'):
                break

        # Refresh the screen
        stdscr.refresh()

    h, w = 30, 81

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
    
    # Add text
    # Top bar
    stdscr.addstr(0, 25, " 𝞼-Quant ")

    # Game Names
    stdscr.addstr(4, 2, "[0] Zetamac")
    stdscr.addstr(5, 2, "[1] 24")
    stdscr.addstr(6, 2, "[3] Sequences")
    stdscr.addstr(7, 2, "[4] Probability")
    stdscr.addstr(8, 2, "[5] Approximation")
    stdscr.addstr(9, 2, "[6] Approximation")
    stdscr.addstr(10, 2, "SIMS")
    stdscr.addstr(11, 2, "[A] Type Speed")
    stdscr.addstr(12, 2, "[B] Live Problems")
    stdscr.addstr(13, 2, "[C] Trading/Gambling")
    stdscr.addstr(14, 2, "[D] Full Interview")

    # Skill Level
    stdscr.addstr(4, 40, "▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒", curses.color_pair(2))
    stdscr.addstr(5, 40, "▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒", curses.color_pair(2))
    stdscr.addstr(6, 40, "▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒", curses.color_pair(2))
    stdscr.addstr(7, 40, "▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒", curses.color_pair(2))

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
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    current_row = 0
    
    draw_menu(stdscr, current_row)
    
    while True:
        key = stdscr.getch()
        
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(["Zetamac", "24", "Sequences", "Probability"]) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            #stdscr.addstr(0, 0, f"You selected '{["Zetamac", "24", "Sequences", "Probability"][current_row]}'")
            stdscr.refresh()
            stdscr.getch()
            break
            
        draw_menu(stdscr, current_row)
        stdscr.refresh()
    

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

if __name__ == "__main__":
    curses.wrapper(main)

    
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

if __name__ == "__main__":
    curses.wrapper(main)



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
