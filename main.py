# Quant-S9
import curses
import json
import datetime


# The `screen` is a window that acts as the master window
# that takes up the whole screen. Other windows created
# later will get painted on to the `screen` window.
screen = curses.initscr()

# lines, columns, start line, start column
my_window = curses.newwin(15, 20, 0, 0)

# Long strings will wrap to the next line automatically
# to stay within the window
my_window.addstr(4, 4, "Hello from 4,4")
my_window.addstr(5, 15, "Hello from 5,15 with a long string")

# Print the window to the screen
my_window.refresh()
curses.napms(2000)

# Clear the screen, clearing my_window contents that were printed to screen
# my_window will retain its contents until my_window.clear() is called.
screen.clear()
screen.refresh()

# Clear the window and redraw over the current window space
# This does not require clearing the whole screen, because the window
# has not moved position.
my_window.clear()
my_window.refresh()
curses.napms(1000)

curses.endwin()


#master sql. invites, books, did u sketch, erm


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










'''
{
	"player_info" : {
		"24" : {
			"num_played" : 0
			"history" : []
		}
		"zetamac" : {
			"num_played" : 0
			"history" : []
		}
		
	}
}
'''
