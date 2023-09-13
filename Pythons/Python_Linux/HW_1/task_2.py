"""Задание № 2. Доработать функцию из предыдущего задания таким образом, чтобы у неё появился дополнительный режим работы,
в котором вывод разбивается на слова с удалением всех знаков пунктуации (их можно взять из списка string.punctuation
модуля string). В этом режиме должно проверяться наличие слова в выводе."""

import subprocess
import string


def check_out(cmd, text, split_mode=False):
    """
    Функция для выполнения команды и проверки наличия текста в её выводе.

    Параметры:
    cmd (str): Команда для выполнения.
    text (str): Текст для поиска в выводе команды.
    split_mode (bool, optional): Если True, функция будет искать точное совпадение слова в выводе команды,
                             игнорируя знаки пунктуации. По умолчанию False.

    Возвращает:
    bool: True, если текст найден в выводе команды и команда успешно выполнена. Иначе False.
    """
    # Выполнение команды
    output = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')

    if split_mode:
        # Удаление знаков пунктуации из вывода
        s = output.stdout
        for c in string.punctuation:
            s = s.replace(c, "")

        # Разбиение вывода на слова
        list_out = s.split()

        # Проверка наличия слова в выводе и успешного выполнения команды
        if text in list_out and output.returncode == 0:
            return True
        else:
            return False
    else:
        # Проверка наличия текста в выводе и успешного выполнения команды
        if text in output.stdout and output.returncode == 0:
            return True
        else:
            return False


# Проверка наличия слова 'Linux' в выводе команды 'uname -a'
print(check_out('uname -a', 'Linux', split_mode=True))
