import time
import tkinter as tk

from random import shuffle
from tkinter.messagebox import showinfo, showerror


class MyButton(tk.Button):
    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super().__init__(master, width=3, font='Calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False


class MineSweeper:
    ROW = 5
    COLUMNS = 7
    MINES = 4

    COLORS = {
        0: 'white',
        1: 'blue',
        2: '#008200',
        3: '#FF0000',
        4: '#000084',
        5: '#840000',
        6: '#008284',
        7: '#840084',
        8: '#FF0000',
    }

    def __init__(self):
        self.window = tk.Tk()
        self.timer = None
        self.timer_label = None
        self.buttons = []

        for i in range(self.ROW + 2):
            temp = []
            for j in range(self.COLUMNS + 2):
                btn = MyButton(self.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind('<Button-3>', self.right_click)
                temp.append(btn)
            self.buttons.append(temp)

        self.IS_GAME_OVER = False
        self.IS_FIRST_CLICK = True

    def right_click(self, event):
        cur_btn = event.widget

        if self.IS_GAME_OVER:
            return

        if cur_btn['state'] == 'active':
            cur_btn['state'] = 'disabled'
            cur_btn['text'] = '?'
        elif cur_btn['text'] == '?':
            cur_btn['text'] = ''
            cur_btn['state'] = 'active'

    def click(self, clicked_btn: MyButton):
        if self.IS_GAME_OVER:
            return

        if self.IS_FIRST_CLICK:
            self.start_timer()
            self.insert_mines(clicked_btn.number)
            self.count_mines_in_buttons()
            self.print_buttons()
            self.IS_FIRST_CLICK = False

        if clicked_btn.is_mine:
            clicked_btn.config(text='*', background='red', disabledforeground='black')
            clicked_btn.is_open = True
            self.IS_GAME_OVER = True
            showinfo('Game over', 'You lose')
            self.open_all_buttons()
            self.stop_timer()
        else:
            color = self.COLORS.get(clicked_btn.count_bomb, 'black')
            if clicked_btn.count_bomb:
                clicked_btn.config(text=clicked_btn.count_bomb, disabledforeground=color)
                clicked_btn.is_open = True
            else:
                self.breadth_first_search(clicked_btn)

        clicked_btn.config(state='disabled')
        clicked_btn.config(relief=tk.SUNKEN)

        self.check_game_won()

    def check_game_won(self):
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttons[i][j]
                if not btn.is_mine and not btn.is_open:
                    return

        self.IS_GAME_OVER = True
        self.open_all_buttons()
        self.stop_timer()
        showinfo('Game over', 'Congratulations! You win')

    def breadth_first_search(self, btn: MyButton):
        queue = [btn]

        while queue:
            cur_btn = queue.pop()
            color = self.COLORS.get(cur_btn.count_bomb, 'black')
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            else:
                cur_btn.config(text='', disabledforeground=color)
            cur_btn.is_open = True
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.count_bomb == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= self.ROW \
                                and 1 <= next_btn.y <= self.COLUMNS and next_btn not in queue:
                            queue.append(next_btn)

    def reload(self):
        self.window.destroy()
        self.__init__()
        self.create_widgets()
        self.IS_FIRST_CLICK = True
        self.IS_GAME_OVER = False

    def create_settings_win(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.wm_title('Settings')

        tk.Label(win_settings, text='Row Count:').grid(row=0, column=0)
        row_entry = tk.Entry(win_settings)
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        row_entry.insert(0, str(self.ROW))

        tk.Label(win_settings, text='Column Count:').grid(row=1, column=0)
        column_entry = tk.Entry(win_settings)
        column_entry.grid(row=1, column=1, padx=20, pady=20)
        column_entry.insert(0, str(self.COLUMNS))

        tk.Label(win_settings, text='Mines Count:').grid(row=2, column=0)
        mines_entry = tk.Entry(win_settings)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)
        mines_entry.insert(0, str(self.MINES))

        save_btn = tk.Button(win_settings, text='Apply',
                             command=lambda: self.change_settings(row_entry, column_entry, mines_entry))
        save_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def change_settings(self, row: tk.Entry, column: tk.Entry, mines: tk.Entry):
        try:
            self.ROW = int(row.get())
            self.COLUMNS = int(column.get())
            self.MINES = int(mines.get())
        except ValueError:
            showerror('Error', 'Only integers are allowed for row, column, and mines.')
            return

        self.reload()

    def create_widgets(self):
        menu_bar = tk.Menu(self.window)
        self.window.config(menu=menu_bar)

        settings_menu = tk.Menu(menu_bar, tearoff=0)
        settings_menu.add_command(label='Play', command=self.reload)
        settings_menu.add_command(label='Settings', command=self.create_settings_win)
        settings_menu.add_command(label='Exit', command=self.window.destroy)
        menu_bar.add_cascade(label='File', menu=settings_menu)

        self.timer_label = tk.Label(self.window, text="Time: 0")
        self.timer_label.grid(row=self.ROW + 2, columnspan=self.COLUMNS + 2, padx=10, pady=10)

        count = 1
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, sticky='wens')
                count += 1

        for i in range(1, self.ROW + 1):
            self.window.rowconfigure(i, weight=1)

        for i in range(1, self.COLUMNS + 1):
            self.window.columnconfigure(i, weight=1)

    def open_all_buttons(self):
        for i in range(self.ROW + 2):
            for j in range(self.COLUMNS + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='*', background='red', disabledforeground='black')
                elif btn.count_bomb in self.COLORS:
                    color = self.COLORS.get(btn.count_bomb, 'black')
                    btn.config(text=btn.count_bomb, fg=color)

    def start(self):
        self.create_widgets()
        self.window.mainloop()

    def print_buttons(self):
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('B', end='')
                else:
                    print(btn.count_bomb, end='')
            print()

    def insert_mines(self, number: int):
        index_mines = self.get_mines_places(number)
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.number in index_mines:
                    btn.is_mine = True

    def count_mines_in_buttons(self):
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            if neighbour.is_mine:
                                count_bomb += 1
                btn.count_bomb = count_bomb

    @staticmethod
    def get_mines_places(exclude_number: int):
        indexes = list(range(1, MineSweeper.COLUMNS * MineSweeper.ROW + 1))
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[:MineSweeper.MINES]

    def start_timer(self):
        self.timer = time.time()
        self.update_timer()

    def update_timer(self):
        if self.IS_GAME_OVER:
            return

        elapsed_time = int(time.time() - self.timer)
        self.timer_label.config(text=f"Time: {elapsed_time}")
        self.timer_label.after(1000, self.update_timer)

    def stop_timer(self):
        self.timer_label.after_cancel(self.update_timer)


if __name__ == '__main__':
    game = MineSweeper()
    game.start()
