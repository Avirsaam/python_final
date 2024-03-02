"""
Напишите код, который запускается из командной строки и
получает на вход путь до директории на ПК.

Соберите информацию о содержимом в виде объектов namedtuple.
Каждый объект хранит:
 - имя файла без расширения или название каталога,
 - расширение, если это файл,
 - флаг каталога,
 - название родительского каталога.

 Написать 3-5 тестов к задаче.

Сдавать дз ссылкой на репозиторий GitHub(проверьте что он не приватный перед отправкой).
"""
import sys
from collections import namedtuple
import argparse
from pathlib import Path

FileSystemObject = namedtuple('FileSystemObject', ['node_name', 'extension', 'is_dir', 'parent_name'])

def parse_directory(root_dir):
    """
    Рекурсивно сканирует дирекорию и поддикектории файловой системы
    Возвращает список состоящий из экземпляров
    класса FileSystemObject созданного на основе namedtuple
    """

    result = []
    for obj in Path(root_dir).iterdir():
        this_object = (FileSystemObject(
            node_name=obj.name[:obj.name.find(obj.suffix)] if len(obj.suffix) else obj.name,
            extension=obj.suffix[1:],
            is_dir=obj.is_dir(),
            parent_name=obj.parent.resolve().stem
        ))
        result.append(this_object)

        if obj.is_dir() and any(obj.iterdir()):
            result.extend(parse_directory(Path(root_dir / Path(this_object.node_name))))

    return result




def argparser(args):
    """
    Функция парсер аргументов,
    возвращает имя директории для сканирования или останавливает
    программу с выводом справки в случае некорректности ввода в командной строке
    """
    argparser = argparse.ArgumentParser(description='скрипт-парсер файловой системы', exit_on_error=False)
    argparser.add_argument('dir_path', metavar='dir_path', type=str, nargs='?',
                           help='путь к директории (относительный или абсолютный), текущая директория по умолчанию')

    return argparser.parse_args(args).dir_path



if __name__ == '__main__':
    if len(sys.argv) != 2:
        argparser(['-h'])
    root_dir = Path(argparser(sys.argv[1:]))
    parse_result = []
    if root_dir.exists():
        print(parse_directory(root_dir))
    else:
        print(f'Path provided {root_dir} is not a valid path')






