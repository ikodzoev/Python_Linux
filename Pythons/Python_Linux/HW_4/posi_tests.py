"""Переделать все шаги позитивных тестов на выполнение по SSH. Проверить работу."""
import yaml
from ssh_checks import ssh_checkout, upload_files, ssh_getout


class TestPositive:

    def __init__(self):
        # Загрузка данных из конфигурационного файла
        with open("config.yaml") as f:
            self.data = yaml.safe_load(f)

    def save_log(self, start_time, name):
        # Сохранение журнала системных логов
        with open(name, "w") as f:
            f.write(ssh_getout(self.data['host'], self.data['user'], self.data['password'],
                               f"journalctl --since '{start_time}'"))

    def run_ssh_command(self, command, expected_output):
        # Выполнение SSH-команды и проверка ожидаемого вывода
        return ssh_checkout(self.data['host'], self.data['user'], self.data['password'], command, expected_output)

    def test_load_and_install(self, start_time):
        # Тест 0: Загрузка файлов и установка пакета p7zip.deb
        res = [upload_files(self.data['host'], self.data['user'], self.data['password'], self.data['local_path'],
                            self.data['remote_path']),
               self.run_ssh_command("echo '123' | sudo -S dpkg -i p7zip.deb", "Настраивается пакет"),
               self.run_ssh_command("echo '123' | sudo -S dpkg -s p7zip-full", "Status: installed is ok")]
        self.save_log(start_time, 'test_log.txt')
        assert all(res), "test load and install FAIL"

    def test_new_archive(self, start_time):
        # Тест 1: Создание архива
        res = []
        folder_tst = self.data['folder_in']
        folder_out = self.data['folder_out']
        output_file = self.data['output_file']
        key_t = self.data['archive_type']

        res.append(
            self.run_ssh_command(f"cd {folder_tst}; 7z a {key_t} {folder_out}/{output_file}", "Everything is Ok"))
        res.append(self.run_ssh_command(f"ls {folder_out}; ", output_file))
        self.save_log(start_time, 'test_log.txt')
        assert all(res), "test new archive FAIL"

    def test_extract_and_lists(self, start_time):
        # Тест 2: Распаковка архива и Тест 6: Проверка списка файлов в архиве
        res = []
        folder_tst = self.data['folder_in']
        folder_out = self.data['folder_out']
        output_file = self.data['output_file']
        folder_ext = self.data['folder_ext']

        res.append(self.run_ssh_command(f"cd {folder_tst}; 7z a {folder_out}/{output_file}", "Everything is Ok"))
        res.append(self.run_ssh_command(f"cd {folder_out}; 7z e {output_file} -o{folder_ext}", "Everything is Ok"))
        for file_name in self.data['make_files']:
            res.append(self.run_ssh_command(f"cd {folder_out}; 7z l {output_file}", file_name))
        assert all(res), "test extract and lists FAIL"

    def test_check_file(self, start_time):
        # Тест 3: Проверка файла в архиве
        folder_out = self.data['folder_out']
        output_file = self.data['output_file']
        assert self.run_ssh_command(f"cd {folder_out}; 7z t {output_file}", "Everything is Ok"), "test check file FAIL"

    def test_update_archive(self, start_time):
        # Тест 4: Обновление архива
        folder_out = self.data['folder_out']
        output_file = self.data['output_file']
        assert self.run_ssh_command(f"cd {folder_out}; 7z u {output_file}",
                                    "Everything is Ok"), "test update archive FAIL"

    def test_remove_contents(self):
        # Тест 5: Удаление содержимого архива
        folder_out = self.data['folder_out']
        output_file = self.data['output_file']
        assert self.run_ssh_command(f"cd {folder_out}; 7z d {output_file}",
                                    "Everything is Ok"), "test remove contents FAIL"

    def test_extract_archive(self, start_time):
        # Тест 6: Распаковка с сохранением структуры
        res = []
        folder_tst = self.data['folder_in']
        folder_out = self.data['folder_out']
        output_file = self.data['output_file']
        folder_ext = self.data['folder_ext']
        make_sub_folders = self.data['make_sub_folders']

        res.append(self.run_ssh_command(f"cd {folder_tst}; 7z a {folder_out}/{output_file}", "Everything is Ok"))
        res.append(self.run_ssh_command(f"cd {folder_out}; 7z x {output_file} -o{folder_ext}", "Everything is Ok"))
        for file_name in self.data['make_files']:
            res.append(self.run_ssh_command(f"ls {folder_ext}; ", file_name))

        res.append(self.run_ssh_command(f"ls {folder_ext}; ", make_sub_folders[0]))
        res.append(self.run_ssh_command(f"ls {folder_ext}/{make_sub_folders[0]}; ", make_sub_folders[1]))
        assert all(res), "test extract archive FAIL"

    def test_compare_hash(self, start_time):
        # Тест 7: Сравнение хешей
        res = []
        folder_tst = self.data['folder_in']
        make_files = self.data['make_files']

        for file_name in make_files:
            hash_file = self.run_ssh_command(f"cd {folder_tst}; crc32 {file_name}").upper()
            res.append(self.run_ssh_command(f"cd {folder_tst}; 7z h {file_name}", hash_file))
        assert all(res), "test compare hash FAIL"

    def test_remove(self, start_time):
        # Тест 8: Удаление пакета p7zip-full
        res = [self.run_ssh_command("echo '123' | sudo -S dpkg -r p7zip-full", "Удаляется p7zip-full"),
               self.run_ssh_command("echo '123' | sudo -S dpkg -s p7zip-full", "Status: uninstall is ok")]
        self.save_log(start_time, 'test_log.txt')
        assert all(res), "test remove FAIL"
