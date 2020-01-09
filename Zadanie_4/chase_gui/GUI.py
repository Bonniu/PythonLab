import json
import tkinter.colorchooser as cch
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox

import Simulate
from Simulate import Sheep
from Simulate import Wolf

simulate = Simulate.Simulate()
simulate.init_sheeps()

auto_step: bool = False
auto_secs: int = 1000
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
    load_file_string = filedialog.askopenfilename(initialdir="/", title="Select file to open",
                                                  filetypes=(("JSON files", "*.json"), ("All Files", "*.*")))
    try:
        with open(load_file_string, 'r') as load_file_obj:
            json_str = json.load(load_file_obj)
            simulate.sheeps = []
            add_sheeps(json_str['sheeps'])
            simulate.wolf = Wolf.Wolf(json_str['wolf'][0], json_str['wolf'][1])
            repaint_animals()
    except json.decoder.JSONDecodeError:
        print('Błąd w trakcie wczytywania z pliku')
        tkinter.messagebox.showerror('Błąd', 'Błąd w trakcie wczytywania z pliku')
    tkinter.messagebox.showinfo('Informacja', 'Wczytano stan z pliku ' + load_file_string)


def add_sheeps(tab):
    for i in range(len(tab)):
        new_sheep = Sheep.Sheep()
        new_sheep.set_pos(tab[i][0], tab[i][1])
        simulate.sheeps.append(new_sheep)


def create_json_to_save():
    _ = []
    for i in simulate.sheeps:
        if i.is_alive:
            _.append((i.x, i.y))
    data_json = {
        'wolf': (simulate.wolf.x, simulate.wolf.y),
        'sheeps': _
    }
    return data_json


def save_file():
    save_file_string = filedialog.asksaveasfile(initialdir="/", title="Select file to save",
                                                filetypes=(("JSON files", "*.json"), ("All Files", "*.*")))

    try:
        with open(save_file_string.name, 'w') as save_file_obj:
            json.dump(create_json_to_save(), save_file_obj, indent=4)
    except json.decoder.JSONDecodeError:
        print('Błąd w trakcie zapisywania do pliku')
        tkinter.messagebox.showerror('Błąd', 'Błąd w trakcie zapisywania do pliku')
    tkinter.messagebox.showinfo('Informacja', 'Zapisano stan do pliku ' + save_file_string.name)


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
    range_ *= 1 / scale
    new_x = (x - srodek) * range_ / (2 * srodek)
    new_y = (y - srodek) * range_ / (2 * srodek)
    new_y *= -1
    return new_x, new_y


# -------------------------------------- settings


def open_settings_window():
    settings_root = Tk()
    settings_root.title("Settings")
    settings_root.geometry("350x250")
    settings_root.resizable(False, False)

    label1 = Label(settings_root, text="Kolor owiec:")
    label1.grid(row=0, column=0, padx=12, pady=12)

    def color_sheep_settings():
        color = cch.askcolor()
        global sheep_color
        sheep_color = color[1]
        settings_root.lift()

    btn1 = Button(settings_root, text="Wybierz kolor owcy", fg="black", command=color_sheep_settings)
    btn1.grid(row=0, column=1, padx=12, pady=12)

    label2 = Label(settings_root, text="Kolor wilka: ")
    label2.grid(row=1, column=0, padx=12, pady=12)

    def color_wolf_settings():
        color = cch.askcolor()
        global wolf_color
        wolf_color = color[1]
        settings_root.lift()

    btn2 = Button(settings_root, text="Wybierz kolor wilka", fg="black", command=color_wolf_settings)
    btn2.grid(row=1, column=1, padx=12, pady=12)

    label3 = Label(settings_root, text="Kolor tła: ")
    label3.grid(row=2, column=0, padx=12, pady=12)

    def color_background_settings():
        color = cch.askcolor()
        mid_frame.configure(bg=color[1])
        settings_root.lift()

    btn3 = Button(settings_root, text="Wybierz kolor tła", fg="black", command=color_background_settings)
    btn3.grid(row=2, column=1, padx=12, pady=12)

    label4 = Label(settings_root, text="Czas kroku symulacji: ")
    label4.grid(row=3, column=0, padx=12, pady=12)

    chosen_number = Combobox(settings_root, width=10, state="readonly")
    chosen_number['values'] = (0.5, 1, 1.5, 2)
    chosen_number.grid(row=3, column=1, padx=12, pady=12)
    chosen_number.current(1)

    def on_closing():
        global auto_secs
        tmp: dict = {'0.5': 500, '1': 1000, '1.5': 1500, '2': 2000}
        auto_secs = tmp[chosen_number.get()]
        settings_root.destroy()
        repaint_animals()

    settings_root.protocol("WM_DELETE_WINDOW", on_closing)


# -------------------------------------------- kolory

def repaint_animals():
    mid_frame.delete("all")
    for sheep in simulate.sheeps:
        if sheep.is_alive:
            paint_dot(sheep.x, sheep.y, 250, sheep_color)
    paint_dot(simulate.wolf.x, simulate.wolf.y, 250, wolf_color)
    alive_sheeps.configure(text=simulate.alive_sheeps())


def paint_dot(x, y, srodek=250, color=sheep_color, promien=4):
    start_range = Simulate.init_pos_limit * -1.5
    end_range = Simulate.init_pos_limit * 1.5
    range_ = end_range - start_range
    range_ *= 1 / scale
    promien *= scale
    point_x = x * (srodek / (range_ / 2)) + srodek
    point_y = (-y) * (srodek / (range_ / 2)) + srodek
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

    pasek_menu.add_cascade(label="File", menu=menu_file)
    pasek_menu.add_cascade(label="Settings", command=open_settings_window)

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
        if alive_sheeps['text'] == 0 and auto_step:
            return False
        elif alive_sheeps['text'] == 0:
            tkinter.messagebox.showinfo('Informacja', 'Brak owiec na planszy, nie wykonano żadnego ruchu')
            return False
        else:
            simulate.move_sheeps()
            simulate.move_wolf()
            repaint_animals()
            return True

    btn1 = Button(top2_frame, text="Step", fg="blue", command=step_btn)
    btn1.pack(side=LEFT, fill=X)

    def auto_step_fun():
        global auto_step
        auto_step = not auto_step
        if auto_step:
            btn3.configure(text="Stop", fg="red")
            btn1.configure(state="disabled")
            btn2.configure(state="disabled")
            mid_frame.unbind("<Button-1>")
            mid_frame.unbind("<Button-3>")
            pasek_menu.entryconfig(1, state=DISABLED)
            pasek_menu.entryconfig(2, state=DISABLED)

        else:
            btn3.configure(text="Start", fg="green")
            btn1.configure(state="normal")
            btn2.configure(state="normal")
            mid_frame.bind("<Button-1>", left_click)
            mid_frame.bind("<Button-3>", right_click)
            pasek_menu.entryconfig(1, state=NORMAL)
            pasek_menu.entryconfig(2, state=NORMAL)

    btn3 = Button(top2_frame, text="Start", fg="green", command=auto_step_fun)

    btn3.pack(side=LEFT, fill=X)

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

    def clock():
        root.after(auto_secs, clock)  # run itself again after 1000 ms
        if auto_step:
            if not step_btn():
                auto_step_fun()
                tkinter.messagebox.showinfo('Informacja', 'Brak owiec na planszy, koniec symulacji')

    clock()

    root.mainloop()


if __name__ == "__main__":
    # print owce

    simulate.print_sheeps()
    #  ruch owiec
    # simulate.move_sheeps()
    #  ruch wilka
    # simulate.move_wolf()
    # open_file()
    main_function()
