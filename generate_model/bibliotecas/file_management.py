import zipfile, shutil,os
from . import progress_bar, logger

def create_dirs(path):
    os.makedirs(path, exist_ok=True)

def create_temp_dirs(path):
    os.makedirs(os.path.join(path, "ortho"), exist_ok=True)
    os.makedirs(os.path.join(path, "dtm"), exist_ok=True)
    os.makedirs(os.path.join(path, "dsm"), exist_ok=True)
    os.makedirs(os.path.join(path, "footprint"), exist_ok=True)
    os.makedirs(os.path.join(path, "street"), exist_ok=True)
    os.makedirs(os.path.join(path, "tree"), exist_ok=True)
    os.makedirs(os.path.join(path, "water"), exist_ok=True)
    os.makedirs(os.path.join(path, "downolads"), exist_ok=True)

def unzip_file(zip_file, destination):
    zf = zipfile.ZipFile(f"{zip_file}")

    p = progress_bar.create(len(zf.infolist()))
    logger.update_progress(step_current=0, step_maximum=len(zf.infolist()))
    for file in zf.infolist():
        progress_bar.update(p)
        logger.increase_step_current()
        zf.extract(file, path=f"{destination}/")

    progress_bar.done(p)

def unzip_file_list(zip_file_list, destination_list):
    for index, url in enumerate(zip_file_list):
        unzip_file(zip_file_list[index], destination_list[index])


def copy_file(source, destination):
    shutil.copy(f"{source}", f"{destination}")

def move_file(source, destination):
    shutil.move(f"{source}", f"{destination}")

def path_cleanup(path):
    return path.split("|")[0]
