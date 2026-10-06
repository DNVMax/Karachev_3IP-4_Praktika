import os
import random
import tkinter as tk
from tkinter import ttk, messagebox

from models import (all_users, find_user, user_by_login, login_exists, add_user, update_user, delete_user, register_fail, unlock_user, reset_attempts)

current_user = None
current_edit = None
entry_login = None

bg = "#f9f1e5"
field_bg = "#ffffff"
field_fg = "#22262b"

font_title = ("Arial", 16, "bold")
font_label = ("Arial", 11, "bold")
font_button = ("Arial", 12, "bold")

root = tk.Tk
root.title("Учебное приложение и капча")
root.geometry("720x640")
root.configure(bg=bg)

container = tk.Frame(root, bg=bg)
container.pack(fill="both", expand=True, padx=20, pady=20)

def clear_screen():
    for w in container.winfo_children():
        w.destroy()

def make_title(text):
    return tk.Label(container, text=text, bg=bg, fg=field_fg, font=font_title)

def make_label(text):
    return tk.Label(container, text=text, bg=bg, fg=field_fg, font=font_label, anchor="w")

def make_entry(password=False):
    entry = tk.Entry(container, font=font_button, bg=field_bg, fg=field_fg, insertbackground=field_fg, relief="solid", borderwidth=1)
    if password:
        entry.configure(show="*")
    return entry

def make_button(text, command, parent=None):
    host = container if parent is None else parent
    return tk.Button(host, text=text, command=command, font=font_button)

base_dir = os.path.dirname(os.path.abspath(__file__))
captcha_dir = os.path.join(base_dir, "captcha")
correct_order = [1, 2, 3, 4]
piece_size = 90

captcha_images={}
captcha_empty=None
captcha_host=None
captcha_slots=[]
captcha_piece_buttons={}
captcha_placed=[]
captcha_shuffled=[]
captcha_passed=False
captcha_fails=0

def load_captcha_images():
    global captcha_images, captcha_empty
    captcha_images={}
    for piece in (1, 2, 3, 4):
        path = os.path.join(captcha_dir, "piece_" + str(piece) + ".png")
        captcha_images[piece] = tk.PhotoImage(file=path).subsample(8)
    captcha_empty=tk.PhotoImage(width=piece_size, height=piece_size)
    

def build_captcha(host):
    global captcha_slots, captcha_piece_buttons, captcha_placed, captcha_shuffled
    for w in host.winfo_children():
        w.destroy
    captcha_slots=[]
    captcha_piece_buttons={}
    captcha_placed=[]
    captcha_shuffled=correct_order[:]
    random.shuffle(captcha_shuffled)
    while captcha_shuffled == correct_order:
        random.shuffle(captcha_shuffled)
    tk.Label(host, text="Соберите картинку: кликайте фрагментыпо порядку", bg=bg, fg=field_fg, font=font_label, anchor="w").pack(fill="x")
    board=tk.Frame(host, bg=bg)
    board.pack(pady=(6, 6))
    for index in range(4):
        slot = tk.Label(board, image=captcha_empty, bg=field_bg, relief="solid", borderwidth=1)
        slot.grid(row=index//2, column=index%2)
        captcha_slots.append(slot)
    pieces=tk.Frame(host, bg=bg)
    pieces.pack(pady=(0, 6))
    for piece in captcha_shuffled:
        btn=tk.Button(pieces, image=captcha_images[piece], relief="solid", borderwidth=1, cursor="hand2", command=lambda p=piece: place_piece(p))
        btn.pack(side="left", padx=3)
        captcha_piece_buttons[piece]=btn
        make_button("Сбросить капчу", new_captcha_round, parent=host).pack(ipadx=16, ipady=3)

def new_captcha_round():
    global captcha_passed
    captcha_passed=False
    build_captcha(captcha_host)

def place_piece(piece):
    if captcha_passed or len(captcha_placed) >= 4:
        return
    captcha_placed.append(piece)
    captcha_piece_buttons[piece].configure(state="disabled")
    captcha_slots[len(captcha_placed) - 1].configure(image=captcha_images[piece])
    if len(captcha_placed) == 4:
        check_captcha()
    
    def check_captcha():
        global captcha_passed, captcha_fails
        login = entry_login.get().strip()
        if captcha_placed == correct_order:
            captcha_passed = True
            messagebox.showinfo("Капча", "Пазл собран верно! Можно нажать 'войти'")
            return
        if login_exists(login):
            became_locked=register_fail(login)
            if became_locked:
                messagebox.showerror("Блокировка", "Вы заблокированы, обратитесь к администратору.")
            else:
                messagebox.showerror("Капча", "Пазл собран неверно, опробуйте ещё. Ориентируйтесь на продолжение рисунка.")
        else:
            captcha_fails = captcha_fails +1
            if captcha_fails >=3:
                messagebox.showerror("Блокировка", "Третья неудачная капча подряд!", "При входе учётная записб будет заблокирована.")
            else:
                messagebox.showerror("Капча", "Пазл собран неверно, опробуйте ещё. Ориентируйтесь на продолжение рисунка.")
        new_captcha_round()

def try_login(login, password):
    global current_user, captcha_fails
    login = login.strip()
    password = password.strip()
    if not login or not password:
        messagebox.showwarning("Внимание", "Заполните логин и пароль")
        return
    if captcha_fails>0:
        if login_exists(login):
            for _ in range(captcha_fails):
                register_fail(login)
        captcha_fails = 0
    if not captcha_passed:
        messagebox.showwarning("Капча", "Сначала соберите капчу, затем нажмите 'Войти'")
        return
    user = find_user(login, password)
    if user is None:
        became_locked = register_fail(login)
        if became_locked:
            messagebox.showerror("Блокиовка", "Вы заблокированы, обратитесь к администратору")
        else:
            messagebox.showerror("Ошибка входа", "Вы ввели неверный логин или пароль.", "Пожалуйста проверьте ещё раз введённые данные")
        return
    if user["locked"]:
        messagebox.showerror("Блокировка", "Вы заблокированы, обратитесь к администратору")
        return
    reset_attempts(login)
    current_user=user
    messagebox.showinfo("Авторизация", "Вы успешно авторизовались")
    new_captcha_round()
    if user["role"] == "Адмиистратор":
        open_admin()
    else:
        open_user()

def toggle_password_visibility(entry_pass, var):
    if var.get():
        entry_pass.configure(show="")
    else:
        entry_pass.configure(show="*")

def open_login():
    global entry_login, captcha_host
    clear_screen()
    make_title("Вход в систему").pack(pady=(0, 10))

    make_label("Логин").pack(fill="x")
    entry_login=make_entry()
    entry_login.pack(fill="x", pady=(0, 8))
    make_label("Пароль").pack(fill="x")
    entry_pass = make_entry(password=True)
    entry_pass.pack(fill="x", pady=(0, 4))

    show_var = tk.BooleanVar(value=False)
    tk.Checkbutton(container, text="Показать пароль", variable=show_var, command=lambda: toggle_password_visibility(entry_pass, show_var), bg=bg, fg=field_fg, activebackground=bg, activeforeground=field_fg, selectcolor=field_bg, font=font_label, anchor="w").pack(fill="x", pady=(0,10))

    captcha_host = tk.Frame(container, bg=bg)
    captcha_host.pack(fill="x", pady=(0,10))
    build_captcha(captcha_host)

    make_button("Войти", lambda: try_login(entry_login.get(), entry_pass.get()).pack(fill="x", ipady=6))

def open_user():
    clear_screen()
    make_title("Рабочее место пользователя").pack(pady=(0, 10))
    make_label("Вы вошли как:" + current_user["login"]).pack(fill="x", pady=(0, 20))
    make_label("Роль:" + current_user["role"]).pack(fill="x", pady=(0, 20))
    make_button("Выйти", open_login).pack(ipadx=24, ipady=4)

def open_edit_user(login):
    global CURRENT_EDIT
    user = user_by_login(login)
    if user is None:
        messagebox.showwarning("Внимание", "Сначала выберите строку в таблице.")
        return
    CURRENT_EDIT = login
    clear_screen()
    make_title("Изменение пользователя").pack(pady=(0, 10))
    make_label("Логин: " + login).pack(fill="x", pady=(0, 10))

    make_label("ФИО").pack(fill="x")
    e_name = make_entry()
    e_name.insert(0, user["full_name"])
    e_name.pack(fill="x", pady=(0, 8))

    make_label("Пароль").pack(fill="x")
    e_pass = make_entry()
    e_pass.insert(0, user["password"])
    e_pass.pack(fill="x", pady=(0, 8))

    make_label("Роль").pack(fill="x")
    combo_role = ttk.Combobox(container, values=["Пользователь", "Администратор"], state="readonly", font=font_button)
    combo_role.set(user["role"])
    combo_role.pack(fill="x", pady=(0, 10))

    lock_text="Заблокирован: да" if user["locked"] else "Заблокирован: нет"
    lock_label=make_label(lock_text)
    lock_label.pack(fill="x", pady=(0, 10))

    def refresh_lock():
        current = user_by_login(current_edit)
        lock_label.configure(text="Заблокирован: да" if current["locked"] else "Заблокирован: нет")
    
    def do_unlock():
        unlock_user(current_edit)
        refresh_lock()
        messagebox.showinfo("Готово", +current_edit + "Разблокирован")
    
    def do_save():
        name = e_name.get().strip()
        password = e_pass.get().strip()
        if not name or not password:
            messagebox.showwarning("Внимание", "ФИО и пароль не могут быть пустыми.")
            return
        update_user(current_edit, password, combo_role.get(), name)
        messagebox.showinfo("Готово", "Данные пользователя сохранены")
        open_admin()

def open_admin():
    clear_screen()
    make_title("Панель администраора").pack(pady=(0, 5))
    make_label("Вы вошли как:" + current_user["login"]).pack(fill="x", pady=(0, 10))

    tree = ttk.Treeview(container,
                         columns=("login", "full_name", "role", "locked"),
                         show="headings", height=8)
    tree.heading("login", text="Логин")
    tree.heading("full_name", text="ФИО")   
    tree.heading("role", text="Роль")
    tree.heading("locked", text="Заблокирован")
    tree.column("login", width=120, anchor="w")
    tree.column("full_name", width=180, anchor="w")
    tree.column("role", width=130, anchor="w")
    tree.column("locked", width=110, anchor="center")
    for u in all_users():
        tree.insert("", "end", values=(u["login"], u["full_name"], u["role"], "да" if u["locked"] else "нет"))
    tree.pack(fill="both", expand=True, pady=(0, 10))



