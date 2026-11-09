import tkinter as tk
from math import log2

COMMON_PASSWORDS = {"123456", "password", "abc123", "111111"}

def calculate_entropy(password):
    pool = 0
    if any(c.islower() for c in password): pool += 26
    if any(c.isupper() for c in password): pool += 26
    if any(c.isdigit() for c in password): pool += 10
    if any(c in "!@#$%^&*()_+" for c in password): pool += 12
    if pool == 0: return 0
    return len(password) * log2(pool)

def analyze_password(password):
    suggestions = []
    if password.lower() in COMMON_PASSWORDS:
        return ("WEAK ❌", "#FF4B4B", ["This is a very common password!"])
    
    score = 0
    if len(password) >= 12: score += 2
    elif len(password) >= 8: score += 1
    else: suggestions.append("Use at least 8–12 characters")
    
    if any(c.islower() for c in password): score += 1
    else: suggestions.append("Add lowercase letters")
    if any(c.isupper() for c in password): score += 1
    else: suggestions.append("Add uppercase letters")
    if any(c.isdigit() for c in password): score += 1
    else: suggestions.append("Add numbers")
    if any(c in "!@#$%^&*()_+" for c in password): score += 1
    else: suggestions.append("Add special characters")
    
    if len(set(password)) < len(password) / 2:
        score -= 1
        suggestions.append("Avoid repeated characters")
    
    entropy = calculate_entropy(password)

    if score >= 6 and entropy > 60:
        return ("STRONG ✅", "#00FF7F", suggestions)
    elif score >= 4:
        return ("MEDIUM ⚠️", "#FFA500", suggestions)
    else:
        return ("WEAK ❌", "#FF4B4B", suggestions)


def update_strength(*args):
    password = entry.get()
    if not password:
        result_label.config(text="WAITING FOR INPUT", fg="#555555")
        suggestion_label.config(text="")
        return
    
    strength, color, suggestions = analyze_password(password)
    result_label.config(text=f"{strength}", fg=color)
    
    if suggestions:
        suggestion_label.config(text="\n".join([f"• {s}" for s in suggestions]))
    else:
        suggestion_label.config(text="Security Verified! ✔️", fg="#00FF7F")

def toggle_password():
    if entry.cget('show') == '*':
        entry.config(show='')
        eye_btn.config(text='🙈')
    else:
        entry.config(show='*')
        eye_btn.config(text='👁')

root = tk.Tk()
root.title("Bakhtawar Mochi's Security")
root.geometry("450x550")
root.configure(bg="#0F0F0F")

tk.Label(root, text="Password Checker", font=("Impact", 28), 
         bg="#0F0F0F", fg="#00FF7F").pack(pady=(30, 5))
tk.Label(root, text="Protected by Bakhtawar Mochi", font=("Arial", 9), 
         bg="#0F0F0F", fg="#444444").pack(pady=(0, 20))

card = tk.Frame(root, bg="#1A1A1A", padx=30, pady=30, highlightthickness=1, highlightbackground="#333")
card.pack(padx=40, fill="both", expand=True)

tk.Label(card, text="Input Password", font=("Arial", 10, "bold"), 
         bg="#1A1A1A", fg="#888888").pack(anchor="w")

input_frame = tk.Frame(card, bg="#252525", bd=0)
input_frame.pack(fill="x", pady=10)

entry = tk.Entry(input_frame, show="*", font=("Consolas", 14), 
                 bg="#252525", fg="white", borderwidth=0, 
                 insertbackground="white", highlightthickness=0)
entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")
entry.bind("<KeyRelease>", update_strength)

eye_btn = tk.Button(input_frame, text="👁", command=toggle_password, 
                    bg="#252525", fg="#888", relief="flat", 
                    activebackground="#333", cursor="hand2")
eye_btn.pack(side="right", padx=5)

tk.Frame(card, height=1, bg="#333").pack(fill="x", pady=20)

result_label = tk.Label(card, text="WAITING FOR INPUT", font=("Arial", 16, "bold"), 
                        bg="#1A1A1A", fg="#555555")
result_label.pack()

suggestion_label = tk.Label(card, text="", font=("Arial", 10), 
                            bg="#1A1A1A", fg="#AAAAAA", justify="left")
suggestion_label.pack(pady=20)

root.mainloop()