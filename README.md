# Sheet Music Editor

Семетровий проєкт "Нотний редактор".

Програма з графічним інтерфейсом, яка має такі властивості:

- написання власної пісні з додаванням акордів та вибору тональності;

- збереження пісні у файл json;

- транспонування акордів, а саме тризвуків та септакордів;

- відкриття файлу txt і робота з ним;

- програвання акордів.
---
Програма має три класи: GUI, Song, Transposer. 

Бібліотеки:
- tkinker
- pytransposer
- musicpy
- scamp
tkinter - "Label", "Button", "Frame", "Listbox", "Text"
          "Scrollbar", "Canvas", "Toplevel", "Entry", "Tk"

pytransposer - "tr.transpose_chord" (транспонування тризвуків)

musicpy - "get_chord", "mp.alg.detect" (транспонування септакордів)

scamp - "play_chord" (вітвореня акордів, Guitar Nylon X)

---
Посилання на [презентація](https://www.canva.com/design/DAGHAMRkDqg/0w9uHvJZKA1hyqgQbZ7LQQ/edit)

У презентації продемонстровано як працює програма та коротко розписано про структуру коду UML-діаграма.

UML-діаграма
<img width="1060" alt="Знімок екрана 2024-06-04 о 16 29 23" src="https://github.com/katyasolovii/project/assets/144212333/b7c4b9c4-5099-4d16-9bf2-7f37e34ec54e">
