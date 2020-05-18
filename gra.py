﻿import random
import time
from tkinter import *

saguhaghgirw
eafisbieg
asdhugibsrb
uaiegrs


def word_count():

    f = open("baza slow.txt", "r", encoding="utf-8")            # otwarcie pliku tekstowego
    database = f.read().split()                                 # zapisanie każdego słowa w tablicy

                                                                # Wyznaczenie ilości słów w poszczególnych poziomach trudności
    easy = -1                                                   # odrzucenie słowa "łatwe"
    medium = -1                                                 # odrzucenie słowa "średnie"
    i = 0

    while (database[i] != "Średnie:"):                          # przeliczenie słów z poziomu łatwego
        easy += 1
        i += 1

    while (database[i] != "Trudne:"):                           # przeliczenie słów z poziomu średniego
        medium += 1
        i += 1

    hard = len(database) - easy - medium - 3                    # przeliczenie słow z poziomu łatwego
    f.close()                                                   # zamknięcie pliku tekstowego
    return database, easy, medium, hard


def check(frame, i, words):
    frame.destroy()
    print("dobrze jest")
    return # powrót do odpowiedniego view


def view(frame, i, words, n):                                   # wyświetlanie po kliknięciu
    print(words[0*n])
    frame.destroy()
    if n > 0:
        frame1 = Frame(window)
        frame1.grid()
        label = Label(frame1, text="Tura " + str(i + 1), font=("Arial", 24,))
        label.grid()
        word = Label(frame1, text=words[0])
        word.grid()
        print(words[0])
        if n > 1:
            button = Button(frame1, text="Następne słowo >>", command=lambda: view(frame1, i, words[1:], n - 1))
            button.grid()
        else:
            button = Button(frame1, text="Sprawdź ile pamiętasz!", command=lambda: check(frame1, i, words))
            button.grid()
        frame1.mainloop()
    return


def view_on_time(frame, i, words, n, t):                           # wyświetlanie po czasie
    frame.destroy()
    if n > 0:
        frame1 = Frame(window)
        frame1.grid()
        label = Label(frame1, text="Tura " + str(i + 1), font=("Arial", 24,))
        label.grid()
        word = Label(frame1, text=words[0])
        word.grid()
        print(words[0])
        frame1.mainloop()
        time.sleep(t)
        view_on_time(frame1, i, words[1:], n - 1, t)
        #frame1.after(t*1000, view_on_time(frame1, i, words[1:], n-1, t))
    else:
        return


def draw(level, n):                                             # Losowanie n słów z odpowiedniego poziomu trudności
    if level == 1:
        words = random.sample(database[1:easy], n)
    elif level == 2:
        words = random.sample(database[easy+2:easy+medium+2], n)
    elif level == 3:
        words = random.sample(database[len(database)-hard:], n)
    return words


def zabawa(frame, level, mode):                                 # działanie gry
    frame.forget()
    if mode == 1:

        if level == 1:
            # dźwięk
            words = draw(level, 3*flashcards[0])
            for i in range(3):
                view(frame, i, words[i*flashcards[0]:], flashcards[0])

        elif level == 2:
            # dźwięk
            words = draw(level, 3 * flashcards[1])
            for i in range(3):
                view(frame, i, words[i*flashcards[1]:], flashcards[1])

        elif level == 3:
            # dźwięk
            words = draw(level, 3 * flashcards[2])
            for i in range(3):
                view(frame, i, words[i*flashcards[2]:], flashcards[2])

    elif mode == 2:
        print("<krótka instrukcja>")

        if level == 1:
            # dźwięk
            words = draw(level, 3 * on_time[0])
            for i in range(3):
                view_on_time(frame, i, words[i*on_time[0]:], on_time[0], T[0])

        elif level == 2:
            # dźwięk
            words = draw(level, 3 * on_time[1])
            for i in range(3):
                view_on_time(frame, i, words[i*on_time[1]:], on_time[1], T[1])

        elif level == 3:
            # dźwięk
            words = draw(level, 3 * on_time[2])
            for i in range(3):
                view_on_time(frame, i, words[i*on_time[2]:], on_time[2], T[2])
    window.mainloop()


def game():
    global var1
    global var2
    buttonFrame = Frame(window)
    buttonFrame.grid()
    label = Label(buttonFrame, text="Wybierz poziom trudności i tryb gry")
    label.grid()
    var1 = IntVar()
    var2 = IntVar()
    rad1 = Radiobutton(buttonFrame, text='Łatwy', variable=var1, value=1)
    rad1.grid()
    rad2 = Radiobutton(buttonFrame, text='Średni', variable=var1, value=2)
    rad2.grid()
    rad3 = Radiobutton(buttonFrame, text='Trudny', variable=var1, value=3)
    rad3.grid()
    rad4 = Radiobutton(buttonFrame, text='Na ilość fiszek', variable=var2, value=1)
    rad4.grid()
    rad5 = Radiobutton(buttonFrame, text='Na czas', variable=var2, value=2)
    rad5.grid()
    button = Button(buttonFrame, text="Dalej", command=lambda: zabawa(buttonFrame, var1.get(), var2.get()))
    button.grid()
    mainloop()


def clear(frame, n):
    frame.destroy()
    if n == 0:
        begin()
    elif n == 1:
        game()
    elif n == 2:
        statistics()
    elif n == 3:
        rules()


def statistics():
    f = open("statystyki.txt", "r", encoding="utf-8")
    buttonFrame = Frame(window)
    buttonFrame.grid()
    label = Label(buttonFrame, text=f.read())
    button = Button(buttonFrame, text="Wróć", fg="green", width=20, command=lambda: clear(buttonFrame, 0))
    label.grid()
    button.grid()
    window.mainloop()


def rules():
    f = open("zasady gry.txt", "r", encoding="utf-8")
    buttonFrame = Frame(window)
    buttonFrame.grid()
    label = Label(buttonFrame, text=f.read(), font=("Arial", 18, "italic"))
    button = Button(buttonFrame, text="Wróć", fg="green", width=20, command=lambda: clear(buttonFrame, 0))
    label.grid()
    button.grid()
    window.mainloop()


def begin():
    # dźwięk
    buttonFrame = Frame(window)
    buttonFrame.grid()
    label = Label(buttonFrame, text="Witaj w grze memory!!!\n", font=("Arial", 24,))
    label.grid(row=0, column=3, columnspan=2, ipady=10, pady=10, padx=5)
    button1 = Button(buttonFrame, text="Zacznij grę", font=("Arial", 24), fg = "green", width=20, command=lambda: clear(buttonFrame, 1))
    button1.grid(row=1, column=3, ipady=10, pady=10, padx=5)
    button2 = Button(buttonFrame, text="Statystyki", font=("Arial", 24), fg = "yellow", width=20, command=lambda: clear(buttonFrame, 2))
    button2.grid(row=2, column=3, ipady=10, pady=10, padx=5)
    button3 = Button(buttonFrame, text="Zasady gry", font=("Arial", 24), fg = "red", width=20, command=lambda:  clear(buttonFrame, 3))
    button3.grid(row=3, column=3, ipady=10, pady=10, padx=5)
    button4 = Button(buttonFrame, text="Wyjdź", font=("Arial", 24), fg="green", width=20, command=quit)
    button4.grid(row=4, column=3, ipady=10, pady=10, padx=5)
    window.mainloop()



########################################################################################################################


window = Tk()
window.title("Gra w Memory")
window.geometry("800x600")
flashcards = [5, 8, 10]
on_time = [5, 5, 7]
T = [5, 3, 7]

database, easy, medium, hard = word_count()                     # Otwarcie pliku z bazą słów
begin()



# tekst: http://uoo.univ.szczecin.pl/~jakubs/py/gfx.html