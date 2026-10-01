import json
import os
import shutil
import socket
import sys
from datetime import datetime
from pathlib import Path


# Определяем операционную систему.
if sys.platform == "win32":
    os_name = "Windows"
elif sys.platform == "linux":
    os_name = "Linux"
elif sys.platform == "darwin":
    os_name = "macOS"
else:
    print(f"Эта операционная система не поддерживается: {sys.platform}")
    sys.exit(1)

# Получаем версию и архитектуру без запуска команд ОС.
if os_name == "Windows":
    major, minor, build = sys.getwindowsversion().platform_version
    os_version = f"{major}.{minor}.{build}"
    architecture = (
        os.environ.get("PROCESSOR_ARCHITEW6432")
        or os.environ.get("PROCESSOR_ARCHITECTURE")
        or None
    )
else:
    system_info = os.uname()
    os_version = system_info.release
    architecture = system_info.machine or None

# Проверяем раздел, на котором находится скрипт.
script_folder = Path(__file__).resolve().parent
try:
    disk_info = shutil.disk_usage(script_folder)
except OSError as error:
    print(f"Не удалось получить сведения о диске: {error}")
    sys.exit(1)

# Собираем данные в словарь. Размеры храним в байтах.
data = {
    "collected_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    "os": {
        "name": os_name,
        "version": os_version,
        "architecture": architecture,
    },
    "computer": {
        "hostname": socket.gethostname(),
        "logical_cpu_count": os.cpu_count(),
    },
    "disk": {
        "path": str(script_folder),
        "total_bytes": disk_info.total,
        "used_bytes": disk_info.used,
        "free_bytes": disk_info.free,
    },
    "python": {
        "version": sys.version.split()[0],
    },
}

# Сохраняем JSON рядом со скриптом.
output_file = script_folder / "os_info.json"
try:
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
except OSError as error:
    print(f"Не удалось записать файл: {error}")
    sys.exit(1)

print(f"Операционная система: {os_name}")
print(f"Результат сохранён в: {output_file}")
