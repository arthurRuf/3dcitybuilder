import zipfile, shutil,os
from . import progress_bar, logger

def create_dirs(path):
    os.makedirs(path, exist_ok=True)

def create_temp_dirs(path):
    os.makedirs(f"{path}/ortho", exist_ok=True)
    os.makedirs(f"{path}/dtm", exist_ok=True)
    os.makedirs(f"{path}/dsm", exist_ok=True)
    os.makedirs(f"{path}/footprint", exist_ok=True)

def unzip_file(zip_file, destination):
    zf = zipfile.ZipFile(f"{zip_file}")

    p = progress_bar.create(len(zf.infolist()))
    logger.update_progress(step_current=0, step_maximum=len(zf.infolist()))
    for file in zf.infolist():
        progress_bar.update(p)
        logger.increase_step_current()
        zf.extract(file, path=f"{destination}/")

    progress_bar.done(p)


def copy_file(source, destination):
    shutil.copy(f"{source}", f"{destination}")

def move_file(source, destination):
    shutil.move(f"{source}", f"{destination}")

def path_cleanup(path):
    return path.split("|")[0]
