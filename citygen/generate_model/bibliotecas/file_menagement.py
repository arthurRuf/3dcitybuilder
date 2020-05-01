import zipfile, shutil
from . import progress_bar


def unzip_file(zip_file, destination):
    zf = zipfile.ZipFile(f"{zip_file}")

    p = progress_bar.create(len(zf.infolist()))
    for file in zf.infolist():
        progress_bar.update(p)
        zf.extract(file, path=f"{destination}/")

    progress_bar.done(p)


def copy_file(source, destination):
    shutil.copy(f"{source}", f"{destination}")
