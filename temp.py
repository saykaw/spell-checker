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

        self.my_dict = set()
        with open("mydict.txt", "r") as f:
            self.my_dict = set(f.read().split("\n"))
        self.my_dict.remove('')

        self.word_list = self.my_dict
        self.last_pos = 0
        self.old_spaces = 0

        self.word_suggestions = {}

        self.mainloop()

    def check(self, event):
        content = self.text.get("1.0", tk.END)
        space_count = content.count(" ")

        for word in self.wrong_words:
            if word not in content or word in self.word_list:
                self.text.tag_delete(word)


        if space_count != self.old_spaces:
            self.old_spaces = space_count
            for word in content.split(" "):
                word = re.sub(r"[^\w]", "", word.lower())
                if word in self.word_list and word not in self.checked_words:
                    self.checked_words.add(word)
                if word not in self.word_list and word not in self.checked_words:
                    cursor_index = self.text.index(tk.INSERT)
                    position = content.lower().find(word)
                    self.text.tag_add(word, f"1.{position}", f"1.{position + len(word)}")
                    self.text.tag_config(word, foreground="red")
                    self.text.tag_bind(word, "<Double-Button>", self.show_suggestions)
                    self.wrong_words.add(word)
       
    def show_suggestions(self, event):
        word = self.text.tag_names(tk.CURRENT)[0]
        self.word_suggestions[word] = spell.suggest(word)
        suggestions = self.word_suggestions[word]
        if suggestions:
            suggestion_menu = tk.Menu(self, tearoff=0, font=("Roboto", 14))
            for suggestion in suggestions:
                suggestion_menu.add_command(label=suggestion, command=lambda w=word, s=suggestion: self.replace_word(w, s))
            self.add_word_option(suggestion_menu, word) # Call the new method to add the "Add Word to Dictionary" option
            suggestion_menu.tk_popup(self.winfo_pointerx(), self.winfo_pointery()) # Show the menu at the mouse position
            self.text.tag_bind(tk.CURRENT, '<Button-3>', lambda event: suggestion_menu.post(event.x_root, event.y_root))



    def replace_word(self, word, suggestion):
        start = self.text.search(word, '1.0', tk.END)
        end = f"{start}+{len(word)}c"
        self.text.delete(start, end)
        self.text.insert(start, suggestion)

    def add_word_option(self, suggestion_menu, word):
        suggestion_menu.add_command(label="Add Word to Dictionary", command=lambda:self.add_word_to_dict(word))

    def add_word_to_dict(self, word):
        
        print(word)
        if word:
            with open("mydict.txt", "a") as f:
                f.write(word + "\n")
            self.word_list.add(word)
            self.bind("<Motion>", self.check)


App()