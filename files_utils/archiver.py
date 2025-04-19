import zipfile
from datetime import datetime
import shutil
import os
from files_utils.logg import log_message


def archive_old_files(file_list, base_path):
    if not file_list:
        return

    if not os.path.exists("archive"):
        os.makedirs("archive")

    date = datetime.now().strftime("%Y-%m-%d")
    archive_name = os.path.join("archive", f"old_files_{date}.zip")

    with zipfile.ZipFile(archive_name, "w") as zipf:
        for file in file_list:
            try:
                zipf.write(file, os.path.relpath(file, base_path))
                os.remove(file)
                log_message(f"Файл заархивирован и удалён: {file}")
            except Exception as e:
                log_message(f"Не удалось заархивировать {file}: {e}")