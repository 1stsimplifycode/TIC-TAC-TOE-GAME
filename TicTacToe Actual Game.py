from tkinter import *
from tkinter import messagebox
import random as r

label = None

def button(frame, row, col):  # Creates button
    bu = Button(frame, padx=1, bg='papaya whip', width=3, text=' ', font=('Courier New', 60, 'bold'),
                relief='sunken', bd=10, command=lambda: click(row, col))
    return bu

def change_a():  # Changes operand after each turn
    global a
    for i in opls:
        if not (i == a):
            a = i
            if a == 'X':
                label.config(text="X's Turn")
            else:
                label.config(text="O's Turn")
            break

def reset():  # Resets the board after each match
    global a
    for i in range(3):
        for j in range(3):
            b[i][j]['text'] = ' '
            b[i][j]['state'] = NORMAL
    a = r.choice(opls)
    label.config(text=a + "'s Turn")

def check():  # Checks match result
    for i in range(3):
        if all(b[i][j]["text"] == a for j in range(3)) or all(b[j][i]["text"] == a for j in range(3)):
            messagebox.showinfo("Congrats!!", "'" + a + "' has won")
            reset()

    if all(b[i][i]["text"] == a for i in range(3)) or all(b[i][2 - i]["text"] == a for i in range(3)):
        messagebox.showinfo("Congrats!!", "'" + a + "' has won")
        reset()

    elif all(all(b[i][j]["state"] == DISABLED for j in range(3)) for i in range(3)):
        messagebox.showinfo("Tied!!", "The match ended in a draw")
        reset()

def click(row, col):
    global a
    b[row][col].config(text=a, state=DISABLED, disabledforeground=colour[a])
    check()
    change_a()

def multi_player():
    global root, label
    multi = Toplevel(root)
    multi.title('Multi-Player')

    label = Label(multi, text=a + "'s Turn", font=('Georgia', 20, 'bold'))
    label.grid(row=4, column=0, columnspan=3)

    for i in range(3):
        for j in range(3):
            b[i].append(button(multi, i, j))
            b[i][j].grid(row=i+1, column=j)

def playbuttonclick():
    global root
    root.withdraw()  # Hide the root window
    playmenu = Toplevel(root)
    playmenu.title('Game Mode')
    playmenu.geometry('750x350')

    def go_back():
        playmenu.destroy()
        root.deiconify()  # Show the root window again when 'Back' is clicked

    label = Label(playmenu, text="Choose your Game Adventure",font=("Helvetica", 30))
    label.grid(row=3,column=0)
    
    back_button = Button(playmenu, image=imgback, command=go_back)
    back_button.grid(row=12, column=0)

    singlebutton = Button(playmenu, image=imgsingle, command=single_player_mode)
    singlebutton.grid(row=6, column=0, pady=5)

    multibutton = Button(playmenu, image=imgmulti, command=multi_player)
    multibutton.grid(row=9, column=0, pady=10)

def single_player_mode():
    import GUPTASHREE

a = r.choice(['O', 'X'])  # Two operators defined

root = Tk()
root.title('Tic-Tac-Toe')
root.geometry('500x180')

imgplay = PhotoImage(file=r'C://Users//mailt//OneDrive//Desktop//__pycache__//Picture1.png')
imgsingle = PhotoImage(file=r'C://Users//mailt//OneDrive//Desktop//__pycache__//single.png')
imgmulti = PhotoImage(file=r'C://Users//mailt//OneDrive//Desktop//__pycache__//multi.png')
imgez = PhotoImage(file=r'C://Users//mailt//OneDrive//Desktop//__pycache__//easy.png')
imghd = PhotoImage(file=r'C://Users//mailt//OneDrive//Desktop//__pycache__//hard.png')
imgback=PhotoImage(file=r'C://Users//mailt//OneDrive//Desktop//__pycache__//BACK.png')

play = Button(root, image=imgplay, command=playbuttonclick)
play.grid(row=2, column=0, pady=10)

opls = ['X', 'O']
colour = {'O': 'sky blue', 'X': 'light pink'}
b = [[], [], []]

root.mainloop()


