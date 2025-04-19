import sys
import os

from files_utils.analyzer import analyze_directory
from files_utils.cache import load_cache, save_cache
from files_utils.archiver import archive_old_files
from files_utils.logg import log_message

def main():
    try:
        path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
        log_message(f"Запуск анализа директории: {path}")

        cache = load_cache()
        result = analyze_directory(path, cache)
        save_cache(result["new_cache"])
        archive_old_files(result["old_files"], path)

        print("Готово!")
    except Exception as e:
        log_message(f"Ошибка при запуске: {e}")
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
