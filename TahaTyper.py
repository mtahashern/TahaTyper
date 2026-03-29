import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import random
import os
import sys
from PIL import Image, ImageTk
import pynput.keyboard as keyboard
from pynput.keyboard import Key, Controller
import keyboard as hotkey_lib

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class TahaTyper:
    def __init__(self, root):
        self.root = root
        self.root.title("TahaTyper - Professional Auto Typer")
        self.root.geometry("500x750")
        self.root.configure(bg="#2c3e50")
        
        # Set Window Icon
        try:
            icon_path = resource_path("TahaTyper.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Could not load icon: {e}")
            
        self.keyboard = Controller()
        self.is_typing = False
        self.typing_thread = None
        
        # Default Settings
        self.start_hotkey = "f6"
        self.stop_hotkey = "f7"
        
        self.setup_ui()
        self.setup_hotkeys()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom Colors
        bg_color = "#2c3e50"
        accent_color = "#3498db"
        text_color = "#ecf0f1"
        
        main_frame = tk.Frame(self.root, bg=bg_color, padx=20, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Logo Image
        try:
            logo_path = resource_path("TahaTyper_Logo.png")
            if os.path.exists(logo_path):
                img = Image.open(logo_path)
                img = img.resize((150, 150), Image.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
                logo_label = tk.Label(main_frame, image=self.logo_img, bg=bg_color)
                logo_label.pack(pady=(0, 5))
        except Exception as e:
            print(f"Could not load logo image: {e}")

        # Title
        title_label = tk.Label(main_frame, text="TahaTyper", font=("Helvetica", 24, "bold"), 
                              bg=bg_color, fg=accent_color)
        title_label.pack(pady=(0, 10))

        # Text Input
        tk.Label(main_frame, text="Text to Type:", bg=bg_color, fg=text_color, font=("Helvetica", 10)).pack(anchor="w")
        self.text_area = scrolledtext.ScrolledText(main_frame, height=6, font=("Consolas", 10))
        self.text_area.pack(fill=tk.X, pady=(0, 15))

        # Speed Control
        speed_frame = tk.LabelFrame(main_frame, text="Typing Speed (ms delay)", bg=bg_color, fg=text_color, padx=10, pady=10)
        speed_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.speed_var = tk.IntVar(value=50)
        self.speed_slider = tk.Scale(speed_frame, from_=10, to=300, orient=tk.HORIZONTAL, 
                                    variable=self.speed_var, bg=bg_color, fg=text_color, 
                                    highlightthickness=0, troughcolor="#34495e")
        self.speed_slider.pack(fill=tk.X)

        # Options
        options_frame = tk.LabelFrame(main_frame, text="Human-Like Behavior", bg=bg_color, fg=text_color, padx=10, pady=10)
        options_frame.pack(fill=tk.X, pady=(0, 15))

        self.random_delay = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Randomized Delays", variable=self.random_delay, 
                       bg=bg_color, fg=text_color, selectcolor=bg_color, activebackground=bg_color).pack(anchor="w")

        self.punctuation_pauses = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Pause after Punctuation", variable=self.punctuation_pauses, 
                       bg=bg_color, fg=text_color, selectcolor=bg_color, activebackground=bg_color).pack(anchor="w")

        self.mistakes_enabled = tk.BooleanVar(value=False)
        tk.Checkbutton(options_frame, text="Simulate Mistakes (Rare)", variable=self.mistakes_enabled, 
                       bg=bg_color, fg=text_color, selectcolor=bg_color, activebackground=bg_color).pack(anchor="w")

        self.loop_enabled = tk.BooleanVar(value=False)
        tk.Checkbutton(options_frame, text="Loop Typing", variable=self.loop_enabled, 
                       bg=bg_color, fg=text_color, selectcolor=bg_color, activebackground=bg_color).pack(anchor="w")

        # Status & Countdown
        self.status_label = tk.Label(main_frame, text="Status: Ready", bg=bg_color, fg="#f1c40f", font=("Helvetica", 10, "bold"))
        self.status_label.pack(pady=5)

        # Buttons
        btn_frame = tk.Frame(main_frame, bg=bg_color)
        btn_frame.pack(fill=tk.X, pady=10)

        self.start_btn = tk.Button(btn_frame, text="START (F6)", command=self.start_typing, 
                                  bg="#27ae60", fg="white", font=("Helvetica", 12, "bold"), height=2)
        self.start_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        self.stop_btn = tk.Button(btn_frame, text="STOP (F7)", command=self.stop_typing, 
                                 bg="#c0392b", fg="white", font=("Helvetica", 12, "bold"), height=2)
        self.stop_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

        # Instructions
        tk.Label(main_frame, text="Tip: Press F6 to start typing into the active window.\nPress F7 to emergency stop.", 
                 bg=bg_color, fg="#bdc3c7", font=("Helvetica", 8), justify=tk.CENTER).pack(pady=10)

    def setup_hotkeys(self):
        try:
            hotkey_lib.add_hotkey(self.start_hotkey, self.start_typing)
            hotkey_lib.add_hotkey(self.stop_hotkey, self.stop_typing)
        except Exception as e:
            print(f"Hotkey setup error: {e}")

    def start_typing(self):
        if self.is_typing:
            return
        
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to type!")
            return

        self.is_typing = True
        self.status_label.config(text="Status: Starting in 3s...", fg="#e67e22")
        self.start_btn.config(state=tk.DISABLED)
        
        self.typing_thread = threading.Thread(target=self.typing_process, args=(text,))
        self.typing_thread.daemon = True
        self.typing_thread.start()

    def stop_typing(self):
        self.is_typing = False
        self.status_label.config(text="Status: Ready", fg="#f1c40f")
        self.start_btn.config(state=tk.NORMAL)

    def typing_process(self, text):
        for i in range(3, 0, -1):
            if not self.is_typing: return
            self.root.after(0, lambda x=i: self.status_label.config(text=f"Status: Starting in {x}s..."))
            time.sleep(1)
        
        self.root.after(0, lambda: self.status_label.config(text="Status: TYPING...", fg="#2ecc71"))

        while self.is_typing:
            for char in text:
                if not self.is_typing:
                    break
                
                if self.mistakes_enabled.get() and random.random() < 0.02:
                    wrong_char = random.choice("abcdefghijklmnopqrstuvwxyz")
                    self.keyboard.type(wrong_char)
                    time.sleep(self.speed_var.get() / 1000.0)
                    self.keyboard.press(Key.backspace)
                    self.keyboard.release(Key.backspace)
                    time.sleep(self.speed_var.get() / 500.0)

                self.keyboard.type(char)
                
                base_delay = self.speed_var.get() / 1000.0
                if self.random_delay.get():
                    delay = base_delay * random.uniform(0.5, 1.5)
                else:
                    delay = base_delay
                
                if self.punctuation_pauses.get() and char in ".,!?\n":
                    delay += random.uniform(0.3, 0.7)
                
                time.sleep(delay)

            if not self.loop_enabled.get():
                break
            
            if self.is_typing:
                time.sleep(1)

        self.root.after(0, self.stop_typing)

if __name__ == "__main__":
    root = tk.Tk()
    app = TahaTyper(root)
    root.mainloop()
