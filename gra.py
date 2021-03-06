import random
import time
from tkinter import *
from tkinter import messagebox
from pygame import mixer
from datetime import datetime
from PIL import ImageTk, Image


def word_count():
    global database

    f = open("baza slow.txt", "r", encoding="utf-8")  # otwarcie pliku tekstowego w trybie "r" - read
    database = f.read().split()                       # utworzenie tablicy i zapisanie do niej każdego słowa z pliku

    # Wyznaczenie ilości słów w poszczególnych poziomach trudności
    easy_word_count = -1                                             # -1 bo odrzucamy pole ze słowem "łatwe"
    medium_word_count = -1                                           # -1 bo odrzucamy pole ze słowem "średnie"
    iterator = 0

    while database[iterator] != "Średnie:":                          # przeliczenie słów z poziomu łatwego
        easy_word_count += 1
        iterator += 1

    while database[iterator] != "Trudne:":                           # przeliczenie słów z poziomu średniego
        medium_word_count += 1
        iterator += 1

    hard_word_count = len(database) - easy_word_count - medium_word_count - 3  # przeliczenie słow z poziomu trudnego
    f.close()                                                                  # zamknięcie pliku tekstowego
    return database, easy_word_count, medium_word_count, hard_word_count


def reset_statistics():
    result = messagebox.askquestion("UWAGA!", "Czy na pewno chcesz usunąć wszyskie statystyki?")
    if result == "yes":
        file = open("statystyki.txt", "r+", encoding="utf-8")
        file.truncate(0)
        file.close()


def save_score_to_file(frame, user_name: str, score_string: str):
    time_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")             # wczytanie czasu jako sformatowanego stringa

    file = open("statystyki.txt", "r+", encoding="utf-8")                  # otwarcie pliku w trybie r+
    content = file.read()                                                  # przepisanie zawartości
    file.truncate(0)                                                       # usunięcie zawartości
    file.close()                                                           # zamknięcie pliku

    file = open("statystyki.txt", "w", encoding="utf-8")                   # otwarcie pliku w trybie w
    file.write(user_name + " " + time_string + "\n" + score_string + "\n" + content)    # zapisanie punktacji
    file.close()                                                           # zamknięcie pliku
    mixer.music.load("muzyka_startowa.mp3")
    mixer.music.play(-1)
    clear(frame, 0)


def submit_user_name_and_points(frame):
    global score
    frame.destroy()

    frame1 = Frame(window)                                                     # utwórz ramkę
    frame1.configure(background="olive")
    frame1.pack(side=TOP, pady=55, padx=60, fill="both", expand=True)

    your_score_label = Label(frame1, text="Brawo! Twój wynik to:", font=("Arial", 22),
                             bg="dark olive green", width=30)   # napis "Twój wynik"

    # łańcuch znaków odpowiednio zformatowny w celu wyświetlania punktacjii
    score_display_string = "\nWynik tury nr 1: " + str(score[0])\
        + " pkt\nWynik tury nr 2: " + str(score[1])\
        + " pkt\nWynik tury nr 3: " + str(score[2])\
        + " pkt\n\n"

    score = []

    score_label = Label(frame1, text=score_display_string, font=("Arial", 14), bg="olive")  # wyświetlenie punktacji

    enter_name_label = Label(frame1, text="Wprowadź swoje imię:", font=("Arial", 22),
                             bg="dark olive green", width=30)         # teskt "Wprowadź imię"

    enter_name_field = Entry(frame1, width=15, font=("Arial", 18,))                           # pole do wpisania nazwy

    # przycisk do zapisania punkacjii i powroti do menu głównego
    submit_button = Button(frame1, text=" ZAPISZ I POWRÓĆ DO MENU ", fg="#DEB887", font=("Arial", 12),
                           bg="dark olive green", cursor="plus", activebackground="dark olive green",
                           command=lambda: save_score_to_file(frame1, enter_name_field.get(), score_display_string))

    # Kolejność poszczególnych widgetów

    your_score_label.pack(pady=35, ipady=15)
    score_label.pack()
    enter_name_label.pack(ipady=15)
    enter_name_field.pack(pady=25, padx=3)
    submit_button.pack(side=RIGHT, ipady=5, ipadx=10, padx=90)

    frame1.mainloop()


def enter_words(frame, tura, words, mode, t):

    frame.destroy()

    def enter_pressed():                                        # funkcja do czyszczenia i zapisywania pola wprowadzania
        global var1

        def check():                                            # funkcja do zliczania punktów
            frame1.forget()
            global score                                        # zaimportuj globalną tablicę score
            point = 0                                           # zmienna do zliczania punktów
            print(entered_words_array, int(tura*len(Words)/3))  # linijka kontrolna
            print(Words)                                        # linijka kontrolna
            for word in range(len(entered_words_array)):        # zlicz punkty dla danej tury
                if entered_words_array[word] == Words[int(word+tura*len(Words)/3)]:
                    point += 1
            score.append(point)                                 # dodaj punkty z danej tury do tablicy
            print("weszło", score)                              # linijka kontrolna
            if tura < 2 and mode == 1:                          # kolejna tura na ilość
                view(frame1, words, len(words)/(2-tura), tura + 1)
            elif tura < 2 and mode == 2:                        # kolejna tura na czas
                view_on_time(frame1, tura+1, words, len(words)/(2-tura), t)
            else:
                submit_user_name_and_points(frame1)
            return

        def next_word(number_of_words: int):
            if len(entered_words_array) == number_of_words:                     # jeśli wszystkie słowa zostały wpisane
                entry_label.configure(text="Wpisałeś wszyskie słowa!")  # zakutalizuj text przed polem wpisywania
                entry_field.pack_forget()                               # usuń pole do wpisywania
                entry_field.unbind("<Return>")                          # nie pozwalaj na użycie klawisza "enter"
                if tura == 2:
                    button_check = Button(frame1, text=" SPRAWDŹ SWOJE WYNIKI ", bg="dark olive green", fg="#DEB887",
                                          font=("Arial", 12), cursor="plus", activebackground="dark olive green",
                                          command=lambda: check())      # przycisk prowadzący do sprawdzania odpowiedzi
                else:
                    button_check = Button(frame1, text=" PRZEJDŹ DO KOLEJNEJ RUNDY ", bg="dark olive green",
                                          font=("Arial", 12), fg="#DEB887", cursor="plus", activebackground="dark olive green",
                                          command=lambda: check())  # przycisk prowadzący do sprawdzania odpowiedzi
                button_check.pack(anchor=NE, ipady=8, ipadx=4, pady=90, padx=90)
            else:                                                       # jeśli nie wszystkie słowa zostały wpisane
                entry_label.configure(text="Wprowadź słowo " +
                                      str(1 + len(entered_words_array)) + ":")  # zakutalizuj text przed polem

        entered_words_array.append(entry_field.get())  # dodaj słowo do tablicy wpisanych słów
        entry_field.delete(0, END)  # wyczyść pole wspisywania

        # Dobranie ilości słów, które trzeba wpisać adekwatnie do trybu
        if var1.get() == 1 and mode == 1:
            next_word(flashcards[0])
        elif var1.get() == 2 and mode == 1:
            next_word(flashcards[1])
        elif var1.get() == 3 and mode == 1:
            next_word(flashcards[2])
        elif var1.get() == 1 and mode == 2:
            next_word(on_time[0])
        elif var1.get() == 2 and mode == 2:
            next_word(on_time[1])
        elif var1.get() == 3 and mode == 2:
            next_word(on_time[2])

    frame1 = Frame(window)
    frame1.pack(side=TOP, pady=55, padx=60, fill="both", expand=True)
    frame1.configure(bg="olive")

    entered_words_array = []                                    # utworzenie tablicy słów wpisanych przez gracza

    entry_label = Label(frame1, text="Wprowadź słowo " + str(1+len(entered_words_array)) + ":",
                        font=("Arial", 22), width=30, bg="dark olive green")                   # tekst "wprowadź słowo"
    entry_label.pack(pady=35, ipady=15)

    entry_field = Entry(frame1, width=15, font=("Arial", 18,))                                 # pole do wpisywania
    entry_field.pack(pady=20)

    entry_field.bind("<Return>", lambda event: enter_pressed())            # "enter" do zapisania słowa
    entry_field.bind("<F1>", lambda event: print(entered_words_array))     # f1 do wyświetlenie listy słów <dev_key>


def view(frame, words, number_of_words, tura=0):                                # wyświetlanie słów w trybie "na ilość"
    frame.destroy()
    if number_of_words > 0:
        frame1 = Frame(window)
        frame1.configure(background="olive")
        frame1.pack(side=TOP, pady=55, padx=60, fill="both", expand=True)
        label_tura = Label(frame1, text="To jest runda nr " + str(tura + 1), font=("Arial", 22,),
                           bg="dark olive green", width=30)
        label_tura.pack(pady=35,ipady=15)
        word = Label(frame1, text=words[0], font=("Arial", 36,), bg="olive")
        word.pack(ipady=30)
        if number_of_words > 1:
            button = Button(frame1, text=" NASTĘPNE SŁOWO >>", bg="dark olive green", fg="#DEB887",
                            font=("Arial", 12), cursor="plus", activebackground="dark olive green",
                            command=lambda: view(frame1, words[1:], number_of_words - 1, tura))
            button.pack(side=RIGHT, ipady=5, ipadx=10, padx=90)
        else:
            button = Button(frame1, text=" SPARAWDŹ, ILE PAMIĘTASZ ", bg="dark olive green", fg="#DEB887",
                            font=("Arial", 12), cursor="plus", activebackground="dark olive green",
                            command=lambda: enter_words(frame1, tura, words[1:], 1, 0))
            button.pack(side=RIGHT, ipady=5, ipadx=10, padx=90)
            return
        frame1.mainloop()


def view_on_time(frame, i, words, n, t):                           # wyświetlanie słów w trybie "na czas"
    frame.destroy()
    frame1 = Frame(window)
    frame1.configure(background="olive")
    frame1.pack(side=TOP, pady=55, padx=60, fill="both", expand=True)
    if n > 0:
        label = Label(frame1, text="To jest runda nr " + str(i + 1),  font=("Arial", 22), bg="dark olive green",
                      width=30)
        label.pack(pady=35, ipady=15)
        word = Label(frame1, text=words[0], font=("Arial", 36,), bg="olive")
        word.pack(ipady=30)
        print(words[0])
        window.update()
        time.sleep(t)
        view_on_time(frame1, i, words[1:], n - 1, t)
    else:
        label_tura = Label(frame1, text="Wyświetlono wszystkie słowa", font=("Arial", 22,),
                           bg="dark olive green", width=30)
        label_tura.pack(pady=35,ipady=15)
        button = Button(frame1, text=" Sprawdź, ile pamiętasz >>", bg="dark olive green", fg="#DEB887",
                        activebackground="dark olive green", font=("Arial", 12,), cursor="plus",
                        command=lambda: enter_words(frame1, i, words, 2, t))
        button.pack(side=RIGHT, ipady=5, ipadx=10, padx=90)
    frame1.mainloop()


def draw(difficulty_level, number_of_words):                       # Losowanie n słów z odpowiedniego poziomu trudności
    global Words
    words = []
    if difficulty_level == 1:                                                   # poziom łatwy
        words = random.sample(database[1:easy], number_of_words)
    elif difficulty_level == 2:                                                 # poziom średni
        words = random.sample(database[easy+2:easy+medium+2], number_of_words)
    elif difficulty_level == 3:                                                 # poziom trudny
        words = random.sample(database[len(database)-hard:], number_of_words)
    Words = words
    return words


def zabawa(frame, difficulty_level, mode):                                 # działanie gry
    frame.forget()
    if mode == 1:                                               # jeśli tryb na ilość fiszek:

        if difficulty_level == 1:                                              # poziom łatwy
            mixer.music.load("muzyka_latwy.mp3")
            mixer.music.play(-1)
            words = draw(difficulty_level, 3 * flashcards[0])
            view(frame, words[0*flashcards[0]:], flashcards[0])

        elif difficulty_level == 2:                                            # poziom średni
            mixer.music.load("muzyka_sredni.mp3")
            mixer.music.play(-1)
            words = draw(difficulty_level, 3 * flashcards[1])
            view(frame, words[0*flashcards[1]:], flashcards[1])

        elif difficulty_level == 3:                                            # poziom trudny
            mixer.music.load("muzyka_trudny.mp3")
            mixer.music.play(-1)
            words = draw(difficulty_level, 3 * flashcards[2])
            view(frame, words[0*flashcards[2]:], flashcards[2])

    elif mode == 2:                                             # jeśli tryb na czas:
        print("<krótka instrukcja>")

        if difficulty_level == 1:                                              # poziom łatwy
            mixer.music.load("muzyka_latwy.mp3")
            mixer.music.play(-1)
            words = draw(difficulty_level, 3 * on_time[0])
            for i in range(3):
                view_on_time(frame, i, words[i*on_time[0]:], on_time[0], T[0])

        elif difficulty_level == 2:                                            # poziom średni
            mixer.music.load("muzyka_sredni.mp3")
            mixer.music.play(-1)
            words = draw(difficulty_level, 3 * on_time[1])
            for i in range(3):
                view_on_time(frame, i, words[i*on_time[1]:], on_time[1], T[1])

        elif difficulty_level == 3:                                            # poziom trudny
            mixer.music.load("muzyka_trudny.mp3")
            mixer.music.play(-1)
            words = draw(difficulty_level, 3 * on_time[2])
            for i in range(3):
                view_on_time(frame, i, words[i*on_time[2]:], on_time[2], T[2])


def game():
    global var1
    global var2
    buttonframe = Frame(window)
    buttonframe.configure(bg="olive")
    buttonframe.pack(side=TOP, pady=55, padx=60, fill="both", expand=True)

    var1 = IntVar()
    var2 = IntVar()

    label1 = Label(buttonframe, text="Wybierz poziom trudności:", bg="dark olive green",
                   font=("Arial", 22), width=30)
    label1.pack(pady=35, ipady=15)

    rad1 = Radiobutton(buttonframe, text='Łatwy', font=("Arial", 14), bg="olive", cursor="plus", variable=var1,
                       value=1, activebackground="olive",)
    rad1.pack()
    rad2 = Radiobutton(buttonframe, text='Średni', font=("Arial", 14), bg="olive", cursor="plus", variable=var1,
                       value=2, activebackground="olive",)
    rad2.pack()
    rad3 = Radiobutton(buttonframe, text='Trudny', font=("Arial", 14), bg="olive", cursor="plus", variable=var1,
                       value=3, activebackground="olive",)
    rad3.pack()

    empty = Label(buttonframe, text="", bg="olive",)
    empty.pack()

    label2 = Label(buttonframe, text="...oraz tryb gry:", font=("Arial", 22), bg="dark olive green",
                   width=30, activebackground="olive",)
    label2.pack(pady=10, ipady=15)
    rad4 = Radiobutton(buttonframe, text='Na ilość fiszek', font=("Arial", 14), bg="olive", cursor="plus",
                       variable=var2, value=1, activebackground="olive",)
    rad4.pack()
    rad5 = Radiobutton(buttonframe, text='Na czas', font=("Arial", 14), bg="olive", cursor="plus", variable=var2,
                       value=2, activebackground="olive",)
    rad5.pack()

    button = Button(buttonframe, text="DALEJ", fg="#DEB887", bg="dark olive green", font=("Arial", 12),
                    cursor="plus", activebackground="dark olive green",
                    command=lambda: zabawa(buttonframe, var1.get(), var2.get()) if var1.get() != 0 and var2.get() != 0
                    else print("nie wybrano poziomu lub trybu"))
    button.pack(side=RIGHT, ipady=5, ipadx=10, padx=90)


def clear(frame, number_of_button_pressed):                             # rozdzielacz
    frame.destroy()
    if number_of_button_pressed == 0:                                   # jeżeli koniec programu
        begin()
    elif number_of_button_pressed == 1:                                 # jeżeli naciśnięto "zacznij grę"
        game()
    elif number_of_button_pressed == 2:                                 # jeżeli naiśnięto "satystyki"
        statistics()
    elif number_of_button_pressed == 3:                                 # jeżeli naciśnięto "Zasady gry"
        rules()


def statistics():

    statistics_file = open("statystyki.txt", "r", encoding="utf-8")  #
    statistics_text = statistics_file.read()                         #
    statistics_file.close()                                          # ODCZYT I ZAMKNIĘCIE TEKSTU Z PLIKU

    buttonframe = Frame(window)             # GLÓWNE OKNO
    buttonframe.configure(bg="olive")

    label_statistic = Label(buttonframe, text="Twoje dotychczasowe osiągnięcia:", font=("Arial", 22,),
                            bg="dark olive green", width=30)  # NAPIS TYTULOWY

    button_reset = Button(buttonframe, text="RESETUJ\nSTATYSTYKI", font=("Arial", 12), bg="dark olive green",
                          fg="#DEB887", width=15, cursor="plus", activebackground="dark olive green",
                          command=lambda: reset_statistics())  # PRZYCISK RESETOWANIA STATYSTYK

    statistics_window = Text(buttonframe, background="olive", width=40, height=12.5 )    # UTOWORZENIE 'PODOKNA' DO WPISANIA TESKTU ZE STATYSTYK
    statistics_window.insert("1.0", statistics_text)             # WSPIANIE TEKSTU Z STATYSTYK DO 'PODOKNA'
    statistics_window.config(state="disabled")                   # BLOKOWANIE MOŻLIWOŚCI EDYCJI

    scrollbar = Scrollbar(buttonframe, )                  # UTWORZENIE SROLLBARA ( oczywiste no nie? :) )

    scrollbar.config(command=statistics_window.yview)        # COKOLWIEK TO ROBI, DZIĘKI TEMU
    statistics_window.config(yscrollcommand=scrollbar.set)   # SCROLLOWANIE DZIALA

    button = Button(buttonframe, text="POWRÓT", fg="#DEB887", font=("Arial", 12), bg="dark olive green", width=15,
                    cursor="plus", activebackground="dark olive green",
                    command=lambda: clear(buttonframe, 0))  # PRZYSICK POWROTU DO MENU GLÓWNEGO

    # KOLEJNOŚC WYŚWIETLANIA WIDGETÓW

    buttonframe.pack(side=TOP, pady=55, padx=60, fill="both", expand=True)

    label_statistic.pack(pady=35, ipady=15)

    statistics_window.pack(padx=(50, 0), pady=(0, 35), fill=Y, side=LEFT)
    scrollbar.pack(ipady=15, pady=(0, 35), side=LEFT, fill=Y)


    button_reset.pack(padx=(0, 50), anchor=NE)
    button.pack(pady=35, padx=(0, 50), ipady=9, anchor=NE)



def rules():

    rules_file = open("zasady_gry.txt", "r", encoding="utf-8")  #
    rules_text = rules_file.read()                              #
    rules_file.close()                                          # ODCZYT TEKSTU Z PLIKU

    buttonframe = Frame(window)         #
    buttonframe.pack(side=TOP, pady=55, padx=60, fill="both", expand=True)          #
    buttonframe.configure(bg="olive")   # OKNO GLÓWNE

    rules_label = Label(buttonframe, text=rules_text, justify=LEFT, wraplength=680,
                        font=("Arial", 15, "italic"), bg="olive")  # WYŚWIETLANIE TREŚCI PLIKU Z ZASADAMI

    return_button = Button(buttonframe, text="POWRÓT", fg="#DEB887", font=("Arial", 12, "italic"),
                           cursor="plus", bg="dark olive green", activebackground="dark olive green",
                           command=lambda: clear(buttonframe, 0))  # PRZYCISK POWROTU

    # ROZMIESZCZENIE WIDGETÓW
    rules_label.pack(pady=20, ipadx=7)
    return_button.pack(side=RIGHT, ipady=1, ipadx=7, padx=75)


def begin():

    buttonframe = Frame(window)
    buttonframe.pack(side=TOP, pady=55, padx=60, fill="both", expand=True)
    buttonframe.configure(background="olive")       # OKNO GLÓWNE

    # WIADOAMOŚC TYTULOWA
    label = Label(buttonframe, text="Witaj w grze MEMORY", font=("Arial", 30), bg="olive")
    label.pack(pady=30)

    # PRZYCISK ZACZNIJ GRĘ
    button1 = Button(buttonframe, text="Zacznij grę", font=("Arial", 24), bg="dark olive green",
                     fg="#DEB887", width=20, cursor="plus", activebackground="dark olive green",
                     command=lambda: clear(buttonframe, 1))
    button1.pack(ipady=10, padx=5)

    # PRZYCISK STATYSTYKI
    button2 = Button(buttonframe, text="Statystyki", font=("Arial", 24), bg="dark olive green",
                     fg="#DEB887", width=20, cursor="plus", activebackground="dark olive green",
                     command=lambda: clear(buttonframe, 2))
    button2.pack(ipady=10, pady=10, padx=5)

    # PRZYCISK ZASADY GRY
    button3 = Button(buttonframe, text="Zasady gry", font=("Arial", 24), bg="dark olive green",
                     fg="#DEB887", width=20, cursor="plus", activebackground="dark olive green",
                     command=lambda:  clear(buttonframe, 3))
    button3.pack(ipady=10, padx=5)

    # PRZYCISK WYJDŹ
    button4 = Button(buttonframe, text="Wyjdź", font=("Arial", 24), bg="dark olive green",
                     fg="#DEB887", width=20, cursor="plus", activebackground="dark olive green", command=quit)
    button4.pack(ipady=10, pady=10, padx=5)


########################################################################################################################


mixer.init()                                                    # uruchomienie modulu muzyki
mixer.music.load("muzyka_startowa.mp3")
mixer.music.play(-1)

window = Tk()
window.title("Gra w Memory")
window.geometry("800x600")
image2 = Image.open("krata.jpg")
image1 = ImageTk.PhotoImage(image2)
background_label = Label(window, image=image1)
background_label.image1 = image1
background_label.place(x=-400, y=0, height=800, width=1800)


flashcards = [5, 8, 10]                                         # ilosć słów do wyświetlnia dla poszczególnych poziomów
on_time = [5, 5, 7]
T = [5, 3, 7]

# ZMIENNE GLOBALNE
score = []
Words = []
var1 = 0
var2 = 0

database, easy, medium, hard = word_count()                     # Otwarcie pliku z bazą słów
begin()
window.mainloop()


# tekst: http://uoo.univ.szczecin.pl/~jakubs/py/gfx.html
# biblioteka tkinter: https://www.obliczeniowo.com.pl/496
# yt: https://www.youtube.com/watch?v=YXPyB4XeYLA
