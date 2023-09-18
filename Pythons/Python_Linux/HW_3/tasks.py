"""Задание 1. Дополнить проект фикстурой, которая после каждого шага теста дописывает в заранее созданный файл stat.txt
строку вида: время, кол-во файлов из конфига, размер файла из конфига, статистика загрузки процессора из файла
/proc/loadavg (можно писать просто всё содержимое этого файла).
Задание 2. (дополнительное задание)
Дополнить все тесты ключом команды 7z -t (тип архива). Вынести этот параметр в конфиг."""

import pytest
import subprocess
import time
import os
import yaml  # Импорт библиотеки PyYAML
from HW_1.task_2 import check_out

# Чтение типа архива из конфигурационного файла YAML
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
archive_type = config['archive_type']


@pytest.fixture(autouse=True)
def log_stats():
    # Выполняется перед каждым тестом
    start_time = time.time()
    yield  # Здесь выполняется тест
    # Выполняется после каждого теста
    end_time = time.time()
    duration = end_time - start_time
    with open('/proc/loadavg', 'r') as f:
        loadavg = f.read().strip()
    with open('stat.txt', 'a') as f:
        f.write(f'{duration}, {len(os.listdir())}, {os.path.getsize("test.7z")}, {loadavg}\n')


def test_list_files():
    cmd = f"7z l -t{archive_type} test.7z"  # Команда вывода списка файлов (l)
    assert check_out(cmd, "test.7z")


def test_extract_archive():
    cmd = f"7z x -t{archive_type} test.7z"  # Команда разархивирования test.7z с путями (x)
    assert check_out(cmd, "Everything is Ok")


def test_calc_hash():
    cmd = f"7z h -t{archive_type} test.7z"  # Команда расчёта хеша файла test.7z (h)
    expected_hash = "5E4994D2"  # Ожидаемое значение хеша
    output = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    calculated_hash = output.stdout.strip()
    assert calculated_hash == expected_hash
