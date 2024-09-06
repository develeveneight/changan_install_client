import platform
import os
import secrets
import shutil
import string
import subprocess
from sys import exit

import requests
from tqdm import tqdm

from helpers.lang import en, ru, zh, ar, pt, es, tr, id


# TODO: Add docstring dor methods

def set_language():
    _lang = os.getenv('LANG', 'en')
    if _lang == 'en':
        return en
    elif _lang == 'ru':
        return ru
    elif _lang == 'zh':
        return zh
    elif _lang == 'ar':
        return ar
    elif _lang == 'pt':
        return pt
    elif _lang == 'es':
        return es
    elif _lang == 'tr':
        return tr
    elif _lang == 'id':
        return id


lang = set_language()


def clear_screen():
    # Для Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # Для Mac и Linux
    else:
        _ = os.system('clear')


def cmd(app, params, show_stdout=True):
    args_list = [str(app)]
    if isinstance(params, list):
        args_list.extend(params)
    else:
        args_list.append(params)
    try:
        # print(args_list)
        result = subprocess.run(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if show_stdout:
            print(result)
        if result.returncode == 0:
            if show_stdout:
                print(result.stdout, result.stderr)
            return result.stdout if result.stdout else result.stderr
        else:
            if show_stdout:
                print(result.stderr)
            return False
    except Exception as e:
        print("Exception: ", e)
        return False


def clear_folder(folder_path, force_folder=False):
    if not force_folder:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    else:
        shutil.rmtree(folder_path)


def exit_on_any_key():
    print(lang.PRESS_ANY_KEY_TO_EXIT)
    system = platform.system()
    if system == "Windows":
        import msvcrt
        msvcrt.getch()  # Ожидает нажатия любой клавиши
        exit()
    else:
        exit()


def clear_input_buffer():
    system = platform.system()
    if system == "Windows":
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()


def continue_on_any_key():
    system = platform.system()
    if system == "Windows":
        import msvcrt
        clear_input_buffer()
        print(lang.PRESS_ANY_KEY)
        msvcrt.getch()  # Ожидает нажатия любой клавиши
    else:
        input("Press Enter to continue...")  # Ожидает нажатия клавиши Enter


def generate_custom_id(length):
    characters = string.ascii_letters + string.digits
    unique_value = ''.join(secrets.choice(characters) for _ in range(length))
    return unique_value


def download_file(url, file_path):
    # Отправка HTTP GET-запроса
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))  # Общий размер файла
        block_size = 8192  # Размер блока в байтах
        desc = generate_custom_id(16)

        with open(file_path, 'wb') as f:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=desc) as progress_bar:
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:  # Проверка, что блок данных не пустой
                        f.write(chunk)
                        progress_bar.update(len(chunk))  # Обновление прогресс-бара на размер блока
