import hashlib
import os
import time
import glob
import tempfile
import shutil
from collections import defaultdict
from files_utils.logg import log_message


def get_md5(file_path):
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    except Exception as e:
        log_message(f"Ошибка при вычислении MD5 для {file_path}: {e}")
        return None
    return hash_md5.hexdigest()


def analyze_directory(path, old_cache):
    new_cache = {}
    old_files = []
    duplicates = defaultdict(list)
    folder_sizes = {}

    now = time.time()

    all_files = glob.glob(os.path.join(path, "**"), recursive=True)

    for file_path in all_files:
        if not os.path.isfile(file_path):
            continue

        try:
            stat = os.stat(file_path)
            mtime = stat.st_mtime
            size = stat.st_size

            if file_path in old_cache and old_cache[file_path]['mtime'] == mtime:
                continue

            file_info = {'mtime': mtime, 'size': size}
            new_cache[file_path] = file_info

            folder = os.path.dirname(file_path)
            folder_sizes[folder] = folder_sizes.get(folder, 0) + size

            if (now - mtime) > 30 * 86400:
                old_files.append(file_path)

            md5 = get_md5(file_path)
            if md5:
                duplicates[(size, md5)].append(file_path)

        except Exception as e:
            log_message(f"Ошибка при анализе {file_path}: {e}")

    try:
        with tempfile.NamedTemporaryFile("w", delete=False, suffix="_report.txt", encoding="utf-8") as temp_report:
            for folder, size in folder_sizes.items():
                temp_report.write(f"{folder}: {round(size / 1024 / 1024, 2)} MB\n")
        shutil.move(temp_report.name, "report.txt")
    except Exception as e:
        log_message(f"Ошибка при создании отчета: {e}")

    return {"new_cache": new_cache, "old_files": old_files}
