import tkinter as tk

def move_button():
    global dx, dy, x_pos, y_pos

    new_x = x_pos + dx * 10
    new_y = y_pos + dy * 10

    window_width = window.winfo_width()
    window_height = window.winfo_height()
    button_width = button.winfo_width()
    button_height = button.winfo_height()

    if new_x + button_width >= window_width:
        new_x = window_width - button_width
        dx = -1

    if new_x <= 0:
        new_x = 0
        dx = 1

    if new_y + button_height >= window_height:
        new_y = window_height - button_height
        dy = -1

    if new_y <= 0:
        new_y = 0
        dy = 1

    x_pos = new_x
    y_pos = new_y
    button.place(x=x_pos, y=y_pos)

window = tk.Tk()
window.title("Max Verstappen")
window.geometry("500x500")

dx = 1
dy = 1

button = tk.Button(window,text="Uwu",background="lightblue",)

button.place(x=245, y=245, width=100, height=100 )
x_pos = 245
y_pos = 245

button.config(command=move_button)
window.mainloop()
