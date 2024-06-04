from tkinter import ttk
from tkinter import Tk
import tkinter as tk
from tkinter import filedialog
import json
import pytransposer.transposer as tr
from musicpy import get_chord, mp
from scamp import Session
import os

class GUI:
    def __init__(self, root) -> None:
        """Ініціалізує екземпляр класу GUI.

        Створює екземпляр класу 'Song' та 'Transposer'.
        Створює стилі для віджетів.

        Args:
            root: 'кореневе' вікно Tkinter.
        """
        self.root = root
        self.song_instance = Song() 
        self.transposer_instance = Transposer()
        self.root.title("The Sheet Music Editor")
        self.root.configure(bg="LightBlue1")
        root.resizable(width=False, height=False)
        self.style = ttk.Style()
        self.style.theme_use('classic')
        self.style.configure("TFrame", background="LightBlue1")
        self.style.configure("TLabel", foreground="black", background="LightBlue1", font=("arial", 20, "bold"))
        self.style.configure("TButton", foreground="black", background="LightBlue1", font=("arial", 20, "bold"))
        self.style.configure("W.TButton", foreground="black", background="LightBlue1", font=("arial", 14))
        
    def location(self, width, height):
        """Розміщує вікна рівно по середині.

        Отримує дані про параметри відповідного вікна і знаходить параметри екрана користувача.
        
        Notes
        -----
        (1, 2 аргументи) ширина, довжина вікна; (3, 4 аргументи) відступ від лівого краю, верхнього краю  
        root.geometry("500x500+500+200")

        """
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def main_widget(self):
        """ Створює початкове вікно.

        Вікно містить заголовок та дві кнопки: 
        - кнопка "Start" викликає метод 'menu';
        - кнопка "Exit" закриває програму.

        Notes
        -----
        justify - визначає спосіб вирівнювання тексту у віджеті.

        """
        heading = ttk.Label(self.root, text="Hello!\n It's The Song Editor!\n Let's create your own song and transform it!\n", style="TLabel", justify="center")
        heading.pack()
        self.location(600, 250)

        button_f = ttk.Frame(self.root, style="TFrame")
        button_f.pack(pady=30)

        start_button = ttk.Button(button_f, text="Start", command=self.menu, style="TButton", width=7)
        start_button.pack(side="left", padx=20)

        exit_button = ttk.Button(button_f, text="Exit", command=self.root.quit, style="TButton", width=7)
        exit_button.pack(side="left", padx=20)

        self.root.mainloop()
    
    def menu(self):
        """" Створює меню програми.

        Вікно містить у собі чотири кнопки:
        - "Create a song" викликає метод 'create_song';
        - "Open File" викликає метод 'open_file ';
        - "Transpose the song" викликає метод 'open_json';
        - "Exit" - вийти з програми.

        """
        self.clear_windows()

        create_button = ttk.Button(root, text="Create a song", command=self.create_song, style="TButton", width=17)
        create_button.pack(pady=25) 
        self.location(400, 400)

        choose_button = ttk.Button(root, text="Open File", command=self.open_file, style="TButton", width=17)
        choose_button.pack(pady=25)

        transpose_button =ttk.Button(root, text="Transpose the song", command= self.open_json, style="TButton", width=17)
        transpose_button.pack(pady=25)

        exit_button = ttk.Button(root, text="Exit", command=self.root.quit, style="TButton", width=17)
        exit_button.pack(pady=25) 

    def clear_windows(self):
        """" Очищає екран від попереднього вмісту вікна.
        
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_song(self):
        """ Вікно для написання тексту своєї власної пісні.

        Це вікно має такі опції як:
        - полотне, на якому можна писати текст пісні;
        - кнопка "Save", викликає метод 'save_song';
        - кнопка "Back" викликає метод 'menu'.

        Notes
        -----
        Параметр "command" приймає посилання на функцію, тому не приймає аргументи всереині функції.
        Метод 'read_text' класу "Song" потребує екземпляр класу "GUI", що мати доступ до тексту з полотна. 
        Тому використовуємо self для цього.

        """
        self.clear_windows()

        heading = ttk.Label(root, text="Create text for song!",  style="TLabel", justify="center")
        heading.pack(pady=20)
        self.location(600, 600)

        txt_frame = ttk.Frame(root, style="TFrame")
        txt_frame.pack(pady=10)

        self.text_song = tk.Text(txt_frame, height=23, width=60, foreground="white", font=("arial", 16))
        self.text_song.pack()

        button_frame = ttk.Frame(root, style="TFrame")
        button_frame.pack(pady=10)

        save_button = ttk.Button(button_frame, text="Save", command=lambda: self.song_instance.read_text(self), style="TButton", width=7)
        save_button.pack(side="left", padx=10)

        back_button = ttk.Button(button_frame, text="Back", command=self.menu, style="TButton", width=7)
        back_button.pack(side="left", padx=10)

    def open_file(self):
        """ Відкриває діалогове вікно для вибору текстового файлу з розширенням .txt і завантажує цей файл.

        Після вибору файлу, метод зчитує його вміст і передає у метод 'read_text' клас 'Song'.

        """
        file_path = filedialog.askopenfilename(
            title="Select a Text File", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.song_instance.read_text(self, content) 

    def add_chords(self):
        """ Створює вікно для додавання акордів до слів і вибору тональності.

        Має такі конмоненти:
        - список тональностей Listbox;
        - смуга прокручування Scrollbar;
        - кнопка для збереження тональності 'Save Tonality';
        - полотно (Canvas) з словами пісні;
        - кнопка для збереження тексту як json файл 'Save song';
        - кнопка для транспонування 'Transpose this song';
        - кнопка 'Back' повертає до 'menu'.

        Notes
        -----
        !!! Щоб транспонувати пісню, потрібно спершу натиснути на кнопку 'Save song', таким чином текст з акордами та тональністю
        збережуть в json file. Це потрібно для подальшого коду.

        """
        self.clear_windows()

        heading = ttk.Label(root, text="Add chords!", style="TLabel", justify="center")
        heading.pack(pady=20)
        self.location(1450, 750)

        text_tonal = ttk.Label(root, text="Choose a Tonality:", style="TLabel", justify="center")
        text_tonal.pack(pady=10)

        frame_for_tonal = ttk.Frame(self.root, style="TFrame")
        frame_for_tonal.pack(pady=10)
        
        self.choice_tonality = tk.Listbox(frame_for_tonal, height=5, width=15, selectmode="single")
        for tonality in Song().tonalities:
            self.choice_tonality.insert("end", tonality)
        self.choice_tonality.pack(side="left")

        scroll = ttk.Scrollbar(frame_for_tonal)
        scroll.pack(side="left", fill="y")

        scroll.config(command=self.choice_tonality.yview)
        self.choice_tonality.config(yscrollcommand=scroll.set)

        save_tonality_button = ttk.Button(self.root, text="Save Tonality", command=lambda: self.song_instance.save_tonality(self), width=12)
        save_tonality_button.pack(pady=10)

        frame_for_chords = ttk.Frame(self.root, style="TFrame")
        frame_for_chords.pack(pady=10)

        canvas = tk.Canvas(frame_for_chords, background="LightBlue1")
        scrollbar = ttk.Scrollbar(frame_for_chords, orient="vertical", command=canvas.yview)
        scrollbar1 = ttk.Scrollbar(frame_for_chords, orient="horizontal", command=canvas.xview)
        scrollable_frame = ttk.Frame(canvas, style="TFrame")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set, width=1350, height=350)

        self.line_frames = []
        # словник для того, щоб зберегти акорд біля слова після введення його
        self.word_buttons = {} 
        m_row = max(row for word, (row, position) in self.song_instance.text_lines)
        for row in range(0, m_row + 1):
            line = ttk.Frame(scrollable_frame)
            line.pack(fill="x", pady=5)
            self.line_frames.append(line)
        
        for word, (row, position) in self.song_instance.text_lines:
            word_button = ttk.Button(self.line_frames[row], text=word, command=lambda w=word, r=row, p=position: self.window_for_chors(w, r, p), style="W.TButton", width=20)
            word_button.pack(side="left", padx=5)
            self.word_buttons[(word, (row, position))] = word_button 

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        scrollbar1.pack(side="bottom", fill="x")
        
        buttons_frame = ttk.Frame(root, style="TFrame")
        buttons_frame.pack(pady=15)

        save_c_button = ttk.Button(buttons_frame, text="Save song", command=lambda: self.song_instance.save_file_song(self), style="TButton", width=15)
        save_c_button.pack(side="left", padx=10)

        back_button = ttk.Button(buttons_frame, text="Transpose this song", command= self.open_json, style="TButton", width=18)
        back_button.pack(side="left", padx=10)

        back_button = ttk.Button(buttons_frame, text="Back", command=self.menu, style="TButton", width=15)
        back_button.pack(side="left", padx=10)


    def window_for_chors(self, word, row, position):
        """ Створює вікно для введення акорду.

        Вікно містить заголовок, поле для введення акорду і кнопку "Save", яка викликає метод 'save_chords' класу 'Song' 
        для збереження акорду до відповідного слова.

        Args:
            word (str): слово, до якого додається акорд.
            row (int): номер рядка, де знаходиться слово.
            position (int): позиція слова в рядку.

        """
        self.chord_window = tk.Toplevel(self.root, background="LightBlue1")
        self.chord_window.title("Add Chord")
        self.chord_window.geometry("200x150+20+20")

        heading = ttk.Label(self.chord_window, text="Enter chord", style="TLabel")
        heading.pack(pady=10)

        self.chord_entry = ttk.Entry(self.chord_window)
        self.chord_entry.pack(pady=10)

        button_save = ttk.Button(self.chord_window, text="Save", command=lambda w=word, r=row, p=position: self.song_instance.save_chords(self, w, r, p), style="W.TButton")
        button_save.pack(pady=10)

    def window_for_transpose(self, song_data):
        """ Вікно, яке забезпечує транспонування пісні.

        Args:
            song (dict): словник пісні з тональностю та слово-позиція-акорд.

        Notes
        -----
        Складається з вдох кнопок:
        - "+" підвищення на півтон;
        - "-"пониження на півтон.
        - рамки (фрейма) з текстом пісні, біля відповідного слова відповідних акорд.
        - кнопка "Back" викликає метод 'menu';
        - кнопка "Save this song" викликає метод 'save_file_song' клас 'Song';
        - викликає всередині метод 'display_lyrics'.
        
        """
        self.clear_windows()
        self.current_tonality = song_data['tonality']
        heading = ttk.Label(self.root, text="Transpose Song!", style="TLabel")
        heading.pack(pady=20)
        self.location(1450, 750)

        tonality_label = ttk.Label(self.root, text=f"Tonality: {self.current_tonality}", style="TLabel")
        tonality_label.pack(pady=10)

        tones_frame = ttk.Frame(self.root, style="TFrame")
        tones_frame.pack(pady=15)

        plus_button = ttk.Button(tones_frame, text="+", command=lambda: self.transposer_instance.plus_tones(self), style="TButton", width=3)
        plus_button.pack(side="left", padx=10)

        minus_button = ttk.Button(tones_frame, text="-", command=lambda: self.transposer_instance.minus_tones(self), style="TButton", width=3)
        minus_button.pack(side="left", padx=10)
        
        self.words_and_positions = song_data["words_and_positionand_and_chords"]

        self.display_lyrics()

        button_frame = ttk.Frame(root, style="TFrame")
        button_frame.pack(pady=10)
        
        save_song_button = ttk.Button(button_frame, text="Save this song", command=lambda: self.song_instance.save_file_song(self), style="TButton", width=14)
        save_song_button.pack(side="left", padx=12) 

        play_song_button = ttk.Button(button_frame, text="Play song", command=lambda: self.transposer_instance.play_song(self), style="TButton", width=10)
        play_song_button.pack(side="left", padx=12)  
             
        back_button = ttk.Button(button_frame, text="Back", command=self.menu, style="TButton", width=10)
        back_button.pack(side="left", padx=12)

    def display_lyrics(self):
        """ Відображає текст пісні із акордами.

        Цей метод встановлює рамку з текстовим віджетом tk.Text і смугою прокрутки Scrollbar.
        Заповнює віджет рядками, де кожне слово може мати відповідний акорд.

        Notes
        -----
        eval - витягує слово і його позицію з відповідного ключа.
        insert(позиція, текст) - вставляє текст в поле перед символом, індекс якого вказаний як параметр позиції.

        """
        lyrics_frame = ttk.Frame(self.root, style="TFrame")
        lyrics_frame.pack(pady=10)

        scrollbar = ttk.Scrollbar(lyrics_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        lyrics_text = tk.Text(lyrics_frame, yscrollcommand=scrollbar.set, font=("arial", 20), width=100, height=20)
        lyrics_text.pack(side="left")
        scrollbar.config(command=lyrics_text.yview)

        lines = {}
        for key, chord in self.words_and_positions.items():
            word, (row, position) = eval(key)
            if row not in lines:
                lines[row] = []
            lines[row].append((word, position, chord))
        formatted_lines = []

        for row in sorted(lines.keys()):
            line_text = []
            # сортує елемнти списку по позиції слова в рядку
            for word, position, chord in sorted(lines[row], key=lambda x: x[1]):
                if chord:
                    display_word = f"{word}({chord})"
                else: 
                    display_word = f"{word}"
                line_text.append(display_word)
            formatted_lines.append("  ".join(line_text))
        lyrics_text.insert("end", "\n".join(formatted_lines))

    def open_json(self):
        """Відкриває діалогове вікно для вибору файлу з розширенням .json і завантажує цей файл.
        
        Після вибору файлу, метод зчитує його вміст і передає у метод 'window_for_transpose'.
        """
        file_path = filedialog.askopenfilename(
            title="Select a JSON File", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                self.song = json.load(file)
                self.window_for_transpose(self.song)   


class Song:
    def __init__(self) -> None:
        self.word_to_chord_map = {}
        self.tonalities = ["C", "Am", "G", "Em", "D", "Bm", "A", "F#m", "E", "C#m", "B", "G#m", "F#", "D#m", "Gb", "Db", "Ab", "Fm", "Eb", "Cm", "Bb", "Gm", "F", "Dm", "default"]
        self.chords = []
        self.text_lines = []
        self.selected_tonality = None
        self.transposer = Transposer()

    def read_text(self, gui_instance, content=None):
        """ Зчитує текст з екземпляра GUI або з наданого content, обробляє його, викликаючи метод 'split_lines'.
        В кінці викликає метод 'add_chords' в класі GUI.
    
        Args:
        gui_instance: екземпляр GUI, з якого зчитується текст, якщо content None.
        content (str): текст для обробки. Якщо немає, текст буде зчитаний з екземпляра GUI.

        Notes
        -----
        1.0 - з якого номеру рядка починати, і з якого номеру символу (перший рядок і перший символ у тексті).

        """
        if content:
            text = content
        else:
            text = gui_instance.text_song.get("1.0", "end")
        self.split_lines(text)
        gui_instance.add_chords()

    def split_lines(self, text):
        """Розділяє наданий текст на рядки і слова, і ставить кожне слово на його позицію.
    
        Args:
        text (str): текст для розділення та обробки.
        
        """
        lines = text.split("\n")
        for row, line in enumerate(lines):
            words = line.split()
            for position, word in enumerate(words):
                el_word = word.strip(".,?!()")
                key = (el_word, (row, position))
                self.word_to_chord_map[key] = None  
                self.text_lines.append(key)
        print(self.text_lines)
        print(self.word_to_chord_map)

    def save_chords(self, gui_instance, word, row, position):
        """ Зберігає акорд як значення відповідного ключа у словнику 'self.word_to_chord_map'.

        Також зберігає всі акорди у список 'self.chords', для методу 'definition_of_tonic' клас Transposer.
        У кінці викликає метод 'chord_window.destroy' клас GUI.

        Args:
        gui_instance: екземпляр GUI, з якого отримується введений акорд.
        word (str): слово, до якого додається акорд.
        row (int): номер рядка, де знаходиться слово.
        position (int): позиція слова в рядку.

        Notes
        -----
        config(configure) - змінює властивості віджетій

        """
        chord = gui_instance.chord_entry.get()
        if not chord:
            chord = None
        key = (word, (row, position))
        self.word_to_chord_map[key] = chord
        if chord is not None:
            self.chords.append(chord)
            # отримує слово по ключі і змінює (оновлює) кнопку (до відповідного слово співставляє відповідний акорд)
            button = gui_instance.word_buttons[key] 
            button.config(text=f"{word} ({chord})")  
        print(self.chords)
        print(self.word_to_chord_map)
        print(f"Chord for '{word}': {chord}")
        gui_instance.chord_window.destroy()
        

    def save_file_song(self, gui_instance):
        """ Зберігає у форматі JSON слова пісні разом із відповідними акордами (якщо вони є) у файл.

        Записуємо через if, надаючи можливість користувачу під час транпонування акордів також зберігати пісню у файл, але вже з новими акордами.

        Args: 
        gui_instance: екземпляр GUI, з якого отримується словник слово-розташування-акорд.

        Notes
        -----
        indent - кількість пробілів для відступів при збережені файла json
        os.path.exists - перевіряє чи існує відповідний файл

        """
        if self.word_to_chord_map:
            words_and_chords = {str(key): chord for key, chord in self.word_to_chord_map.items()}
            song_data = {
                "tonality": self.selected_tonality,
                "words_and_positionand_and_chords": words_and_chords,
            }
        else:
            words_and_chords = {str(key): chord for key, chord in gui_instance.words_and_positions.items()}
            song_data = {
                "tonality": gui_instance.current_tonality,
                "words_and_positionand_and_chords": words_and_chords,
            }
        name = 'song_file'
        type_file= '.json'
        filename = name + type_file
        num = 1

        while os.path.exists(filename):
            filename = f"{name}_{num}{type_file}"
            num += 1

        with open(filename, 'w') as file:
            json.dump(song_data, file, indent=4)

        print(f"Пісня збережена у файл '{filename}'")


    def save_tonality(self, gui_instance):
        """ Зберігає тональніть пісні в змінну self.selected_tonality.
        У випадку, якщо користувач обрав зі списку значення "default", викликається метод 'tonic_chord'.

        Args: 
        gui_instance: екземпляр GUI.

        Notes
        -----
        curselection() - дозволяє отримати у вигляді кортежу індекси вибраних елементів.

        """
        choice = gui_instance.choice_tonality.curselection()
        selected_index = choice[0]
        selected_tonality = gui_instance.choice_tonality.get(selected_index)  
        if selected_tonality == "default":
            self.tonic_chord()
        else:
            self.selected_tonality = selected_tonality
        print(f"Selected Tonality: {self.selected_tonality}")

    def tonic_chord(self):
        """Викликає метод 'definition_of_tonic', передаючи вже створений екзамепляр класу 'Transposer'
        
        """
        self.transposer.definition_of_tonic(self)


class Transposer:
    def __init__(self) -> None:
        self.notes = {'C': 60, 'Dbb': 60, 'B#': 60, 'C#': 61, 'Db': 61, 'D': 62, 'Ebb': 62, 'D#': 63, 
                      'Eb': 63, 'E': 64, 'Fb': 64, 'E#': 66, 'F': 65, 'F#': 66, 'Gb': 66, 'G': 67, 'Abb': 67, 
                      'G#': 68, 'Ab': 68, 'A': 69, 'Bbb': 69, 'A#': 70, 'Bb': 70, 'B': 71, 'Cb': 71}

    def definition_of_tonic(self, song_instance):
        """" Визначає тональність по останньому акорду (зі списку 'self.chords' класу 'Song') і 
        зберігає в змінні 'self.selected_tonality' клас 'Song'.

        Використовує бібліотеку pytransposer.

        Args:
        song_instance: Екземпляр Song, який містить список всіх акордів.

        """
        last_chord = song_instance.chords[-1] 
        print(last_chord)
        a = get_chord(last_chord,'m').names()
        song_instance.selected_tonality = a[0]

    def plus_tones(self, gui_instance):
        """Підвищує акорди на півтон.

        Використовує бібліотеки musicpy та pytransposer.

        Args:
        - gui_instance: екземпляр класу GUI.

        Змінює стан об'єкта gui_instance.
        """
        transposed_map = {}
        for key, chord in gui_instance.words_and_positions.items():
            word, (row, position) = eval(key)
            if chord != None and "7" not in chord:
                transposed_chord = tr.transpose_chord(chord, 1)
                transposed_map[str((word, (row, position)))] = transposed_chord
            elif chord != None  and "7" in chord:
                if "#" in chord or "b" in chord:
                    note = chord[:2]
                    scale = chord[2:]
                else:
                    note = chord[0]
                    scale = chord[1:]
                transposed_chord = get_chord(note, scale).up(1)
                chord_type = mp.alg.detect(transposed_chord)
                transposed_map[str((word, (row, position)))] = chord_type
            else:
                transposed_map[str((word, (row, position)))] = chord
        gui_instance.words_and_positions = transposed_map
        if "m" in gui_instance.current_tonality and "#" in gui_instance.current_tonality:
            note = gui_instance.current_tonality[:-1]
            chord_type = gui_instance.current_tonality[-1]
            transposed_note = tr.transpose_chord(note, 1)
            new_tonality = transposed_note + chord_type
        elif "m" in gui_instance.current_tonality and len(gui_instance.current_tonality) == 2:
            gui_instance.current_tonality = gui_instance.current_tonality.replace("m", "b")
            new_tonality = tr.transpose_chord(gui_instance.current_tonality, 1)
        else:
            new_tonality = tr.transpose_chord(gui_instance.current_tonality, 1)
        gui_instance.song_data = {
            "tonality": new_tonality,
            "words_and_positionand_and_chords": transposed_map,
        }
        gui_instance.clear_windows()
        gui_instance.window_for_transpose(gui_instance.song_data)

    def minus_tones(self, gui_instance):
        """Понижує акорди на півтон.
        
        Використовує бібліотеки musicpy та pytransposer.transposer.

        Args:
        - gui_instance: екземпляр класу GUI.

        Змінює стан об'єкта gui_instance.

        """
        transposed_map = {}
        for key, chord in gui_instance.words_and_positions.items():
            word, (row, position) = eval(key)
            if chord != None and "7" not in chord:
                transposed_chord = tr.transpose_chord(chord, -1)
                transposed_map[str((word, (row, position)))] = transposed_chord
            elif chord != None  and "7" in chord:
                if "#" in chord or "b" in chord:
                    note = chord[:2]
                    scale = chord[2:]
                else:
                    note = chord[0]
                    scale = chord[1:]
                transposed_chord = get_chord(note, scale).down(1)
                chord_type = mp.alg.detect(transposed_chord)
                transposed_map[str((word, (row, position)))] = chord_type
            else:
                transposed_map[str((word, (row, position)))] = chord
        gui_instance.words_and_positions = transposed_map
        if "m" in gui_instance.current_tonality and "#" in gui_instance.current_tonality:
            note = gui_instance.current_tonality[:-1]
            chord_type = gui_instance.current_tonality[-1]
            transposed_note = tr.transpose_chord(note, -1)
            new_tonality = transposed_note + chord_type
            gui_instance.current_tonality = new_tonality
        elif "m" in gui_instance.current_tonality and len(gui_instance.current_tonality) == 2:
            gui_instance.current_tonality = gui_instance.current_tonality.replace("m ", "b")
            new_tonality = tr.transpose_chord(gui_instance.current_tonality, -1)
            gui_instance.current_tonality = new_tonality
        else:
            new_tonality = tr.transpose_chord(gui_instance.current_tonality, -1)
            gui_instance.current_tonality = new_tonality
        gui_instance.song_data = {
            "tonality": new_tonality,
            "words_and_positionand_and_chords": transposed_map,
        }
        gui_instance.clear_windows()
        gui_instance.window_for_transpose(gui_instance.song_data)

    def play_song(self, gui_instance):
        """Відтрорює акорди.

        Args:
        - gui_instance: екземпляр класу GUI, який надає доступ до словника 'words_and_positions' (слово-позиція-акорд).

        Notes
        -----
        Session() - звуковва доріжка, яка дає можливість записувати акорди.
        Session складається з Ensemble (має різні інструменти), Clock(керує час, тривалість), 
        Transcriber(записує музику, яку можуть грати всі інструменти)

        """
        list_of_chords = []
        for key, chord in  gui_instance.words_and_positions.items():
            if chord != None:
                list_of_chords.append(chord)
        for chord in list_of_chords:
            notes = chord[0]
            scale = chord[1:]
            if scale == "b":
                scale = "minor"
            elif scale == "":
                scale = "major"
            elif scale == "#":
                notes = tr.transpose_chord(notes, 2)
                scale = "minor"
            elif "#" in scale and "7" in scale:
                scale = scale[1:]
                notes = tr.transpose_chord(notes, 1)
            elif "b" in scale and "7" in scale:
                scale = scale[1:]
                notes = tr.transpose_chord(notes, -1)
            p_chord = get_chord(notes, scale)
            print(p_chord)
            s = Session(max_threads=3) 
            guitar = s.new_part('Guitar Nylon X')
            list_notes = []
            for note in p_chord:
                list_notes.append(self.notes[note.name])
            duration = 0
            if "A" or "E" in p_chord:
                duration += 1
            guitar.play_chord(list_notes, 1.0, duration)


root = Tk()
song_editor = GUI(root)
song_editor.main_widget()