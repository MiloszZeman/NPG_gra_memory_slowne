import random
import time
from tkinter import *
from pygame import mixer





def word_count():

    f = open("baza slow.txt", "r", encoding="utf-8")            # otwarcie pliku tekstowego w trybie "r" - read
    database = f.read().split()                                 # utworzenie tablicy i zapisanie do niej każdego słowa
                                                                # z pliku "baza slow.txt"

                                                                # Wyznaczenie ilości słów w poszczególnych poziomach trudności
    easy_word_count = -1                                                   # -1 bo odrzucamy pole ze słowem "łatwe"
    medium_word_count = -1                                                 # -1 bo odrzucamy pole ze słowem "średnie"
    iterator = 0

    while (database[iterator] != "Średnie:"):                          # przeliczenie słów z poziomu łatwego
        easy_word_count += 1
        iterator += 1

    while (database[iterator] != "Trudne:"):                           # przeliczenie słów z poziomu średniego
        medium_word_count += 1
        iterator += 1

    hard_word_count = len(database) - easy_word_count - medium_word_count - 3     # przeliczenie słow z poziomu trudnego
    f.close()                                                                     # zamknięcie pliku tekstowego
    return database, easy_word_count, medium_word_count, hard_word_count


def enter_words(frame, i, words, nr, t):

    frame.destroy()

    def enter_pressed():                                       # funkcja do czyszczenia i zapisywania pola wprowadzania

        def check():                                           # funkcja do zliczania punktów
            frame1.forget()
            point = 0
            print(entered_words_array, int(i*len(Words)/3))
            print(Words)
            for k in range(len(entered_words_array)):
                if entered_words_array[k] == Words[int(k+i*len(Words)/3)]:
                    point += 1
            score.append(point)
            print("weszło", score)
            if i < 2 and nr == 1:                               # kolejna tura
                view(frame1, i+1, words, len(words)/(2-i))
            elif i < 2 and nr == 2:
                view_on_time(frame1, i+1, words, len(words)/(2-i),t)
            else:
                clear(frame1, 0)
            return

        entered_words_array.append(entry_field.get())               # dodaj słowo do tablicy wpisanych słów
        entry_field.delete(0, END)                                  # wyczyść pole wspisywania

        if len(entered_words_array) == 5:                           # jeśli wszystkie słowa zostały wpisane
            entry_label.configure(text="Wpisałeś wszyskie słowa!")  # zakutalizuj text przed polem wpisywania
            entry_field.grid_remove()                               # usuń pole do wpisywania
            entry_field.unbind("<Return>")                          # nie pozwalaj na użycie klawisza "enter"
            button_check = Button(frame1, text="Sprawdź odpowiedzi!",
                                      command=lambda: check())       #przycisk prowadzący do sprawdzania odpowiedzi
            button_check.grid()
        else:                                                       # jeśli nie wszystkie słowa zostały wpisane
            entry_label.configure(text="Wprowadź słowo " +
                                   str(1 + len(entered_words_array)) + ":")  # zakutalizuj text przed polem wpisywania

    frame1 = Frame(window)
    frame1.grid()

    entered_words_array = []                                    #  utworzenie tablicy słów wpisanych przez gracza

    entry_label = Label(frame1, text="Wprowadź słowo " + str(1+len(entered_words_array)) + ":",
                        font=("Arial", 24,))                    # tekst "wprowadź słowo"
    entry_label.grid()

    entry_field = Entry(frame1)                                 # pole do wpisywania
    entry_field.grid()

    entry_field.bind("<Return>", lambda event: enter_pressed())            # "enter" do zapisania słowa
    entry_field.bind("<F1>", lambda event: print(entered_words_array))     # f1 do wyświetlenie listy słów <dev_key>



def view(frame, i, words, n):                                   # wyświetlanie słów w trybie "na ilość"
    frame.destroy()
    if n > 0:
        frame1 = Frame(window)
        frame1.grid()
        label = Label(frame1, text="Tura " + str(i + 1), font=("Arial", 24,))
        label.grid()
        word = Label(frame1, text=words[0])
        word.grid()
        if n > 1:
            button = Button(frame1, text="Następne słowo >>", command=lambda: view(frame1, i, words[1:], n - 1))
            button.grid()
        else:
            button = Button(frame1, text="Sprawdź ile pamiętasz!", command=lambda: enter_words(frame1, i, words[1:], 1, 0))
            button.grid()
            return
        frame1.mainloop()


def view_on_time(frame, i, words, n, t):                           # wyświetlanie słów w trybie "na czas"
    frame.destroy()
    frame1 = Frame(window)
    frame1.grid()
    if n > 0:
        label = Label(frame1, text="Tura " + str(i + 1), font=("Arial", 24,))
        label.grid()
        word = Label(frame1, text=words[0])
        word.grid()
        print(words[0])
        window.update()
        time.sleep(t)
        view_on_time(frame1, i, words[1:], n - 1, t)
    else:
        button =Button(frame1, text="Sprawdź ile pamiętasz", command=lambda: enter_words(frame1, i, words, 2, t))
        button.grid()
    frame1.mainloop()


def draw(level, n):                                             # Losowanie n słów z odpowiedniego poziomu trudności
    global Words
    if level == 1:
        words = random.sample(database[1:easy], n)
    elif level == 2:
        words = random.sample(database[easy+2:easy+medium+2], n)
    elif level == 3:
        words = random.sample(database[len(database)-hard:], n)
    Words=words
    return words


def zabawa(frame, level, mode):                                 # działanie gry
    frame.forget()
    if mode == 1:                                               # jeśli tryb na ilość fiszek:

        if level == 1:                                              # poziom łatwy
            mixer.music.load("muzyka_latwy.mp3")
            mixer.music.play()
            words = draw(level, 3 * flashcards[0])
            for i in range(3):
                view(frame, i, words[i*flashcards[0]:], flashcards[0])

        elif level == 2:                                              # poziom średni
            mixer.music.load("muzyka_sredni.mp3")
            mixer.music.play()
            words = draw(level, 3 * flashcards[1])
            for i in range(3):
                view(frame, i, words[i*flashcards[1]:], flashcards[1])

        elif level == 3:                                            # poziom trudny
            mixer.music.load("muzyka_trudny.mp3")
            mixer.music.play()
            words = draw(level, 3 * flashcards[2])
            for i in range(3):
                view(frame, i, words[i*flashcards[2]:], flashcards[2])

    elif mode == 2:                                             # jeśli tryb na czas:
        print("<krótka instrukcja>")

        if level == 1:                                              #poziom łatwy
            mixer.music.load("muzyka_latwy.mp3")
            mixer.music.play()
            words = draw(level, 3 * on_time[0])
            for i in range(3):
                view_on_time(frame, i, words[i*on_time[0]:], on_time[0], T[0])


        elif level == 2:                                            #poziom średni
            mixer.music.load("muzyka_sredni.mp3")
            mixer.music.play()
            words = draw(level, 3 * on_time[1])
            for i in range(3):
                view_on_time(frame, i, words[i*on_time[1]:], on_time[1], T[1])

        elif level == 3:                                            #poziom trudny
            mixer.music.load("muzyka_trudny.mp3")
            mixer.music.play()
            words = draw(level, 3 * on_time[2])
            for i in range(3):
                view_on_time(frame, i, words[i*on_time[2]:], on_time[2], T[2])


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


def rules():
    f = open("zasady gry.txt", "r", encoding="utf-8")
    buttonFrame = Frame(window)
    buttonFrame.grid()
    label = Label(buttonFrame, text=f.read(), font=("Arial", 18, "italic"))
    button = Button(buttonFrame, text="Wróć", fg="green", width=20, command=lambda: clear(buttonFrame, 0))
    label.grid()
    button.grid()


def begin():
    mixer.music.load("muzyka_startowa.mp3")
    mixer.music.play()
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



########################################################################################################################

mixer.init()                                                    # uruchomienie modulu muzyki

window = Tk()
window.title("Gra w Memory")
window.geometry("800x600")
flashcards = [5, 8, 10]                                         # ilosć słów do wyświetlnia dla poszczególnych poziomów
on_time = [5, 5, 7]
T = [5, 3, 7]
score = []

database, easy, medium, hard = word_count()                     # Otwarcie pliku z bazą słów
begin()
window.mainloop()


# tekst: http://uoo.univ.szczecin.pl/~jakubs/py/gfx.html
# biblioteka tkinter: https://www.obliczeniowo.com.pl/496
# yt: https://www.youtube.com/watch?v=YXPyB4XeYLA