"""Переделать все шаги негативных тестов на выполнение по SSH. Проверить работу."""
from ssh_checks import ssh_checkout_negatives
import yaml


class TestNegative:

    def __init__(self):
        # Загрузка данных из конфигурационного файла
        with open("config.yaml") as f:
            self.data = yaml.safe_load(f)

    def run_ssh_negative_check(self, command):
        # Выполнение SSH-команды с ожидаемой неудачной проверкой
        return ssh_checkout_negatives(self.data['host'], self.data['user'], self.data['password'], command, "")

    def negative_tests(self, make_folders, make_bad_files):
        # Тест 1: Попытка извлечения из некорректного архива
        assert self.run_ssh_negative_check(f"cd {self.data['folder_out']}; 7z e {make_bad_files}"), "test 1 FAIL"
        # Тест 2: Попытка проверки некорректного архива
        assert self.run_ssh_negative_check(f"cd {self.data['folder_out']}; 7z t arx2bad.7z"), "test 2 FAIL"
