from utils.imports import *
from swift import get_settings

def owner_filter():
    async def func(_, __, message: Message):
        settings = get_settings()
        return message.from_user and message.from_user.id == settings['owner_id']
    
    return filters.create(func, "OwnerFilter")

def is_owner(user_id: int) -> bool:
    settings = get_settings()
    return user_id == settings['owner_id']

def allowed_users_filter():
    async def func(_, __, message: Message):
        settings = get_settings()
        return (message.from_user and 
                (message.from_user.id == settings['owner_id'] or 
                 message.from_user.id in settings['allow']))
    
    return filters.create(func, "AllowedUsersFilter")

async def answer(message: Message, text: str = None, photo: bool = False, response: str = None):
    if text:
        await message.reply(text)
    if photo and response:
        await message.reply_photo(photo=response)

ALLOWED_MIME_TYPES = [
    "text/plain",
    "application/x-python",
    "application/javascript",
    "application/json",
    "text/html",
    "text/css",
    "text/csv",
    "application/xml",
    "text/markdown",
]

ALLOWED_EXTENSIONS = [".txt", ".py", ".js", ".json", ".html", ".css", ".csv", ".xml", ".md"]

async def read_text_file(client, message, file):
    if file.file_size > 10 * 1024 * 1024:
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
        
        file_bytes = file_data.getvalue()
        
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
