from tkinter import *
import random
import time
import threading

# Global variables
colors = ["blue", "green", "red", "orange", "pink", "black", "cyan", "purple"]
buttons = []
speed = 0
clicks = 0
flag_num = 0
width = 2

###################################################################################
###################################################################################
################################# Board Class #####################################
###################################################################################
###################################################################################

class Board:

    def __init__(self):
        self.rows = 0
        self.cols = 0
        self.mines = 0
        self.boxes_left = 0
        self.mine_pos = []
        self.shown = []
        self.values = []

    def set_all(self, r, c, m):
        self.rows = r
        self.cols = c
        self.mines = m
        self.boxes_left = r * c - m
        self.mine_pos = []
        self.shown = [[0] * self.cols for i in range(self.rows)]
        self.values = [[0] * self.cols for i in range(self.rows)]

    def set_mines(self, fx, fy):

        # Avoid generating mines near the first click position by setting the unavailable
        # positions to the aux value -2
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

        # Once mines are correctly generated, the altered values are set to 0 again
        aux1 = -1
        while aux1 <= 1:
            aux2 = -1
            while aux2 <= 1:
                if 0 <= fx + aux1 < self.rows and 0 <= fy + aux2 < self.cols:
                    self.values[fx + aux1][fy + aux2] = 0
                aux2 += 1
            aux1 += 1

        # In this nested loop each position in values matrix is added 1 for
        # each -1 (value for mine) nearby it
        for i in range(self.rows):

            for j in range(self.cols):

                if self.values[i][j] == -1:

                    for k in range(i - 1, i + 2):

                        for l in range(j - 1, j + 2):

                            if 0 <= k < self.rows and 0 <= l < self.cols:

                                if self.values[k][l] != -1:
                                    self.values[k][l] += 1

###################################################################################
###################################################################################
################################### GUI PART ######################################
###################################################################################
###################################################################################

window = Tk()
window.title("MineSweeper")
window.config(bg="grey")

board = Board()
mine_counter = Label


# Yet to implement
def Clock():
    clock = Label(text="000", height=2, font=20)
    clock.grid(row=0, column=0, columnspan=3)
    t1 = time.perf_counter()
    a = 1

    while True:
        t2 = time.perf_counter()
        m = int(t2 - t1)
        if m > a:
            a += 1
            clock["text"] = '{:0>3}'.format(m)


# Builds the button object matrix using board and displays it, along with the mine counter.
def BuildBoard():
    global mine_counter

    for widgets in window.winfo_children():
        widgets.destroy()

    # Tkinter no funciona muy bien con los hilos al parecer :(
    # clock = threading.Thread(target=Clock)
    # clock.start()

    mine_counter = Label(window, font=20, text="Mines left: " + str(board.mines), bg="grey", height=3)
    mine_counter.grid(row=0, column=0, columnspan=board.cols)

    for x in range(0, board.rows):
        buttons.append([])
        for y in range(0, board.cols):
            b = Button(window, text=" ", font=4, height=1, width=width, bg="grey",
                       command=lambda x=x, y=y: clickOn(x, y))
            b.bind("<Button-3>", lambda e, x=x, y=y: rightClickOn(x, y))
            b.grid(row=x + 1, column=y, sticky=N + W + S + E)
            buttons[x].append(b)


def EasyMode():
    global speed
    speed = 1 / 5
    board.set_all(8, 8, 10)
    BuildBoard()


def MidMode():
    global speed
    speed = 1 / 15
    board.set_all(16, 16, 40)
    BuildBoard()


def HardMode():
    global speed, width
    width = 1
    speed = 1 / 30
    board.set_all(16, 30, 99)
    BuildBoard()


def ShowMenu():
    label1 = Label(window, text="Select difficulty", font=20, background="grey", height=3, width=20)
    label1.grid(row=0, column=0, columnspan=8)
    button_easy = Button(window, text="Easy", font=20, background="cyan2", height=3, width=20, padx=20,
                         command=EasyMode)
    button_easy.grid(row=1, column=0)
    button_medium = Button(window, text="Medium", font=20, background="yellow2", height=3, width=20, padx=20,
                           command=MidMode)
    button_medium.grid(row=2, column=0)
    button_hard = Button(window, text="Hard", font=20, background="red2", height=3, width=20, padx=20, command=HardMode)
    button_hard.grid(row=3, column=0)


# Flag mechanics.
def rightClickOn(x, y):
    global mine_counter, flag_num

    if not board.shown[x][y]:
        if buttons[x][y]["text"] == "!":
            buttons[x][y]["text"] = "?"
            flag_num -= 1
        elif buttons[x][y]["text"] == "?":
            buttons[x][y]["text"] = " "
        else:
            buttons[x][y]["text"] = "!"
            flag_num += 1

        if board.mines - flag_num >= 0:
            mine_counter["text"] = "Mines left: " + str(board.mines - flag_num)

        window.update_idletasks()


# Recursive function, reveals the clicked box and if it's an empty box it shows al the nearby ones by executing this
# same function on them. If its a mine, you lose instantly and the program is interrupted. It also checks the number of
# boxes left to win, and when the number reaches 0, it shows the win screen.
def clickOn(x, y):
    global clicks
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
        t1 = time.perf_counter()
        a = speed

        while shown_mines < len(board.mine_pos):
            t2 = time.perf_counter()
            m = (round(t2 - t1, 2))
            if m > a:
                a += speed
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
        l = Label(window2, text="Has perdido", font=20, padx=80, pady=20)
        l.grid(row=0, column=0)
        b = Button(window2, width=4, text="ok :'(", font=20, bg="red", command=lambda: exit())
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
        l = Label(window2, text="Has ganao tiaco", font=20, padx=80, pady=20)
        l.grid(row=0, column=0)
        b = Button(window2, width=6, text="yay! :D", font=20, bg="cyan", command=lambda: exit())
        b.grid(row=1, column=0)
        window2.mainloop()


# "Main" function
ShowMenu()

window.mainloop()
