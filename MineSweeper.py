from tkinter import *
import random
from datetime import datetime

clicks = 0
colors = ["blue", "green", "red", "orange", "pink", "black", "cyan", "purple"]


class Board:

    def __init__(self, r, c, m):

        self.rows = r
        self.cols = c
        self.mines = m
        self.boxes_left = r * c - m
        self.mine_pos = []
        self.shown = [[0] * self.cols for i in range(self.rows)]
        self.values = [[0] * self.cols for i in range(self.rows)]

    def set_mines(self, fx, fy):

        aux1 = -1
        while aux1 <= 1:
            aux2 = -1
            while aux2 <= 1:
                if 0 <= fx + aux1 < self.rows and 0 <= fy + aux2 < self.cols:
                    self.values[fx + aux1][fy + aux2] = -2
                aux2 += 1
            aux1 += 1

        for i in range(self.mines):

            x = random.randint(0, self.rows - 1)
            y = random.randint(0, self.cols - 1)

            while self.values[x][y] == -1 or self.values[x][y] == -2:
                x = random.randint(0, self.rows - 1)
                y = random.randint(0, self.cols - 1)

            self.values[x][y] = -1
            self.mine_pos.append((x, y))

        aux1 = -1
        while aux1 <= 1:
            aux2 = -1
            while aux2 <= 1:
                if 0 <= fx + aux1 < self.rows and 0 <= fy + aux2 < self.cols:
                    self.values[fx + aux1][fy + aux2] = 0
                aux2 += 1
            aux1 += 1

        for i in range(self.rows):

            for j in range(self.cols):

                if self.values[i][j] == -1:

                    for k in range(i - 1, i + 2):

                        for l in range(j - 1, j + 2):

                            if 0 <= k < self.rows and 0 <= l < self.cols:

                                if self.values[k][l] != -1:
                                    self.values[k][l] += 1


###################################################################################
################################### GUI PART ######################################
###################################################################################

window = Tk()
window.title("MineSweeper")

# label1 = Label(window, text="Select difficulty", font=20)
# label1.grid(row=0, column=0, columnspan=8)

# Create board object

rows = 8
cols = 8
mines = 10

board = Board(rows, cols, mines)

# Create button matrix and display it
buttons = []


def BuildBoard():
    global buttons
    global board

    for x in range(0, board.rows):
        buttons.append([])
        for y in range(0, board.cols):
            b = Button(window, text=" ", font=4, height=2, bg="grey", width=4,
                       command=lambda x=x, y=y: clickOn(x, y))
            b.bind("<Button-3>", lambda e, x=x, y=y: onRightClick(x, y))
            b.grid(row=x + 1, column=y, sticky=N + W + S + E)
            buttons[x].append(b)


BuildBoard()


# Flag mechanics.
def onRightClick(x, y):
    if not board.shown[x][y]:
        if buttons[x][y]["text"] == "!":
            buttons[x][y]["text"] = "?"
        elif buttons[x][y]["text"] == "?":
            buttons[x][y]["text"] = " "
        else:
            buttons[x][y]["text"] = "!"


# Recursive function, reveals the clicked box and if it's an empty box it shows al the nearby ones by executing this
# same function on them. If its a mine, you lose instantly and the program is interrupted. It also checks the number of
# boxes left to win, and when the number reaches 0, it shows the win screen.
def clickOn(x, y):
    global buttons, clicks, board, rows, cols, mines
    clicks += 1

    # We set up the board right after the first click, in order not to lose instantly
    if clicks == 1:
        board.set_mines(x, y)

    # Case box is a bomb
    if board.values[x][y] == -1:
        buttons[x][y]["text"] = "*"
        buttons[x][y]["bg"] = "red"
        buttons[x][y]["state"] = "disabled"

        board.mine_pos.remove((x, y))
        shown_mines = 0
        t1 = datetime.now()
        a = 1 / 3

        while shown_mines < len(board.mine_pos):
            t2 = datetime.now()
            m = (t2.minute * 60 + t2.second + (int(t2.microsecond / 100000) / 10) - t1.minute * 60 - t1.second - (
                    int(t1.microsecond / 100000) / 10))
            if m > a:
                a += 1 / 3
                i = board.mine_pos[shown_mines][0]
                j = board.mine_pos[shown_mines][1]
                shown_mines += 1
                buttons[i][j]["text"] = "*"
                buttons[i][j]["bg"] = "red"
                window.update_idletasks()

        for widget in window.winfo_children():
            widget["state"] = "disabled"

        # Loss screen
        window2 = Tk()
        window2.title("pringao")
        l = Label(window2, text="Eres malardo", font=20, padx=80, pady=20)
        l.grid(row=0, column=0)
        b = Button(window2, width=4, text="ok :'(", font=20, bg="grey", command=lambda: exit())
        b.grid(row=1, column=0)
        window2.mainloop()

    # Case box has mines close
    if 9 > board.values[x][y] > 0:
        buttons[x][y]["text"] = str(board.values[x][y])
        buttons[x][y]["bg"] = "white"
        buttons[x][y]["disabledforeground"] = colors[board.values[x][y] - 1]
        buttons[x][y]["state"] = "disabled"
        board.shown[x][y] = True
        board.boxes_left -= 1

    # Case box has no mines close. Recursion is applied here
    if board.values[x][y] == 0:

        board.boxes_left -= 1
        buttons[x][y]["text"] = " "
        buttons[x][y]["bg"] = "white"
        buttons[x][y]["state"] = "disabled"
        board.shown[x][y] = True
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if 0 <= i < board.rows and 0 <= j < board.cols and (i != x or j != y) and not board.shown[i][j]:
                    clickOn(i, j)

    # Check win condition
    if board.boxes_left == 0:
        print("has ganao")
        for widget in window.winfo_children():
            widget["state"] = "disabled"

        # To avoid further win checks
        board.boxes_left -= 1
        # parar coronometro

        # Win screen
        window2 = Tk()
        window2.title("epico")
        l = Label(window2, text="Has ganao tiaco", font=20, padx=20, pady=20)
        l.grid(row=0, column=0)
        b = Button(window2, width=6, text="yay! :D", font=20, bg="blue", command=lambda: exit())
        b.grid(row=1, column=0)
        window2.mainloop()


window.mainloop()
