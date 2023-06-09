import tkinter as tk

from tkinter import messagebox


ALL_OPERATIONS = '+-/*'
DEFAULT_VALUE = '0'


def add_digit(digit):
    value = calc.get()

    if value == DEFAULT_VALUE:
        value = value[1:]

    calc.delete(0, tk.END)
    calc.insert(0, value + digit)


def add_operation(operation):
    value = calc.get()

    if value[-1] in ALL_OPERATIONS:
        value = value[:-1]
    elif any(('+' in value, '-' in value, '/' in value, '*' in value)):
        calculate()
        value = calc.get()

    calc.delete(0, tk.END)
    calc.insert(0, value + operation)


def calculate():
    value = calc.get()

    if value[-1] in ALL_OPERATIONS:
        value = value + value[:-1]

    calc.delete(0, tk.END)

    try:
        calc.insert(0, eval(value))
    except (NameError, SyntaxError):
        messagebox.showinfo('Error', 'Only digit')
        calc.insert(0, DEFAULT_VALUE)
    except ZeroDivisionError:
        messagebox.showinfo('Error', 'cannot be divided by zero')
        calc.insert(0, DEFAULT_VALUE)


def clear():
    calc.delete(0, tk.END)
    calc.insert(0, DEFAULT_VALUE)


def make_digit_button(digit):
    return tk.Button(text=digit, bd=5, font=('Arial', 13), command=lambda: add_digit(digit))


def make_operation_button(operation):
    return tk.Button(text=operation, bd=5, font=('Arial', 13), fg='red', command=lambda: add_operation(operation))


def make_calc_button(operation):
    return tk.Button(text=operation, bd=5, font=('Arial', 13), command=calculate)


def make_clear_button(operation):
    return tk.Button(text=operation, bd=5, font=('Arial', 13), command=clear)


def press_key(event):
    if event.char.isdigit():
        add_digit(event.char)
    if event.char in ALL_OPERATIONS:
        add_operation(event.char)
    if event.char == '\r':
        calculate()


win = tk.Tk()
win.title('Calculator')
win.geometry('240x270+100+200')
win['bg'] = '#33ffe6'

photo = tk.PhotoImage(file='my.png')
win.iconphoto(False, photo)

win.bind('<Key>', press_key)

calc = tk.Entry(win, justify=tk.RIGHT, font=('Arial', 15), width=15)
calc.insert(0, DEFAULT_VALUE)
calc.grid(row=0, column=0, columnspan=4, sticky='we', padx=5)

make_digit_button('1').grid(row=1, column=0, sticky='wens', padx=5, pady=5)
make_digit_button('2').grid(row=1, column=1, sticky='wens', padx=5, pady=5)
make_digit_button('3').grid(row=1, column=2, sticky='wens', padx=5, pady=5)
make_digit_button('4').grid(row=2, column=0, sticky='wens', padx=5, pady=5)
make_digit_button('5').grid(row=2, column=1, sticky='wens', padx=5, pady=5)
make_digit_button('6').grid(row=2, column=2, sticky='wens', padx=5, pady=5)
make_digit_button('7').grid(row=3, column=0, sticky='wens', padx=5, pady=5)
make_digit_button('8').grid(row=3, column=1, sticky='wens', padx=5, pady=5)
make_digit_button('9').grid(row=3, column=2, sticky='wens', padx=5, pady=5)
make_digit_button('0').grid(row=4, column=0, sticky='wens', padx=5, pady=5)

make_operation_button('+').grid(row=1, column=3, sticky='wens', padx=5, pady=5)
make_operation_button('-').grid(row=2, column=3, sticky='wens', padx=5, pady=5)
make_operation_button('/').grid(row=3, column=3, sticky='wens', padx=5, pady=5)
make_operation_button('*').grid(row=4, column=3, sticky='wens', padx=5, pady=5)

make_calc_button('=').grid(row=4, column=2, sticky='wens', padx=5, pady=5)
make_clear_button('c').grid(row=4, column=1, sticky='wens', padx=5, pady=5)

win.grid_columnconfigure(0, minsize=60)
win.grid_columnconfigure(1, minsize=60)
win.grid_columnconfigure(2, minsize=60)
win.grid_columnconfigure(3, minsize=60)

win.grid_rowconfigure(1, minsize=60)
win.grid_rowconfigure(2, minsize=60)
win.grid_rowconfigure(3, minsize=60)
win.grid_rowconfigure(4, minsize=60)

if __name__ == '__main__':
    win.mainloop()
