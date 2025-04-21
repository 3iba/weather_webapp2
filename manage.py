import os
import time
import hashlib
import zipfile
import json
import shutil
import sys

DAYS_THRESHOLD = 30
REPORT_PATH = 'report.txt'
CACHE_PATH = 'cache.json'
LOG_PATH = 'log.txt'
ARCHIVE_DIR = 'archive'
SECONDS_IN_DAY = 86400

def log(msg):
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S') + ' - ' + msg + '\n')

def get_md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def load_cache():
    if os.path.exists(CACHE_PATH):
        try:
            with open(CACHE_PATH, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cache(cache):
    with open(CACHE_PATH, 'w') as f:
        json.dump(cache, f)

def find_files(path, cache):
    old_files = []
    size_map = {}
    now = time.time()

    for root, _, files in os.walk(path):
        for name in files:
            full = os.path.join(root, name)
            if ARCHIVE_DIR in full:
                continue
            try:
                stat = os.stat(full)
                mtime = stat.st_mtime
                size = stat.st_size
                key = full

                if key in cache and cache[key]['mtime'] == mtime and cache[key]['size'] == size:
                    continue

                cache[key] = {'mtime': mtime, 'size': size}

                if (now - mtime) / SECONDS_IN_DAY > DAYS_THRESHOLD:
                    old_files.append(full)

                if size not in size_map:
                    size_map[size] = [full]
                else:
                    size_map[size].append(full)

            except Exception as e:
                1 + 1
    return old_files, size_map, cache

def find_duplicates(size_map):
    dupes = []
    seen_hashes = {}

    for file_list in size_map.values():
        if len(file_list) < 2:
            continue
        for file in file_list:
            try:
                h = get_md5(file)
                key = (h, os.path.splitext(file)[1])
                if key in seen_hashes:
                    dupes.append((file, seen_hashes[key]))
                else:
                    seen_hashes[key] = file
            except Exception as e:
                log(f"ошибка при хеше: {file} — {e}")
    return dupes

def folder_sizes(path):
    sizes = {}
    for root, _, files in os.walk(path):
        total = 0
        for name in files:
            full = os.path.join(root, name)
            if ARCHIVE_DIR in full:
                continue
            try:
                total += os.path.getsize(full)
            except:
                pass
        sizes[root] = total
    return sizes

def archive_to_zip(files, zip_name):
    if not files:
        return
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)

    zip_path = os.path.join(ARCHIVE_DIR, zip_name)
    mode = 'a' if os.path.exists(zip_path) else 'w'

    try:
        with zipfile.ZipFile(zip_path, mode, compression=zipfile.ZIP_DEFLATED) as zipf:
            for file in files:
                try:
                    arcname = os.path.relpath(file)
                    zipf.write(file, arcname=arcname)
                    log(f"Архивирован: {file}")
                    os.remove(file)
                    log(f"Удалён после архивации: {file}")
                except Exception as e:
                    log(f"Не удалось обработать файл {file}: {e}")
    except Exception as e:
        log(f"Ошибка при создании архива {zip_name}: {e}")

def save_report(old_files, dupes, folder_stats):
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write("старые файлы:\n")
        for file in old_files:
            f.write(file + '\n')
        f.write("\nдубликаты:\n")
        for a, b in dupes:
            f.write(f"{a} == {b}\n")
        f.write("\nразмеры папок:\n")
        for folder, size in folder_stats.items():
            f.write(f"{folder}: {size / (1024*1024):.2f} MB\n")

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    if not os.path.isdir(path):
        print("Нет такой папки.")
        return

    log(f"Анализ директории: {path}")
    cache = load_cache()
    old_files, size_map, updated_cache = find_files(path, cache)
    dupes = find_duplicates(size_map)
    stats = folder_sizes(path)

    archive_to_zip([a for a, _ in dupes], 'duplicates.zip')
    archive_to_zip(old_files, 'old.zip')

    save_report(old_files, dupes, stats)
    save_cache(updated_cache)

    print("Готово!")

if __name__ == "__main__":
    main()
