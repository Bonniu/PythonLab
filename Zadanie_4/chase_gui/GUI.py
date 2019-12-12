from tkinter import *
import Simulate

liczba = 0

root = Tk()


def config():
    print('xd')



def open_file():
    print('open_file function')


def save_file():
    print('save_file function')


def quit_file():
    print('quit_file function')
    root.quit()
    root.destroy()


def left_click(event):
    print('leftclick')


def settings():
    print('settings')
    settings_main = Tk()
    settings_main.title("Wilk i owce2")
    settings_main.mainloop()


def right_click(event):
    print('rightclick')


def ramki():
    root.title("Wilk i owce")
    root.resizable(False, False)

    pasek_menu = Menu(root)
    root.config(menu=pasek_menu)

    menu_file = Menu(pasek_menu, tearoff=0)
    menu_file.add_command(label="Open", command=open_file)
    menu_file.add_command(label="Save", command=save_file)
    menu_file.add_command(label="Quit", command=quit_file)

    menu_settings = Menu(pasek_menu, tearoff=0)
    menu_settings.add_command(label="Settings", command=settings)

    pasek_menu.add_cascade(label="File", menu=menu_file)
    pasek_menu.add_cascade(label="Settings", menu=menu_settings)

    top_frame = Frame(root)
    top_frame.pack()

    top2_frame = Frame(root)
    top2_frame.pack()

    mid_frame = Frame(root, width=500, height=500, background="#88ff33")
    mid_frame.bind("<Button-1>", left_click)
    mid_frame.bind("<Button-3>", right_click)
    mid_frame.pack()

    bot_frame = Frame(root)
    bot_frame.pack()

    label_info = Label(top_frame, text="Symulacja wilka i owiec", fg="blue")
    label_info.pack(side=TOP)

    def step_btn():
        print('step')
        global liczba
        liczba += 1
        alive_sheeps.configure(text=liczba)

    btn1 = Button(top2_frame, text="Step", fg="green", command=step_btn)
    btn1.pack(side=LEFT, fill=X)

    def reset_btn():
        print('step')
        global liczba
        liczba = 0
        alive_sheeps.configure(text=liczba)

    btn2 = Button(top2_frame, text="Reset", fg="red", command=reset_btn)
    btn2.pack(side=RIGHT, fill=X)

    alive_sheeps_label = Label(bot_frame, text="Żywe owce: ", fg="red")
    alive_sheeps_label.pack(side=LEFT)
    alive_sheeps = Label(bot_frame, text="0", fg="red")
    alive_sheeps.pack(side=RIGHT)

    root.mainloop()


# def grid():
#     root = Tk()
#     root.title("XD1111112")
#
#     label_info = Label(root, text="ELO HERE", fg="blue")
#     btn1 = Button(root, text="Step", fg="green")
#     btn2 = Button(root, text="Reset", fg="red")
#     label_info.grid(row=0, columnspan=2)
#     btn1.grid(row=1, column=0)
#     btn2.grid(row=1, column=1)
#
#     root.mainloop()
#

ramki()
# grid()
