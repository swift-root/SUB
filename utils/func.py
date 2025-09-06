from utils.imports import *
import io

async def answer(message: Message, text: str = None, photo: bool = False, response: str = None):
    if text:
        await message.reply(text)
    if photo and response:
        await message.reply_photo(photo=response)

ALLOWED_MIME_TYPES = [
    "text/plain",  # .txt
    "application/x-python",  # .py
    "application/javascript",  # .js
    "application/json",  # .json
    "text/html",  # .html
    "text/css",  # .css
    "text/csv",  # .csv
    "application/xml",  # .xml
    "text/markdown",  # .md
]

ALLOWED_EXTENSIONS = [".txt", ".py", ".js", ".json", ".html", ".css", ".csv", ".xml", ".md"]

async def read_text_file(client, message, file):
    if file.file_size > 10 * 1024 * 1024:  # Лимит 10 МБ
        await message.edit("[❗️] Файл слишком большой для обработки.")
        return None

    mime_type = file.mime_type
    file_ext = os.path.splitext(file.file_name)[1].lower()

    if mime_type not in ALLOWED_MIME_TYPES and file_ext not in ALLOWED_EXTENSIONS:
        await message.edit(f"[❗️] Неподдерживаемый формат файла: <code>{file_ext}</code>")
        return None

    try:
        file_data = io.BytesIO()
        await client.download_media(file, file_name=file_data)
        
        # Получаем содержимое как байты
        file_bytes = file_data.getvalue()
        
        # Пробуем разные кодировки
        try:
            file_content = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            try:
                file_content = file_bytes.decode("latin-1")
            except Exception:
                await message.edit("[❌] Не удалось определить кодировку файла.")
                return None

        return file_content

    except Exception as e:
        await message.edit(f"[❌] Ошибка при чтении файла: {str(e)}")
        return None