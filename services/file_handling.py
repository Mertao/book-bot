import os

BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}


# Функция, возвращающая строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    end_signs = ',.!:;?'
    counter = 0
    if len(text) < start + size:  # если длина текста меньше
        size = len(text) - start    # делаем сайз равным всей длине текста (длина - старт)
        text = text[start:start + size]     # получаем срез текста 
    else:
        # если последний символ равен '.' и предпоследний символ в ',.!:;?'
        if text[start + size] == '.' and text[start + size - 1] in end_signs:
            text = text[start:start + size - 2]  # то мы убираем 2 последних символа
            size -= 2   # и, соответственно, уменьшаем size на 2 убранных символа
        else:
            # иначе обрезаем текст от старта и до конца
            text = text[start:start + size]
        # циклом проходимся от конца текста до первого символа из ',.!:;?'
        for i in range(size - 1, 0, -1):
            # если находим символ из ',.!:;?' то останавливаем цикл
            if text[i] in end_signs:
                break
            counter = size - i  # присваиваем переменной counter наш size - отрезок до символа
    page_text = text[:size - counter]  # итоговый текст равен size - отрезок до символа
    page_size = size - counter  # длина текста
    return page_text, page_size


# Функция, формирующая словарь книги
def prepare_book(path: str) -> None:
    # открываем и читаем файл
    with open(path, 'r') as file:
        text = file.read()
    start, page_number = 0, 1  # определяем старт и номер страницы
    while start < len(text):  # пока старт < длины текста
        # в функцию передаем текст, стартовую позицию и размер страницы
        # обратно получаем сам текст и размер получившийся страницы
        page_text, page_size = _get_part_text(text, start, PAGE_SIZE)
        start += page_size  # к старту прибавляем размер получившийся страницы
        # добавляем страницу в словарь по значению номер страницы:текст
        book[page_number] = page_text.strip()
        # прибавляем счетчик страниц
        page_number += 1


# Вызов функции prepare_book для подготовки книги из текстового файла
prepare_book(os.path.join(os.getcwd(), BOOK_PATH))
