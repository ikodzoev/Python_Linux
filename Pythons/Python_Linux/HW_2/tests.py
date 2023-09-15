"""Задание 1.Условие:
Дополнить проект тестами, проверяющими команды вывода списка файлов (l) и разархивирования с путями (x).
Задание 2. Доработать проект, добавив тест команды расчёта хеша (h).
Проверить, что хеш совпадает с рассчитанным командой crc32."""

import subprocess
from HW_1.task_2 import check_out

def test_list_files():
    cmd = "ls"  # Команда вывода списка файлов (l)
    assert check_out(cmd, "test.7z")

def test_extract_archive():
    cmd = "7z x test.7z"  # Команда разархивирования test.7z с путями (x)
    assert check_out(cmd, "Everything is Ok")

def test_calc_hash():
    cmd = "crc32 test.7z"  # Команда расчёта хеша файла test.7z (h)
    expected_hash = "5E4994D2"  # Ожидаемое значение хеша
    output = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    calculated_hash = output.stdout.strip()
    assert calculated_hash == expected_hash

