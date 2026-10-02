from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
root = tk.Tk()
root.title("Капча по практике")
root.geometry("640x480")
root.configure(bg="#f9f1e5")

label=tk.Label(root, text="Привет! Это капча!")
label.pack()

entry = tk.Entry(root)
entry.pack()
text = entry.get()
entry.delete(0, "end")
entry.insert(0, "admin")
btn = tk.Button(root, text="Войти",

command=lambda: 
    tk.try_login(tk.entry_login.get(), tk.entry_pass.get()))

messagebox.showinfo("Готово", "Пользователь добавлен")
messagebox.showwarning("Внимание", "Заполните все поля")
messagebox.showerror("Ошибка", "Неверный логин или пароль")
if messagebox.askyesno("Выход", "Выйти из программы?"):
    root.destroy()

root.mainloop()
