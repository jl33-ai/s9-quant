import curses

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

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    h, w = stdscr.getmaxyx()

    # Define the buttons
    buttons = [Button("Button 1"), Button("Button 2"), Button("Button 3"), Button("Button 4")]
    buttons[0].selected = True  # The first button is selected initially

    current_index = 0
    while True:
        # Calculate the starting x position for centering the buttons
        total_width = sum([len(btn.text) + 4 for btn in buttons]) + (len(buttons) - 1) * 3  # +4 for [ ] and spaces, 3 spaces between buttons
        start_x = w // 2 - total_width // 2

        # Draw the buttons
        for btn in buttons:
            btn.render(stdscr, h // 2, start_x)
            start_x += len(btn.text) + 4 + 3  # Move the x position to the next button's start

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
            stdscr.addstr(h - 2, w // 2 - 10, f"{buttons[current_index].text} was pressed!")
            stdscr.refresh()
            stdscr.getch()  # Wait for any key press
            break

curses.wrapper(main)