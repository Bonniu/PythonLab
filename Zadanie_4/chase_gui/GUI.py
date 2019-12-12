from tkinter import *
import tkinter.messagebox
import tkinter.colorchooser as cch

import Simulate
import Sheep

simulate = Simulate.Simulate()
simulate.init_sheeps()

scale = 1
root = Tk()
sheep_color = "#0000ff"
wolf_color = "#ff0000"
mid_frame = Canvas(root, width=500, height=500, background="#00ff00")
bot_frame = Frame(root)
alive_sheeps = Label(bot_frame, text="0", fg="red")
top2_frame = Frame(root)


def on_change_scale(event):
    dict_ = {-2: 0.4, -1: 0.7, 0: 1, 1: 1.3, 2: 1.6}
    global scale
    scale = dict_[sss.get()]
    repaint_animals()


sss = Scale(top2_frame, from_=-2, to=2, orient=HORIZONTAL, command=on_change_scale)


# -------------------------------------- operacje na plikach

def open_file():
    print('open_file function')
    tkinter.messagebox.showerror('xdxd')


def save_file():
    print('save_file function')
    tkinter.messagebox.showinfo('xdxd')


def quit_file():
    print('quit_file function')
    root.quit()
    root.destroy()


# -------------------------------------- mysz
def left_click(event):
    x, y = convert_mouse_to_xy(event.x, event.y)
    sheep = Sheep.Sheep()
    sheep.set_pos(x, y)
    simulate.sheeps.append(sheep)
    repaint_animals()


def right_click(event):
    x, y = convert_mouse_to_xy(event.x, event.y)
    simulate.wolf.x = x
    simulate.wolf.y = y
    repaint_animals()


def convert_mouse_to_xy(x, y, srodek=250):
    start_range = Simulate.init_pos_limit * -1.5
    end_range = Simulate.init_pos_limit * 1.5
    range_ = end_range - start_range
    new_x = (x - srodek) * range_ / (2 * srodek)
    new_y = (y - srodek) * range_ / (2 * srodek)
    return new_x, new_y


# -------------------------------------- kolory

def color_sheep_settings():
    color = cch.askcolor()
    global sheep_color
    sheep_color = color[1]
    repaint_animals()


def color_wolf_settings():
    color = cch.askcolor()
    global wolf_color
    wolf_color = color[1]
    repaint_animals()


def color_background_settings():
    color = cch.askcolor()
    mid_frame.configure(bg=color[1])
    repaint_animals()


def repaint_animals():
    mid_frame.delete("all")
    paint_dot(simulate.wolf.x, simulate.wolf.y, 250, wolf_color)
    for sheep in simulate.sheeps:
        if sheep.is_alive:
            paint_dot(sheep.x, sheep.y, 250, sheep_color)
    alive_sheeps.configure(text=simulate.alive_sheeps())


def paint_dot(x, y, srodek, color=sheep_color, promien=4):
    start_range = Simulate.init_pos_limit * -1.5
    end_range = Simulate.init_pos_limit * 1.5
    range_ = end_range - start_range
    range_ *= 1 / scale
    promien *= scale
    point_x = x * (srodek / (range_ / 2)) + srodek
    point_y = y * (srodek / (range_ / 2)) + srodek
    mid_frame.create_oval(point_x - promien, point_y - promien, point_x + promien, point_y + promien, fill=color,
                          outline=color)
    mid_frame.pack()


# -------------------------------------- main function

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

    top2_frame.pack()

    mid_frame.bind("<Button-1>", left_click)
    mid_frame.bind("<Button-3>", right_click)
    repaint_animals()

    bot_frame.pack()

    label_info = Label(top_frame, text="Symulacja wilka i owiec", fg="blue")
    label_info.pack(side=TOP)

    def step_btn():
        if alive_sheeps['text'] == 0:
            tkinter.messagebox.showinfo('Informacja', 'Brak owiec na planszy, nie wykonano żadnego ruchu')
        else:
            simulate.move_sheeps()
            simulate.move_wolf()
            repaint_animals()

    btn1 = Button(top2_frame, text="Step", fg="green", command=step_btn)
    btn1.pack(side=LEFT, fill=X)

    def reset_btn():
        simulate.sheeps = []
        simulate.wolf.x = 0
        simulate.wolf.y = 0
        repaint_animals()

    btn2 = Button(top2_frame, text="Reset", fg="red", command=reset_btn)
    btn2.pack(side=RIGHT, fill=X)

    sss.pack(side=RIGHT, fill=X)

    alive_sheeps_label = Label(bot_frame, text="Żywe owce: ", fg="red")
    alive_sheeps_label.pack(side=LEFT)

    alive_sheeps.pack(side=RIGHT)

    root.mainloop()


if __name__ == "__main__":
    # print owce

    simulate.print_sheeps()
    #  ruch owiec
    # simulate.move_sheeps()
    #  ruch wilka
    # simulate.move_wolf()

    main_function()
