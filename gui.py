import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import tkinter.messagebox
import nltk
from nltk.corpus import words
from spellchecker import SpellChecker 
import re

spell = SpellChecker()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.checked_words = set()
        self.wrong_words = set()
        # configure window
        self.title("Spell Checker")
        self.geometry(f"{720}x{480}")

        self.text = ScrolledText(self, font = ("Roboto", 16))
        self.text.bind("<KeyRelease>", self.check)
        self.text.pack()

        self.word_list = set(word.lower() for word in words.words())
        self.last_pos = 0
        self.old_spaces = 0

        self.word_suggestions = {}

        self.mainloop()

    def check(self, event):
        content = self.text.get("1.0", tk.END)
        space_count = content.count(" ")

        for word in self.wrong_words:
            if word not in content:
                self.text.tag_delete(word)


        if space_count != self.old_spaces:
            self.old_spaces = space_count
            for word in content.split(" "):
                word = re.sub(r"[^\w]", "", word.lower())
                if word in self.word_list and word not in self.checked_words:
                    self.checked_words.add(word)
                if word not in self.word_list and word not in self.checked_words:
                    cursor_index = self.text.index(tk.INSERT)
                    position = content.find(word)
                    self.text.tag_add(word, f"1.{position}", f"1.{position + len(word)}")
                    self.text.tag_config(word, foreground="red")
                    self.text.tag_bind(word, "<Button-1>", self.show_suggestions)
                    self.wrong_words.add(word)

    # def show_suggestions(self, event):
    #     word = self.text.tag_names(tk.CURRENT)[0]
    #     self.word_suggestions[word] = spell.suggest(word)
    #     suggestions = self.word_suggestions[word]
    #     if suggestions:
    #         suggestion_window = tk.Toplevel(self)
    #         suggestion_window.title("Suggestions")
    #         suggestion_window.geometry("300x200")
    #         suggestion_list = tk.Listbox(suggestion_window, font=("Roboto", 14))
    #         for suggestion in suggestions:
    #             suggestion_list.insert(tk.END, suggestion)
    #         suggestion_list.pack(fill=tk.BOTH, expand=True)

    def show_suggestions(self, event):
        word = self.text.tag_names(tk.CURRENT)[0]
        self.word_suggestions[word] = spell.suggest(word)
        suggestions = self.word_suggestions[word]
        if suggestions:
            suggestion_menu = tk.Menu(self, tearoff=0, font=("Roboto", 14))
            for suggestion in suggestions:
                suggestion_menu.add_command(label=suggestion, command=lambda w=word, s=suggestion: self.replace_word(w, s))
            suggestion_menu.tk_popup(self.winfo_pointerx(), self.winfo_pointery()) # Show the menu at the mouse position
            self.text.tag_bind(tk.CURRENT, '<Button-3>', lambda event: suggestion_menu.post(event.x_root, event.y_root))

    def replace_word(self, word, suggestion):
        start = self.text.search(word, '1.0', tk.END)
        end = f"{start}+{len(word)}c"
        self.text.delete(start, end)
        self.text.insert(start, suggestion)

App()