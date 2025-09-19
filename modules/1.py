from utils.imports import *
from utils.func import *

#meta name: System
#meta developer: @lscmods & @lscuserbot
#meta description: Системные модули
#meta img: https://i.pinimg.com/736x/1e/57/41/1e5741cd9716634b91d34923d4afad55.jpg

start_time = time.time()
system = platform.system()

async def is_owner(_, client, message):
    try:
        user_id = message.from_user.id
        # Проверяем в базе данных
        db_owners = get_owners_from_db()
        return user_id in db_owners
    except:
        return False

# Создаем кастомный фильтр
owner_filter = filters.create(is_owner)

# Функция для получения владельцев из БД
def get_owners_from_db():
    try:
        settings = load_settings()
        return settings.get('allow', [])
    except:
        return []

# Функция для обновления владельцев в БД
def update_owners_in_db(new_owners):
    try:
        settings = load_settings()
        settings['allow'] = new_owners
        with open('settings/settings.json', 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Ошибка при обновлении владельцев в БД: {e}")
        return False

# Обновляем глобальную переменную allow из БД при загрузке
allow = get_owners_from_db()

@app.on_message(filters.command("ping", prefix) & owner_filter)
async def ping(client, message):
    starts_time = time.time()
    await message.edit("<emoji id=5445284980978621387>🚀</emoji>")
    ends_time = time.time()
    ping_time = (ends_time - starts_time) * 1000
    moscow_timezone = pytz.timezone('Europe/Moscow')
    current_time = datetime.now(moscow_timezone)
    formatted_time = current_time.strftime('%d.%m.%Y %H:%M:%S')
    end_time = time.time() - start_time
    hours, rem = divmod(end_time, 3600)
    minutes, seconds = divmod(rem, 60)
    args = message.text.split()
    force_premium = len(args) > 1 and args[1].lower() == 'prem'
    me = await client.get_me()
    has_premium = getattr(me, 'is_premium', False) or force_premium
    if has_premium:
        text = f"<b><emoji id=5920515922505765329>⚡️</emoji> PING: <code>{ping_time:.2f} ms</code>\n<emoji id=6037268453759389862>⏲️</emoji> Аптайм: <code>{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}</code></b>"
    else:
        text = f"<b>🚀 PING: <code>{ping_time:.2f} ms</code>\n└─  Аптайм: <code>{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}</code></b>"

    await message.edit(text)    

@app.on_message(filters.command('info', prefixes=prefix) & owner_filter)
async def info_command(client: Client, message: Message):
    await message.delete()

    try:
        # Проверяем есть ли параметр prem
        args = message.text.split()
        force_premium = len(args) > 1 and args[1].lower() == 'prem'
        
        current_version = await get_version()
        version_check = await check_version(client, prefix)
        
        moscow_timezone = pytz.timezone('Europe/Moscow')
        current_time = datetime.now(moscow_timezone)
        formatted_time = current_time.strftime('%d.%m.%Y %H:%M:%S')

        me = await client.get_me()
        owner_name = me.first_name
        if me.last_name:
            owner_name += " " + me.last_name

        has_premium = getattr(me, 'is_premium', False) or force_premium

        try:
            cpu_usage = f'{psutil.cpu_percent()}%'
            ram_usage = f'{psutil.virtual_memory().used / (1024 * 1024):.2f} MB'
        except:
            cpu_usage = ram_usage = 'Неизвестно'

        uptime = time.time() - start_time
        hours, rem = divmod(uptime, 3600)
        minutes, seconds = divmod(rem, 60)

        if system == "Windows":
            platform_info = "Windows"
            platform_info_premium = f"<emoji id=5469825590884310445>🚫</emoji> Windows {platform.release()} ({platform.version()})"
        elif system == "Linux":
            if "termux" in sys.argv[0]:
                platform_info = "Termux"
                platform_info_premium = f"<emoji id=5465488910865932234>🤖</emoji> Termux"
            elif "p3droid" in sys.argv[0]:
                platform_info = "Pydroid3"
                platform_info_premium = f"<emoji id=5465488910865932234>🤖</emoji> Pydroid3"
            else:
                platform_info = "Linux"
                platform_info_premium = f"<emoji id=5462990382360962124>🤓</emoji> Linux"
        else:
            platform_info = "Unknown"
            platform_info_premium = f"<emoji id=5873121512445187130>❓</emoji> Unknown"

        if has_premium:
            version_line = f"<emoji id=6030400221232501136>🤖</emoji> <b>Swift v.{current_version}</b>"
            
            if isinstance(version_check, str):
                update_notice = f"\n<blockquote><i>Доступно обновление: {current_version} → {version_check}</i></blockquote>"
            else:
                update_notice = ""

            info_text = f"""
{version_line}{update_notice}

<emoji id=6035084557378654059>👤</emoji> Владелец: <b>{owner_name}</b>
<emoji id=6039404727542747508>⌨️</emoji> Префикс: «{prefix}»
<emoji id=6037268453759389862>⏲️</emoji> Аптайм: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}

<emoji id=5920515922505765329>⚡️</emoji> CPU: <i>~{cpu_usage}</i>
<emoji id=5938492039971737551>💼</emoji> RAM: <i>~{ram_usage}</i>

<emoji id=5884330496619450755>☁️</emoji> Платформа: {platform_info_premium}
<emoji id=5983150113483134607>⏰️</emoji> Время: <b>{formatted_time}</b> MSK

<emoji id=6028338546736107668>⭐️</emoji> Команды: <code>{prefix}help</code>
            """
        else:
            version_line = f"» <b>Swift v.{current_version}</b>"
            
            if isinstance(version_check, str):
                update_notice = f"\n├ <i>Доступно обновение: {current_version} → {version_check}</i>"
            else:
                update_notice = ""

            info_text = f"""
{version_line}{update_notice}

• <b>Владелец:</b> {owner_name}
• <b>Префикс:</b> «{prefix}»
• <b>Аптайм:</b> {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}

• <b>CPU:</b> ~{cpu_usage}
• <b>RAM:</b> ~{ram_usage}

• <b>Платформа:</b> {platform_info}
• <b>Время:</b> {formatted_time} MSK

• <b>Команды:</b> <code>{prefix}help</code>"""

        photo_path = "settings/swift.jpg"
        if os.path.exists(photo_path):
            await client.send_photo(
                chat_id=message.chat.id,
                photo=photo_path,
                caption=info_text
            )
        else:
            await client.send_message(
                chat_id=message.chat.id,
                text=info_text
            )

    except Exception as e:
        error_msg = f"⚠️ Ошибка в команде info: {str(e)}"
        print(error_msg)
        await client.send_message(message.chat.id, error_msg)

@app.on_message(filters.command("help", prefix) & owner_filter)
async def modules_help_command(client: Client, message: Message):
    args = message.text.split()
    
    force_premium = len(args) > 1 and args[-1].lower() == 'prem'  # Проверяем последний аргумент
    
    me = await client.get_me()
    has_premium = getattr(me, 'is_premium', False) or force_premium
    
    # Если есть больше 1 аргумента и последний не 'prem', или есть только 'prem'
    if len(args) > 1 and not (len(args) == 2 and args[1].lower() == 'prem'):
        # Получаем имя модуля (исключаем 'prem' если он есть)
        module_query = args[1].strip().lower() if args[1].lower() != 'prem' else args[2].strip().lower() if len(args) > 2 else ""
        
        exact_match = None
        partial_matches = []
        
        for name in modules_info:
            if module_query == name.lower():
                exact_match = name
                break
            elif module_query in name.lower():
                partial_matches.append(name)
        
        if exact_match:
            module_info = modules_info[exact_match]
            commands = modules_help.get(exact_match, {})

            # Определяем формат названия модуля
            name_format = "<b>{}</b>" if module_info.get("name", "").lower() == "system" else "<code>{}</code>"
            formatted_name = name_format.format(exact_match)

            # Формируем ответ в зависимости от has_premium (учитывает force_premium!)
            if has_premium:
                response = (
                    f"<emoji id=6030848053177486888>❓</emoji> <b>Помощь по модулю {formatted_name}</b>\n\n"
                    f"<emoji id=6039630677182254664>📂</emoji> <b>Путь:</b> <code>./modules/{module_info['file_name']}</code>\n"
                    f"<emoji id=6035084557378654059>👤</emoji> <b>Автор:</b> {module_info['developer']}\n"
                    f"<emoji id=6039779802741739617>✏️</emoji> <b>Описание:</b> {module_info['description']}\n\n"
                    f"<emoji id=6034831751308644168>💬</emoji> <b>Команды:</b>\n"
                )
                for cmd, desc in commands.items():
                    response += f"   ▸ <code>{prefix}{cmd}</code> — {desc}\n"
            else:
                response = (
                    f"> <b>Помощь по модулю {formatted_name}</b>\n\n"
                    f"> <b>Путь:</b> <code>./modules/{module_info['file_name']}</code>\n"
                    f"> <b>Автор:</b> {module_info['developer']}\n"
                    f"> <b>Описание:</b> {module_info['description']}\n\n"
                    f"> <b>Команды:</b>\n"
                )
                for cmd, desc in commands.items():
                    response += f"  ▸ <code>{prefix}{cmd}</code> — {desc}\n"

            try:
                if module_info["img"]:
                    await message.delete()
                    await message.reply_photo(
                        module_info["img"],
                        caption=response
                    )
                else:
                    await message.edit_text(response)
            except Exception as e:
                print(f"Ошибка при отправке фото/сообщения: {e}")
                await message.edit_text(response)
                
        elif partial_matches:
            if has_premium:
                response = " <b><emoji id=6032850693348399258>🔎</emoji> Модуль не найден. Ближайшие совпадения:</b>\n\n"
                for match in partial_matches:
                    response += f"  ▸ <code>{prefix}help {match}</code>\n"
            else:
                response = "<b>> Модуль не найден. Ближайшие совпадения:</b>\n\n"
                for match in partial_matches:
                    response += f"  ▸ <code>{prefix}help {match}</code>\n"
            await message.edit_text(response, disable_web_page_preview=True)
            
        else:
            await message.edit_text("Модуль не найден.", disable_web_page_preview=True)
            
    else:
        total_modules = len(modules_info)
        hidden_modules = sum(1 for info in modules_info.values() if info["hidden"])
        
        system_module = None
        other_modules = []
        
        for module_name, info in modules_info.items():
            if info["hidden"]:
                continue
            if info.get("name", "").lower() == "system" and info["file_name"] == "1.py":
                system_module = (module_name, info)
            else:
                other_modules.append((module_name, info))
        
        if has_premium:
            response = f"<b><emoji id=6039630677182254664>📂</emoji> Загружено модулей:</b> {total_modules} (скрыто: {hidden_modules})\n\n"
        else:
            response = f"> <b>Загружено модулей:</b> {total_modules} (скрыто: {hidden_modules})\n\n"
        
        if system_module:
            module_name, info = system_module
            commands = modules_help.get(module_name, {})
            command_list = " | ".join(commands.keys()) if commands else "—"
            if has_premium:
                response += "<b><emoji id=5850309953293653168>⚙️</emoji> Системные модули:</b>\n"
                response += f"   <emoji id=5940433880585605708>🔨</emoji>  <i>{module_name}</i> — {command_list}\n\n"
            else:
                response += "<b>> Системные модули:</b>\n"
                response += f"  ▸ <i>{module_name}</i> — {command_list}\n\n"
        
        if other_modules:
            if has_premium:
                response += "<b><emoji id=5850309953293653168>⚙️</emoji> Модули:</b>\n"
            else:
                response += "<b>> Модули:</b>\n"

            for module_name, info in other_modules:
                commands = modules_help.get(module_name, {})
                command_list = " | ".join(commands.keys()) if commands else "—"
                if has_premium:
                    response += f"   <emoji id=5940433880585605708>🔨</emoji>  <code>{module_name}</code> — {command_list}\n"
                else:
                    response += f"  ▸ <code>{module_name}</code> — {command_list}\n"
        
        await message.edit_text(response, disable_web_page_preview=True)

@app.on_message(filters.command("lm", prefixes=prefix) & owner_filter)
async def load_module(client: Client, message: Message):
    args = message.text.split()
    force_premium = len(args) > 1 and args[-1].lower() == 'prem'
    me = await client.get_me()
    has_premium = getattr(me, 'is_premium', False) or force_premium

    if not message.reply_to_message or not message.reply_to_message.document:
        await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Ответьте на сообщение с файлом модуля (.py)")
        return

    document = message.reply_to_message.document
    if not document.file_name.endswith(".py"):
        await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Файл должен быть с расширением .py")
        return

    temp_path = await message.reply_to_message.download()

    meta_data = {
        "name": document.file_name[:-3],
        "developer": "Неизвестный разработчик",
        "description": "Нет описания",
        "img": None,
        "libs": None,
        "commands": {}
    }

    with open(temp_path, "r", encoding="utf-8") as f:
        content = f.read()
        for line in content.split('\n'):
            if line.startswith("#meta name:"):
                meta_data["name"] = line.split(":", 1)[1].strip()
            elif line.startswith("#meta developer:"):
                meta_data["developer"] = line.split(":", 1)[1].strip()
            elif line.startswith("#meta description:"):
                meta_data["description"] = line.split(":", 1)[1].strip()
            elif line.startswith("#meta img:"):
                meta_data["img"] = line.split(":", 1)[1].strip()
            elif line.startswith("#meta libs:"):
                meta_data["libs"] = line.split(":", 1)[1].strip()
            elif line.startswith("modules_help[") and "]" in line:
                try:
                    module_name = line.split("['")[1].split("']")[0]
                    if module_name == meta_data["name"]:
                        commands_section = content.split("modules_help[")[1].split("] = {")[1].split("}")[0]
                        for cmd_line in commands_section.split('\n'):
                            if '": ' in cmd_line:
                                cmd = cmd_line.split('"')[1]
                                desc = cmd_line.split('": "')[1].split('"')[0]
                                meta_data["commands"][cmd] = desc
                except Exception as e:
                    print(f"⚠️ Ошибка парсинга команд: {e}")
                    meta_data["commands"] = {}

    if meta_data["name"] in modules_info:
        os.remove(temp_path)
        await message.edit_text(f"<emoji id=5774077015388852135>❌</emoji> Модуль с названием <code>{meta_data['name']}</code> уже установлен!")
        return

    modules_dir = "modules"
    if not os.path.exists(modules_dir):
        os.makedirs(modules_dir)

    new_filename = document.file_name
    name_changed = False

    if os.path.exists(os.path.join(modules_dir, document.file_name)):
        name_changed = True
        file_ext = document.file_name.split(".")[-1]
        new_filename = f"{generate_random_name()}.{file_ext}"

    new_path = os.path.join(modules_dir, new_filename)
    os.rename(temp_path, new_path)

    load_modules()

    if has_premium:
        response = (
            f"<emoji id=5774022692642492953>✅</emoji> <b>Установлен модуль</b> <code>{meta_data['name']}</code>\n"
            f"<emoji id=6035084557378654059>👤</emoji> <b>Разработчик:</b> {meta_data['developer']}\n"
            f"<emoji id=6039779802741739617>✏️</emoji> <b>Описание:</b> {meta_data['description']}"
        )
    else:
        response = (
            f"> Установлен модуль <code>{meta_data['name']}</code>\n"
            f"> Разработчик: {meta_data['developer']}\n"
            f"> Описание: {meta_data['description']}"
        )

    if meta_data["commands"]:
        if has_premium:
            response += "\n\n<emoji id=6034831751308644168>💬</emoji> <b>Команды модуля:</b>\n"
            for cmd, desc in meta_data["commands"].items():
                response += f"   ▸ <code>{prefix}{cmd}</code> — {desc}\n"
        else:
            response += "\n\n> Команды модуля:\n"
            for cmd, desc in meta_data["commands"].items():
                response += f"   ▸ <code>{prefix}{cmd}</code> - {desc}\n"

    if name_changed:
        response += f"\n[⚠️] <i>Файл с названием <code>{document.file_name}</code> уже был, поэтому название файла было изменено на <code>{new_filename}</code></i>"

    try:
        if meta_data["img"]:
            await message.delete()
            msg = await message.reply_photo(meta_data["img"], caption=response)
        else:
            msg = await message.edit_text(response)
    except Exception as e:
        print(f"Ошибка при отправке фото: {e}")
        msg = await message.edit_text(response)

    if meta_data["libs"]:
        await install_libraries(msg, meta_data["name"], meta_data["libs"])

@app.on_message(filters.command("dlm", prefixes=prefix) & owner_filter)
async def download_load_module(client: Client, message: Message):
    args = message.text.split()
    force_premium = len(args) > 1 and args[-1].lower() == 'prem'
    me = await client.get_me()
    has_premium = getattr(me, 'is_premium', False) or force_premium

    if len(message.command) < 2:
        await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Укажите URL для скачивания модуля\nПример: <code>.dlm https://example.com/module.py</code>")   
        return

    url = message.command[1].strip()

    try:
        parsed_url = urlparse(url)
        file_name = os.path.basename(parsed_url.path)

        if not file_name.lower().endswith('.py'):
            await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Файл должен быть с расширением .py")
            return

        response = requests.get(url, stream=True)
        response.raise_for_status()

        temp_dir = "temp_downloads"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        temp_path = os.path.join(temp_dir, file_name)

        with open(temp_path, "wb") as f:
            for chunk in response.iter_content(1024):
                if chunk:
                    f.write(chunk)

        meta_data = {
            "name": file_name[:-3],
            "developer": "Неизвестный разработчик",
            "description": "Нет описания",
            "img": None,
            "libs": None,
            "commands": {}
        }

        with open(temp_path, "r", encoding="utf-8") as f:
            content = f.read()
            for line in content.split('\n'):
                if line.startswith("#meta name:"):
                    meta_data["name"] = line.split(":", 1)[1].strip()
                elif line.startswith("#meta developer:"):
                    meta_data["developer"] = line.split(":", 1)[1].strip()
                elif line.startswith("#meta description:"):
                    meta_data["description"] = line.split(":", 1)[1].strip()
                elif line.startswith("#meta img:"):
                    meta_data["img"] = line.split(":", 1)[1].strip()
                elif line.startswith("#meta libs:"):
                    meta_data["libs"] = line.split(":", 1)[1].strip()
                elif line.startswith("modules_help[") and "]" in line:
                    try:
                        module_name = line.split("['")[1].split("']")[0]
                        if module_name == meta_data["name"]:
                            commands_section = content.split("modules_help[")[1].split("] = {")[1].split("}")[0]
                            for cmd_line in commands_section.split('\n'):
                                if '": ' in cmd_line:
                                    cmd = cmd_line.split('"')[1]
                                    desc = cmd_line.split('": "')[1].split('"')[0]
                                    meta_data["commands"][cmd] = desc
                    except Exception as e:
                        print(f"⚠️ Ошибка парсинга команд: {e}")
                        meta_data["commands"] = {}

        if meta_data["name"] in modules_info:
            os.remove(temp_path)
            await message.edit_text(f"<emoji id=5774077015388852135>❌</emoji> Модуль с названием <code>{meta_data['name']}</code> уже установлен!")
            return

        modules_dir = "modules"
        if not os.path.exists(modules_dir):
            os.makedirs(modules_dir)

        new_filename = file_name
        name_changed = False

        if os.path.exists(os.path.join(modules_dir, file_name)):
            name_changed = True
            file_ext = file_name.split(".")[-1]
            new_filename = f"{generate_random_name()}.{file_ext}"

        new_path = os.path.join(modules_dir, new_filename)
        os.rename(temp_path, new_path)

        load_modules()

        if has_premium:
            response_text = (
                f"<emoji id=5774022692642492953>✅</emoji> <b>Установлен модуль</b> <code>{meta_data['name']}</code>\n"
                f"<emoji id=6035084557378654059>👤</emoji>  <b>Разработчик:</b> {meta_data['developer']}\n"
                f"<emoji id=6039779802741739617>✏️</emoji> <b>Описание:</b> {meta_data['description']}"
            )
        else:
            response_text = (
                f"> Установлен модуль <code>{meta_data['name']}</code>\n"
                f"> Разработчик: {meta_data['developer']}\n"
                f"> Описание: {meta_data['description']}"
            )

        if meta_data["commands"]:
            if has_premium:
                response_text += "\n\n<emoji id=6034831751308644168>💬</emoji> <b>Команды модуля:</b>\n"
                for cmd, desc in meta_data["commands"].items():
                    response_text += f"   ▸ <code>{prefix}{cmd}</code> — {desc}\n"
            else:
                response_text += "\n\n> Команды модуля:\n"
                for cmd, desc in meta_data["commands"].items():
                    response_text += f"   ▸ <code>{prefix}{cmd}</code> - {desc}\n"

        if name_changed:
            response_text += f"\n[⚠️] <i>Файл с названием <code>{file_name}</code> уже был, поэтому название файла было изменено на <code>{new_filename}</code></i>"

        try:
            if meta_data["img"]:
                await message.delete()
                msg = await message.reply_photo(meta_data["img"], caption=response_text)
            else:
                msg = await message.edit_text(response_text)
        except Exception as e:
            print(f"Ошибка при отправке фото: {e}")
            msg = await message.edit_text(response_text)

        if meta_data["libs"]:
            await install_libraries(msg, meta_data["name"], meta_data["libs"])

    except requests.exceptions.RequestException as e:
        await message.edit_text(f"<emoji id=5774077015388852135>❌</emoji> Ошибка при скачивании файла: {str(e)}")
    except Exception as e:
        await message.edit_text(f"<emoji id=5774077015388852135>❌</emoji> Произошла ошибка: {str(e)}")
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)

@app.on_message(filters.command("um", prefixes=prefix) & owner_filter)
async def download_module(client: Client, message: Message):
    args = message.text.split()
    force_premium = len(args) > 1 and args[-1].lower() == 'prem'
    me = await client.get_me()
    has_premium = getattr(me, 'is_premium', False) or force_premium

    if len(message.command) < 2:
        await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Укажите название модуля")
        return
    
    user_input = message.command[1].strip()
    modules_dir = "modules"
    
    filepath_by_filename = os.path.join(modules_dir, f"{user_input}.py")
    file_exists = os.path.exists(filepath_by_filename)
    
    matches = []
    for mod_name, info in modules_info.items():
        if user_input.lower() == mod_name.lower():
            matches = [(mod_name, info)]
            break
        elif user_input.lower() in mod_name.lower():
            matches.append((mod_name, info))
    
    if file_exists and not matches:
        await message.delete()
        if has_premium:
            await message.reply_document(
                filepath_by_filename,
                caption=f"<emoji id=5774022692642492953>✅</emoji> <b>Модуль</b> <code>{user_input}</code> <b>выгружен</b>"
            )
        else:
            await message.reply_document(
                filepath_by_filename,
                caption=f"[✅] Модуль <code>{user_input}</code> выгружен"
            )
    elif not file_exists and len(matches) == 1:
        mod_name, info = matches[0]
        await message.delete()
        if has_premium:
            await message.reply_document(
                info["path"],
                caption=f"<emoji id=5774022692642492953>✅</emoji> <b>Модуль</b> <code>{mod_name}</code> <b>выгружен</b>"
            )
        else:
            await message.reply_document(
                info["path"],
                caption=f"[✅] Модуль <code>{mod_name}</code> выгружен"
            )
    elif file_exists and len(matches) == 1:
        mod_name, info = matches[0]
        if os.path.normpath(info["path"]) == os.path.normpath(filepath_by_filename):
            await message.delete()
            if has_premium:
                await message.reply_document(
                    info["path"],
                    caption=f"<emoji id=5774022692642492953>✅</emoji> <b>Модуль</b> <code>{mod_name}</code> <b>выгружен</b>"
                )
            else:
                await message.reply_document(
                    info["path"],
                    caption=f"[✅] Модуль <code>{mod_name}</code> выгружен"
                )
        else:
            await message.edit_text(
                f"[⚠️] Найдено нечеткое совпадение: <code>{mod_name}</code>\n"
                f"Вы действительно хотите выгрузить этот модуль?\n\n"
                f"Да — <code>{prefix}um {mod_name}</code>"
            )
    elif len(matches) > 1:
        if has_premium:
            help_text = "<emoji id=6032850693348399258>🔎</emoji> <b>Точных совпадений не найдено! Выберите нужный вариант:</b>\n\n"
        else:
            help_text = "[🔎] Точных совпадений не найдено! Выберите нужный вариант:\n\n"
        help_text += "\n".join([
            f"▫️ <code>{mod_name}</code> (Имя файла: <code>{info['file_name']}</code>)" 
            for mod_name, info in matches
        ])
        await message.edit_text(help_text)
    else:
        await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Модуль не найден")

@app.on_message(filters.command("dm", prefixes=prefix) & owner_filter)
async def delete_module(client: Client, message: Message):
    args = message.text.split()
    force_premium = len(args) > 1 and args[-1].lower() == 'prem'
    me = await client.get_me()
    has_premium = getattr(me, 'is_premium', False) or force_premium

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.edit_text("[❗] Укажите имя модуля или файла.")
        return

    user_input = args[1].strip()

    for mod_name, info in modules_info.items():
        if (user_input.lower() == mod_name.lower() and 
            (info.get("name", "").lower() == "system" or info["file_name"] == "1.py")):
            await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Этот модуль нельзя выгрузить!")
            return
        if (f"{user_input}.py".lower() == info["file_name"].lower() and 
            (info.get("name", "").lower() == "system" or info["file_name"] == "1.py")):
            await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Этот модуль нельзя выгрузить!")
            return

    deleted = False
    deleted_name = None

    filepath_by_filename = os.path.join("modules", f"{user_input}.py")
    if os.path.exists(filepath_by_filename):
        with open(filepath_by_filename, "r", encoding="utf-8") as f:
            content = f.read()
            if "#meta name: System" in content or filepath_by_filename.endswith("1.py"):
                await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Этот модуль нельзя выгрузить!")
                return

        for mod_name, info in modules_info.items():
            if info["file_name"] == f"{user_input}.py":
                deleted_name = mod_name
                break
        
        if not deleted_name:
            deleted_name = user_input
        
        os.remove(filepath_by_filename)
        deleted = True

    if not deleted and user_input in modules_info:
        file_path = modules_info[user_input]["path"]
        if os.path.exists(file_path):
            os.remove(file_path)
            deleted_name = user_input
            deleted = True

    if not deleted:
        matches = []
        for mod_name in modules_info.keys():
            if user_input.lower() in mod_name.lower():
                matches.append(mod_name)

        if len(matches) == 0:
            await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Не найден ни модуль, ни файл с таким именем.")
            return
        elif len(matches) == 1:
            confirm_text = (
                f"[⚠️] Найдено нечеткое совпадение: {matches[0]}\n"
                f"Вы действительно хотите удалить этот модуль?\n\n"
                f"Да — {prefix}dm {matches[0]}"
            )
            await message.edit_text(confirm_text)
            return
        else:
            help_text = "<emoji id=6032850693348399258>🔎</emoji> Точных совпадений не найдено! Выберите нужный вариант:\n\n"
            help_text += "\n".join([f"▫️ <code>{mod}</code>" for mod in matches])
            await message.edit_text(help_text)
            return

    if deleted:
        if deleted_name in modules_info:
            del modules_info[deleted_name]
        
        load_modules()
        
        if has_premium:
            await message.edit_text(f"<emoji id=5774022692642492953>✅</emoji> <b>Модуль</b> <code>{deleted_name}</code> <b>успешно удалён</b>\n<blockquote><i>Начинаю перезагрузку...</blockquote></i>")
        else:
            await message.edit_text(f"[✅] Модуль <code>{deleted_name}</code> успешно удалён\n<blockquote><i>Начинаю перезагрузку...</blockquote></i>")
        os.execv(sys.executable, [sys.executable] + sys.argv)
    else:
        await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Не удалось удалить модуль")

@app.on_message(filters.command("restart", prefix) & owner_filter)
async def restart_bot(client: Client, message: Message):
    args = message.text.split()
    force_premium = len(args) > 1 and args[-1].lower() == 'prem'
    me = await client.get_me()
    has_premium = getattr(me, 'is_premium', False) or force_premium

    if has_premium:
        await message.edit_text("<emoji id=5778647930038653243>✨</emoji> <b>Полная перезагрузка бота...</b>")
    else:
        await message.edit_text("[🔄] Полная перезагрузка бота...")
    
    with open("settings/restart_info.txt", "w") as f:
        f.write(f"{message.chat.id}\n{message.id}\n{time.time()}")
    
    os.execv(sys.executable, [sys.executable] + sys.argv)

@app.on_message(filters.command("setprefix", prefix) & owner_filter)
async def set_prefix(client: Client, message: Message):
    args = message.text.split()
    force_premium = len(args) > 1 and args[-1].lower() == 'prem'
    me = await client.get_me()
    has_premium = getattr(me, 'is_premium', False) or force_premium

    if len(message.command) < 2:
        await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Укажите новый префикс")
        return
    
    new_prefix = message.command[1]
    if len(new_prefix) < 1 or len(new_prefix) > 3:
        await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Префикс должен быть от 1 до 3 символов")
        return
    
    update_settings(prefix=new_prefix)
    globals()['prefix'] = new_prefix
    
    if has_premium:
        await message.edit_text(f"<emoji id=5774022692642492953>✅</emoji> <b>Префикс изменен на</b> <code>{new_prefix}</code>\n<blockquote><i>Начинаю перезагрузку...</blockquote></i>")
    else:
        await message.edit_text(f"[✅] Префикс изменен на <code>{new_prefix}</code>\n<blockquote><i>Начинаю перезагрузку...</blockquote></i>")
    os.execv(sys.executable, [sys.executable] + sys.argv)

@app.on_message(filters.command("owners", prefix) & owner_filter)
async def manage_owners(client: Client, message: Message):
    args = message.text.split()
    force_premium = len(args) > 1 and args[-1].lower() == 'prem'
    me = await client.get_me()
    has_premium = getattr(me, 'is_premium', False) or force_premium

    if len(args) == 1:
        # Показать текущих владельцев
        owners = get_owners_from_db()
        if not owners:
            await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Нет владельцев в базе данных")
            return
        
        owners_info = []
        for owner_id in owners:
            try:
                user = await client.get_users(owner_id)
                name = user.first_name
                if user.last_name:
                    name += f" {user.last_name}"
                owners_info.append(f"{name} (@{user.username}) [{user.id}]" if user.username else f"{name} [{user.id}]")
            except:
                owners_info.append(f"Неизвестный пользователь [{owner_id}]")
        
        if has_premium:
            response = "<emoji id=6035084557378654059>👤</emoji> <b>Текущие владельцы:</b>\n\n"
            for info in owners_info:
                response += f"   ▸ {info}\n"
        else:
            response = "> Текущие владельцы:\n\n"
            for info in owners_info:
                response += f"  ▸ {info}\n"
        
        await message.edit_text(response)
        return

    subcommand = args[1].lower()
    
    if subcommand == "reload":
        # Перезагрузить владельцев из БД
        global allow
        allow = get_owners_from_db()
        if has_premium:
            await message.edit_text("<emoji id=5774022692642492953>✅</emoji> <b>Список владельцев перезагружен из базы данных</b>")
        else:
            await message.edit_text("[✅] Список владельцев перезагружен из базы данных")
        return
    
    elif subcommand == "add" and len(args) >= 3:
        # Добавить владельца
        try:
            if message.reply_to_message:
                user = message.reply_to_message.from_user
                user_id = user.id
            else:
                user_input = args[2]
                if user_input.startswith("@"):
                    user = await client.get_users(user_input)
                else:
                    user = await client.get_users(int(user_input))
                user_id = user.id
            
            current_owners = get_owners_from_db()
            if user_id in current_owners:
                await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Этот пользователь уже является владельцем")
                return
            
            current_owners.append(user_id)
            if update_owners_in_db(current_owners):
                global allow
                allow = current_owners
                if has_premium:
                    await message.edit_text(f"<emoji id=5774022692642492953>✅</emoji> <b>Пользователь добавлен в владельцы</b>")
                else:
                    await message.edit_text(f"[✅] Пользователь добавлен в владельцы")
            else:
                await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Ошибка при обновлении базы данных")
        
        except Exception as e:
            await message.edit_text(f"<emoji id=5774077015388852135>❌</emoji> Ошибка: {e}")
    
    elif subcommand == "remove" and len(args) >= 3:
        # Удалить владельца
        try:
            if message.reply_to_message:
                user_id = message.reply_to_message.from_user.id
            else:
                user_input = args[2]
                if user_input.startswith("@"):
                    user = await client.get_users(user_input)
                    user_id = user.id
                else:
                    user_id = int(user_input)
            
            current_owners = get_owners_from_db()
            if user_id not in current_owners:
                await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Этот пользователь не является владельцем")
                return
            
            current_owners = [uid for uid in current_owners if uid != user_id]
            if update_owners_in_db(current_owners):
                global allow
                allow = current_owners
                if has_premium:
                    await message.edit_text(f"<emoji id=5774022692642492953>✅</emoji> <b>Пользователь удален из владельцев</b>")
                else:
                    await message.edit_text(f"[✅] Пользователь удален из владельцев")
            else:
                await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Ошибка при обновлении базы данных")
        
        except Exception as e:
            await message.edit_text(f"<emoji id=5774077015388852135>❌</emoji> Ошибка: {e}")
    
    else:
        await message.edit_text(
            "<emoji id=5774077015388852135>❌</emoji> Неправильный формат команды\n\n"
            f"<code>{prefix}owners</code> - показать владельцев\n"
            f"<code>{prefix}owners reload</code> - перезагрузить из БД\n"
            f"<code>{prefix}owners add [user]</code> - добавить владельца\n"
            f"<code>{prefix}owners remove [user]</code> - удалить владельца"
        )

# Обновляем команды addowner и delowner для работы с БД
@app.on_message(filters.command("addowner", prefix) & owner_filter)
async def add_owner(client: Client, message: Message):
    args = message.text.split()
    force_premium = len(args) > 1 and args[-1].lower() == 'prem'
    me = await client.get_me()
    has_premium = getattr(me, 'is_premium', False) or force_premium

    if not message.reply_to_message and len(message.command) < 2:
        await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Укажите пользователя (ответом, ID или @username)")
        return
    
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user
            user_id = user.id
            user_name = user.first_name or user.username or str(user.id)
        else:
            user_input = message.command[1]
            if user_input.startswith("@"):
                user = await client.get_users(user_input)
                user_name = user.first_name or user.username
            else:
                user = await client.get_users(int(user_input))
                user_name = user.first_name or str(user.id)
            user_id = user.id

        current_owners = get_owners_from_db()
        if user_id in current_owners:
            await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Этот пользователь уже является владельцем")
            return

        current_owners.append(user_id)
        if update_owners_in_db(current_owners):
            global allow
            allow = current_owners
            
            if has_premium:
                await message.edit_text(f"<emoji id=5774022692642492953>✅</emoji> <b>Пользователь</b> {user_name}[{user_id}] <b>добавлен в владельцы</b>")
            else:
                await message.edit_text(f"[✅] Пользователь {user_name}[{user_id}] добавлен в владельцы")
        else:
            await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Ошибка при обновлении базы данных")
            
    except Exception as e:
        await message.edit_text(f"<emoji id=5774077015388852135>❌</emoji> Ошибка: {e}")

@app.on_message(filters.command("delowner", prefix) & owner_filter)
async def del_owner(client: Client, message: Message):
    args = message.text.split()
    force_premium = len(args) > 1 and args[-1].lower() == 'prem'
    me = await client.get_me()
    has_premium = getattr(me, 'is_premium', False) or force_premium

    if not message.reply_to_message and len(message.command) < 2:
        await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Укажите пользователя (ответом или ID)")
        return

    try:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            user_input = message.command[1]
            if user_input.startswith("@"):
                user = await client.get_users(user_input)
                user_id = user.id
            else:
                user_id = int(user_input)

        current_owners = get_owners_from_db()
        if user_id not in current_owners:
            await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Этот пользователь не является владельцем")
            return

        current_owners = [uid for uid in current_owners if uid != user_id]
        if update_owners_in_db(current_owners):
            global allow
            allow = current_owners
            
            if has_premium:
                await message.edit_text(f"<emoji id=5774022692642492953>✅</emoji> <b>Пользователь</b> [{user_id}] <b>удален из владельцев</b>")
            else:
                await message.edit_text(f"[✅] Пользователь [{user_id}] удален из владельцев")
        else:
            await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Ошибка при обновлении базы данных")

    except Exception as e:
        await message.edit_text(f"<emoji id=5774077015388852135>❌</emoji> Ошибка: {e}")

@app.on_message(filters.command("update", prefix) & owner_filter)
async def update_bot(client: Client, message: Message):
    args = message.text.split()
    force_premium = len(args) > 1 and args[-1].lower() == 'prem'
    me = await client.get_me()
    has_premium = getattr(me, 'is_premium', False) or force_premium

    if not os.path.exists("utils/updater.py"):
        await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Файл обновления не найден!")
        return

    if has_premium:
        await message.edit_text("<emoji id=5778647930038653243>✨</emoji> <b>Подготовка к обновлению...</b>")
    else:
        await message.edit_text("[🔄] Подготовка к обновлению...")

    old_version = await get_version()
    with open("settings/update_info.txt", "w") as f:
        f.write(f"{message.chat.id}\n{message.id}\n{old_version}")

    try:
        python_exec = sys.executable
        if os.name == 'nt':
            subprocess.Popen(
                [python_exec, "utils/updater.py"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            subprocess.Popen(
                [python_exec, "utils/updater.py"],
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        print("💤 Ждём перед выходом...")
        await asyncio.sleep(2)
        os._exit(0)

    except Exception as e:
        await message.edit_text(f"<emoji id=5774077015388852135>❌</emoji> Ошибка запуска обновления: {e}")
        if os.path.exists("settings/update_info.txt"):
            os.remove("settings/update_info.txt")

@app.on_message(filters.command("im", prefixes=prefix) & filters.user(allow) & filters.reply)
async def info_module(client: Client, message: Message):
    args = message.text.split()
    force_premium = len(args) > 1 and args[-1].lower() == 'prem'
    me = await client.get_me()
    has_premium = getattr(me, 'is_premium', False) or force_premium

    reply = message.reply_to_message
    if not reply.document or not reply.document.file_name.endswith(".py"):
        await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Ответьте на файл модуля с расширением .py")
        return
    
    temp_path = await reply.download()
    
    meta_data = {
        "name": reply.document.file_name[:-3],
        "developer": "Неизвестный разработчик",
        "description": "Нет описания",
        "img": None,
        "libs": None,
        "commands": {}
    }
    
    with open(temp_path, "r", encoding="utf-8") as f:
        content = f.read()
        for line in content.split('\n'):
            if line.startswith("#meta name:"):
                meta_data["name"] = line.split(":", 1)[1].strip()
            elif line.startswith("#meta developer:"):
                meta_data["developer"] = line.split(":", 1)[1].strip()
            elif line.startswith("#meta description:"):
                meta_data["description"] = line.split(":", 1)[1].strip()
            elif line.startswith("#meta img:"):
                meta_data["img"] = line.split(":", 1)[1].strip()
            elif line.startswith("#meta libs:"):
                meta_data["libs"] = line.split(":", 1)[1].strip()
            elif line.startswith("modules_help[") and "]" in line:
                try:
                    module_name = line.split("['")[1].split("']")[0]
                    if module_name == meta_data["name"]:
                        commands_section = content.split("modules_help[")[1].split("] = {")[1].split("}")[0]
                        for cmd_line in commands_section.split('\n'):
                            if '": ' in cmd_line:
                                cmd = cmd_line.split('"')[1]
                                desc = cmd_line.split('": "')[1].split('"')[0]
                                meta_data["commands"][cmd] = desc
                except:
                    pass
    
    os.remove(temp_path)
    
    if has_premium:
        response = f"<emoji id=6028435952299413210>ℹ</emoji> <b>Информация о модуле</b> <code>{meta_data['name']}</code>\n\n"
    else:
        response = f"> Информация о модуле <code>{meta_data['name']}</code>:\n\n"
    
    if meta_data["libs"]:
        if has_premium:
            response += f"<emoji id=6039802767931871481>⬇️</emoji> <b>Необходимы библиотеки:</b> <code>{meta_data['libs']}</code>\n"
        else:
            response += f"> Необходимы библиотеки: <code>{meta_data['libs']}</code>\n"
    
    if has_premium:
        response += (
            f"<emoji id=6035084557378654059>👤</emoji> <b>Автор модуля:</b> {meta_data['developer']}\n"
            f"<emoji id=6039779802741739617>✏️</emoji> <b>Описание модуля:</b> {meta_data['description']}\n\n"
        )
    else:
        response += (
            f"> Автор модуля: {meta_data['developer']}\n"
            f"> Описание модуля: {meta_data['description']}\n\n"
        )
    
    if meta_data["commands"]:
        if has_premium:
            response += "<emoji id=6034831751308644168>💬</emoji> <b>Команды модуля:</b>\n"
            for cmd, desc in meta_data["commands"].items():
                response += f"   ▸ <code>{prefix}{cmd}</code> — {desc}\n"
        else:
            response += "> Команды модуля:\n"
            for cmd, desc in meta_data["commands"].items():
                response += f"   ▸ <code>{prefix}{cmd}</code> - {desc}\n"
    
    try:
        if meta_data["img"]:
            await message.delete()
            await message.reply_photo(meta_data["img"], caption=response)
        else:
            await message.edit_text(response)
    except Exception as e:
        print(f"Ошибка при отправке фото: {e}")
        await message.edit_text(response)

@app.on_message(filters.command("hidden", prefix) & owner_filter)
async def hidden_module(client: Client, message: Message):
    args = message.text.split()
    force_premium = len(args) > 1 and args[-1].lower() == 'prem'
    me = await client.get_me()
    has_premium = getattr(me, 'is_premium', False) or force_premium

    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.edit_text(
            "<emoji id=5774077015388852135>❌</emoji> Неправильный формат команды\n"
            f"Используйте: <code>{prefix}hidden on/off название_модуля</code>"
        )
        return
    
    action = args[1].lower()
    module_query = args[2].strip()
    
    if action not in ["on", "off"]:
        await message.edit_text(
            "<emoji id=5774077015388852135>❌</emoji> Неправильное действие\n"
            f"Используйте: <code>{prefix}hidden on/off название_модуля</code>"
        )
        return
    
    exact_match = None
    partial_matches = []
    
    for name in modules_info:
        if module_query.lower() == name.lower():
            exact_match = name
            break
        elif module_query.lower() in name.lower():
            partial_matches.append(name)
    
    if not exact_match and not partial_matches:
        await message.edit_text("<emoji id=5774077015388852135>❌</emoji> Модуль не найден")
        return
    
    if not exact_match and len(partial_matches) > 1:
        if has_premium:
            response = "<emoji id=6032850693348399258>🔎</emoji> <b>Найдено несколько совпадений:</b>\n\n"
        else:
            response = "[🔎] Найдено несколько совпадений:\n\n"
        response += "\n".join([f"» <code>{match}</code>" for match in partial_matches])
        await message.edit_text(response)
        return
    
    module_name = exact_match if exact_match else partial_matches[0]
    module_info = modules_info[module_name]
    file_path = module_info["path"]

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        new_lines = []
        hidden_found = False
        
        for line in lines:
            if line.startswith("#meta hidden:"):
                new_lines.append(f"#meta hidden: {action == 'on'}\n")
                hidden_found = True
            else:
                new_lines.append(line)
        
        if not hidden_found:
            for i, line in enumerate(new_lines):
                if line.startswith("#meta "):
                    new_lines.insert(i+1, f"#meta hidden: {action == 'on'}\n")
                    break
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        
        load_modules()
        
        status = "скрыт" if action == "on" else "показан"
        if has_premium:
            await message.edit_text(f"<emoji id=5774022692642492953>✅</emoji> <b>Модуль</b> <code>{module_name}</code> <b>теперь {status} в списке помощи</b>")
        else:
            await message.edit_text(f"[✅] Модуль <code>{module_name}</code> теперь {status} в списке помощи")
    except Exception as e:
        await message.edit_text(f"<emoji id=5774077015388852135>❌</emoji> Ошибка при изменении модуля: {e}")


modules_help['System'] = {
    "ping": "Узнать пинг",
    "info": "Информация о боте",
    "lm": "Установить модуль",
    "dlm": "Установить модуль по ссылке",
    "dm": "Удалить модуль",
    "um": "Выгрузить модуль файлом",
    "im": "Информация о модуле по файлу",
    "help": "Помощь по модулям",
    "hidden": "Скрытие модуля из листа помощи",
    "setprefix": "сменить префикс",
    "addowner": "Добавить пользователя в управление ботом",
    "delowner": "Исключить пользователя в управление ботом",
    "owners": "Управление владельцами через БД",
    "update": "Обновить бота",
    "restart": "Перезапустить бота",
}

