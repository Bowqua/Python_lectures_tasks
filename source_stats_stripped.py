import sys
from pathlib import Path
from fontTools.misc import filenames


def project_stats(path, extensions):
    """
    Вернуть число строк в исходниках проекта.

    Файлами, входящими в проект, считаются все файлы
    в папке ``path`` (и подпапках), имеющие расширение
    из множества ``extensions``.
    """

    project_dir = Path(path)
    if not project_dir.is_dir():
        raise NotADirectoryError(path)

    files = iter_filenames(project_dir)
    cs_files = with_extensions(extensions, files)

    return total_number_of_lines(cs_files)

def total_number_of_lines(filenames):
    """
    Вернуть общее число строк в файлах ``filenames``.
    """

    count_lines = lambda f: sum(1 for _ in f.open("r", encoding="utf-8")) if f.is_file() else 0
    return sum(map(count_lines, filenames))

def number_of_lines(filename):
    """
    Вернуть число строк в файле.
    """

    count_lines = lambda f: (f, sum(1 for _ in f.open("r", encoding="utf-8")) if f.is_file() else 0)
    return dict(map(count_lines, filenames))

def iter_filenames(path):
    """
    Итератор по именам файлов в дереве.
    """

    path = Path(path)
    if not path.is_dir():
        raise NotADirectoryError(path)

    return filter(lambda f: f.is_file(), path.rglob("*"))

def with_extensions(extensions, filenames):
    """
    Оставить из итератора ``filenames`` только
    имена файлов, у которых расширение - одно из ``extensions``.
    """

    extensions_set = set(ext.lower() for ext in extensions)
    return filter(lambda f: f.suffix.lower() in extensions_set, filenames)

def get_extension(filename):
    """ Вернуть расширение файла """

    return Path(filename).suffix

def print_usage():
    print("Usage: python project_sourse_stats_3.py <NSimulator>")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_usage()
        sys.exit(1)

    project_path = sys.argv[1]
    print(project_stats("NSimulator", {'.cs'}))