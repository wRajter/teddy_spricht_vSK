import random
import tkinter as tk
import tkinter.messagebox
import pandas as pd
from tkinter import ttk
from tkinter import *
# import unidecode
from tkinter import PhotoImage


LARGE_FONT = ("Courier", 20, "bold")
MEDIUM_FONT = ("Courier", 15)
BACKGROUND_COLOR = "#6699CC"
# BACKGROUND_COLOR_ALT = "#B1DDC6"


class LanguageWorkout(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        tk.Tk.title(self, "Teddy spricht")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty dictionary
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (HomePage, WorkoutPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.config(background=BACKGROUND_COLOR)
            frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
            # frame.grid(row=0, column=0, sticky="nsew")

        # initializing frame of that object from
        # home page, Spending, Profit etc. respectively with
        # for loop
        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# first window frame home page
class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Hlavná stránka", font=LARGE_FONT,
                          background=BACKGROUND_COLOR,
                          foreground="#FFFFFF")
        label.grid(row=0, column=0, pady=20, padx=40)

        # WORKOUT
        pic_flag = PhotoImage(file="figs/de_to_svk_small.png")
        pic_flag_resize = pic_flag.subsample(3, 3)

        button1 = tk.Button(self, text="Prekladat ",
                            font=MEDIUM_FONT,
                            background=BACKGROUND_COLOR,
                            highlightbackground=BACKGROUND_COLOR,
                            foreground="#FFFFFF",
                            image=pic_flag_resize,
                            compound=RIGHT,
                            command=lambda: controller.show_frame(WorkoutPage))
        button1.image = pic_flag_resize
        button1.grid(row=1, column=0, pady=20, padx=40)

        button2 = tk.Button(self, text="Slovník DE->SVK", width=15, height=1,
                            font=MEDIUM_FONT,
                            background=BACKGROUND_COLOR,
                            highlightbackground=BACKGROUND_COLOR,
                            foreground="#FFFFFF",
                            command=lambda: controller.show_frame(Vocabulary))
        button2.grid(row=2, column=0, pady=20, padx=40, ipadx=30, ipady=5)


class WorkoutPage(tk.Frame):
    words = pd.read_csv("data/german_words_1500_SK.csv")
    dict_words = words.to_dict(orient="records")
    current_word = dict((random.choice(dict_words)))
    print(current_word)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.question = ttk.Label(self, text=f"Prelož '{self.current_word['German']}'",
                                  font=LARGE_FONT,
                                  background=BACKGROUND_COLOR,
                                  foreground="#FFFFFF")
        self.question.grid(row=0, column=0, pady=20, padx=40, sticky="w")

        # USER ENTRY
        self.translation_entry = ttk.Entry(self, width=15, font=MEDIUM_FONT)
        self.translation_entry.bind('<Return>', self.checking_answer)
        self.translation_entry.grid(row=1, column=0, pady=20, padx=40)

        # CHECK BUTTON
        self.check_button = Button(self, text="Skontroluj", width=12, height=1,
                                   font=MEDIUM_FONT,
                                   background=BACKGROUND_COLOR,
                                   highlightbackground=BACKGROUND_COLOR,
                                   foreground="#FFFFFF",
                                   command=self.checking_answer)
        self.check_button.grid(row=2, column=0, pady=20, padx=40)

        # BACK HOME BUTTON
        button2 = ttk.Button(self, text="Spät",
                             command=lambda: controller.show_frame(HomePage))
        button2.grid(row=3, column=0, pady=20, padx=40)

        # BRAIN TEDDY
        # self.canvas_brain1 = Canvas(self, width=320, height=300)
        # self.brain1 = PhotoImage(file="images/image843.png")
        # self.canvas_brain1.create_image(10, 40, anchor=NW, image=self.brain1)
        # #self.canvas_brain1.config(bg=BACKGROUND_COLOR, highlightthickness=0)
        # self.canvas_brain1.grid(row=0, column=1, rowspan=3)

    def random_word(self):
        self.current_word = (random.choice(self.dict_words))
        print(self.current_word["German"].lower())

    def checking_answer(self, *args):
        user_input = unidecode(self.translation_entry.get().lower())  # unidecode removes diacritics
        answer_split = self.current_word['Slovak'].split('/')   # split into possible answers if more than one
        answer_adjusted = [unidecode(word.lower())
                           for word
                           in answer_split] # removing diacritics and making lowercase letters
        print(answer_adjusted)
        if user_input in answer_adjusted:
            self.question.config(text=f"Správne!\n{self.current_word['German']} znamená {', '.join(answer_adjusted)}")
            self.check_button.config(text="Dalšie slovo", command=self.next_word)
            self.translation_entry.bind('<Shift_R>', self.next_word)
        else:
            self.question.config(text=f"'{self.current_word['German']}' znamená {', '.join(answer_adjusted)}")
            self.check_button.config(text="Dalšie slovo", command=self.next_word)
            self.translation_entry.bind('<Shift_R>', self.next_word)

    def next_word(self, *args):
        self.random_word()
        self.translation_entry.delete(0, "end")
        self.check_button.config(text="Skontroluj", command=self.checking_answer)
        self.question.config(text=f"Prelož '{self.current_word['German']}'")


class Vocabulary(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def save_txt():
            with open('data/german_words_1500_SK.csv', 'w', encoding="utf8") as f:
                f.write(self.text_box.get(1.0, END))
            tkinter.messagebox.showinfo(title='Slovník', message='Zmeny boli úspešne uložené.')

        with open('data/german_words_1500_SK.csv', 'r', encoding="utf8") as f:
            text = f.read()

        # scrollbar
        self.text_scroll = Scrollbar(self)
        self.text_scroll.grid(row=0, column=2, sticky='ns')

        # text box
        self.text_box = Text(self, width=40, height=10, font=MEDIUM_FONT, undo=True, yscrollcommand=self.text_scroll.set)
        self.text_box.insert(END, text)
        self.text_box.grid(row=0, column=0, pady=10, padx=0, columnspan=2)

        # config scrollbar
        self.text_scroll.config(command=self.text_box.yview)

        # save button
        self.save = ttk.Button(self, text='Uložit zmeny', command=save_txt)
        self.save.grid(row=1, column=0, pady=20, padx=10)

        # BACK HOME BUTTON
        button2 = ttk.Button(self, text="Spät",
                             command=lambda: controller.show_frame(HomePage))
        button2.grid(row=1, column=1, pady=20, padx=40)


app = LanguageWorkout()
app.mainloop()



