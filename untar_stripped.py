import argparse
import os.path
import tarfile
import sys
from datetime import *


class TarParser:
    _HEADER_FMT1 = '100s8s8s8s12s12s8sc100s255s'
    _HEADER_FMT2 = '6s2s32s32s8s8s155s12s'
    _HEADER_FMT3 = '6s2s32s32s8s8s12s12s112s31x'
    _READ_BLOCK = 16 * 2**20

    _FILE_TYPES = {
        b'0': 'Regular file',
        b'1': 'Hard link',
        b'2': 'Symbolic link',
        b'3': 'Character device node',
        b'4': 'Block device node',
        b'5': 'Directory',
        b'6': 'FIFO node',
        b'7': 'Reserved',
        b'D': 'Directory entry',
        b'K': 'Long linkname',
        b'L': 'Long pathname',
        b'M': 'Continue of last file',
        b'N': 'Rename/symlink command',
        b'S': "`sparse' regular file",
        b'V': "`name' is tape/volume header name"
    }

    def __init__(self, filename):
        '''
        Открывает tar-архив `filename' и производит его предобработку
        (если требуется)
        '''

        if not os.path.isfile(filename):
            raise FileNotFoundError(f'File {filename} not found')
        try:
            self.tar = tarfile.open(filename, "r")
        except tarfile.TarError as e:
            raise ValueError(f"Error opening {e}")
        self.files = sorted(self.tar.getnames())


    def extract(self, dest=os.getcwd()):
        '''
        Распаковывает данный tar-архив в каталог `dest'
        '''

        if not os.path.isdir(dest):
            os.makedirs(dest)
        self.tar.extractall(path=dest)
        self.tar.close()

    def files(self):
        '''
        Возвращает итератор имён файлов (с путями) в архиве
        '''

        return iter(self.files)

    def file_stat(self, filename):
        '''
        Возвращает информацию о файле `filename' в архиве.
        '''

        if filename not in self.files:
            raise ValueError(f"File {filename} not found")

        tar_info = self.tar.getmember(filename)
        info = [
            ('Filename', tar_info.name),
            ("Type", self._FILE_TYPES.get(tar_info.type, "Unknown")),
            ("Mode", f"{tar_info.mode:06o}"),
            ("UID", str(tar_info.uid)),
            ("GID", str(tar_info.gid)),
            ("Size",str(tar_info.size)),
            ('Modification time', datetime.datetime.fromtimestamp(tar_info.mtime)
             .strftime('%d %b %Y %H:%M:%S')),
            ("Checksum", str(tar_info.chksum)),
            ("User name", str(tar_info.uname)),
            ("Group name", str(tar_info.gname)),
        ]

        return info


def print_file_info(stat, f=sys.stdout):
    max_width = max(map(lambda s: len(s[0]), stat))
    for field in stat:
        print("{{:>{}}} : {{}}".format(max_width).format(*field), file=f)


def main():
    parser = argparse.ArgumentParser(
        usage='{} [OPTIONS] FILE'.format(os.path.basename(sys.argv[0])),
        description='Tar extractor')
    parser.add_argument('-l', '--list', action='store_true', dest='ls',
                        help='list the contents of an archive')
    parser.add_argument('-x', '--extract', action='store_true', dest='extract',
                        help='extract files from an archive')
    parser.add_argument('-i', '--info', action='store_true', dest='info',
                        help='get information about files in an archive')
    parser.add_argument('fn', metavar='FILE',
                        help='name of an archive')

    args = parser.parse_args()
    if not (args.ls or args.extract or args.info):
        sys.exit("Error: action must be specified")

    try:
        tar = TarParser(args.fn)

        if args.info:
            for fn in sorted(tar.files()):
                print_file_info(tar.file_stat(fn))
                print()
        elif args.ls:
            for fn in sorted(tar.files()):
                print(fn)

        if args.extract:
            tar.extract()
    except Exception as e:
        sys.exit(e)

if __name__ == '__main__':
    main()
