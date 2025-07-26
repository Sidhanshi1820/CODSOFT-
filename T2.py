import tkinter as tk
from tkinter import messagebox as msg, simpledialog, ttk
import os
import json
from datetime import datetime, date
import re

# Fallback for colored print if termcolor not installed (for console prints)
try:
    from termcolor import colored
except ImportError:
    def colored(text, color=None):
        return text

print(colored('Hello World!', 'red'))
print(colored('Success!', 'green'))

DATA_FILE = "todo.json"
PRIORITIES = ["Low", "Medium", "High", "Critical"]
CATEGORIES = ["Personal", "Work", "Shopping", "Health", "Education", "Finance", "Other"]
PRIORITY_COLORS = {
    "Low": "#28a745",
    "Medium": "#ffc107", 
    "High": "#fd7e14",
    "Critical": "#dc3545"
}

class ModernTodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # Modern window configuration
        self.configure_window()
        
        # Data
        self.tasks = []
        self.load_tasks()
        self.sort_by = "date"
        self.show_completed = True

        # Configure modern styling
        self.configure_styles()
        
        # Create modern icon
        self.iconphoto(True, self.create_app_icon())
        
        # UI
        self.create_app_heading()
        self.give_separation_line()
        self.item_input_frame = self.create_input_frame()
        self.item_entry_box = self.create_new_item_entry_box()
        self.priority_var = tk.StringVar(value="Medium")
        self.category_var = tk.StringVar(value="Personal")
        self.create_priority_menu()
        self.create_category_menu()
        self.due_entry = self.create_due_entry()
        self.create_add_button()
        self.create_search_and_sort_bar()
        self.list_display_frame = self.create_display_frame()
        self.todo_display_listbox = self.create_todo_list_box()
        self.listbox_scrollbar = self.add_listbox_scrollbar()
        self.show_scrollbar()
        self.operation_button_frame = self.create_operation_frame()

        # Enhanced icons with fallback text
        self.setup_icons()

        # Enhanced buttons
        self.create_enhanced_buttons()

        # Status bar
        self.create_status_bar()
        
        # Keyboard shortcuts
        self.setup_keyboard_shortcuts()

        # Auto-save feature
        self.auto_save_timer()

        # Initial display
        self.listbox_load()
        self.update_status_bar()

    def configure_window(self):
        """Configure modern window appearance and behavior"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        app_width = 1200
        app_height = 950
        set_x = int((screen_width / 2) - (app_width / 2))
        set_y = int((screen_height / 2) - (app_height / 2))
        self.geometry(f'{app_width}x{app_height}+{set_x}+{set_y}')
        self.title("TodoList Manager")
        self.resizable(True, True)
        self.minsize(800, 600)
        
        # Modern color scheme
        self.configure(bg="#f8f9fa")
        
    def configure_styles(self):
        """Configure modern TTK styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure custom styles
        self.style.configure('Title.TLabel', 
                           font=('Segoe UI', 28, 'bold'),
                           foreground='#2c3e50',
                           background='#f8f9fa')
        
    def create_app_icon(self):
        """Create a simple app icon"""
        icon = tk.PhotoImage(width=32, height=32)
        icon.put("#2c3e50", to=(0, 0, 32, 32))
        icon.put("#3498db", to=(8, 8, 24, 24))
        return icon

    # ---- UI Design ----

    def create_app_heading(self):
        heading_frame = tk.Frame(self, bg="#2c3e50", height=80)
        heading_frame.pack(fill=tk.X)
        heading_frame.pack_propagate(False)
        
        heading = tk.Label(heading_frame, 
                          text="📝 TodoList Manager Pro", 
                          font=('Segoe UI', 32, 'bold'), 
                          fg="#ecf0f1", 
                          bg="#2c3e50")
        heading.pack(expand=True)
        
        # Add subtitle
        subtitle = tk.Label(heading_frame,
                           text="Advanced Task Management System",
                           font=('Segoe UI', 12),
                           fg="#bdc3c7",
                           bg="#2c3e50")
        subtitle.pack()

    def give_separation_line(self):
        frame = tk.Frame(self, bg="#3498db", height=3)
        frame.pack(fill=tk.X)

    def create_input_frame(self):
        frame = tk.Frame(self, bg="#ecf0f1", height=120, padx=20, pady=15)
        frame.pack(fill=tk.X)
        frame.pack_propagate(False)
        
        # Add input label
        input_label = tk.Label(frame, 
                              text="Add New Task:", 
                              font=('Segoe UI', 14, 'bold'),
                              bg="#ecf0f1",
                              fg="#2c3e50")
        input_label.pack(anchor='w', pady=(0, 5))
        
        # Create input row frame
        self.input_row = tk.Frame(frame, bg="#ecf0f1")
        self.input_row.pack(fill=tk.X, pady=5)
        
        return frame

    def create_new_item_entry_box(self):
        entry = tk.Entry(self.input_row, 
                        width=40, 
                        borderwidth=2, 
                        relief='solid',
                        font=('Segoe UI', 14),
                        bg="#ffffff",
                        fg="#2c3e50")
        entry.pack(side=tk.LEFT, padx=(0,10), ipady=8)
        
        # Add placeholder text functionality
        self.add_placeholder(entry, "Enter your task here...")
        return entry
    
    def add_placeholder(self, entry, placeholder_text):
        """Add placeholder text to entry widget"""
        entry.insert(0, placeholder_text)
        entry.config(fg='#7f8c8d')
        
        def on_focus_in(event):
            if entry.get() == placeholder_text:
                entry.delete(0, tk.END)
                entry.config(fg='#2c3e50')
        
        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder_text)
                entry.config(fg='#7f8c8d')
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)

    def create_priority_menu(self):
        tk.Label(self.input_row, text="Priority:", font=('Segoe UI', 12), bg="#ecf0f1").pack(side=tk.LEFT, padx=(0,5))
        menu = ttk.Combobox(self.input_row, textvariable=self.priority_var, values=PRIORITIES, state="readonly", width=8)
        menu.pack(side=tk.LEFT, padx=(0,10))
        return menu
    
    def create_category_menu(self):
        tk.Label(self.input_row, text="Category:", font=('Segoe UI', 12), bg="#ecf0f1").pack(side=tk.LEFT, padx=(0,5))
        menu = ttk.Combobox(self.input_row, textvariable=self.category_var, values=CATEGORIES, state="readonly", width=10)
        menu.pack(side=tk.LEFT, padx=(0,10))
        return menu

    def create_due_entry(self):
        tk.Label(self.input_row, text="Due Date:", font=('Segoe UI', 12), bg="#ecf0f1").pack(side=tk.LEFT, padx=(0,5))
        due = tk.Entry(self.input_row, 
                      width=12, 
                      borderwidth=2, 
                      relief='solid',
                      font=('Segoe UI', 12),
                      bg="#ffffff")
        due.pack(side=tk.LEFT, padx=(0,10), ipady=4)
        self.add_placeholder(due, "YYYY-MM-DD")
        
        # Add date validation on key release
        due.bind('<KeyRelease>', self.validate_date)
        return due
    
    def validate_date(self, event):
        """Real-time date validation"""
        date_text = event.widget.get()
        if date_text and date_text != "YYYY-MM-DD":
            try:
                datetime.strptime(date_text, "%Y-%m-%d")
                event.widget.config(bg="#d4edda")  # Light green for valid
            except ValueError:
                if len(date_text) >= 10:  # Only show red if they've typed enough
                    event.widget.config(bg="#f8d7da")  # Light red for invalid
                else:
                    event.widget.config(bg="#ffffff")  # Default
        else:
            event.widget.config(bg="#ffffff")

    def create_add_button(self):
        button = tk.Button(self.input_row, 
                          text="➕ Add Task", 
                          width=15, 
                          borderwidth=0, 
                          font=('Segoe UI', 12, 'bold'), 
                          bg="#27ae60", 
                          fg="#ffffff",
                          cursor="hand2",
                          relief='flat',
                          command=self.add_item)
        button.pack(side=tk.LEFT, padx=5, ipady=8)
        
        # Add hover effect
        def on_enter(e):
            button.config(bg="#2ecc71")
        def on_leave(e):
            button.config(bg="#27ae60")
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def create_search_and_sort_bar(self):
        frame = tk.Frame(self, bg="#34495e", pady=10)
        frame.pack(fill=tk.X)
        
        # Left side - Search and filters
        left_frame = tk.Frame(frame, bg="#34495e")
        left_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(left_frame, text="🔍 Search:", 
                font=("Segoe UI", 12, 'bold'), 
                bg="#34495e", 
                fg="#ecf0f1").pack(side=tk.LEFT, padx=(0,5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.listbox_load())
        search_entry = tk.Entry(left_frame, 
                               textvariable=self.search_var, 
                               font=("Segoe UI", 12), 
                               width=25,
                               bg="#ffffff",
                               relief='solid',
                               borderwidth=1)
        search_entry.pack(side=tk.LEFT, padx=(0,15), ipady=4)
        self.add_placeholder(search_entry, "Search tasks...")
        
        # Right side - Sort and show options
        right_frame = tk.Frame(frame, bg="#34495e")
        right_frame.pack(side=tk.RIGHT, padx=20)
        
        tk.Label(right_frame, text="📊 Sort by:", 
                font=("Segoe UI", 12, 'bold'), 
                bg="#34495e", 
                fg="#ecf0f1").pack(side=tk.LEFT, padx=(0,5))
        
        self.sort_var = tk.StringVar(value="Due Date")
        sort_menu = ttk.Combobox(right_frame, 
                                textvariable=self.sort_var, 
                                values=["Due Date", "Priority", "Category", "Created", "Completed"],
                                state="readonly",
                                width=12)
        sort_menu.pack(side=tk.LEFT, padx=(0,15))
        sort_menu.bind('<<ComboboxSelected>>', lambda _: self.update_sort())
        
        self.show_completed_var = tk.BooleanVar(value=True)
        completed_check = tk.Checkbutton(right_frame, 
                                       text="✅ Show Completed", 
                                       variable=self.show_completed_var, 
                                       bg="#34495e",
                                       fg="#ecf0f1",
                                       selectcolor="#34495e",
                                       activebackground="#34495e",
                                       activeforeground="#ecf0f1",
                                       font=("Segoe UI", 11),
                                       command=self.listbox_load)
        completed_check.pack(side=tk.LEFT)
        
        # Add task counter
        self.task_counter_label = tk.Label(right_frame,
                                         text="",
                                         font=("Segoe UI", 10),
                                         bg="#34495e",
                                         fg="#bdc3c7")
        self.task_counter_label.pack(side=tk.LEFT, padx=(15,0))

    def create_display_frame(self):
        frame = tk.Frame(self, bg="#ecf0f1", padx=20, pady=15)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Add frame title
        frame_title = tk.Label(frame,
                              text="📋 Your Tasks",
                              font=("Segoe UI", 16, 'bold'),
                              bg="#ecf0f1",
                              fg="#2c3e50")
        frame_title.pack(anchor='w', pady=(0,10))
        
        return frame

    def create_todo_list_box(self):
        # Create frame for listbox with modern styling
        listbox_frame = tk.Frame(self.list_display_frame, bg="#ffffff", relief='solid', borderwidth=1)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        listbox = tk.Listbox(listbox_frame, 
                           font=('Segoe UI', 13), 
                           bg="#ffffff", 
                           fg="#2c3e50", 
                           selectbackground="#3498db", 
                           selectforeground="#ffffff",
                           activestyle=tk.NONE, 
                           cursor="hand2",
                           borderwidth=0,
                           highlightthickness=0)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add double-click to edit
        listbox.bind('<Double-Button-1>', lambda e: self.edit_task())
        
        return listbox

    def add_listbox_scrollbar(self):
        scrollbar = ttk.Scrollbar(self.list_display_frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,10), pady=10)
        return scrollbar

    def show_scrollbar(self):
        self.todo_display_listbox.config(yscrollcommand=self.listbox_scrollbar.set)
        self.listbox_scrollbar.config(command=self.todo_display_listbox.yview)

    def create_operation_frame(self):
        frame = tk.Frame(self, bg="#2c3e50", height=80)
        frame.pack(fill=tk.X)
        frame.pack_propagate(False)
        
        # Add operations title
        ops_title = tk.Label(frame,
                           text="🛠 Task Operations",
                           font=("Segoe UI", 14, 'bold'),
                           bg="#2c3e50",
                           fg="#ecf0f1")
        ops_title.pack(pady=(10,5))
        
        # Button container
        self.button_container = tk.Frame(frame, bg="#2c3e50")
        self.button_container.pack(expand=True)
        
        return frame

    def setup_icons(self):
        """Setup modern icons with text fallbacks"""
        self.icons = {
            'edit': '✏',
            'delete': '🗑', 
            'complete': '✅',
            'incomplete': '↩',
            'clear': '🧹',
            'clear_completed': '🗑✅'
        }

    def create_enhanced_buttons(self):
        """Create modern styled buttons with hover effects"""
        buttons_config = [
            ("edit", "✏ Edit", "#3498db", self.edit_task),
            ("complete", "✅ Complete", "#27ae60", self.cross_item),
            ("incomplete", "↩ Reopen", "#f39c12", self.uncross_item),
            ("delete", "🗑 Delete", "#e74c3c", self.delete_crossed_item),
            ("clear", "🧹 Clear All", "#95a5a6", self.clear_list),
            ("clear_completed", "🗑✅ Clear Done", "#e67e22", self.clear_completed)
        ]
        
        for btn_id, text, color, command in buttons_config:
            btn = tk.Button(self.button_container,
                          text=text,
                          font=("Segoe UI", 11, 'bold'),
                          bg=color,
                          fg="#ffffff",
                          relief='flat',
                          borderwidth=0,
                          cursor="hand2",
                          command=command,
                          width=12)
            btn.pack(side=tk.LEFT, padx=8, pady=10, ipady=8)
            
            # Add hover effects
            self.add_button_hover_effect(btn, color)

    def add_button_hover_effect(self, button, original_color):
        """Add hover effect to buttons"""
        def on_enter(e):
            # Darken color on hover
            darker_color = self.darken_color(original_color)
            button.config(bg=darker_color)
            
        def on_leave(e):
            button.config(bg=original_color)
            
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def darken_color(self, hex_color):
        """Darken a hex color"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(max(0, int(c * 0.8)) for c in rgb)
        return f"#{darker_rgb[0]:02x}{darker_rgb[1]:02x}{darker_rgb[2]:02x}"

    def create_status_bar(self):
        """Create a modern status bar"""
        self.status_frame = tk.Frame(self, bg="#34495e", height=30)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(self.status_frame,
                                   text="Ready",
                                   font=("Segoe UI", 10),
                                   bg="#34495e",
                                   fg="#ecf0f1")
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Add current time
        self.time_label = tk.Label(self.status_frame,
                                 text="",
                                 font=("Segoe UI", 10),
                                 bg="#34495e",
                                 fg="#bdc3c7")
        self.time_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
        self.update_time()

    def update_time(self):
        """Update the time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.after(1000, self.update_time)

    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.bind('<Control-n>', lambda e: self.item_entry_box.focus())
        self.bind('<Control-s>', lambda e: self.save_tasks())
        self.bind('<Delete>', lambda e: self.delete_crossed_item())
        self.bind('<F2>', lambda e: self.edit_task())
        self.bind('<space>', lambda e: self.cross_item())
        self.bind('<Control-f>', lambda e: self.search_var.set('') or self.focus_search())
        
        # Bind Enter key to add task when in entry box
        self.item_entry_box.bind('<Return>', lambda e: self.add_item())

    def focus_search(self):
        """Focus on search box"""
        for widget in self.search_frame.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.focus()
                break

    def auto_save_timer(self):
        """Auto-save every 30 seconds"""
        self.save_tasks()
        self.after(30000, self.auto_save_timer)

    def update_status_bar(self):
        """Update the status bar with task statistics"""
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks if t.get("crossed", False)])
        pending_tasks = total_tasks - completed_tasks
        overdue_tasks = self.count_overdue_tasks()
        
        status_text = f"Total: {total_tasks} | Pending: {pending_tasks} | Completed: {completed_tasks}"
        if overdue_tasks > 0:
            status_text += f" | ⚠ Overdue: {overdue_tasks}"
            
        self.status_label.config(text=status_text)
        
        # Update task counter in search bar
        if hasattr(self, 'task_counter_label'):
            self.task_counter_label.config(text=f"📊 {total_tasks} tasks")

    def count_overdue_tasks(self):
        """Count overdue tasks"""
        today = date.today().strftime("%Y-%m-%d")
        overdue = 0
        for task in self.tasks:
            if (not task.get("crossed", False) and 
                task.get("due") and 
                task.get("due") < today):
                overdue += 1
        return overdue

    # ---- Data Handling ----

    def load_tasks(self):
        """Load tasks from JSON file with error handling"""
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump([], f)
        try:
            with open(DATA_FILE, "r") as f:
                self.tasks = json.load(f)
                # Validate and update task structure for backward compatibility
                self.validate_task_structure()
        except Exception as e:
            print(colored(f"Error loading tasks: {e}", "red"))
            self.tasks = []

    def validate_task_structure(self):
        """Ensure all tasks have required fields"""
        for task in self.tasks:
            # Add missing fields with defaults
            if "category" not in task:
                task["category"] = "Other"
            if "created" not in task:
                task["created"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if "priority" not in task:
                task["priority"] = "Medium"
            if "due" not in task:
                task["due"] = ""
            if "crossed" not in task:
                task["crossed"] = False
            if "notes" not in task:
                task["notes"] = ""

    def save_tasks(self):
        """Save tasks to JSON file with backup"""
        try:
            # Create backup before saving
            if os.path.exists(DATA_FILE):
                backup_file = f"{DATA_FILE}.backup"
                with open(DATA_FILE, "r") as f:
                    backup_data = f.read()
                with open(backup_file, "w") as f:
                    f.write(backup_data)
            
            # Save current tasks
            with open(DATA_FILE, "w") as f:
                json.dump(self.tasks, f, indent=2)
                
        except Exception as e:
            print(colored(f"Error saving tasks: {e}", "red"))
            msg.showerror("Save Error", f"Could not save tasks: {e}")

    def update_sort(self):
        """Update sort criteria and refresh display"""
        mapping = {
            "Due Date": "date",
            "Priority": "priority", 
            "Category": "category",
            "Created": "created",
            "Completed": "crossed"
        }
        self.sort_by = mapping[self.sort_var.get()]
        self.listbox_load()

    def export_tasks(self):
        """Export tasks to different formats"""
        try:
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", ".json"), ("Text files", ".txt"), ("CSV files", "*.csv")]
            )
            if file_path:
                if file_path.endswith('.json'):
                    with open(file_path, 'w') as f:
                        json.dump(self.tasks, f, indent=2)
                elif file_path.endswith('.txt'):
                    with open(file_path, 'w') as f:
                        for task in self.tasks:
                            status = "✅" if task.get("crossed") else "📌"
                            f.write(f"{status} {task['text']} | Priority: {task.get('priority', 'Medium')} | Due: {task.get('due', 'No date')}\n")
                msg.showinfo("Export Complete", f"Tasks exported to {file_path}")
        except Exception as e:
            msg.showerror("Export Error", f"Could not export tasks: {e}")

    def import_tasks(self):
        """Import tasks from JSON file"""
        try:
            from tkinter import filedialog
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json")]
            )
            if file_path:
                with open(file_path, 'r') as f:
                    imported_tasks = json.load(f)
                self.tasks.extend(imported_tasks)
                self.validate_task_structure()
                self.save_tasks()
                self.listbox_load()
                msg.showinfo("Import Complete", f"Imported {len(imported_tasks)} tasks")
        except Exception as e:
            msg.showerror("Import Error", f"Could not import tasks: {e}")

    # ---- Listbox and Task Management ----

    def listbox_load(self):
        """Load and display tasks in listbox with enhanced formatting"""
        self.todo_display_listbox.delete(0, tk.END)
        filter_text = self.search_var.get().lower()
        show_completed = self.show_completed_var.get()
        tasks = self.tasks

        # Filtering
        if filter_text and filter_text != "search tasks...":
            tasks = [t for t in tasks if (
                filter_text in t["text"].lower() or
                filter_text in t.get("category", "").lower() or
                filter_text in t.get("priority", "").lower()
            )]

        # Show/hide completed
        if not show_completed:
            tasks = [t for t in tasks if not t.get("crossed", False)]

        # Sorting
        if self.sort_by == "priority":
            tasks.sort(key=lambda t: PRIORITIES.index(t.get("priority", "Medium")))
        elif self.sort_by == "date":
            tasks.sort(key=lambda t: t.get("due") or "9999-99-99")
        elif self.sort_by == "category":
            tasks.sort(key=lambda t: t.get("category", "Other"))
        elif self.sort_by == "created":
            tasks.sort(key=lambda t: t.get("created", ""))
        elif self.sort_by == "crossed":
            tasks.sort(key=lambda t: t.get("crossed", False))

        # Display tasks with enhanced formatting
        for idx, task in enumerate(tasks):
            status_icon = '✅' if task.get("crossed", False) else '📌'
            priority_icon = self.get_priority_icon(task.get("priority", "Medium"))
            category_icon = self.get_category_icon(task.get("category", "Other"))
            
            # Format due date
            due_text = task.get("due", "")
            if due_text:
                due_date = datetime.strptime(due_text, "%Y-%m-%d").date()
                today = date.today()
                if due_date < today and not task.get("crossed", False):
                    due_display = f"⚠ {due_text} (OVERDUE)"
                elif due_date == today:
                    due_display = f"⏰ {due_text} (TODAY)"
                else:
                    due_display = f"📅 {due_text}"
            else:
                due_display = "📅 No date"

            display = f"{status_icon} {priority_icon} {category_icon} {task['text']} | {due_display}"

            self.todo_display_listbox.insert(tk.END, display)
            
            # Color coding
            if task.get("crossed", False):
                self.todo_display_listbox.itemconfig(idx, fg="#7f8c8d")
            elif due_text and due_text < date.today().strftime("%Y-%m-%d"):
                self.todo_display_listbox.itemconfig(idx, fg="#e74c3c")  # Red for overdue
            elif task.get("priority") == "Critical":
                self.todo_display_listbox.itemconfig(idx, fg="#c0392b")  # Dark red for critical
            elif task.get("priority") == "High":
                self.todo_display_listbox.itemconfig(idx, fg="#e67e22")  # Orange for high
            else:
                self.todo_display_listbox.itemconfig(idx, fg="#2c3e50")  # Default

        # Update status bar
        self.update_status_bar()

    def get_priority_icon(self, priority):
        """Get icon for priority level"""
        icons = {
            "Low": "🔵",
            "Medium": "🟡", 
            "High": "🟠",
            "Critical": "🔴"
        }
        return icons.get(priority, "🟡")

    def get_category_icon(self, category):
        """Get icon for category"""
        icons = {
            "Personal": "👤",
            "Work": "💼",
            "Shopping": "🛒",
            "Health": "🏥",
            "Education": "📚",
            "Finance": "💰",
            "Other": "📋"
        }
        return icons.get(category, "📋")

    def add_item(self):
        """Add new task with enhanced validation"""
        new_item = self.item_entry_box.get().strip()
        priority = self.priority_var.get()
        category = self.category_var.get()
        due = self.due_entry.get().strip()
        
        # Validate input
        if not new_item or new_item == "Enter your task here...":
            msg.showwarning("Input Error", "Task cannot be empty.")
            return
            
        if due and due != "YYYY-MM-DD":
            try:
                due_date = datetime.strptime(due, "%Y-%m-%d").date()
                # Warn if adding task with past due date
                if due_date < date.today():
                    if not msg.askyesno("Past Due Date", 
                                      f"The due date {due} is in the past. Add anyway?"):
                        return
            except ValueError:
                msg.showwarning("Date Error", "Due date must be in YYYY-MM-DD format.")
                return
        else:
            due = ""
            
        # Check for duplicate tasks
        if any(task['text'].lower() == new_item.lower() for task in self.tasks):
            if not msg.askyesno("Duplicate Task", 
                              "A similar task already exists. Add anyway?"):
                return
        
        # Create new task
        new_task = {
            "text": new_item, 
            "crossed": False,
            "priority": priority,
            "category": category,
            "due": due, 
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "notes": ""
        }
        
        self.tasks.append(new_task)
        self.save_tasks()
        self.listbox_load()
        
        # Clear input fields
        self.item_entry_box.delete(0, tk.END)
        self.add_placeholder(self.item_entry_box, "Enter your task here...")
        self.due_entry.delete(0, tk.END)
        self.add_placeholder(self.due_entry, "YYYY-MM-DD")
        
        # Show success message
        self.status_label.config(text=f"✅ Added task: {new_item}")
        self.after(3000, lambda: self.status_label.config(text="Ready"))

    def cross_item(self):
        """Mark task as completed with confirmation"""
        try:
            idx = self.todo_display_listbox.curselection()[0]
            tasks = self.get_filtered_and_sorted_tasks()
            real_idx = self.tasks.index(tasks[idx])
            
            if not self.tasks[real_idx]["crossed"]:
                self.tasks[real_idx]["crossed"] = True
                self.tasks[real_idx]["completed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_tasks()
                self.listbox_load()
                self.status_label.config(text=f"✅ Completed: {self.tasks[real_idx]['text']}")
                self.after(3000, lambda: self.status_label.config(text="Ready"))
            else:
                msg.showinfo("Already Completed", "This task is already marked as completed.")
            
            self.todo_display_listbox.selection_clear(0, tk.END)
        except IndexError:
            msg.showwarning(title="WARNING", message="Select a task to mark as completed.")
        except Exception as e:
            print(colored(f"CROSS EVENT ERROR: {e}", "yellow"))

    def uncross_item(self):
        """Mark task as incomplete"""
        try:
            idx = self.todo_display_listbox.curselection()[0]
            tasks = self.get_filtered_and_sorted_tasks()
            real_idx = self.tasks.index(tasks[idx])
            
            if self.tasks[real_idx]["crossed"]:
                self.tasks[real_idx]["crossed"] = False
                if "completed_date" in self.tasks[real_idx]:
                    del self.tasks[real_idx]["completed_date"]
                self.save_tasks()
                self.listbox_load()
                self.status_label.config(text=f"🔄 Reopened: {self.tasks[real_idx]['text']}")
                self.after(3000, lambda: self.status_label.config(text="Ready"))
            else:
                msg.showinfo("Not Completed", "This task is not marked as completed.")
                
            self.todo_display_listbox.selection_clear(0, tk.END)
        except IndexError:
            msg.showwarning(title="WARNING", message="Select a task to reopen.")
        except Exception as e:
            print(colored(f"UNCROSS EVENT ERROR: {e}", "yellow"))

    def edit_task(self):
        """Enhanced edit task dialog with notes support"""
        try:
            idx = self.todo_display_listbox.curselection()[0]
            tasks = self.get_filtered_and_sorted_tasks()
            real_idx = self.tasks.index(tasks[idx])
            current = self.tasks[real_idx]
            
            # Create modern edit dialog
            popup = tk.Toplevel(self)
            popup.geometry("700x500")
            popup.transient(self)
            popup.title(f"Edit Task #{real_idx + 1}")
            popup.configure(bg="#ecf0f1")
            popup.resizable(False, False)

            # Main frame
            main_frame = tk.Frame(popup, bg="#ecf0f1", padx=20, pady=20)
            main_frame.pack(fill=tk.BOTH, expand=True)

            # Title
            title_label = tk.Label(main_frame, 
                                 text="✏ Edit Task", 
                                 fg="#2c3e50", 
                                 bg="#ecf0f1",
                                 font=("Segoe UI", 18, "bold"))
            title_label.pack(pady=(0, 20))

            # Task text
            tk.Label(main_frame, text="Task Description:", 
                    font=("Segoe UI", 12, "bold"), 
                    bg="#ecf0f1", fg="#2c3e50").pack(anchor='w')
            entry = tk.Text(main_frame, width=60, height=3, 
                           font=("Segoe UI", 12), 
                           bg="#ffffff", relief='solid', borderwidth=1)
            entry.insert('1.0', current["text"])
            entry.pack(pady=(5, 15), fill=tk.X)

            # Priority and Category in a row
            row1 = tk.Frame(main_frame, bg="#ecf0f1")
            row1.pack(fill=tk.X, pady=(0, 15))
            
            # Priority
            tk.Label(row1, text="Priority:", 
                    font=("Segoe UI", 12, "bold"), 
                    bg="#ecf0f1", fg="#2c3e50").pack(side=tk.LEFT)
            pri_var = tk.StringVar(value=current.get("priority", "Medium"))
            pri_menu = ttk.Combobox(row1, textvariable=pri_var, 
                                  values=PRIORITIES, state="readonly", width=10)
            pri_menu.pack(side=tk.LEFT, padx=(10, 20))
            
            # Category
            tk.Label(row1, text="Category:", 
                    font=("Segoe UI", 12, "bold"), 
                    bg="#ecf0f1", fg="#2c3e50").pack(side=tk.LEFT)
            cat_var = tk.StringVar(value=current.get("category", "Other"))
            cat_menu = ttk.Combobox(row1, textvariable=cat_var, 
                                  values=CATEGORIES, state="readonly", width=12)
            cat_menu.pack(side=tk.LEFT, padx=(10, 0))

            # Due date
            tk.Label(main_frame, text="Due Date (YYYY-MM-DD):", 
                    font=("Segoe UI", 12, "bold"), 
                    bg="#ecf0f1", fg="#2c3e50").pack(anchor='w')
            due_entry = tk.Entry(main_frame, width=20, 
                               font=("Segoe UI", 12), 
                               bg="#ffffff", relief='solid', borderwidth=1)
            due_entry.insert(0, current.get("due", ""))
            due_entry.pack(anchor='w', pady=(5, 15))

            # Notes
            tk.Label(main_frame, text="Notes:", 
                    font=("Segoe UI", 12, "bold"), 
                    bg="#ecf0f1", fg="#2c3e50").pack(anchor='w')
            notes_text = tk.Text(main_frame, width=60, height=5, 
                                font=("Segoe UI", 11), 
                                bg="#ffffff", relief='solid', borderwidth=1)
            notes_text.insert('1.0', current.get("notes", ""))
            notes_text.pack(pady=(5, 20), fill=tk.X)

            def save_edit():
                new_text = entry.get('1.0', tk.END).strip()
                new_priority = pri_var.get()
                new_category = cat_var.get()
                new_due = due_entry.get().strip()
                new_notes = notes_text.get('1.0', tk.END).strip()
                
                if not new_text:
                    msg.showwarning("Input Error", "Task cannot be empty.")
                    return
                    
                if new_due:
                    try:
                        datetime.strptime(new_due, "%Y-%m-%d")
                    except ValueError:
                        msg.showwarning("Date Error", "Due date must be in YYYY-MM-DD format.")
                        return
                
                # Update task
                self.tasks[real_idx]["text"] = new_text
                self.tasks[real_idx]["priority"] = new_priority
                self.tasks[real_idx]["category"] = new_category
                self.tasks[real_idx]["due"] = new_due
                self.tasks[real_idx]["notes"] = new_notes
                self.tasks[real_idx]["modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                self.save_tasks()
                self.listbox_load()
                popup.destroy()
                
                self.status_label.config(text=f"✏ Updated: {new_text}")
                self.after(3000, lambda: self.status_label.config(text="Ready"))

            # Buttons
            btn_frame = tk.Frame(main_frame, bg="#ecf0f1")
            btn_frame.pack(pady=20)
            
            save_btn = tk.Button(btn_frame, text="💾 Save Changes", 
                               width=15, command=save_edit, 
                               bg="#27ae60", fg="#fff", 
                               font=("Segoe UI", 12, "bold"),
                               relief='flat', cursor="hand2")
            save_btn.pack(side=tk.LEFT, padx=10)
            
            cancel_btn = tk.Button(btn_frame, text="❌ Cancel", 
                                 width=15, command=popup.destroy, 
                                 bg="#95a5a6", fg="#fff", 
                                 font=("Segoe UI", 12, "bold"),
                                 relief='flat', cursor="hand2")
            cancel_btn.pack(side=tk.LEFT, padx=10)
            
            popup.grab_set()
            entry.focus()
            
        except IndexError:
            msg.showwarning(title="WARNING", message="Select a task to edit.")
        except Exception as e:
            print(colored(f"EDIT EVENT ERROR: {e}", "yellow"))

    def delete_crossed_item(self):
        """Delete completed tasks with enhanced confirmation"""
        completed_tasks = [i for i, t in enumerate(self.tasks) if t.get("crossed", False)]
        
        if not completed_tasks:
            msg.showinfo("No Completed Tasks", "No completed tasks to delete.")
            return
        
        # Show detailed confirmation dialog
        task_list = "\n".join([f"• {self.tasks[i]['text']}" for i in completed_tasks[:10]])
        if len(completed_tasks) > 10:
            task_list += f"\n... and {len(completed_tasks) - 10} more tasks"
        
        confirm_msg = f"Delete {len(completed_tasks)} completed task(s)?\n\n{task_list}"
        
        if msg.askyesno("Confirm Deletion", confirm_msg):
            # Delete in reverse order to avoid index shift
            for i in reversed(completed_tasks):
                print(colored(f"DELETED TASK: {self.tasks[i]['text']}", "red"))
                del self.tasks[i]
            
            self.save_tasks()
            self.listbox_load()
            self.status_label.config(text=f"🗑 Deleted {len(completed_tasks)} completed tasks")
            self.after(3000, lambda: self.status_label.config(text="Ready"))

    def clear_list(self):
        """Clear all tasks with enhanced confirmation"""
        if not self.tasks:
            msg.showinfo("Empty List", "Task list is already empty.")
            return
            
        confirm_msg = f"This will permanently delete all {len(self.tasks)} tasks.\n\nThis action cannot be undone!"
        
        if msg.askyesno("Clear All Tasks", confirm_msg):
            self.tasks.clear()
            self.save_tasks()
            self.listbox_load()
            self.status_label.config(text="🧹 All tasks cleared")
            self.after(3000, lambda: self.status_label.config(text="Ready"))

    def clear_completed(self):
        """Clear only completed tasks"""
        completed_count = len([t for t in self.tasks if t.get("crossed", False)])
        
        if completed_count == 0:
            msg.showinfo("No Completed Tasks", "No completed tasks to clear.")
            return
            
        if msg.askyesno("Clear Completed", f"Delete {completed_count} completed task(s)?"):
            self.tasks = [t for t in self.tasks if not t.get("crossed", False)]
            self.save_tasks()
            self.listbox_load()
            self.status_label.config(text=f"🗑✅ Cleared {completed_count} completed tasks")
            self.after(3000, lambda: self.status_label.config(text="Ready"))

    def get_filtered_and_sorted_tasks(self):
        """Get the currently displayed tasks (after filter/sort), for mapping to the main list."""
        filter_text = self.search_var.get().lower()
        show_completed = self.show_completed_var.get()
        tasks = self.tasks
        
        # Filtering
        if filter_text and filter_text != "search tasks...":
            tasks = [t for t in tasks if (
                filter_text in t["text"].lower() or
                filter_text in t.get("category", "").lower() or
                filter_text in t.get("priority", "").lower()
            )]
            
        # Show/hide completed
        if not show_completed:
            tasks = [t for t in tasks if not t.get("crossed", False)]
            
        # Sorting
        if self.sort_by == "priority":
            tasks.sort(key=lambda t: PRIORITIES.index(t.get("priority", "Medium")))
        elif self.sort_by == "date":
            tasks.sort(key=lambda t: t.get("due") or "9999-99-99")
        elif self.sort_by == "category":
            tasks.sort(key=lambda t: t.get("category", "Other"))
        elif self.sort_by == "created":
            tasks.sort(key=lambda t: t.get("created", ""))
        elif self.sort_by == "crossed":
            tasks.sort(key=lambda t: t.get("crossed", False))
            
        return tasks

    def show_task_details(self):
        """Show detailed view of selected task"""
        try:
            idx = self.todo_display_listbox.curselection()[0]
            tasks = self.get_filtered_and_sorted_tasks()
            real_idx = self.tasks.index(tasks[idx])
            task = self.tasks[real_idx]
            
            # Create details dialog
            details = tk.Toplevel(self)
            details.geometry("500x600")
            details.title(f"Task Details - #{real_idx + 1}")
            details.configure(bg="#ecf0f1")
            details.transient(self)
            
            # Main frame
            main_frame = tk.Frame(details, bg="#ecf0f1", padx=20, pady=20)
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Title
            title = tk.Label(main_frame, 
                           text="📋 Task Details",
                           font=("Segoe UI", 18, "bold"),
                           bg="#ecf0f1", fg="#2c3e50")
            title.pack(pady=(0, 20))
            
            # Task info
            info_frame = tk.Frame(main_frame, bg="#ffffff", relief='solid', borderwidth=1)
            info_frame.pack(fill=tk.X, pady=10)
            
            details_text = f"""
📝 Task: {task['text']}

🔴 Priority: {task.get('priority', 'Medium')}
📂 Category: {task.get('category', 'Other')}
📅 Due Date: {task.get('due', 'No date set')}
📊 Status: {'✅ Completed' if task.get('crossed') else '⏳ Pending'}

📝 Created: {task.get('created', 'Unknown')}
{f"✅ Completed: {task.get('completed_date', 'Unknown')}" if task.get('crossed') else ""}
{f"✏ Modified: {task.get('modified', 'Never')}" if task.get('modified') else ""}

📄 Notes:
{task.get('notes', 'No notes added.')}
            """
            
            text_widget = tk.Text(info_frame, 
                                font=("Segoe UI", 11),
                                bg="#ffffff",
                                fg="#2c3e50",
                                wrap=tk.WORD,
                                borderwidth=0,
                                height=20)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
            text_widget.insert('1.0', details_text.strip())
            text_widget.config(state='disabled')
            
            # Close button
            close_btn = tk.Button(main_frame,
                                text="❌ Close",
                                command=details.destroy,
                                bg="#95a5a6", fg="#ffffff",
                                font=("Segoe UI", 12, "bold"),
                                relief='flat', cursor="hand2")
            close_btn.pack(pady=20)
            
        except IndexError:
            msg.showwarning("No Selection", "Please select a task to view details.")

    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Task", command=lambda: self.item_entry_box.focus(), accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Import Tasks", command=self.import_tasks)
        file_menu.add_command(label="Export Tasks", command=self.export_tasks)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Edit Task", command=self.edit_task, accelerator="F2")
        edit_menu.add_command(label="Complete Task", command=self.cross_item, accelerator="Space")
        edit_menu.add_separator()
        edit_menu.add_command(label="Clear Completed", command=self.clear_completed)
        edit_menu.add_command(label="Clear All", command=self.clear_list)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Task Details", command=self.show_task_details)
        view_menu.add_separator()
        view_menu.add_checkbutton(label="Show Completed", variable=self.show_completed_var, command=self.listbox_load)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
        help_menu.add_command(label="About", command=self.show_about)

    def show_shortcuts(self):
        """Display keyboard shortcuts"""
        shortcuts_text = """
Keyboard Shortcuts:

Ctrl+N       - Focus on new task entry
Ctrl+S       - Save tasks
Ctrl+F       - Focus on search
F2           - Edit selected task
Space        - Complete/Incomplete task
Delete       - Delete completed tasks
Enter        - Add new task (when in entry box)
Double-click - Edit task
        """
        
        shortcuts_window = tk.Toplevel(self)
        shortcuts_window.title("Keyboard Shortcuts")
        shortcuts_window.geometry("400x300")
        shortcuts_window.configure(bg="#ecf0f1")
        shortcuts_window.transient(self)
        
        text_widget = tk.Text(shortcuts_window,
                            font=("Segoe UI", 11),
                            bg="#ffffff",
                            fg="#2c3e50",
                            wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        text_widget.insert('1.0', shortcuts_text.strip())
        text_widget.config(state='disabled')

    def show_about(self):
        """Display about dialog"""
        about_text = """
TodoList Manager Pro
Version 2.0

A modern, feature-rich task management application
built with Python and Tkinter.

Features:
• Task priorities and categories
• Due date tracking with overdue alerts
• Search and filtering
• Notes and detailed task information
• Import/Export functionality
• Keyboard shortcuts
• Auto-save
• Modern UI design

© 2025 TodoList Manager Pro
        """
        
        msg.showinfo("About TodoList Manager Pro", about_text)

    def run(self):
        """Start the application"""
        try:
            # Create menu bar
            self.create_menu_bar()
            
            # Show welcome message for first-time users
            if not self.tasks:
                self.status_label.config(text="👋 Welcome! Start by adding your first task above.")
            
            # Start the main loop
            self.mainloop()
            
        except Exception as e:
            print(colored(f"Application error: {e}", "red"))
            msg.showerror("Application Error", f"An error occurred: {e}")

def main():
    """Main function with error handling"""
    try:
        print(colored("Starting TodoList Manager Pro...", "cyan"))
        app = ModernTodoApp()
        app.run()
    except Exception as e:
        print(colored(f"Fatal error: {e}", "red"))
        if 'tk' in globals():
            msg.showerror("Fatal Error", f"Application failed to start: {e}")

if __name__ == '__main__':
    main()