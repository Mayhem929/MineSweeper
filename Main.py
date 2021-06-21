from tkinter import *
import functools
import random

clicknum = 0
counter = 0
gameover = False
colors = ["blue", "green", "red", "orange", "pink", "black", "cyan"]

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

                x = random.randint(0, self.rows-1)
                y = random.randint(0, self.cols-1)

                while self.values[x][y] == -1 or self.values[x][y] == -2 :

                    global counter
                    counter +=1


                    x = random.randint(0, self.rows-1)
                    y = random.randint(0, self.cols-1)

                    if counter % 1000000 == 0:
                        print(counter, x, y, i)


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

window = Tk()
window.title("MineSweeper")

def left_click(event):
    event.widget.configure(bg="green")


def right_click(event):
    event.widget.configure(bg="red")

board = Board(10, 10, 90)

buttons = []

for x in range(0, board.rows):
    buttons.append([])
    for y in range(0, board.cols):
        b = Button(window, text=" ", activeforeground="blue", font=4, height=2, bg="grey", width=4, command=lambda x=x,y=y: clickOn(x,y))
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
        buttons[x][y]["bg"] = "red"
        buttons[x][y]["state"] = "disabled"

    if 9 > board.values[x][y] > 0:
        buttons[x][y]["text"] = str(board.values[x][y])
        buttons[x][y]["bg"] = "white"
        buttons[x][y]["disabledforeground"] = colors[board.values[x][y]-1]
        buttons[x][y]["state"] = "disabled"
        board.shown[x][y] = True

    if board.values[x][y] == 0:

        buttons[x][y]["text"] = " "
        buttons[x][y]["bg"] = "white"
        buttons[x][y]["state"] = "disabled"
        board.shown[x][y] = True
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if 0 <= i < board.rows and 0 <= j < board.cols and (i != x or j != y) and not board.shown[i][j]:
                    clickOn(i,j)


window.mainloop()
