import tkinter as tk
from tkinter import scrolledtext, messagebox
import csv
import os

# ---------------- Load dictionary from CSV ----------------
def load_dictionary_from_csv(file_path="dic.csv"):
    dictionary = {}
    if not os.path.exists(file_path):
        messagebox.showerror("Error", f"CSV file not found:\n{file_path}")
        return dictionary
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = str(row.get("name", "")).strip().lower()
                meaning = str(row.get("meaning", "")).strip()
                if word:
                    dictionary[word] = meaning
    except UnicodeDecodeError:
        # fallback for non-UTF8 CSV
        with open(file_path, "r", encoding="latin-1") as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = str(row.get("name", "")).strip().lower()
                meaning = str(row.get("meaning", "")).strip()
                if word:
                    dictionary[word] = meaning
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load CSV file:\n{e}")
    return dictionary

# ---------------- GUI ----------------
class DictApp:
    def __init__(self, root, dictionary):
        self.root = root
        self.dictionary = dictionary
        self.words_sorted = sorted(dictionary.keys())

        root.title("Student Dictionary Search")
        root.geometry("700x450")

        # Search bar
        top = tk.Frame(root)
        top.pack(fill="x", padx=8, pady=6)

        tk.Label(top, text="Search:").pack(side="left", padx=(10, 4))
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(top, textvariable=self.search_var, width=40)
        self.search_entry.pack(side="left")
        self.search_entry.bind("<KeyRelease>", self.on_type)
        self.search_entry.bind("<Return>", self.find_word)

        # Suggestions
        left = tk.Frame(root)
        left.pack(side="left", fill="y", padx=8, pady=6)

        tk.Label(left, text="Suggestions:").pack(anchor="w")
        self.listbox = tk.Listbox(left, width=30, height=20)
        self.listbox.pack(side="left", fill="y")
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # Meaning area
        right = tk.Frame(root)
        right.pack(side="left", fill="both", expand=True, padx=8, pady=6)

        tk.Label(right, text="Meaning:").pack(anchor="w")
        self.meaning_area = scrolledtext.ScrolledText(right, wrap="word", height=20)
        self.meaning_area.pack(fill="both", expand=True)

        # Show first few suggestions
        self.update_suggestions()

    def update_suggestions(self, prefix=""):
        self.listbox.delete(0, tk.END)
        prefix = prefix.lower()
        if not prefix:
            for w in self.words_sorted[:200]:
                self.listbox.insert(tk.END, w)
        else:
            matches = [w for w in self.words_sorted if prefix in w]
            for w in matches[:200]:
                self.listbox.insert(tk.END, w)

    def on_type(self, event=None):
        q = self.search_var.get().strip()
        self.update_suggestions(q)

    def on_select(self, event=None):
        sel = self.listbox.curselection()
        if sel:
            word = self.listbox.get(sel[0])
            self.search_var.set(word)
            self.show_meaning(word)

    def find_word(self, event=None):
        q = self.search_var.get().strip().lower()
        if q in self.dictionary:
            self.show_meaning(q)
        else:
            messagebox.showinfo("Not found", f"No entry found for '{q}'")

    def show_meaning(self, word):
        meaning = self.dictionary.get(word.lower(), "")
        self.meaning_area.delete("1.0", tk.END)
        self.meaning_area.insert(tk.END, meaning if meaning else "(No meaning available)")

# ---------------- Main ----------------
if __name__ == "__main__":
    root = tk.Tk()
    dictionary = load_dictionary_from_csv("dic.csv")  # replace with your CSV file name
    app = DictApp(root, dictionary)
    root.mainloop()
