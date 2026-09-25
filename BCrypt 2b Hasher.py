import tkinter as tk
from tkinter import ttk, messagebox
import bcrypt
import pyperclip
import secrets
import string
import time
from datetime import datetime

class BCryptCompactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 BCrypt 2b Hasher")
        self.root.geometry("500x650")  # Ukuran lebih compact
        
        # Variabel mode
        self.dark_mode = False
        self.current_hash = None
        
        # Warna tema
        self.light_colors = {
            "bg": "#f8f9fa",
            "fg": "#2c3e50",
            "frame_bg": "#ffffff",
            "button_bg": "#3498db",
            "button_fg": "white",
            "entry_bg": "white",
            "entry_fg": "black",
            "hash_bg": "#f1f8ff",
            "hash_fg": "#2c3e50",
            "accent": "#2980b9"
        }
        
        self.dark_colors = {
            "bg": "#1a1a2e",
            "fg": "#ecf0f1",
            "frame_bg": "#162447",
            "button_bg": "#0f3460",
            "button_fg": "#e94560",
            "entry_bg": "#1f4068",
            "entry_fg": "white",
            "hash_bg": "#1b1b2f",
            "hash_fg": "#4cc9f0",
            "accent": "#e94560"
        }
        
        self.current_colors = self.light_colors
        
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        # Container utama dengan padding
        main_frame = tk.Frame(self.root, bg=self.current_colors["bg"], padx=20, pady=15)
        main_frame.pack(fill="both", expand=True)
        
        # Header dengan switch mode
        header_frame = tk.Frame(main_frame, bg=self.current_colors["bg"])
        header_frame.pack(fill="x", pady=(0, 15))
        
        # Judul
        title_label = tk.Label(header_frame, text="BCRYPT 2b HASHER", 
                              font=("Arial", 18, "bold"), 
                              bg=self.current_colors["bg"], 
                              fg=self.current_colors["accent"])
        title_label.pack(side="left")
        
        # Switch mode button di kanan
        self.mode_button = tk.Button(header_frame, text="🌙", 
                                    font=("Arial", 12),
                                    command=self.toggle_mode,
                                    bg=self.current_colors["button_bg"],
                                    fg=self.current_colors["button_fg"],
                                    bd=0, padx=10)
        self.mode_button.pack(side="right")
        
        # Password Input Section
        input_frame = tk.LabelFrame(main_frame, text=" PASSWORD INPUT ", 
                                   font=("Arial", 10, "bold"),
                                   bg=self.current_colors["frame_bg"],
                                   fg=self.current_colors["fg"],
                                   padx=15, pady=15)
        input_frame.pack(fill="x", pady=(0, 15))
        
        # Password Entry
        self.password_entry = tk.Entry(input_frame, font=("Arial", 12), 
                                      show="•", width=40)
        self.password_entry.pack(fill="x", pady=(0, 10))
        self.password_entry.bind("<KeyRelease>", self.check_password_strength)
        self.password_entry.focus()
        
        # Strength indicator
        self.strength_label = tk.Label(input_frame, text="Strength: -", 
                                      font=("Arial", 9),
                                      bg=self.current_colors["frame_bg"])
        self.strength_label.pack(anchor="w")
        
        # Config Frame
        config_frame = tk.Frame(main_frame, bg=self.current_colors["bg"])
        config_frame.pack(fill="x", pady=(0, 15))
        
        # Cost Factor
        tk.Label(config_frame, text="Cost Factor:", 
                font=("Arial", 10),
                bg=self.current_colors["bg"]).pack(side="left", padx=(0, 10))
        
        self.cost_var = tk.IntVar(value=12)
        cost_frame = tk.Frame(config_frame, bg=self.current_colors["bg"])
        cost_frame.pack(side="left")
        
        for value in [8, 10, 12, 14]:
            rb = tk.Radiobutton(cost_frame, text=str(value), 
                               variable=self.cost_var, value=value,
                               font=("Arial", 9),
                               bg=self.current_colors["bg"])
            rb.pack(side="left", padx=5)
        
        # Info cost
        self.cost_info = tk.Label(config_frame, text="", 
                                 font=("Arial", 8),
                                 bg=self.current_colors["bg"],
                                 fg="#7f8c8d")
        self.cost_info.pack(side="right")
        self.update_cost_info()
        
        # Action Buttons
        button_frame = tk.Frame(main_frame, bg=self.current_colors["bg"])
        button_frame.pack(fill="x", pady=(0, 15))
        
        button_style = {"font": ("Arial", 10, "bold"), "padx": 15, "pady": 8}
        
        self.hash_button = tk.Button(button_frame, text="🔒 GENERATE HASH", 
                                    bg="#27ae60", fg="white",
                                    command=self.generate_hash, **button_style)
        self.hash_button.pack(side="left", padx=(0, 10))
        
        self.random_button = tk.Button(button_frame, text="🎲 RANDOM", 
                                      bg="#9b59b6", fg="white",
                                      command=self.generate_random_password, **button_style)
        self.random_button.pack(side="left")
        
        # HASIL HASH (BESAR dan JELAS)
        hash_frame = tk.LabelFrame(main_frame, text=" HASH RESULT ", 
                                  font=("Arial", 11, "bold"),
                                  bg=self.current_colors["frame_bg"],
                                  fg=self.current_colors["fg"],
                                  padx=15, pady=15)
        hash_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Hash output dengan font BESAR
        self.hash_text = tk.Text(hash_frame, height=4, font=("Consolas", 11),
                                wrap="word", bg=self.current_colors["hash_bg"],
                                fg=self.current_colors["hash_fg"],
                                relief="flat", padx=10, pady=10)
        self.hash_text.pack(fill="both", expand=True)
        
        # Scrollbar untuk hash
        hash_scroll = tk.Scrollbar(self.hash_text)
        hash_scroll.pack(side="right", fill="y")
        self.hash_text.config(yscrollcommand=hash_scroll.set)
        hash_scroll.config(command=self.hash_text.yview)
        
        # Action Buttons untuk Hash
        hash_actions = tk.Frame(hash_frame, bg=self.current_colors["frame_bg"])
        hash_actions.pack(fill="x", pady=(10, 0))
        
        self.copy_button = tk.Button(hash_actions, text="📋 COPY", 
                                    bg="#f39c12", fg="white",
                                    font=("Arial", 9, "bold"), padx=10, pady=5,
                                    command=self.copy_hash)
        self.copy_button.pack(side="left", padx=(0, 10))
        
        self.verify_button = tk.Button(hash_actions, text="✅ VERIFY", 
                                      bg="#3498db", fg="white",
                                      font=("Arial", 9, "bold"), padx=10, pady=5,
                                      command=self.verify_password)
        self.verify_button.pack(side="left", padx=(0, 10))
        
        self.clear_button = tk.Button(hash_actions, text="🧹 CLEAR", 
                                     bg="#e74c3c", fg="white",
                                     font=("Arial", 9, "bold"), padx=10, pady=5,
                                     command=self.clear_all)
        self.clear_button.pack(side="left")
        
        # Hash Info
        self.hash_info = tk.Label(hash_frame, text="", 
                                 font=("Arial", 9),
                                 bg=self.current_colors["frame_bg"])
        self.hash_info.pack(anchor="w", pady=(5, 0))
        
        # Footer
        footer_frame = tk.Frame(main_frame, bg=self.current_colors["bg"])
        footer_frame.pack(fill="x")
        
        tk.Label(footer_frame, text="BCrypt 2b | Salt auto | Adaptive", 
                font=("Arial", 8),
                bg=self.current_colors["bg"]).pack()
    
    def apply_theme(self):
        """Apply current theme colors"""
        colors = self.current_colors
        
        self.root.configure(bg=colors["bg"])
        
        # Update semua widget
        for widget in self.root.winfo_children():
            self.update_widget_colors(widget, colors)
    
    def update_widget_colors(self, widget, colors):
        """Update colors for widget and its children"""
        widget_type = str(widget.winfo_class())
        
        try:
            if widget_type in ('Frame', 'TFrame', 'Labelframe', 'LabelFrame'):
                widget.configure(bg=colors.get("frame_bg", colors["bg"]))
            elif widget_type == 'Label':
                if 'fg' in widget.keys():
                    widget.configure(fg=colors["fg"])
                if 'bg' in widget.keys():
                    widget.configure(bg=colors.get("frame_bg", colors["bg"]))
            elif widget_type == 'Button':
                if widget['text'] not in ['🔒 GENERATE HASH', '🎲 RANDOM', '📋 COPY', '✅ VERIFY', '🧹 CLEAR']:
                    widget.configure(bg=colors["button_bg"], fg=colors["button_fg"])
            elif widget_type == 'Entry':
                widget.configure(bg=colors["entry_bg"], fg=colors["entry_fg"])
            elif widget_type == 'Text':
                widget.configure(bg=colors["hash_bg"], fg=colors["hash_fg"])
            elif widget_type == 'Radiobutton':
                widget.configure(bg=colors["bg"], fg=colors["fg"])
        except:
            pass
        
        # Update children
        for child in widget.winfo_children():
            self.update_widget_colors(child, colors)
    
    def toggle_mode(self):
        """Toggle dark/light mode"""
        self.dark_mode = not self.dark_mode
        
        if self.dark_mode:
            self.current_colors = self.dark_colors
            self.mode_button.config(text="☀️")
        else:
            self.current_colors = self.light_colors
            self.mode_button.config(text="🌙")
        
        self.apply_theme()
    
    def check_password_strength(self, event=None):
        """Check password strength"""
        password = self.password_entry.get()
        
        if not password:
            self.strength_label.config(text="Strength: -")
            return
        
        score = 0
        if len(password) >= 8: score += 1
        if len(password) >= 12: score += 1
        if any(c.islower() for c in password): score += 1
        if any(c.isupper() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(c in "!@#$%^&*" for c in password): score += 2
        
        if score >= 6:
            level = "VERY STRONG"
            color = "#27ae60"
        elif score >= 4:
            level = "STRONG"
            color = "#2ecc71"
        elif score >= 2:
            level = "MEDIUM"
            color = "#f39c12"
        else:
            level = "WEAK"
            color = "#e74c3c"
        
        self.strength_label.config(text=f"Strength: {level}", fg=color)
    
    def update_cost_info(self):
        """Update cost factor info"""
        cost = self.cost_var.get()
        times = {8: "0.01s", 10: "0.05s", 12: "0.15s", 14: "0.6s"}
        self.cost_info.config(text=f"{cost} rounds (~{times.get(cost, '?')})")
    
    def generate_hash(self):
        """Generate BCrypt hash"""
        password = self.password_entry.get().strip()
        
        if not password:
            messagebox.showwarning("Warning", "Enter password first!")
            return
        
        # Show loading
        self.hash_button.config(text="⏳ PROCESSING...", state="disabled")
        self.root.update()
        
        try:
            cost = self.cost_var.get()
            salt = bcrypt.gensalt(rounds=cost)
            
            start_time = time.time()
            hashed = bcrypt.hashpw(password.encode(), salt)
            hash_time = time.time() - start_time
            
            self.current_hash = hashed.decode('utf-8')
            
            # Display hash in LARGE text
            self.hash_text.delete("1.0", tk.END)
            self.hash_text.insert("1.0", self.current_hash)
            
            # Make hash text even bigger and bold
            self.hash_text.tag_add("hash", "1.0", "end")
            self.hash_text.tag_config("hash", font=("Consolas", 12, "bold"))
            
            # Add info below
            info = f"✓ Hash generated | Cost: {cost} rounds | Time: {hash_time:.3f}s | Length: {len(self.current_hash)} chars"
            self.hash_info.config(text=info, fg="#27ae60")
            
            # Enable verify button
            self.verify_button.config(state="normal")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {str(e)}")
            self.hash_info.config(text="✗ Failed to generate hash", fg="#e74c3c")
        
        finally:
            self.hash_button.config(text="🔒 GENERATE HASH", state="normal")
    
    def verify_password(self):
        """Verify password with current hash"""
        if not self.current_hash:
            messagebox.showwarning("Warning", "Generate hash first!")
            return
        
        # Simple verification dialog
        verify_window = tk.Toplevel(self.root)
        verify_window.title("Verify Password")
        verify_window.geometry("350x200")
        verify_window.configure(bg=self.current_colors["frame_bg"])
        
        # Center window
        verify_window.transient(self.root)
        verify_window.grab_set()
        
        tk.Label(verify_window, text="Enter password to verify:", 
                font=("Arial", 11),
                bg=self.current_colors["frame_bg"]).pack(pady=(20, 10))
        
        verify_entry = tk.Entry(verify_window, font=("Arial", 12), 
                              show="•", width=30)
        verify_entry.pack(pady=10)
        
        result_label = tk.Label(verify_window, text="", 
                               font=("Arial", 12, "bold"),
                               bg=self.current_colors["frame_bg"])
        result_label.pack(pady=10)
        
        def perform_verify():
            test_pass = verify_entry.get()
            if not test_pass:
                result_label.config(text="Enter password!", fg="orange")
                return
            
            try:
                if bcrypt.checkpw(test_pass.encode(), self.current_hash.encode()):
                    result_label.config(text="✅ MATCH!", fg="#27ae60")
                else:
                    result_label.config(text="❌ NO MATCH!", fg="#e74c3c")
            except:
                result_label.config(text="Error!", fg="red")
        
        tk.Button(verify_window, text="VERIFY", 
                 bg="#3498db", fg="white",
                 font=("Arial", 10, "bold"),
                 command=perform_verify).pack(pady=5)
        
        verify_entry.focus()
        verify_entry.bind("<Return>", lambda e: perform_verify())
    
    def generate_random_password(self):
        """Generate random secure password"""
        length = 16
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        
        password_chars = [
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.digits),
            secrets.choice("!@#$%^&*")
        ]
        password_chars += [secrets.choice(alphabet) for _ in range(length - 4)]
        secrets.SystemRandom().shuffle(password_chars)
        password = ''.join(password_chars)
        
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.check_password_strength()
    
    def copy_hash(self):
        """Copy hash to clipboard"""
        if not self.current_hash:
            messagebox.showwarning("Warning", "No hash to copy!")
            return
        
        pyperclip.copy(self.current_hash)
        
        # Visual feedback
        self.copy_button.config(text="✓ COPIED!", bg="#27ae60", fg="white")
        self.root.after(1000, lambda: self.copy_button.config(
            text="📋 COPY", bg="#f39c12", fg="white"
        ))
    
    def clear_all(self):
        """Clear all inputs and outputs"""
        self.password_entry.delete(0, tk.END)
        self.hash_text.delete("1.0", tk.END)
        self.current_hash = None
        self.hash_info.config(text="")
        self.strength_label.config(text="Strength: -")
        self.cost_var.set(12)
        self.update_cost_info()
        self.verify_button.config(state="disabled")

def main():
    try:
        import bcrypt
    except ImportError:
        print("Install bcrypt first: pip install bcrypt")
        return
    
    root = tk.Tk()
    app = BCryptCompactApp(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
