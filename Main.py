from tkinter import *
import functools
import random

clicknum = 0
gameover = False

class Board:

    def __init__(self,r,c,m,):

        self.rows = r
        self.cols = c
        self.mines = m
        self.shown = [[0]*self.cols for i in range(self.rows)]
        self.values = [[0]*self.cols for i in range(self.rows)]

    def set_mines(self,fx,fy):

            aux1 = -1
            while  aux1 <=1 :
                aux2 = -1
                while aux2 <=1 :
                    if 0 <= fx+aux1 < self.rows and 0 <= fy+aux2 < self.cols:
                        self.values[fx + aux1][fy + aux2] = -2
                    aux2 += 1
                aux1 += 1


            for i in range(self.mines):

                x = random.randint(1, self.rows)
                y = random.randint(1, self.cols)

                while self.values[x][y] == -1 or self.values[x][y] == -2 :

                    x = random.randint(1, self.rows)
                    y = random.randint(1, self.cols)

                self.values[x][y] = -1

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

                            for k in range(i-1,i+2):

                                for l in range(j-1,j+2):

                                    if 0 <= k < self.rows and 0 <= l < self.cols:

                                            if self.values[k][l] != -1:

                                                self.values[k][l] += 1

root = Tk()

def left_click(event):
    event.widget.configure(bg="green")


def right_click(event):
    event.widget.configure(bg="red")

board = Board(8,8,10)

buttons = []

for y in range(0, board.rows):
    buttons.append([])
    for x in range(0, board.cols):
        b = Button(root, text=" ", width=2, command=lambda x=x, y=y: clickOn(x, y))
        b.bind("<Button-3>", lambda e, x=x, y=y: onRightClick(x, y))
        b.grid(row=x + 1, column=y, sticky=N + W + S + E)
        buttons[x].append(b)


def onRightClick(x,y):
    return

def clickOn(x,y):

    global buttons, clicknum, gameover, board
    clicknum += 1

    if clicknum == 1:
        board.set_mines(x, y)

    if board.shown[x][y] == 1:
        return

    if board.values[x][y] == -1:
        buttons[x][y]["text"] = "*"
        gameover = True

    if 9 > board.values[x][y] > 0:
        buttons[x][y]["text"] = board.values[x][y]
        board.shown[x][y] = True

    if board.values[x][y] == 0:

        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if 0 <= i < board.rows and 0 <= j < board.cols:
                    clickOn(i,j)


root.mainloop()