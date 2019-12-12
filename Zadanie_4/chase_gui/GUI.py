from tkinter import *
import tkinter.messagebox
import tkinter.colorchooser as cch

import Simulate

liczba = 0
root = Tk()
sheep_color = "#0000ff"
wolf_color = "#ff0000"
mid_frame = Canvas(root, width=500, height=500, background="#00ff00")
bot_frame = Frame(root)
alive_sheeps = Label(bot_frame, text="0", fg="red")


def open_file():
    print('open_file function')
    tkinter.messagebox.showerror('xdxd')


def save_file():
    print('save_file function')
    tkinter.messagebox.showinfo('xdxd')


def quit_file(root):
    print('quit_file function')
    root.quit()
    root.destroy()


def left_click(event):
    print('leftclick - owca')
    print('{}, {}'.format(event.x, event.y))
    paint_dot_mouse(event.x, event.y, sheep_color)

    global liczba
    liczba += 1
    alive_sheeps.configure(text=liczba)


def settings():
    print('settings')
    settings_main = Tk()
    settings_main.title("Wilk i owce2")
    settings_main.mainloop()


def color_sheep_settings():
    color = cch.askcolor()
    global sheep_color
    sheep_color = color[1]


def color_wolf_settings():
    color = cch.askcolor()
    global wolf_color
    wolf_color = color[1]


def color_background_settings():
    color = cch.askcolor()
    mid_frame.delete("all")
    mid_frame.configure(bg=color[1])


def right_click(event):
    print('rightclick - wilk')
    print('{}, {}'.format(event.x, event.y))
    paint_dot_mouse(event.x, event.y, wolf_color)


def paint_dot(x, y, init_pos_limit, srodek, color=sheep_color):
    start_range = init_pos_limit * -1.5
    end_range = init_pos_limit * 1.5
    range_ = end_range - start_range
    point_x = x * (srodek / (range_ / 2)) + srodek
    point_y = y * (srodek / (range_ / 2)) + srodek
    mid_frame.create_oval(point_x - 4, point_y - 4, point_x + 4, point_y + 4, fill=color, outline=color)
    mid_frame.pack()


def paint_dot_mouse(x, y, color):
    mid_frame.create_oval(x - 4, y - 4, x + 4, y + 4, fill=color, outline=color)
    mid_frame.pack()


def main_function():
    root.title("Wilk i owce")
    root.resizable(False, False)

    pasek_menu = Menu(root)
    root.config(menu=pasek_menu)

    menu_file = Menu(pasek_menu, tearoff=0)
    menu_file.add_command(label="Open", command=open_file)
    menu_file.add_command(label="Save", command=save_file)
    menu_file.add_command(label="Quit", command=quit_file)

    menu_settings = Menu(pasek_menu, tearoff=0)
    menu_settings.add_command(label="Sheep color", command=color_sheep_settings)
    menu_settings.add_command(label="Wolf color", command=color_wolf_settings)
    menu_settings.add_command(label="Background color", command=color_background_settings)

    pasek_menu.add_cascade(label="File", menu=menu_file)
    pasek_menu.add_cascade(label="Settings", menu=menu_settings)

    top_frame = Frame(root)
    top_frame.pack()

    top2_frame = Frame(root)
    top2_frame.pack()

    mid_frame.bind("<Button-1>", left_click)
    mid_frame.bind("<Button-3>", right_click)
    paint_dot(0, 0, 10, 250, color=wolf_color)

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
        mid_frame.delete("all")
        paint_dot(0, 0, 10, 250, color="#ff0000")
        print('step')
        global liczba
        liczba = 0
        alive_sheeps.configure(text=liczba)

    btn2 = Button(top2_frame, text="Reset", fg="red", command=reset_btn)
    btn2.pack(side=RIGHT, fill=X)

    alive_sheeps_label = Label(bot_frame, text="Żywe owce: ", fg="red")
    alive_sheeps_label.pack(side=LEFT)
    alive_sheeps.pack(side=RIGHT)

    root.mainloop()


if __name__ == "__main__":
    main_function()
