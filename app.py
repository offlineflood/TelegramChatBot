# -*- coding: utf-8 -*-
from pyrogram.errors import FloodWait, RPCError
from pyrogram.enums import ChatAction
from pyrogram import Client, filters
from pyrogram.types import Message
from config import config
import asyncio
import random
import time
import os


# Telegram API credentials
OWNER_ID = config["OWNER_ID"]

# Botların konfiqurasiyası
RANDOM_MESSAGES = [
    "Əla dedin! 👏",
    "Bunu gözləmirdim 😲",
    "Razıyam səninlə 👍",
    "Görəsən necə olacaq? 🤔",
    "Bu, məni güldürdü 😂",
    "Çox maraqlı fikirdir 🧐",
    "Bir az daha izah edə bilərsən? 🤓",
    "Səninlə tam razıyam! ✅",
    "Nə gözəl fikirdir! 🌟",
    "Ohaaa 😮",
    "Bunu paylaşmaq lazımdır 📣",
    "Yaxşı zarafat idi 😄",
    "Bir az düşündürücü oldu 🤯",
    "Superrr! 🔥",
    "Niyə belə düşünürsən? 🤨",
    "Səni başa düşürəm 😊",
    "Bir daha deyə bilərsən? 🙃",
    "Aynen öyle! 😎",
    "Bu fikri çox bəyəndim ❤️",
    "İnanılmaz səslənir 😍",
    "Ooo, maraqlı yanaşmadır! 😯",
    "Bu barədə heç fikirləşməmişdim 🤷‍♂️",
    "Davam elə! 💪",
    "Çox güldüm buna 🤣",
    "Açıq danış, utanma 😅",
    "Bəlkə başqa cür baxaq? 🔄",
    "Nə qədər maraqlı mövzudur! 🧠",
    "Ətraflı danışsan yaxşı olar 📚",
    "Sənin fikrini maraqla dinləyirəm 👂",
    "Bu lap film kimidir 🎬",
    "Tam sənlik mövzudur 😏",
    "Xatırlat da sonra 📝",
    "Həqiqətən də təsiredici idi 👌",
    "Bir az qarışıq oldu 😕",
    "Bunu mütləq qeyd etməliyik! 📌",
    "Məncə də belədir! 💯",
    "Xeyli maraq oyatdı məndə 😃",
    "Yenə danış, maraqlıdır 🗣️",
    "Səncə doğrudurmu? 🤷",
    "Növbəti dəfə daha çox danışaq 🕒",
    "Gözlənilməz idi bu 😁",
    "Hə, bu yaxşıdır 😌",
    "Olar, niyə də yox? 🙌",
    "Çox yerində fikir idi 🔍",
    "Bunu dostlara da deyəcəyəm 👫",
    "Əla məqam idi! 🎯",
    "Bunu yazacam yadımda qalsın ✍️",
    "Gözümün qabağında canlandı bu 😅",
    "Ətraflı danışsaq daha yaxşı olar 📖",
    "Çox düşündüm bu barədə 💭"
]

# Botların göndərəcəyi təsadüfi sticker URL-ləri
# (Telegram sticker URL-ləri)
RANDOM_STICKERS = [ 
    "CAACAgIAAxkBAAEGJHxl73HSFZrdnP89gMR6JYRv0ZXXQwACC00AAgaisEpbE2TLAAFmBMseBA",
    "CAACAgIAAxkBAAEGJH1l73HUYtxcQ6KtCEyE3rAKCBY7BwACAjwAAvuCuEqFFE9nScHuAR4E",
    "CAACAgIAAxkBAAEGJH5l73HU63mF79fFsjKGojCV_UH12wAC0T0AAumHuEpwV6TRKtlg4x4E"
]

# Botların göndərəcəyi təsadüfi şəkil və video URL-ləri
# (Telegram şəkil/video URL-ləri)
RANDOM_PHOTOS = [
    "https://te.legra.ph/file/758a5cf4598f061f25963.jpg",
    "https://telegra.ph//file/6f7d35131f69951c74ee5.jpg",
    "https://telegra.ph/file/75277ce3aa4a5401143b7.jpg"
]

# Botların göndərəcəyi təsadüfi video URL-ləri
# (Telegram video URL-ləri)
RANDOM_VIDEOS = [
    "https://graph.org/file/e999c40cb700e7c684b75.mp4",
    "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"
]

# Botların yaradılması
# Botların konfiqurasiyası
bots = []
target_group_id = None
last_message = None
chat_running = False

# Botların yaradılması və konfiqurasiyası
# (Telegram API ID, API Hash, Bot Token)
# Botların yaradılması və konfiqurasiyası      
    log_dir = "log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    for cfg in config["BOTS"]:
        session_path = os.path.join(log_dir, cfg["SESSION_NAME"])
        bot = Client(
            session_path,
            api_id=cfg["API_ID"],
            api_hash=cfg["API_HASH"],
            bot_token=cfg["BOT_TOKEN"]
        )
        try:
            await bot.start()  # Try to start the bot
            bots.append(bot)
            print(f"✅ Bot başladı: {cfg['SESSION_NAME']}")
        except FloodWait as e:
            wait_time = e.value
            print(f"❌ FloodWait ({wait_time} saniyə) - {cfg['SESSION_NAME']}")
            time.sleep(wait_time)  # Wait for the specified time
            await bot.start()  # Retry after the wait time
            bots.append(bot)
            print(f"✅ Bot başladı after FloodWait: {cfg['SESSION_NAME']}")
        except RPCError as e:
            print(f"❌ Pyrogram xəta: {e} - {cfg['SESSION_NAME']}")
        except Exception as e:
            print(f"❌ Digər xəta: {e} - {cfg['SESSION_NAME']}")

        # Add a small delay between each bot to prevent rate limiting
        await asyncio.sleep(2)  # Add delay between bot starts

# Botların yaradılması tamamlandıqdan sonra botların işə düşməsi üçün lazım olan konfiqurasiyaları qeyd edin
# (Telegram API ID, API Hash, Bot Token)        
def register_handlers():
    @bots[0].on_message(filters.command("start") & filters.group)
    async def start_command(client: Client, message: Message):
        global target_group_id, chat_running

        if message.from_user.id != OWNER_ID:
            await message.delete()
            await client.send_message(message.chat.id, "❌ Bu əmri yalnız bot sahibi istifadə edə bilər!")
            return

        if chat_running:
            await message.reply("✅ Botlar artıq işə düşüb.")
            return

        target_group_id = message.chat.id
        chat_running = True
        await message.reply("✅ Botlar işə düşdü.")

    @bots[0].on_message(filters.command("stop") & filters.group)
    async def stop_command(client: Client, message: Message):
        global chat_running

        if message.from_user.id != OWNER_ID:
            await message.delete()
            await client.send_message(message.chat.id, "❌ Bu əmri yalnız bot sahibi istifadə edə bilər!")
            return

        chat_running = False
        await message.reply("✅ Botlar dayanır.")

# Botların işə düşməsi üçün lazım olan konfiqurasiyaları qeyd edin
# (Telegram API ID, API Hash, Bot Token)
async def conversation_loop():
    global last_message, target_group_id, chat_running

    while True:
        if not chat_running or target_group_id is None:
            await asyncio.sleep(1)
            continue

        sender = random.choice(bots)
        reply_to_msg_id = last_message.id if last_message else None
        text = random.choice(RANDOM_MESSAGES)

        try:
            await sender.send_chat_action(target_group_id, ChatAction.TYPING)
            await asyncio.sleep(1)
            msg = await sender.send_message(
                chat_id=target_group_id,
                text=text,
                reply_to_message_id=reply_to_msg_id
            )
            print(f"[{sender.name}] replied with text: {text}")
            last_message = msg
        except Exception as e:
            print(f"Xəta baş verdi: {e}")

        await asyncio.sleep(3)

# Botların göndərəcəyi təsadüfi şəkil URL-ləri
# (Telegram şəkil/video URL-ləri)
async def media_loop():
    global last_message, target_group_id, chat_running

    while True:
        if not chat_running or target_group_id is None:
            await asyncio.sleep(1)
            continue

        sender = random.choice(bots)
        reply_to_msg_id = last_message.id if last_message else None
        media_type = random.choice(["sticker", "photo", "video"])

        try:
            if media_type == "sticker":
                await sender.send_chat_action(target_group_id, ChatAction.CHOOSE_STICKER)
                await asyncio.sleep(1)
                msg = await sender.send_sticker(
                    chat_id=target_group_id,
                    sticker=random.choice(RANDOM_STICKERS),
                    reply_to_message_id=reply_to_msg_id
                )
            elif media_type == "photo":
                await sender.send_chat_action(target_group_id, ChatAction.UPLOAD_PHOTO)
                await asyncio.sleep(2)
                msg = await sender.send_photo(
                    chat_id=target_group_id,
                    photo=random.choice(RANDOM_PHOTOS),
                    reply_to_message_id=reply_to_msg_id
                )
            elif media_type == "video":
                await sender.send_chat_action(target_group_id, ChatAction.UPLOAD_VIDEO)
                await asyncio.sleep(3)
                msg = await sender.send_video(
                    chat_id=target_group_id,
                    video=random.choice(RANDOM_VIDEOS),
                    reply_to_message_id=reply_to_msg_id
                )

            print(f"[{sender.name}] replied with {media_type}: {msg.media}") 
            last_message = msg

        except Exception as e:
            print(f"Xəta baş verdi: {e}")

        await asyncio.sleep(10)

# Botların işə düşməsi üçün lazım olan konfiqurasiyaları qeyd edin
# (Telegram API ID, API Hash, Bot Token)
async def main():
    await create_bots() # 🔧 async function-u await ilə çağır
    
    if not bots:
        print("❌ Heç bir bot işə başlamadı. Çıxılır.")
        return  # Don't crash, just exit
        
    register_handlers()

    # await asyncio.gather(*(bot.start() for bot in bots))
    print("Botlar işə düşdü!")
    await asyncio.sleep(5)

    await asyncio.gather(
        conversation_loop(),
        media_loop()
    )

if __name__ == "__main__":
    asyncio.run(main())
