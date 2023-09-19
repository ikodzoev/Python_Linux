import pytest
import yaml
from ssh_checks import ssh_checkout, ssh_getout
from datetime import datetime

# Загрузка данных из конфигурационного файла
with open("config.yaml") as f:
    data = yaml.safe_load(f)


# Фикстура для записи времени запуска теста
@pytest.fixture()
def start_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Фикстура для создания необходимых каталогов
@pytest.fixture()
def make_folders():
    return ssh_checkout(data['host'], data['user'], data['password'],
                        f"mkdir {data['folder_in']} {data['folder_out']} {data['folder_ext']}", "")


# Фикстура для очистки каталогов
@pytest.fixture()
def clear_folders():
    return ssh_checkout(data['host'], data['user'], data['password'],
                        f"rm -rf {data['folder_in']}/* {data['folder_out']}/* {data['folder_ext']}/*", "")


# Фикстура для создания файлов
@pytest.fixture()
def make_files():
    list_files = []
    for i in range(data['count']):
        filename = f"file_{i}"
        if ssh_checkout(data['host'], data['user'], data['password'],
                        f"cd {data['folder_in']}; dd if=/dev/urandom of={filename} bs={data['bs']} count=1 iflag=fullblock",
                        ""):
            list_files.append(filename)
    return list_files


# Фикстура для создания подкаталога и файла в нем
@pytest.fixture()
def make_sub_folders():
    if ssh_checkout(data['host'], data['user'], data['password'], f"mkdir {data['folder_in']}/{data['sub_folder']} ",
                    ""):
        if ssh_checkout(data['host'], data['user'], data['password'],
                        f"cd {data['folder_in']}/{data['sub_folder']} ; dd if=/dev/urandom of=sub_file bs={data['bs']} count=1 iflag=fullblock",
                        ""):
            return f"{data['sub_folder']}", "sub_file"
        else:
            return f"{data['sub_folder']}", None
    else:
        return None, None


# Фикстура для создания некорректного архива
@pytest.fixture()
def make_bad_files():
    ssh_checkout(data['host'], data['user'], data['password'],
                 f"cd {data['folder_in']}; 7z a {data['folder_out']}/arx2bad", "Everything is Ok")
    ssh_checkout(data['host'], data['user'], data['password'],
                 f"truncate -s 1 {data['folder_out']}/arx2bad.7z", "")
    yield 'arx2bad.7z'
    ssh_checkout(data['host'], data['user'], data['password'],
                 f"rm -f {data['folder_out']}/arx2bad.7z", "")


# Фикстура для сохранения статистики после теста
@pytest.fixture()
def save_stat():
    yield
    # Получение статистики процессора
    static_proc = ssh_getout(data['host'], data['user'], data['password'], "cat /proc/loadavg")
    # Формирование строки статистики
    stat_str = f"{datetime.now()} - количество файлов: {data['count']}, размер: {data['bs']}, статистика процессора: {static_proc}"
    # Запись статистики в файл
    ssh_getout(data['host'], data['user'], data['password'], f"echo '{stat_str}' >> {data['stat_file']}")
