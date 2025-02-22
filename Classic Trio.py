import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import string
from getpass import getpass


#Check if Prime
def isPrime(x):
    p = 1
    if x == 1:
        p = 0
    elif x == 2:
        p = 1
    else:
        i = 2
        while i <= math.sqrt(x):
            if x % i == 0:
                p = 0
                break
            i += 1
    return p == 1

#Encryption and Decryption Functions
def Encrypt(text, vigenere_key, key):
    letters = "abcdefghijklmnopqrstuvwxyz"
    text = text.replace(" ", "~").lower()
    cipher_text = text
    steps = []

    # Prime Check & Random Character Addition
    x = len(text)
    if isPrime(x):
        random_character = random.choice(string.ascii_lowercase)
        cipher_text += random_character
        if(x==2):
            random_character = random.choice(string.ascii_lowercase)
            cipher_text += random_character

        steps.append(f"After Prime Check (random char added): {cipher_text}")

    # Transposition Step
    x = len(cipher_text)       
    div = []
    i = 1
    while (i <= math.sqrt(x)):
        if (x % i == 0):
            div.append(int(i))
            if (x / i != i):
                div.append(int(x / i))
        i += 1

    div.sort()
    # reversing each substring
    i = 0
    while (i < (len(div) - 1)):
        sub = cipher_text[div[i] - 1:div[i + 1]]
        cipher_text = cipher_text.replace(sub, sub[::-1])
        i += 1
    steps.append(f"After Transposition: {cipher_text}")

    # Caesar Cipher
    caesar_text = ""
    for char in cipher_text:
        if char in letters:
            number = (letters.index(char) + int(key)) % 26
            caesar_text += letters[number]
        else:
            caesar_text+=char
    steps.append(f"After Caesar Cipher: {caesar_text}")

    # Vigenère Cipher
    vigenere_key = (vigenere_key * (len(caesar_text) // len(vigenere_key) + 1))[:len(caesar_text)]
    vigenere_text = ""
    for i in range(len(caesar_text)):
        if caesar_text[i] in letters:
            shift = (letters.index(caesar_text[i]) + letters.index(vigenere_key[i])) % 26
            vigenere_text += letters[shift]
        else:
            vigenere_text+=caesar_text[i]
    steps.append(f"After Vigenère Cipher: {vigenere_text}")

    return steps


def Decrypt(text, vigenere_key, key):
    letters = "abcdefghijklmnopqrstuvwxyz"
    steps = []
    text=text.replace('~',' ')
    # Reverse Vigenère Cipher
    vigenere_key = (vigenere_key * (len(text) // len(vigenere_key) + 1))[:len(text)]
    caesar_text = ""
    for i in range(len(text)):
        if text[i] in letters:
            shift = (letters.index(text[i]) - letters.index(vigenere_key[i]) + 26) % 26
            caesar_text += letters[shift]
        else:
            caesar_text+=text[i]
    steps.append(f"After Reverse Vigenère: {caesar_text}")

    # Reverse Caesar Cipher
    transposition_text = ""
    for char in caesar_text:
        if char in letters:
            number = (letters.index(char) - int(key)) % 26
            transposition_text += letters[number]
        else:
            transposition_text+=char
    steps.append(f"After Reverse Caesar Cipher: {transposition_text}")

    # Reverse Transposition
    x = len(transposition_text)
    div = []

    i = 1
    while (i <= math.sqrt(x)):
        if (x % i == 0):
            div.append(int(i))
            if (x / i != i):
                div.append(int(x / i))
        i += 1

    div.sort(reverse=True)

    i = 0
    # reversing
    while i < len(div) - 1:
        sub = transposition_text[div[i + 1] - 1:div[i]]
        transposition_text = transposition_text.replace(sub, sub[::-1])

        i += 1

    steps.append(f"After Reverse Transposition: {transposition_text}")

    return steps


# GUI Wrapper
class CipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Step-by-Step Encryption/Decryption Tool")
        self.root.geometry("500x600")
        self.root.configure(bg="#F0F0F0")

        # Title Label
        title_label = tk.Label(root, text="Encryption/Decryption Tool", font=("Helvetica", 16, "bold"), bg="#F0F0F0")
        title_label.pack(pady=10)

        # Input Frame
        input_frame = tk.Frame(root, bg="#F0F0F0")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Text (hidden) :", bg="#F0F0F0").grid(row=0, column=0, sticky="w", pady=5)
        self.text_entry = tk.Entry(input_frame, width=40, show="*")
        self.text_entry.grid(row=0, column=1, pady=5)

        tk.Label(input_frame, text="Vigenère Key:", bg="#F0F0F0").grid(row=1, column=0, sticky="w", pady=5)
        self.vigenere_entry = tk.Entry(input_frame, width=40)
        self.vigenere_entry.grid(row=1, column=1, pady=5)

        tk.Label(input_frame, text="Caesar Key (number):", bg="#F0F0F0").grid(row=2, column=0, sticky="w", pady=5)
        self.caesar_entry = tk.Entry(input_frame, width=40)
        self.caesar_entry.grid(row=2, column=1, pady=5)

        # Action Buttons
        button_frame = tk.Frame(root, bg="#F0F0F0")
        button_frame.pack(pady=10)

        self.action_var = tk.StringVar(value="Encrypt")
        encrypt_button = ttk.Radiobutton(button_frame, text="Encrypt", variable=self.action_var, value="Encrypt")
        encrypt_button.grid(row=0, column=0, padx=10)

        decrypt_button = ttk.Radiobutton(button_frame, text="Decrypt", variable=self.action_var, value="Decrypt")
        decrypt_button.grid(row=0, column=1, padx=10)

        run_button = tk.Button(button_frame, text="Run", command=self.run_cipher, bg="#4CAF50", fg="white",
                               font=("Helvetica", 10, "bold"))
        run_button.grid(row=0, column=2, padx=10)

        # Output Textbox
        self.output_text = tk.Text(root, height=20, width=60, wrap=tk.WORD, bg="white")
        self.output_text.pack(pady=10)

    def run_cipher(self):
        text = self.text_entry.get()
        vigenere_key = self.vigenere_entry.get()
        caesar_key = self.caesar_entry.get()

        # Validation
        if not text or not vigenere_key or not caesar_key.isdigit():
            messagebox.showerror("Input Error", "Please enter valid text, Vigenère key, and Caesar key (number).")
            return

        # Process
        action = self.action_var.get()
        if action == "Encrypt":
            steps = Encrypt(text, vigenere_key, caesar_key)
        else:
            steps = Decrypt(text, vigenere_key, caesar_key)

        # Display Results Step-by-Step
        self.output_text.delete("1.0", tk.END)
        for step in steps:
            self.output_text.insert(tk.END, step + "\n\n")


# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = CipherApp(root)
    root.mainloop()