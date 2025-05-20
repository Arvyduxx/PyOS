import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
import time

try:
    from tkinterweb import HtmlFrame
    HAS_BROWSER = True
except ImportError:
    HAS_BROWSER = False


class PyOS:
    def __init__(self, root):
        self.root = root
        self.root.title("PyOS - All-in-One")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="black")

        self.create_taskbar()
        self.create_desktop()

        # Create all pages/apps
        self.pages = {
            "desktop": self.desktop_frame,
            "calculator": self.create_calculator_page(),
            "editor": self.create_editor_page(),
            "settings": self.create_settings_page(),
            "paint": self.create_paint_app(),
        }
        if HAS_BROWSER:
            self.pages["browser"] = self.create_browser_page()
        else:
            self.pages["browser"] = self.create_no_browser_page()

        self.show_page("desktop")

    # TASKBAR and START MENU
    def create_taskbar(self):
        self.taskbar = tk.Frame(self.root, bg="#222", height=30)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.start_button = tk.Button(self.taskbar, text="☰ Start", command=self.toggle_start_menu)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.clock_label = tk.Label(self.taskbar, fg="white", bg="#222")
        self.clock_label.pack(side=tk.RIGHT, padx=10)
        self.update_clock()

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.clock_label.config(text=now)
        self.root.after(1000, self.update_clock)

    def toggle_start_menu(self):
        if hasattr(self, 'start_menu') and self.start_menu.winfo_exists():
            self.start_menu.destroy()
        else:
            self.start_menu = tk.Frame(self.root, bg="gray", width=150, height=300)
            self.start_menu.place(x=10, y=300)

            apps = [
                ("Calculator", "calculator"),
                ("Editor", "editor"),
                ("Paint", "paint"),
                ("Browser", "browser"),
                ("Settings", "settings"),
                ("Desktop", "desktop"),
            ]
            for (name, key) in apps:
                tk.Button(self.start_menu, text=name, width=18,
                          command=lambda k=key: self.open_page_from_startmenu(k)).pack(pady=2)

    def open_page_from_startmenu(self, key):
        self.show_page(key)
        if hasattr(self, 'start_menu') and self.start_menu.winfo_exists():
            self.start_menu.destroy()

    # DESKTOP
    def create_desktop(self):
        self.desktop_frame = tk.Frame(self.root, bg="black")
        self.desktop_frame.place(x=0, y=0, relwidth=1, relheight=1)

        # Icons on desktop
        self.create_icon(self.desktop_frame, "Calculator", 50, 50, lambda: self.show_page("calculator"))
        self.create_icon(self.desktop_frame, "Editor", 150, 50, lambda: self.show_page("editor"))
        self.create_icon(self.desktop_frame, "Paint", 250, 50, lambda: self.show_page("paint"))
        self.create_icon(self.desktop_frame, "Browser", 350, 50, lambda: self.show_page("browser"))
        self.create_icon(self.desktop_frame, "Settings", 450, 50, lambda: self.show_page("settings"))

    def create_icon(self, parent, name, x, y, command):
        btn = tk.Button(parent, text=name, width=12, height=2, command=command)
        btn.place(x=x, y=y)

    # PAGE NAVIGATION
    def show_page(self, name):
        # Hide all pages
        for page_name, page in self.pages.items():
            page.place_forget()

        # Show requested page
        self.pages[name].place(x=0, y=0, relwidth=1, relheight=1)
        self.root.update()

        # Close start menu if open
        if hasattr(self, 'start_menu') and self.start_menu.winfo_exists():
            self.start_menu.destroy()

    # CALCULATOR APP
    def create_calculator_page(self):
        frame = tk.Frame(self.root, bg="white")

        self.calc_display = tk.Entry(frame, font=("Arial", 24), bd=5, relief=tk.RIDGE, justify="right")
        self.calc_display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
        ]

        for (text, r, c) in buttons:
            action = lambda x=text: self.on_calc_button(x)
            tk.Button(frame, text=text, font=("Arial", 18), command=action).grid(row=r, column=c, sticky="nsew", padx=5, pady=5)

        for i in range(5):
            frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            frame.grid_columnconfigure(i, weight=1)

        back_btn = tk.Button(frame, text="Back", command=lambda: self.show_page("desktop"))
        back_btn.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

        return frame

    def on_calc_button(self, char):
        if char == '=':
            try:
                result = eval(self.calc_display.get())
                self.calc_display.delete(0, tk.END)
                self.calc_display.insert(0, str(result))
            except:
                messagebox.showerror("Error", "Invalid Expression")
                self.calc_display.delete(0, tk.END)
        else:
            self.calc_display.insert(tk.END, char)

    # EDITOR APP
    def create_editor_page(self):
        frame = tk.Frame(self.root, bg="white")

        self.editor_text = tk.Text(frame, font=("Consolas", 14))
        self.editor_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=5)

        save_btn = tk.Button(btn_frame, text="Save", command=self.editor_save)
        save_btn.pack(side=tk.LEFT, padx=5)

        open_btn = tk.Button(btn_frame, text="Open", command=self.editor_open)
        open_btn.pack(side=tk.LEFT, padx=5)

        back_btn = tk.Button(btn_frame, text="Back", command=lambda: self.show_page("desktop"))
        back_btn.pack(side=tk.LEFT, padx=5)

        return frame

    def editor_save(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write(self.editor_text.get("1.0", tk.END))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")

    def editor_open(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                self.editor_text.delete("1.0", tk.END)
                self.editor_text.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file:\n{e}")

    # SETTINGS APP
    def create_settings_page(self):
        frame = tk.Frame(self.root, bg="white")
        label = tk.Label(frame, text="Settings", font=("Arial", 24))
        label.pack(pady=20)

        back_btn = tk.Button(frame, text="Back", command=lambda: self.show_page("desktop"))
        back_btn.pack(pady=10)

        return frame

    # PAINT APP
    def create_paint_app(self):
        frame = tk.Frame(self.root, bg="white")

        self.paint_color = "black"
        self.last_x = None
        self.last_y = None

        top_frame = tk.Frame(frame)
        top_frame.pack(fill=tk.X)

        color_btn = tk.Button(top_frame, text="Select Color", command=self.select_paint_color)
        color_btn.pack(side=tk.LEFT, padx=5, pady=5)

        clear_btn = tk.Button(top_frame, text="Clear", command=self.clear_canvas)
        clear_btn.pack(side=tk.LEFT, padx=5, pady=5)

        back_btn = tk.Button(top_frame, text="Back", command=lambda: self.show_page("desktop"))
        back_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        self.canvas = tk.Canvas(frame, bg="white", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.paint_start)
        self.canvas.bind("<B1-Motion>", self.paint_draw)
        self.canvas.bind("<ButtonRelease-1>", self.paint_end)

        return frame

    def select_paint_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.paint_color = color

    def clear_canvas(self):
        self.canvas.delete("all")

    def paint_start(self, event):
        self.last_x, self.last_y = event.x, event.y

    def paint_draw(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill=self.paint_color, width=3, capstyle=tk.ROUND, smooth=True)
        self.last_x, self.last_y = event.x, event.y

    def paint_end(self, event):
        self.last_x, self.last_y = None, None

    # WEB BROWSER APP
    def create_browser_page(self):
        frame = tk.Frame(self.root, bg="white")

        url_frame = tk.Frame(frame)
        url_frame.pack(fill=tk.X, pady=5, padx=5)

        self.url_entry = tk.Entry(url_frame, font=("Arial", 14))
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        go_btn = tk.Button(url_frame, text="Go", command=self.load_url)
        go_btn.pack(side=tk.LEFT, padx=5)

        back_btn = tk.Button(url_frame, text="Back", command=lambda: self.show_page("desktop"))
        back_btn.pack(side=tk.LEFT, padx=5)

        self.browser_frame = HtmlFrame(frame, horizontal_scrollbar="auto")
        self.browser_frame.pack(fill=tk.BOTH, expand=True)

        return frame

    def load_url(self):
        url = self.url_entry.get()
        if not url.startswith("http"):
            url = "http://" + url
        try:
            self.browser_frame.load_website(url)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load URL:\n{e}")

    # NO BROWSER INSTALLED PAGE
    def create_no_browser_page(self):
        frame = tk.Frame(self.root, bg="white")
        label = tk.Label(frame, text="Browser app requires 'tkinterweb' package.\nInstall with:\n\npip install tkinterweb", font=("Arial", 16), fg="red")
        label.pack(expand=True)

        back_btn = tk.Button(frame, text="Back", command=lambda: self.show_page("desktop"))
        back_btn.pack(pady=10)

        return frame


if __name__ == "__main__":
    root = tk.Tk()
    app = PyOS(root)
    root.mainloop()

