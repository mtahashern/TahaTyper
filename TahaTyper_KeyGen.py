import hashlib
import tkinter as tk
from tkinter import messagebox

SECRET_SALT = "TAHA_TYPER_SECURE_2026"

def generate_key(machine_id):
    """Generates a valid key for a given Machine ID."""
    machine_id = machine_id.strip().upper()
    if not machine_id:
        return None
    
    # Key is a hash of (MachineID + SecretSalt)
    expected_hash = hashlib.sha256((machine_id + SECRET_SALT).encode()).hexdigest()[:16].upper()
    # Format it like XXXX-XXXX-XXXX-XXXX
    formatted_key = "-".join([expected_hash[i:i+4] for i in range(0, 16, 4)])
    return formatted_key

class KeyGenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TahaTyper - Private Key Generator")
        self.root.geometry("450x300")
        self.root.configure(bg="#1a1b26")
        self.root.resizable(False, False)

        tk.Label(root, text="TahaTyper Key Generator", font=("Segoe UI", 16, "bold"), bg="#1a1b26", fg="#7aa2f7").pack(pady=20)
        
        tk.Label(root, text="Enter User's Machine ID:", bg="#1a1b26", fg="#cfc9c2").pack(pady=5)
        self.id_entry = tk.Entry(root, font=("Consolas", 12), justify="center", bg="#24283b", fg="white", insertbackground="white", width=25)
        self.id_entry.pack(pady=5)

        tk.Button(root, text="GENERATE KEY", command=self.on_generate, bg="#9ece6a", fg="#1a1b26", font=("Segoe UI", 10, "bold"), width=20).pack(pady=20)

        self.result_var = tk.StringVar(value="Key will appear here")
        self.result_entry = tk.Entry(root, textvariable=self.result_var, font=("Consolas", 12), justify="center", bg="#1a1b26", fg="#e0af68", borderwidth=0, readonlybackground="#1a1b26", state="readonly", width=30)
        self.result_entry.pack(pady=5)

        tk.Label(root, text="KEEP THIS TOOL PRIVATE", font=("Segoe UI", 8, "bold"), bg="#1a1b26", fg="#f7768e").pack(side="bottom", pady=10)

    def on_generate(self):
        mid = self.id_entry.get()
        key = generate_key(mid)
        if key:
            self.result_var.set(key)
            self.root.clipboard_clear()
            self.root.clipboard_append(key)
            messagebox.showinfo("Success", f"Key generated and copied to clipboard:\n\n{key}")
        else:
            messagebox.showwarning("Error", "Please enter a valid Machine ID.")

if __name__ == "__main__":
    root = tk.Tk()
    KeyGenApp(root)
    root.mainloop()
