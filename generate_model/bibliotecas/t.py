import os, pathlib

if __name__ == '__main__':
    file_re = os.path.dirname(os.path.realpath(__file__))
    path = pathlib.Path(file_re)
    print(path.parent)
