import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import string
import secrets

# Tooltip class for help messages
class ToolTip(object):
    def __init__(self, widget, text):
        self.waittime = 400
        self.wraplength = 220
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.id = None
        self.tw = None

    def on_enter(self, event=None):
        self.schedule()

    def on_leave(self, event=None):
        self.unschedule()
        self.hide_tip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.show_tip)

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def show_tip(self, event=None):
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hide_tip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()

# Password strength calculation
def calculate_strength(password):
    length = len(password)
    categories = sum([
        any(c.isupper() for c in password),
        any(c.islower() for c in password),
        any(c.isdigit() for c in password),
        any(c in string.punctuation for c in password)
    ])
    if length >= 12 and categories == 4:
        return "Strong", "green"
    elif length >= 8 and categories >= 3:
        return "Medium", "orange"
    else:
        return "Weak", "red"

# Generate one password
def generate_one_password(length, chars):
    return ''.join(secrets.choice(chars) for _ in range(length))

# Main password generation handler
def generate_passwords(event=None):
    try:
        length = int(length_entry.get())
        if length <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a positive integer for password length.")
        return
    try:
        count = int(count_entry.get())
        if count < 1 or count > 50:
            messagebox.showerror("Invalid Input", "You can generate 1 to 50 passwords at once.")
            return
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number of passwords to generate.")
        return

    chars = ""
    if var_upper.get():
        chars += string.ascii_uppercase
    if var_lower.get():
        chars += string.ascii_lowercase
    if var_digits.get():
        chars += string.digits
    if var_symbols.get():
        chars += string.punctuation

    if not chars:
        messagebox.showwarning("No Character Set", "Select at least one character set.")
        return

    password_list = []
    for _ in range(count):
        pwd = generate_one_password(length, chars)
        password_list.append(pwd)
        password_history.append(pwd)
    result_var.set(password_list[0])  # Show the first password
    update_strength_label(password_list[0])
    update_history()
    if count > 1:
        messagebox.showinfo("Passwords Generated", f"{count} passwords generated.\nSee history for all.")

def update_strength_label(password):
    if not password:
        strength_var.set("")
        strength_label.config(fg="black")
        return
    strength, color = calculate_strength(password)
    strength_var.set(f"Strength: {strength}")
    strength_label.config(fg=color)

def copy_to_clipboard(event=None):
    pwd = result_var.get()
    if pwd:
        root.clipboard_clear()
        root.clipboard_append(pwd)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

def clear_fields():
    length_entry.delete(0, tk.END)
    length_entry.insert(0, "12")
    count_entry.delete(0, tk.END)
    count_entry.insert(0, "1")
    result_var.set("")
    strength_var.set("")
    var_upper.set(True)
    var_lower.set(True)
    var_digits.set(True)
    var_symbols.set(False)
    show_var.set(False)
    result_entry.config(show="*")
    history_listbox.selection_clear(0, tk.END)

def toggle_show_password():
    if show_var.get():
        result_entry.config(show="")
    else:
        result_entry.config(show="*")

def update_history():
    history_listbox.delete(0, tk.END)
    for pwd in reversed(password_history):
        history_listbox.insert(tk.END, pwd)

def on_history_select(event):
    if not history_listbox.curselection():
        return
    pwd = history_listbox.get(history_listbox.curselection())
    result_var.set(pwd)
    update_strength_label(pwd)

def export_passwords():
    if not password_history:
        messagebox.showwarning("Nothing to Export", "No passwords generated yet.")
        return
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file", "*.txt")])
    if filepath:
        try:
            with open(filepath, "w") as f:
                for pwd in password_history:
                    f.write(pwd + "\n")
            messagebox.showinfo("Exported", f"Passwords saved to {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

# --- Main GUI setup ---
root = tk.Tk()
root.title("Advanced Password Generator")
root.resizable(False, False)
style = ttk.Style(root)
style.configure("TButton", padding=6)

password_history = []

# Layout
frame = tk.Frame(root, padx=12, pady=10)
frame.grid(row=0, column=0)

tk.Label(frame, text="Password Length:").grid(row=0, column=0, sticky="e")
length_entry = tk.Entry(frame, width=6)
length_entry.insert(0, "12")
length_entry.grid(row=0, column=1, sticky="w")
ToolTip(length_entry, "Number of characters in each password")

tk.Label(frame, text="How Many:").grid(row=0, column=2, sticky="e")
count_entry = tk.Entry(frame, width=4)
count_entry.insert(0, "1")
count_entry.grid(row=0, column=3, sticky="w")
ToolTip(count_entry, "How many passwords to generate at once (max 50)")

tk.Label(frame, text="Include:").grid(row=1, column=0, sticky="e")
checks_frame = tk.Frame(frame)
checks_frame.grid(row=1, column=1, columnspan=3, sticky="w")
var_upper = tk.BooleanVar(value=True)
var_lower = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=False)
tk.Checkbutton(checks_frame, text="Uppercase", variable=var_upper).grid(row=0, column=0)
tk.Checkbutton(checks_frame, text="Lowercase", variable=var_lower).grid(row=0, column=1)
tk.Checkbutton(checks_frame, text="Digits", variable=var_digits).grid(row=0, column=2)
tk.Checkbutton(checks_frame, text="Symbols", variable=var_symbols).grid(row=0, column=3)

tk.Button(frame, text="Generate", command=generate_passwords, width=12).grid(row=2, column=0, columnspan=4, pady=8)
ToolTip(frame.grid_slaves(row=2, column=0)[0], "Generate password(s) (Ctrl+G)")

result_var = tk.StringVar()
result_entry = tk.Entry(frame, textvariable=result_var, width=32, font=("Arial", 12), justify="center", show="*")
result_entry.grid(row=3, column=0, columnspan=4, pady=3)

show_var = tk.BooleanVar(value=False)
tk.Checkbutton(frame, text="Show", variable=show_var, command=toggle_show_password).grid(row=4, column=0, columnspan=1, sticky="w")
ToolTip(frame.grid_slaves(row=4, column=0)[0], "Show/hide password characters")

strength_var = tk.StringVar()
strength_label = tk.Label(frame, textvariable=strength_var, font=("Arial", 10, "bold"))
strength_label.grid(row=4, column=1, columnspan=3, sticky="w")

button_frame = tk.Frame(frame)
button_frame.grid(row=5, column=0, columnspan=4, pady=4)
btn_copy = tk.Button(button_frame, text="Copy", command=copy_to_clipboard, width=10)
btn_copy.grid(row=0, column=0, padx=3)
ToolTip(btn_copy, "Copy password (Ctrl+C)")
btn_clear = tk.Button(button_frame, text="Clear", command=clear_fields, width=10)
btn_clear.grid(row=0, column=1, padx=3)
ToolTip(btn_clear, "Clear all fields and result")
btn_export = tk.Button(button_frame, text="Export", command=export_passwords, width=10)
btn_export.grid(row=0, column=2, padx=3)
ToolTip(btn_export, "Export all generated passwords to a file")

# History section
history_frame = tk.LabelFrame(root, text="Password History (Session)", padx=6, pady=4)
history_frame.grid(row=0, column=1, padx=6, pady=8, sticky="ns")
history_listbox = tk.Listbox(history_frame, width=32, height=13)
history_listbox.pack(side="left", fill="y")
scrollbar = tk.Scrollbar(history_frame, orient="vertical", command=history_listbox.yview)
scrollbar.pack(side="right", fill="y")
history_listbox.config(yscrollcommand=scrollbar.set)
history_listbox.bind("<<ListboxSelect>>", on_history_select)
ToolTip(history_listbox, "Click to recall a previous password")

# Keyboard shortcuts
root.bind('<Control-g>', generate_passwords)
root.bind('<Control-G>', generate_passwords)
root.bind('<Control-c>', copy_to_clipboard)
root.bind('<Control-C>', copy_to_clipboard)

root.mainloop()