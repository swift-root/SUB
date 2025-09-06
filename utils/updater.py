import os
import sys
import time
import stat
import shutil
import requests
import subprocess
import platform
from pathlib import Path

def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)

EXCLUDE_FILES = ['settings/user.txt', 'db/db.db', 'settings/swift.session', '.env']
SKIP_FILES = ['changes.txt', 'README.md', 'install.py']

def get_os_specific_commands():
    system = platform.system()

    if system == "Windows":
        return {
            'python': 'python',
            'pip': 'pip',
            'clear': 'cls'
        }
    else:
        return {
            'python': 'python3',
            'pip': 'pip3',
            'clear': 'clear'
        }

def get_version_changes(new_version):
    try:
        changes_url = "https://raw.githubusercontent.com/swift-root/SUB/main/changes.txt"
        response = requests.get(changes_url, timeout=10)
        if response.status_code == 200:
            changes_text = response.text
            version_section = f"changes(version={new_version}):"

            if version_section in changes_text:
                start_idx = changes_text.index(version_section) + len(version_section)
                end_idx = changes_text.find("changes(version=", start_idx)
                if end_idx == -1:
                    return changes_text[start_idx:].strip()
                return changes_text[start_idx:end_idx].strip()
    except Exception:
        pass
    return "Информация об изменениях недоступна"

def update_bot():
    print("🚀 Запуск процесса обновления...")
    temp_dir = "temp_update"
    commands = get_os_specific_commands()

    try:
        if os.path.exists(temp_dir):
            print("🧹 Очистка временной директории...")
            shutil.rmtree(temp_dir, onerror=on_rm_error)

        print("⏬ Загружаем обновления из репозитория...")
        subprocess.run(["git", "clone", "https://github.com/swift-root/SUB.git", temp_dir],
                      check=True, capture_output=True)

        new_version = "0.0"
        version_file = os.path.join(temp_dir, "settings/version.txt")
        if os.path.exists(version_file):
            with open(version_file, "r", encoding="utf-8") as f:
                new_version = f.read().strip()

        print("🔄 Устанавливаем обновления...")

        for root, dirs, files in os.walk(temp_dir):
            relative_path = os.path.relpath(root, temp_dir)
            dst_root = os.path.join('.', relative_path)

            if not os.path.exists(dst_root):
                os.makedirs(dst_root)

            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dst_root, file)

                if file in SKIP_FILES:
                    continue

                if os.path.basename(dst_file) in EXCLUDE_FILES:
                    continue

                try:
                    shutil.copy2(src_file, dst_file)
                except Exception as e:
                    print(f"⚠️ Ошибка при копировании {src_file}: {e}")

        print("📦 Проверяем зависимости...")
        req_file = os.path.join(temp_dir, "requirements.txt")
        if os.path.exists(req_file):
            try:
                subprocess.check_call([commands['python'], "-m", "pip", "install", "-r", req_file])
            except subprocess.CalledProcessError:
                print("⚠️ Не удалось установить зависимости автоматически")

        changes = get_version_changes(new_version)
        os.makedirs("settings", exist_ok=True)
        with open("settings/version_info.txt", "w", encoding="utf-8") as f:
            f.write(f"{new_version}\n{changes}")

        print("🧹 Очистка временных файлов...")
        shutil.rmtree(temp_dir, onerror=on_rm_error)

        print("✅ Обновление завершено! Перезапускаем бота...")
        time.sleep(2)

        python_exec = sys.executable
        script_path = os.path.abspath("swift.py")

        if platform.system() == "Windows":
            subprocess.Popen([python_exec, script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen([python_exec, script_path], start_new_session=True)

        sys.exit(0)

    except Exception as e:
        print(f"❌ Ошибка при обновлении: {e}")
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir, onerror=on_rm_error)
            except Exception:
                pass
        sys.exit(1)

if __name__ == "__main__":
    update_bot()
