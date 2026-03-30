import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import random
import os
import sys
import hashlib
import platform
from PIL import Image, ImageTk
import pynput.keyboard as pynput_kb
from pynput.keyboard import Key, Controller
import keyboard as hotkey_lib

# --- ACTIVATION SYSTEM CONFIG ---
SECRET_SALT = "TAHA_TYPER_SECURE_2026"

def get_machine_id():
    """Generates a unique ID for the current computer."""
    try:
        # Basic hardware fingerprint
        system_info = platform.node() + platform.processor() + platform.machine()
        return hashlib.sha256(system_info.encode()).hexdigest()[:12].upper()
    except:
        return "UNKNOWN_DEVICE"

def verify_key(user_key):
    """Verifies if the key is valid for this specific machine."""
    machine_id = get_machine_id()
    # Key is a hash of (MachineID + SecretSalt)
    expected_hash = hashlib.sha256((machine_id + SECRET_SALT).encode()).hexdigest()[:16].upper()
    formatted_expected = "-".join([expected_hash[i:i+4] for i in range(0, 16, 4)])
    return user_key.strip().upper() == formatted_expected

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- ACTIVATION UI ---
class ActivationWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.root.title("TahaTyper - Activation")
        self.root.geometry("400x400")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(False, False)

        # UI Elements
        tk.Label(root, text="TahaTyper", font=("Helvetica", 24, "bold"), bg="#2c3e50", fg="#3498db").pack(pady=(30, 5))
        tk.Label(root, text="ACTIVATION REQUIRED", font=("Helvetica", 10, "bold"), bg="#2c3e50", fg="#e74c3c").pack()
        
        tk.Label(root, text="Please enter your Activation Key:", bg="#2c3e50", fg="#ecf0f1", font=("Helvetica", 10)).pack(pady=(30, 5))
        
        self.key_entry = tk.Entry(root, font=("Consolas", 12), justify="center", bg="#34495e", fg="white", insertbackground="white", width=25)
        self.key_entry.pack(pady=10)
        
        mid_frame = tk.Frame(root, bg="#34495e", padx=10, pady=5)
        mid_frame.pack(pady=10)
        tk.Label(mid_frame, text=f"Your Machine ID: {get_machine_id()}", font=("Consolas", 9), bg="#34495e", fg="#f1c40f").pack()
        
        tk.Label(root, text="Send this ID to Taha to get your key.", font=("Helvetica", 8, "italic"), bg="#2c3e50", fg="#bdc3c7").pack()

        self.activate_btn = tk.Button(root, text="ACTIVATE NOW", command=self.check_activation, bg="#27ae60", fg="white", font=("Helvetica", 11, "bold"), width=20, height=2)
        self.activate_btn.pack(pady=30)

        # Check for existing activation
        self.load_activation()

    def check_activation(self):
        key = self.key_entry.get()
        if verify_key(key):
            self.save_activation(key)
            messagebox.showinfo("Success", "TahaTyper Activated Successfully!")
            self.on_success()
        else:
            messagebox.showerror("Error", "Invalid Activation Key for this machine.")

    def save_activation(self, key):
        with open("activation.dat", "w") as f:
            f.write(key)

    def load_activation(self):
        if os.path.exists("activation.dat"):
            with open("activation.dat", "r") as f:
                saved_key = f.read().strip()
                if verify_key(saved_key):
                    self.on_success()

# --- MAIN TYPER APPLICATION ---
class TahaTyper:
    def __init__(self, root):
        self.root = root
        self.root.title("TahaTyper - Pro Edition")
        self.root.geometry("450x650")
        self.root.configure(bg="#2c3e50")
        
        # Set Window Icon
        try:
            icon_path = resource_path("TahaTyper.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except: pass
            
        self.keyboard = Controller()
        self.is_typing = False
        self.typing_thread = None
        
        self.setup_ui()
        self.setup_hotkeys()

    def setup_ui(self):
        # Create a Canvas and Scrollbar for smaller screens
        self.canvas = tk.Canvas(self.root, bg="#2c3e50", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#2c3e50")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=430)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=10)
        self.scrollbar.pack(side="right", fill="y")

        bg_color = "#2c3e50"
        accent_color = "#3498db"
        text_color = "#ecf0f1"
        
        # Logo
        try:
            logo_path = resource_path("TahaTyper_Logo.png")
            if os.path.exists(logo_path):
                img = Image.open(logo_path)
                img = img.resize((100, 100), Image.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
                tk.Label(self.scrollable_frame, image=self.logo_img, bg=bg_color).pack(pady=(10, 5))
        except: pass

        tk.Label(self.scrollable_frame, text="TahaTyper", font=("Helvetica", 20, "bold"), bg=bg_color, fg=accent_color).pack()
        tk.Label(self.scrollable_frame, text="PRO EDITION - ACTIVATED", font=("Helvetica", 8, "bold"), bg=bg_color, fg="#2ecc71").pack(pady=(0, 10))

        # Text Input
        tk.Label(self.scrollable_frame, text="Text to Type:", bg=bg_color, fg=text_color, font=("Helvetica", 10)).pack(anchor="w")
        self.text_area = scrolledtext.ScrolledText(self.scrollable_frame, height=6, font=("Consolas", 10), bg="#34495e", fg="white", insertbackground="white")
        self.text_area.pack(fill=tk.X, pady=(0, 10))

        # Speed Control
        speed_frame = tk.LabelFrame(self.scrollable_frame, text="Typing Speed (ms delay)", bg=bg_color, fg=text_color, padx=10, pady=5)
        speed_frame.pack(fill=tk.X, pady=(0, 10))
        self.speed_var = tk.IntVar(value=50)
        tk.Scale(speed_frame, from_=10, to=300, orient=tk.HORIZONTAL, variable=self.speed_var, bg=bg_color, fg=text_color, highlightthickness=0, troughcolor="#34495e").pack(fill=tk.X)

        # Options
        options_frame = tk.LabelFrame(self.scrollable_frame, text="Human-Like Behavior", bg=bg_color, fg=text_color, padx=10, pady=5)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        self.random_delay = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Randomized Delays", variable=self.random_delay, bg=bg_color, fg=text_color, selectcolor=bg_color, activebackground=bg_color).pack(anchor="w")
        self.punctuation_pauses = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Pause after Punctuation", variable=self.punctuation_pauses, bg=bg_color, fg=text_color, selectcolor=bg_color, activebackground=bg_color).pack(anchor="w")
        self.mistakes_enabled = tk.BooleanVar(value=False)
        tk.Checkbutton(options_frame, text="Simulate Mistakes (Rare)", variable=self.mistakes_enabled, bg=bg_color, fg=text_color, selectcolor=bg_color, activebackground=bg_color).pack(anchor="w")
        self.loop_enabled = tk.BooleanVar(value=False)
        tk.Checkbutton(options_frame, text="Loop Typing", variable=self.loop_enabled, bg=bg_color, fg=text_color, selectcolor=bg_color, activebackground=bg_color).pack(anchor="w")

        # Status
        self.status_label = tk.Label(self.scrollable_frame, text="Status: Ready", bg=bg_color, fg="#f1c40f", font=("Helvetica", 10, "bold"))
        self.status_label.pack(pady=5)

        # Buttons
        btn_frame = tk.Frame(self.scrollable_frame, bg=bg_color)
        btn_frame.pack(fill=tk.X, pady=5)
        self.start_btn = tk.Button(btn_frame, text="START (F6)", command=self.start_typing, bg="#27ae60", fg="white", font=("Helvetica", 12, "bold"), height=2)
        self.start_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        self.stop_btn = tk.Button(btn_frame, text="STOP (F7)", command=self.stop_typing, bg="#c0392b", fg="white", font=("Helvetica", 12, "bold"), height=2)
        self.stop_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

    def setup_hotkeys(self):
        try:
            hotkey_lib.add_hotkey('f6', self.start_typing)
            hotkey_lib.add_hotkey('f7', self.stop_typing)
        except: pass

    def start_typing(self):
        if self.is_typing: return
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text!")
            return
        self.is_typing = True
        self.status_label.config(text="Status: Starting in 3s...", fg="#e67e22")
        self.start_btn.config(state=tk.DISABLED)
        self.typing_thread = threading.Thread(target=self.typing_process, args=(text,), daemon=True)
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
                if not self.is_typing: break
                if self.mistakes_enabled.get() and random.random() < 0.02:
                    wrong_char = random.choice("abcdefghijklmnopqrstuvwxyz")
                    self.keyboard.type(wrong_char)
                    time.sleep(self.speed_var.get() / 1000.0)
                    self.keyboard.press(pynput_kb.Key.backspace); self.keyboard.release(pynput_kb.Key.backspace)
                    time.sleep(self.speed_var.get() / 500.0)
                self.keyboard.type(char)
                base_delay = self.speed_var.get() / 1000.0
                delay = base_delay * random.uniform(0.5, 1.5) if self.random_delay.get() else base_delay
                if self.punctuation_pauses.get() and char in ".,!?\n": delay += random.uniform(0.3, 0.7)
                time.sleep(delay)
            if not self.loop_enabled.get(): break
            if self.is_typing: time.sleep(1)
        self.root.after(0, self.stop_typing)

if __name__ == "__main__":
    root = tk.Tk()
    def launch_app():
        for widget in root.winfo_children(): widget.destroy()
        TahaTyper(root)
    ActivationWindow(root, launch_app)
    root.mainloop()
