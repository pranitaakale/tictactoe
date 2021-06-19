from tkinter import *
from itertools import combinations
import random

root = Tk()

btn_dict = {0: '0'}  # Dictionary to store at which position we have 'X' or 'O'
btn = [0]  # List to store all 9 buttons of the board
win_list = ((1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7))  # Wining Moves

control = False  # Variable to indicate 'Two Player Game'(control=True) or 'You vs Computer'(control=False)
x_score = 0
o_score = 0
ur_score = 0
comp_score = 0

FONT1 = ('Helvetica', 20, 'bold')
FONT2 = ('Helvetica', 14)

label = Label(root, text="Choose Mode", width=20, height=2, font=FONT2)
button1 = Button(root, text="You vs Computer", width=20, height=2, command=lambda x=1: lbl(x), font=FONT2)
button2 = Button(root, text="Two player Game", width=20, height=2, command=lambda x=2: lbl(x), font=FONT2)
btm_frame = Frame(root, width=648)
board_frame = Frame(root)
xScore = Label(root, font=FONT1)
oScore = Label(root, font=FONT1)

reset = Button(btm_frame,text="Reset", width=10, font=FONT2)
win_loss = Label(btm_frame, width=20, font=FONT1)
back = Button(btm_frame, text="Back", width=10, font=FONT2)


def tk():
    root.title('Tic Tac Toe')
    root.geometry('650x550')


def rset():
    win_loss["text"] = " "
    for i in range(1, len(btn)):
        btn[i]["text"] = " "
        btn[i]["state"] = NORMAL
    btn_dict.clear()
    btn_dict[0] = '0'


def disable_btn():
    for i in range(1, 10):
        btn[i].config(state=DISABLED)


def show_btn():
    button1.grid(row=2, column=1, pady=10)
    button2.grid(row=3, column=1, pady=10)
    board_frame.grid_forget()
    btm_frame.grid_forget()
    xScore.grid_forget()
    oScore.grid_forget()
    label.config(text="Choose Mode")
    win_loss["text"] = " "
    for i in range(1,len(btn)):
        btn[i]["text"] = " "
        btn[i]["state"] = NORMAL
        btn[i].grid_forget()
    btn_dict.clear()
    btn_dict[0] = '0'


def hide_btn():
    button1.grid_forget()
    button2.grid_forget()


def lbl(x):
    hide_btn()
    global control
    if x == 1:
        label.config(text="You vs Computer")
        control = False
    else:
        label.config(text="Two player Game")
        control = True
    board()


def menu():
    top_frame = Frame(root, width=650, height=20, bg='grey')
    top_frame.grid(row=0, column=0, columnspan=3)

    label.grid(row=1, column=1, pady=20)

    button1.grid(row=2, column=1, pady=10)
    button2.grid(row=3, column=1, pady=10)


def check_win(ind, y):
    dict1 = {ind: y}
    btn_dict.update(dict1)
    l1 = []
    l2 = []
    for k, v in btn_dict.items():
        if v == "X":
            l1.append(k)
            l1.sort()
        elif v == "O":
            l2.append(k)
            l2.sort()
        else:
            pass

    for t in list(combinations(l1, 3)):
        if t in win_list:
            if y == "X":
                return "x"
    for t in list(combinations(l2, 3)):
        if t in win_list:
            if y == "O":
                return "o"


def ai():
    global comp_score
    # Creating empty list to store all blank positions and predict_moves list to store any predicted moves
    empty = []
    predict_moves = []
    # The loop here will add elements in empty
    for val in range(1, 10):
        if btn[val]["text"] == " ":
            empty.append(val)
    # If the 'empty' list has any elements in it, the 'predict_moves' will be appended, else if 'empty' list is empty
    # this will indicate that there aren't any empty positions even before anyone could win and so it will be a 'Tie'
    if empty:
        for ind in empty:
            if check_win(ind, "O") == "o" or check_win(ind, "X") == "x":
                btn_dict[ind] = " "
                predict_moves.append(ind)
                if empty.index(ind) == len(empty) - 1:
                    break

            else:
                del btn_dict[ind]
        # This if statement is to choose best possible move from 'predict_moves' list (if 'predict_moves' exists)
        if predict_moves:
            for move in predict_moves:
                if check_win(move, "O") == "o":
                    btn_dict[move] = "O"
                    btn[move].config(text="O", state=DISABLED)
                    win_loss["text"] = "You Lost!"
                    comp_score += 10
                    oScore["text"] = "AI Score\n" + str(comp_score)
                    disable_btn()
                    return
                elif check_win(move, "X") == "x":
                    btn_dict[move] = " "
                    if predict_moves.index(move) == len(predict_moves) - 1:
                        btn[move].config(text="O", state=DISABLED)
                        btn_dict[move] = "O"
                else:
                    btn_dict[move] = " "
        # If there aren't any predicted moves the move will be chosen randomly
        else:
            ind = random.choice(empty)
            btn[ind].config(text="O", state=DISABLED)
            btn_dict[ind] = "O"
            return
    else:
        win_loss["text"] = "Draw !"


def x_o(ind):
    global x_score, o_score, ur_score
    xScore.grid(row=2, column=0)
    oScore.grid(row=2, column=2)
    btn[ind]["state"] = DISABLED
    if control:
        xScore["text"] = "X Score\n" + str(x_score)
        oScore["text"] = "O Score\n" + str(o_score)
        for k, v in btn_dict.items():
            if v == '0' or v == "O":
                y = "X"

            elif v == "X":
                y = "O"
            else:
                pass
        btn[ind]["text"] = y
        btn_dict[ind] = y

        var = check_win(ind, y)
        if var == "x":
            win_loss["text"] = "Player 1 won!"
            x_score += 10
            xScore["text"] = "X Score\n"+str(x_score)
            disable_btn()
        elif var == "o":
            win_loss["text"] = "Player 2 won!"
            o_score += 10
            oScore["text"] = "O Score\n" + str(o_score)
            disable_btn()
        else:
            if len(btn_dict) == 10:
                win_loss["text"] = "Draw !"
    else:
        xScore["text"] = "Your Score\n" + str(ur_score)
        oScore["text"] = "AI Score\n" + str(comp_score)
        y = "X"
        btn[ind]["text"] = y
        if check_win(ind, y) == "x":
            win_loss["text"] = "You won!"
            ur_score += 10
            xScore["text"] = "Your Score\n" + str(ur_score)
            disable_btn()
        else:
            ai()


def board():
    board_frame.grid(row=2, column=1, pady=20)
    btm_frame.grid(row=4, column=0, pady=20, columnspan=3)
    reset.config(command=rset)
    reset.grid(row=0, column=0)
    win_loss.grid(row=0, column=1)
    back.config(command=show_btn)
    back.grid(row=0, column=3, padx=5)

    num = 1

    for i in range(1, 4):
        for j in range(1, 4):
            create_btn = Button(board_frame, text=" ", width=6, height=2, font=FONT1, relief=FLAT, bg='light grey',
                                command=lambda ind=num: x_o(ind))
            btn.append(create_btn)
            btn[num].grid(row=i, column=j,padx=1,pady=1)
            num += 1


def tk_():
    root.mainloop()


if __name__ == "__main__":
    tk()
    menu()
    tk_()
