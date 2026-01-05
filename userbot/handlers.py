import asyncio
import time
import json
import os
import sys
import random
from pyrogram import filters
from pyrogram.enums import ChatAction, ChatType
from pyrogram.handlers import MessageHandler
from pyrogram.errors import FloodWait, RPCError, SlowmodeWait
from datetime import datetime
from userbot.database_logger import LogDatabase
from userbot.inline_interface import alive_inline_handler, help_inline_handler
from userbot.islamic import (
    adzan_handler, quran_handler, jadwal_sholat_handler, 
    doa_handler, hadits_handler, asmaul_husna_handler,
    quotes_islami_handler, kisah_nabi_handler, 
    rukun_islam_handler, rukun_iman_handler
)
from userbot.ai import gemini_handler, gpt_handler, claude_handler, perplexity_handler
from userbot.christian import alkitab_handler, renungan_handler, quotes_kristen_handler, kidung_handler, kisah_rasul_handler
from userbot.admin import kick_handler, ban_handler, mute_handler, unmute_handler, zombie_handler, tagall_handler
from userbot.fun import toxic_handler, pantun_handler, quotes_handler, percentage_handler, siapa_handler
from userbot.creating import dl_handler, kang_handler, toimg_handler
from userbot.animations import (
    stop_anim_tasks, superdino_anim, lucu_anim, keren_anim, marah_anim, sedih_anim, ketawa_anim, heart_anim, 
    load_anim, moon_anim, clock_anim, bomb_anim, rocket_anim, police_anim, airplane_anim, car_anim, 
    bike_anim, ufo_anim, ghost_anim, cat_anim, dog_anim, monkey_anim, dragon_anim, rain_anim, 
    snow_anim, thunder_anim, earth_anim, star_anim, fire_anim, money_anim, beer_anim, food_anim, 
    boxing_anim, ball_anim, music_anim, dance_anim, robot_anim, phone_anim, letter_anim, key_anim, 
    firework_anim, bday_anim, sleep_anim, ninja_anim, uub_anim, wave_anim, tree_anim, sun_anim, 
    ocean_anim, game_anim, tv_anim, tools_anim, microscope_anim, space_anim, medical_anim, 
    workout_anim, travel_anim, magic_anim, weather_anim, flags_anim, colors_anim
)

FLOOD_WAIT_THRESHOLD = 30
FLOOD_WAIT_SLEEP = 3600
MONITOR_CHECK_INTERVAL = 300
INITIAL_MONITOR_DELAY = 60
BROADCAST_DELAY_MIN = 2.0
BROADCAST_DELAY_MAX = 4.0
TYPING_DELAY_MIN = 0.5
TYPING_DELAY_MAX = 1.5
AUTOREPLY_MAX_COUNT = 3
GROUP_LIST_CHUNK_SIZE = 15
BROADCAST_TEST_LIMIT = 3
LOG_LIMIT_DEFAULT = 10
MESSAGE_DELETE_DELAY = 3  
QUICK_DELETE_DELAY = 1    

DEFAULT_AUTOREPLY_MSG = "Halo! Saya sedang sibuk."
DEFAULT_SETPAY_MSG = "Belum diatur. Gunakan .setpay [teks] + foto/file"


reply_counts = {}
stopped_users = {}
spam_active = {}

log_db = LogDatabase()

def load_settings():
    path = "database/config.json"
    if not os.path.exists(path):
        os.makedirs("database", exist_ok=True)
        default_config = {
            "pesan": DEFAULT_AUTOREPLY_MSG,
            "aktif": True,
            "pay_text": DEFAULT_SETPAY_MSG,
            "qris_file_id": None,
            "monitor_active": False,
            "blacklist_groups": []
        }
        with open(path, "w") as f:
            json.dump(default_config, f)

    try:
        with open(path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"[ERROR] Failed to load settings: {e}")
        return {
            "pesan": DEFAULT_AUTOREPLY_MSG,
            "aktif": True,
            "pay_text": DEFAULT_SETPAY_MSG,
            "qris_file_id": None,
            "monitor_active": False,
            "blacklist_groups": []
        }

def save_settings(data):
    try:
        with open("database/config.json", "w") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"[ERROR] Failed to save settings: {e}")

async def send_log(client, text):
    try:
        target = "me"
        if hasattr(client, 'inline_manager'):
            target = client.inline_manager.bot_username
            
        await client.send_message(target, f"📝 **UBOT LOG**\n━━━━━━━━━━━━━━━━━━\n{text}")
    except Exception as e:
        print(f"[ERROR] Error sending log: {e}")

async def worker_spam(client, chat_id, text):
    try:
        await client.send_chat_action(chat_id, ChatAction.TYPING)
        await asyncio.sleep(random.uniform(TYPING_DELAY_MIN, TYPING_DELAY_MAX))
        await client.send_message(chat_id, text)
        return True
    except FloodWait as e:
        if e.value > FLOOD_WAIT_THRESHOLD:
            await send_log(client, "⚠️ **LIMIT BESAR TERDETEKSI!**\nBot akan tidur selama 1 jam.")
            await asyncio.sleep(FLOOD_WAIT_SLEEP)
            await client.send_message(chat_id, text)
            return True
        await asyncio.sleep(e.value + 1)
        await client.send_message(chat_id, text)
        return True
    except (SlowmodeWait, RPCError) as e:
        await asyncio.sleep(getattr(e, "value", 2) + 0.5)
        return False
    except Exception as e:
        print(f"[ERROR] Worker spam error: {e}")
        return False

async def ping_ubot(client, message):
    start = time.time()
    await message.edit("Pinging...")
    ms = round((time.time() - start) * 1000, 2)
    await message.edit(f"🚀 **Pong!**\n📶 `{ms}ms` | **Ultimate**")

async def status_ubot(client, message):
    settings = load_settings()
    me = await client.get_me()
    status_ar = "✅ Aktif" if client.is_connected else "❌ Nonaktif"
    caption = (
        "👤 **PROFIL PENGGUNA**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"📝 **Nama:** {me.first_name} {me.last_name or ''}\n"
        f"🆔 **ID:** `{me.id}`\n"
        f"👤 **Username:** @{me.username or '-'}\n"
        f"🤖 **Status Ubot:** {status_ar}\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "👑 **Bot by @MAU_BOBO**"
    )

    try:
        photos = [p async for p in client.get_chat_photos("me", limit=1)]
        if photos:
            await message.delete()
            await client.send_photo(message.chat.id, photos[0].file_id, caption=caption)
        else:
            await message.edit(caption)
    except Exception as e:
        print(f"[ERROR] Status error: {e}")
        await message.edit(caption)

async def cek_id_handler(client, message):
    cmd = message.command
    target = None

    if len(cmd) > 1:
        target = cmd[1]
    elif message.reply_to_message:
        if message.reply_to_message.from_user:
            target = message.reply_to_message.from_user.id
        elif message.reply_to_message.sender_chat:
            target = message.reply_to_message.sender_chat.id
    else:
        target = message.chat.id

    try:
        chat = await client.get_chat(target)
        tipe = str(chat.type).split(".")[-1].replace("_", " ").title()

        out = (
            f"🔍 **INFO IDENTITAS**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📝 **Nama:** {chat.first_name or chat.title}\n"
            f"🆔 **ID:** `{chat.id}`\n"
            f"👤 **Tipe:** {tipe}\n"
        )
        if chat.username:
            out += f"🔗 **Username:** @{chat.username}\n"
        out += "━━━━━━━━━━━━━━━━━━"

        await message.edit(out)
    except Exception as e:
        print(f"[ERROR] Cek ID error: {e}")
        await message.edit(
            "❌ **Gagal mendapatkan ID!**\n"
            "Pastikan username benar atau bot memiliki akses ke chat tersebut."
        )

async def set_pay_handler(client, message):
    target_msg = message
    if message.reply_to_message and (getattr(message.reply_to_message, "photo", None) or getattr(message.reply_to_message, "document", None)):
        target_msg = message.reply_to_message

    if not (getattr(target_msg, "photo", None) or getattr(target_msg, "document", None)):
        return await message.edit(
            "❌ **Gagal!** Kirim/Reply foto atau file QRIS dengan caption `.setpay [teks]`"
        )

    settings = load_settings()
    if target_msg is not message and getattr(target_msg, "caption", None):
        raw_text = target_msg.caption or ""
    else:
        raw_text = (message.text or message.caption or "")

    try:
        pay_text = raw_text.split(None, 1)[1]
    except IndexError:
        return await message.edit(
            "❌ **Gagal!** Masukkan teks keterangan setelah perintah `.setpay`"
        )

    file_id = target_msg.photo.file_id if getattr(target_msg, "photo", None) else target_msg.document.file_id

    settings["qris_file_id"] = file_id
    settings["pay_text"] = pay_text
    save_settings(settings)

    if getattr(message, "photo", None) or getattr(message, "document", None):
        await client.send_message("me", "✅ **Pembayaran (QRIS & Teks) Berhasil Disimpan!**")
        await message.delete()
    else:
        await message.edit("✅ **Pembayaran (QRIS & Teks) Berhasil Disimpan!**")

async def del_pay_handler(client, message):
    settings = load_settings()
    settings["qris_file_id"] = None
    settings["pay_text"] = DEFAULT_SETPAY_MSG
    save_settings(settings)
    await message.edit("🗑️ **Data Pembayaran Berhasil Dihapus!**")

async def pay_handler(client, message):
    settings = load_settings()
    pay_text = settings.get("pay_text", DEFAULT_SETPAY_MSG)
    qris_id = settings.get("qris_file_id")

    await message.delete()

    if qris_id:
        try:
            await client.send_photo(message.chat.id, qris_id, caption=pay_text)
        except Exception:
            await client.send_document(message.chat.id, qris_id, caption=pay_text)
    else:
        await client.send_message(message.chat.id, pay_text)

async def stop_action(client, message):
    user_id = client.me.id
    stop_anim_tasks[user_id] = True
    spam_active[user_id] = False

    notification = await message.edit("🛑 **Stop Action:** Animasi dan spam dihentikan")
    await asyncio.sleep(QUICK_DELETE_DELAY)
    try:
        await notification.delete()
    except Exception:
        pass

async def stop_autoreply_handler(client, message):
    if message.chat.type.name != "PRIVATE":
        notification = await message.edit(
            "❌ **Perintah hanya berfungsi di PM!**\n\n"
            "Gunakan `.stoppm` di chat pribadi dengan user."
        )
        await asyncio.sleep(QUICK_DELETE_DELAY)
        try:
            await notification.delete()
        except Exception:
            pass
        return

    target_user = message.from_user

    if not target_user:
        notification = await message.edit("❌ **Tidak dapat mendeteksi user!**")
        await asyncio.sleep(QUICK_DELETE_DELAY)
        try:
            await notification.delete()
        except Exception:
            pass
        return

    user_id = target_user.id
    user_name = target_user.first_name

    stopped_users[user_id] = user_name

    if user_id in reply_counts:
        del reply_counts[user_id]

    notification = await message.edit(
        f"✅ **Auto-Reply Dihentikan!**\n\n"
        f"👤 User: **{user_name}**\n"
        f"🆔 ID: `{user_id}`\n\n"
        f"User ini tidak akan menerima auto-reply lagi.\n"
        f"Gunakan `.unstoppm` untuk mengaktifkan kembali."
    )
    await asyncio.sleep(QUICK_DELETE_DELAY)
    try:
        await notification.delete()
    except Exception:
        pass

async def unstop_autoreply_handler(client, message):
    if message.chat.type.name != "PRIVATE":
        notification = await message.edit(
            "❌ **Perintah hanya berfungsi di PM!**\n\n"
            "Gunakan `.unstoppm` di chat pribadi dengan user."
        )
        await asyncio.sleep(QUICK_DELETE_DELAY)
        try:
            await notification.delete()
        except Exception:
            pass
        return

    target_user = message.from_user

    if not target_user:
        notification = await message.edit("❌ **Tidak dapat mendeteksi user!**")
        await asyncio.sleep(QUICK_DELETE_DELAY)
        try:
            await notification.delete()
        except Exception:
            pass
        return

    user_id = target_user.id
    user_name = target_user.first_name

    if user_id in stopped_users:
        del stopped_users[user_id]
        notification = await message.edit(
            f"✅ **Auto-Reply Diaktifkan Kembali!**\n\n"
            f"👤 User: **{user_name}**\n"
            f"🆔 ID: `{user_id}`\n\n"
            f"User ini akan menerima auto-reply lagi (max 3x)."
        )
    else:
        notification = await message.edit(
            f"ℹ️ **User ini tidak di-stop**\n\n"
            f"👤 User: **{user_name}**\n"
            f"🆔 ID: `{user_id}`"
        )

    await asyncio.sleep(QUICK_DELETE_DELAY)
    try:
        await notification.delete()
    except Exception:
        pass

async def list_stopped_pm_handler(client, message):
    if not stopped_users:
        return await message.edit(
            "📝 **Daftar Stop PM: Kosong**\n\n"
            "Tidak ada user yang di-stop auto-reply."
        )

    text = "🚫 **DAFTAR USER DI-STOP**\n━━━━━━━━━━━━━━━━━━\n\n"

    for idx, (user_id, user_name) in enumerate(stopped_users.items(), 1):
        text += f"{idx}. **{user_name}**\n   └ ID: `{user_id}`\n\n"

    text += f"━━━━━━━━━━━━━━━━━━\n📊 Total: {len(stopped_users)} user"

    await message.edit(text)

async def clear_stopped_pm_handler(client, message):
    count = len(stopped_users)
    stopped_users.clear()

    await message.edit(
        f"🗑️ **Daftar Stop PM Dibersihkan!**\n\n"
        f"✅ {count} user dihapus dari daftar.\n"
        f"Semua user akan menerima auto-reply lagi."
    )

async def add_blacklist_handler(client, message):
    if message.chat.type.name not in ["GROUP", "SUPERGROUP"]:
        notification = await message.edit(
            "❌ **Command ini hanya untuk grup!**\n\n"
            "Gunakan `.addbl` di grup yang ingin di-blacklist."
        )
        await asyncio.sleep(QUICK_DELETE_DELAY)
        try:
            await notification.delete()
        except Exception:
            pass
        return
    
    chat_id = message.chat.id
    chat_name = message.chat.title or "Grup"
    
    settings = load_settings()
    blacklist = settings.get("blacklist_groups", [])
    
    if chat_id in blacklist:
        notification = await message.edit(
            f"ℹ️ **Grup ini sudah di-blacklist**\n\n"
            f"👥 Grup: **{chat_name}**\n"
            f"🆔 ID: `{chat_id}`"
        )
        await asyncio.sleep(QUICK_DELETE_DELAY)
        try:
            await notification.delete()
        except Exception:
            pass
        return
    
    blacklist.append(chat_id)
    settings["blacklist_groups"] = blacklist
    save_settings(settings)
    
    try:
        await client.update_folder(chat_id, 1) 
    except Exception:
        pass 
    
    notification = await message.edit(
        f"✅ **Grup Berhasil Di-Blacklist!**\n\n"
        f"👥 Grup: **{chat_name}**\n"
        f"🆔 ID: `{chat_id}`\n\n"
        f"🔇 Grup di-mute otomatis\n"
        f"🚫 Mention/tag akan diabaikan\n\n"
        f"Gunakan `.offbl` untuk menghapus dari blacklist."
    )
    
    await asyncio.sleep(MESSAGE_DELETE_DELAY)
    try:
        await notification.delete()
    except Exception:
        pass

async def remove_blacklist_handler(client, message):
    if message.chat.type.name not in ["GROUP", "SUPERGROUP"]:
        notification = await message.edit(
            "❌ **Command ini hanya untuk grup!**\n\n"
            "Gunakan `.offbl` di grup yang ingin dihapus dari blacklist."
        )
        await asyncio.sleep(QUICK_DELETE_DELAY)
        try:
            await notification.delete()
        except Exception:
            pass
        return
    
    chat_id = message.chat.id
    chat_name = message.chat.title or "Grup"
    
    settings = load_settings()
    blacklist = settings.get("blacklist_groups", [])
    
    if chat_id not in blacklist:
        notification = await message.edit(
            f"ℹ️ **Grup ini tidak ada di blacklist**\n\n"
            f"👥 Grup: **{chat_name}**\n"
            f"🆔 ID: `{chat_id}`"
        )
        await asyncio.sleep(QUICK_DELETE_DELAY)
        try:
            await notification.delete()
        except Exception:
            pass
        return
    
    blacklist.remove(chat_id)
    settings["blacklist_groups"] = blacklist
    save_settings(settings)
    
    try:
        await client.update_folder(chat_id, 0)
    except Exception:
        pass 
    
    notification = await message.edit(
        f"✅ **Grup Dihapus dari Blacklist!**\n\n"
        f"👥 Grup: **{chat_name}**\n"
        f"🆔 ID: `{chat_id}`\n\n"
        f"🔔 Grup di-unmute\n"
        f"✅ Mention/tag akan direspons kembali"
    )
    
    await asyncio.sleep(MESSAGE_DELETE_DELAY)
    try:
        await notification.delete()
    except Exception:
        pass

async def list_blacklist_handler(client, message):
    settings = load_settings()
    blacklist = settings.get("blacklist_groups", [])
    
    if not blacklist:
        return await message.edit(
            "📝 **Daftar Blacklist Grup: Kosong**\n\n"
            "Tidak ada grup yang di-blacklist.\n\n"
            "Gunakan `.addbl` di grup untuk menambahkan ke blacklist."
        )
    
    text = "🚫 **DAFTAR BLACKLIST GRUP**\n━━━━━━━━━━━━━━━━━━\n\n"
    
    for idx, chat_id in enumerate(blacklist, 1):
        try:
            chat = await client.get_chat(chat_id)
            chat_name = chat.title or "Unknown"
            chat_username = f"@{chat.username}" if chat.username else "-"
            text += f"{idx}. **{chat_name}**\n"
            text += f"   └ {chat_username}\n"
            text += f"   └ ID: `{chat_id}`\n\n"
        except Exception:
            text += f"{idx}. **Grup Tidak Ditemukan**\n"
            text += f"   └ ID: `{chat_id}`\n\n"
    
    text += f"━━━━━━━━━━━━━━━━━━\n📊 Total: {len(blacklist)} grup\n\n"
    text += "💡 **Tips:**\n"
    text += "• `.addbl` - Tambah grup ke blacklist\n"
    text += "• `.offbl` - Hapus grup dari blacklist"
    
    await message.edit(text)

async def restart_ubot(client, message):
    await message.edit("🔄 **Restarting Userbot...**")
    user_id = client.me.id
    spam_active[user_id] = False
    stop_anim_tasks[user_id] = True
    await asyncio.sleep(2)
    await message.delete()
    os.execl(sys.executable, sys.executable, *sys.argv)

async def dspam_handler(client, message):
    if len(message.command) < 4:
        return await message.edit("❌ **Format:** `.dspam [delay] [count] [text]`")

    try:
        base_delay = float(message.command[1])
        count = int(message.command[2])
        spam_text = message.text.split(None, 3)[3]
    except (ValueError, IndexError) as e:
        print(f"[ERROR] dspam_handler input error: {e}")
        return await message.edit("❌ Input tidak valid.")

    chat_id = message.chat.id
    chat_title = message.chat.title or "Chat"
    user_id = client.me.id

    await message.delete()
    spam_active[user_id] = True
    success_count = 0

    for _ in range(count):
        if not spam_active.get(user_id):
            break

        res = await worker_spam(client, chat_id, spam_text)
        if res:
            success_count += 1

        jitter = random.uniform(0.1, 0.5)
        total_sleep = base_delay + jitter
        if total_sleep > 0:
            await asyncio.sleep(total_sleep)

    await send_log(
        client,
        f"✅ **DSpam Selesai**\n**Chat:** {chat_title}\n**Total Berhasil:** {success_count}"
    )

async def tag_log_handler(client, message):
    try:
        settings = load_settings()
        if message.chat.id in settings.get("blacklist_groups", []):
            return

        chat_name = message.chat.title or "Grup"
        from_user = message.from_user.first_name if message.from_user else "Seseorang"
        from_user_id = message.from_user.id if message.from_user else 0
        msg_id = message.id

        if message.chat.username:
            link = f"https://t.me/{message.chat.username}/{msg_id}"
        else:
            link = f"https://t.me/c/{str(message.chat.id)[4:]}/{msg_id}"

        log_db.add_mention_log(
            from_user_id=from_user_id,
            from_user_name=from_user,
            chat_id=message.chat.id,
            chat_name=chat_name,
            message_text=message.text or "[Media]",
            message_link=link
        )

        log_text = (
            "📩 **LOG TAG / REPLY**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"👤 **Dari:** {from_user}\n"
            f"👥 **Grup:** {chat_name}\n"
            f"💬 **Pesan:** `{message.text or '[Media]'}`\n"
            f"🔗 **Link:** [Buka Pesan]({link})"
        )
        await send_log(client, log_text)
    except Exception as e:
        print(f"[ERROR] tag_log_handler: {e}")

async def new_chat_members_handler(client, message):
    try:
        chat = message.chat
        chat_name = chat.title or "Grup"
        chat_username = chat.username or ""

        for user in message.new_chat_members:
            is_self = user.id == client.me.id
            user_name = user.first_name or "User"
            user_username = user.username or ""

            log_db.add_join_log(
                user_id=user.id,
                user_name=user_name,
                user_username=user_username,
                chat_id=chat.id,
                chat_name=chat_name,
                chat_username=chat_username,
                is_self=is_self
            )

            if is_self:
                log_text = (
                    "✅ **SAYA JOIN GRUP BARU**\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    f"👥 **Grup:** {chat_name}\n"
                    f"🔗 **Username:** @{chat_username if chat_username else 'Tidak ada'}\n"
                    f"🆔 **Chat ID:** `{chat.id}`\n"
                    f"📊 **Status:** Berhasil bergabung\n"
                    f"🕐 **Waktu:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
            else:
                log_text = (
                    "✅ **LOG JOIN GRUP**\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    f"👤 **User:** {user_name}\n"
                    f"🔗 **Username:** @{user_username if user_username else 'Tidak ada'}\n"
                    f"🆔 **User ID:** `{user.id}`\n"
                    f"👥 **Grup:** {chat_name}\n"
                    f"📊 **Status:** Bergabung\n"
                    f"🕐 **Waktu:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )

            await send_log(client, log_text)
    except Exception as e:
        print(f"[ERROR] new_chat_members_handler: {e}")

async def left_chat_member_handler(client, message):
    try:
        chat = message.chat
        user = message.left_chat_member

        if not user:
            return

        chat_name = chat.title or "Grup"
        chat_username = chat.username or ""
        is_self = user.id == client.me.id
        user_name = user.first_name or "User"
        user_username = user.username or ""

        log_db.add_leave_log(
            user_id=user.id,
            user_name=user_name,
            user_username=user_username,
            chat_id=chat.id,
            chat_name=chat_name,
            chat_username=chat_username,
            is_self=is_self
        )

        if is_self:
            log_text = (
                "🚪 **SAYA KELUAR DARI GRUP**\n"
                "━━━━━━━━━━━━━━━━━━\n"
                f"👥 **Grup:** {chat_name}\n"
                f"🔗 **Username:** @{chat_username if chat_username else 'Tidak ada'}\n"
                f"🆔 **Chat ID:** `{chat.id}`\n"
                f"📊 **Status:** Telah keluar\n"
                f"🕐 **Waktu:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
        else:
            log_text = (
                "🚪 **LOG KELUAR GRUP**\n"
                "━━━━━━━━━━━━━━━━━━\n"
                f"👤 **User:** {user_name}\n"
                f"🔗 **Username:** @{user_username if user_username else 'Tidak ada'}\n"
                f"🆔 **User ID:** `{user.id}`\n"
                f"👥 **Grup:** {chat_name}\n"
                f"📊 **Status:** Keluar/Dikick\n"
                f"🕐 **Waktu:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

        await send_log(client, log_text)
    except Exception as e:
        print(f"[ERROR] left_chat_member_handler: {e}")

async def scan_groups_handler(client, message):
    await message.edit("🔍 **Scanning semua grup...**")

    total_groups = 0
    new_logs = 0
    group_list = []

    try:
        async for dialog in client.get_dialogs():
            if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                total_groups += 1
                chat = dialog.chat
                chat_name = chat.title or "Grup"
                chat_username = chat.username or ""

                log_db.add_join_log(
                    user_id=client.me.id,
                    user_name=client.me.first_name,
                    user_username=client.me.username or "",
                    chat_id=chat.id,
                    chat_name=chat_name,
                    chat_username=chat_username,
                    is_self=True
                )
                new_logs += 1

                username_display = f"@{chat_username}" if chat_username else "Tidak ada"
                group_list.append(f"• **{chat_name}**\n  └ {username_display}\n  └ ID: `{chat.id}`")

        if len(group_list) <= GROUP_LIST_CHUNK_SIZE:
            group_text = "\n\n".join(group_list)
            result_text = (
                "✅ **Scan Selesai!**\n"
                "━━━━━━━━━━━━━━━━━━\n"
                f"📊 **Total Grup:** {total_groups}\n"
                f"💾 **Log Tersimpan:** {new_logs}\n\n"
                "📋 **DAFTAR GRUP:**\n\n"
                f"{group_text}\n\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "Gunakan `.jaseball <pesan>` untuk broadcast"
            )
        else:
            group_text = "\n\n".join(group_list[:10])
            result_text = (
                "✅ **Scan Selesai!**\n"
                "━━━━━━━━━━━━━━━━━━\n"
                f"📊 **Total Grup:** {total_groups}\n"
                f"💾 **Log Tersimpan:** {new_logs}\n\n"
                "📋 **DAFTAR GRUP (10 pertama):**\n\n"
                f"{group_text}\n\n"
                f"...dan {total_groups - 10} grup lainnya\n\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "Gunakan `.listgroups` untuk daftar lengkap\n"
                "Gunakan `.jaseball <pesan>` untuk broadcast"
            )

        await message.edit(result_text)

    except Exception as e:
        await message.edit(f"❌ **Error saat scanning:** {str(e)}")
        print(f"[ERROR] scan_groups_handler: {e}")

async def monitor_group_handler(client, message):
    cmd = message.command

    if len(cmd) < 2:
        return await message.edit(
            "❌ **Format salah!**\n\n"
            "**Gunakan:**\n"
            "`.monitor on` - Aktifkan monitoring\n"
            "`.monitor off` - Matikan monitoring\n"
            "`.monitor status` - Cek status"
        )

    action = cmd[1].lower()
    settings = load_settings()

    if action == "on":
        settings["monitor_active"] = True
        save_settings(settings)
        await message.edit("✅ **Monitoring Join/Leave Aktif!**\n\nBot akan otomatis cek grup setiap 5 menit.")

    elif action == "off":
        settings["monitor_active"] = False
        save_settings(settings)
        await message.edit("❌ **Monitoring Join/Leave Dimatikan!**")

    elif action == "status":
        is_active = settings.get("monitor_active", False)
        status = "✅ Aktif" if is_active else "❌ Nonaktif"
        await message.edit(f"📊 **Status Monitoring:** {status}")

    else:
        await message.edit("❌ **Perintah tidak dikenal!** Gunakan: on, off, atau status")

async def list_groups_handler(client, message):
    await message.edit("🔍 **Mengambil daftar grup...**")

    group_list = []
    total = 0

    try:
        async for dialog in client.get_dialogs():
            if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                total += 1
                chat = dialog.chat
                chat_name = chat.title or "Grup"
                chat_username = chat.username or ""
                username_display = f"@{chat_username}" if chat_username else "Tidak ada"

                group_list.append(
                    f"{total}. **{chat_name}**\n"
                    f"   └ {username_display}\n"
                    f"   └ ID: `{chat.id}`"
                )

        if not group_list:
            return await message.edit("📝 **Tidak ada grup ditemukan**")

        chunk_size = GROUP_LIST_CHUNK_SIZE
        chunks = [group_list[i:i + chunk_size] for i in range(0, len(group_list), chunk_size)]

        for idx, chunk in enumerate(chunks):
            chunk_text = "\n\n".join(chunk)

            if idx == 0:
                header = (
                    f"📋 **DAFTAR SEMUA GRUP** ({total} Total)\n"
                    f"━━━━━━━━━━━━━━━━━━\n\n"
                    f"{chunk_text}\n\n"
                )

                if len(chunks) > 1:
                    header += f"━━━━━━━━━━━━━━━━━━\n📄 Halaman 1/{len(chunks)}"
                else:
                    header += "━━━━━━━━━━━━━━━━━━\nGunakan `.jaseball <pesan>` untuk broadcast"

                await message.edit(header)
            else:
                text = f"📄 **Halaman {idx + 1}/{len(chunks)}**\n━━━━━━━━━━━━━━━━━━\n\n{chunk_text}"

                if idx == len(chunks) - 1:
                    text += "\n\n━━━━━━━━━━━━━━━━━━\nGunakan `.jaseball <pesan>` untuk broadcast"

                await client.send_message(message.chat.id, text)

    except Exception as e:
        await message.edit(f"❌ **Error:** {str(e)}")
        print(f"[ERROR] list_groups_handler: {e}")

async def jaseball_handler(client, message):
    if len(message.command) < 2:
        return await message.edit(
            "❌ **Format salah!**\n\n"
            "**Gunakan:**\n"
            "`.jaseball [pesan]` - Kirim pesan ke semua grup\n"
            "`.jaseball test [pesan]` - Test kirim ke 3 grup pertama\n\n"
            "**Contoh:**\n"
            "`.jaseball Halo semuanya! 👋`\n"
            "`.jaseball test Ini pesan test`"
        )

    is_test = message.command[1].lower() == "test"

    if is_test:
        if len(message.command) < 3:
            return await message.edit("❌ Format: `.jaseball test [pesan]`")
        broadcast_text = message.text.split(None, 2)[2]
        max_groups = BROADCAST_TEST_LIMIT
    else:
        broadcast_text = message.text.split(None, 1)[1]
        max_groups = None

    await message.edit("📡 **Memulai broadcast...**")

    group_list = []
    success = 0
    failed = 0
    total_groups = 0

    try:
        async for dialog in client.get_dialogs():
            if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                group_list.append(dialog.chat)
                total_groups += 1

                if max_groups and len(group_list) >= max_groups:
                    break

        if not group_list:
            return await message.edit("❌ **Tidak ada grup ditemukan!**\nGunakan `.scangroups` terlebih dahulu.")

        mode_text = f"(Mode Test - {len(group_list)} grup)" if is_test else f"({len(group_list)} grup)"
        await message.edit(
            f"📡 **Memulai broadcast...** {mode_text}\n"
            f"📊 Progress: 0/{len(group_list)}"
        )

        for idx, chat in enumerate(group_list, 1):
            try:
                await client.send_chat_action(chat.id, ChatAction.TYPING)
                await asyncio.sleep(random.uniform(TYPING_DELAY_MIN, TYPING_DELAY_MAX))

                await client.send_message(chat.id, broadcast_text)
                success += 1

                if idx % 5 == 0 or idx == len(group_list):
                    await message.edit(
                        f"📡 **Broadcasting...** {mode_text}\n"
                        f"📊 Progress: {idx}/{len(group_list)}\n"
                        f"✅ Berhasil: {success}\n"
                        f"❌ Gagal: {failed}"
                    )

                await asyncio.sleep(random.uniform(BROADCAST_DELAY_MIN, BROADCAST_DELAY_MAX))

            except FloodWait as e:
                if e.value > FLOOD_WAIT_THRESHOLD:
                    await send_log(
                        client,
                        f"⚠️ **FLOOD WAIT TERDETEKSI!**\n"
                        f"Menunggu {e.value} detik...\n"
                        f"Progress: {idx}/{len(group_list)}"
                    )
                    await asyncio.sleep(e.value + 5)
                else:
                    await asyncio.sleep(e.value + 1)

                try:
                    await client.send_message(chat.id, broadcast_text)
                    success += 1
                except Exception:
                    failed += 1

            except Exception as e:
                failed += 1
                print(f"[ERROR] Error sending broadcast to {chat.title}: {e}")

        result_text = (
            "✅ **BROADCAST SELESAI!**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"📊 **Total Grup:** {total_groups}\n"
            f"📤 **Dikirim ke:** {len(group_list)} grup\n"
            f"✅ **Berhasil:** {success}\n"
            f"❌ **Gagal:** {failed}\n"
            f"💬 **Pesan:** `{broadcast_text[:50]}...`"
        )

        if is_test:
            result_text += "\n\n⚠️ **Mode Test** - Hanya 3 grup pertama"

        await message.edit(result_text)
        await send_log(client, result_text)

    except Exception as e:
        await message.edit(f"❌ **Error saat broadcast:** {str(e)}")
        print(f"[ERROR] jaseball_handler: {e}")

async def broadcast_worker(client, message, target_list, is_copy=False):
    success = 0
    failed = 0
    total = len(target_list)
    msg_to_copy = message.reply_to_message
    text_to_send = None

    if not is_copy:
        text_to_send = message.text.split(None, 1)[1] if len(message.command) > 1 else None

    settings = load_settings()
    blacklist = settings.get("blacklist_groups", [])

    progress_msg = await message.edit(f"🚀 **Memulai Broadcast...**\n🎯 Target: {total} obrolan")
    start_time = time.time()

    for idx, chat_id in enumerate(target_list, 1):
        if chat_id in blacklist:
            continue

        try:
            await asyncio.sleep(random.uniform(1.5, 3.0))

            if is_copy and msg_to_copy:
                await msg_to_copy.copy(chat_id)
            elif text_to_send:
                await client.send_message(chat_id, text_to_send)
            
            success += 1

        except FloodWait as e:
            await asyncio.sleep(e.value + 5)
            try:
                if is_copy and msg_to_copy:
                    await msg_to_copy.copy(chat_id)
                elif text_to_send:
                    await client.send_message(chat_id, text_to_send)
                success += 1
            except:
                failed += 1
        except Exception:
            failed += 1

        if idx % 10 == 0 or idx == total:
            elapsed = time.time() - start_time
            avg_time = elapsed / idx
            eta = (total - idx) * avg_time
            
            if eta < 60:
                eta_str = f"{int(eta)} detik"
            else:
                eta_str = f"{int(eta//60)} menit"

            try:
                await progress_msg.edit(
                    f"📡 **BROADCAST STATUS**\n"
                    f"━━━━━━━━━━━━━━━━━━\n"
                    f"📊 **Progress:** {round((idx/total)*100)}% ({idx}/{total})\n"
                    f"✅ **Berhasil:** {success}\n"
                    f"❌ **Gagal:** {failed}\n"
                    f"⏳ **ETA:** {eta_str}\n"
                    f"━━━━━━━━━━━━━━━━━━"
                )
            except:
                pass

    return success, failed, total

async def gcast_handler(client, message):
    if not message.reply_to_message and len(message.command) < 2:
        return await message.edit("❌ **Format:** `.gcast [pesan]` atau reply ke media.")

    is_copy = bool(message.reply_to_message)
    target_list = []

    async for dialog in client.get_dialogs():
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            target_list.append(dialog.chat.id)

    if not target_list:
        return await message.edit("❌ **Tidak ada grup ditemukan!**")

    success, failed, total = await broadcast_worker(client, message, target_list, is_copy)

    report = (
        f"✅ **GCAST GROUP SELESAI**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🎯 **Total:** {total}\n"
        f"✅ **Berhasil:** {success}\n"
        f"❌ **Gagal:** {failed}\n"
        f"━━━━━━━━━━━━━━━━━━"
    )
    await message.reply(report)
    await send_log(client, report)

async def gucast_handler(client, message):
    if not message.reply_to_message and len(message.command) < 2:
        return await message.edit("❌ **Format:** `.gucast [pesan]` atau reply ke media.")

    is_copy = bool(message.reply_to_message)
    target_list = []

    await message.edit("🔍 **Scanning Private Chats...**")

    async for dialog in client.get_dialogs():
        if dialog.chat.type == ChatType.PRIVATE and not dialog.chat.is_support:
            target_list.append(dialog.chat.id)

    if not target_list:
        return await message.edit("❌ **Tidak ada user private ditemukan!**")

    success, failed, total = await broadcast_worker(client, message, target_list, is_copy)

    report = (
        f"✅ **GCAST USER SELESAI**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🎯 **Total:** {total}\n"
        f"✅ **Berhasil:** {success}\n"
        f"❌ **Gagal:** {failed}\n"
        f"━━━━━━━━━━━━━━━━━━"
    )
    await message.reply(report)
    await send_log(client, report)

async def show_logs_handler(client, message):
    cmd = message.command
    log_type = cmd[1] if len(cmd) > 1 else "join"
    limit = int(cmd[2]) if len(cmd) > 2 else LOG_LIMIT_DEFAULT

    if log_type == "join":
        logs = log_db.get_join_leave_logs(limit=limit)
        if not logs:
            return await message.edit("📝 **Tidak ada log join/leave**")

        text = "📊 **LOG JOIN/LEAVE GRUP**\n━━━━━━━━━━━━━━━━━━\n\n"
        for log in logs:
            emoji = "✅" if log["type"] == "join" else "🚪"
            action = "Bergabung" if log["type"] == "join" else "Keluar"
            self_tag = " (SAYA)" if log["is_self"] else ""

            text += (
                f"{emoji} **{log['user_name']}{self_tag}**\n"
                f"   └ {action} dari **{log['chat_name']}**\n"
                f"   └ 🕐 {log['timestamp']}\n\n"
            )

        await message.edit(text)

    elif log_type == "mention":
        logs = log_db.get_mention_logs(limit=limit)
        if not logs:
            return await message.edit("📝 **Tidak ada log mention**")

        text = "📩 **LOG MENTION/TAG**\n━━━━━━━━━━━━━━━━━━\n\n"
        for log in logs:
            text += (
                f"👤 **{log['from_user_name']}** di **{log['chat_name']}**\n"
                f"   └ 💬 `{log['message_text'][:50]}...`\n"
                f"   └ 🕐 {log['timestamp']}\n\n"
            )

        await message.edit(text)

    elif log_type == "pm":
        logs = log_db.get_private_message_logs(limit=limit)
        if not logs:
            return await message.edit("📝 **Tidak ada log private message**")

        text = "💬 **LOG PRIVATE MESSAGE**\n━━━━━━━━━━━━━━━━━━\n\n"
        for log in logs:
            text += (
                f"👤 **{log['from_user_name']}**\n"
                f"   └ 💬 `{log['message_text'][:50]}...`\n"
                f"   └ 🕐 {log['timestamp']}\n\n"
            )

        await message.edit(text)

    elif log_type == "stats":
        stats = log_db.get_stats()
        text = (
            "📊 **STATISTIK LOG**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"✅ **Total Join:** {stats['total_joins']}\n"
            f"🚪 **Total Leave:** {stats['total_leaves']}\n"
            f"📩 **Total Mention:** {stats['total_mentions']}\n"
            f"💬 **Total PM:** {stats['total_private_messages']}"
        )
        await message.edit(text)

    else:
        await message.edit(
            "❌ **Format salah!**\n\n"
            "**Gunakan:**\n"
            "`.logs join [jumlah]` - Lihat log join/leave\n"
            "`.logs mention [jumlah]` - Lihat log mention\n"
            "`.logs pm [jumlah]` - Lihat log PM\n"
            "`.logs stats` - Lihat statistik"
        )

async def clear_logs_handler(client, message):
    log_db.clear_all_logs()
    await message.edit("🗑️ **Semua log berhasil dihapus!**")

async def autoreply_handler(client, message):
async def autoreply_handler(client, message):
    settings = load_settings()
    if not settings.get("aktif"):
        return

    user = getattr(message, "from_user", None)
    if not user:
        return

    if message.chat and message.chat.id in [777000, 42777]:
        return

    if getattr(user, "is_verified", False):
        return

    if getattr(user, "is_bot", False):
        return

    me_id = client.me.id
    if user.id == me_id:
        return

    uid = user.id
    if uid in stopped_users:
        return

    user_name = user.first_name or "Unknown"
    msg_text = message.text or "[Media]"

    log_db.add_private_message_log(
        from_user_id=uid,
        from_user_name=user_name,
        message_text=msg_text
    )

    log_msg = f"📩 **Pesan Baru**\n**Dari:** {user_name}\n**Pesan:** {msg_text}"
    await send_log(client, log_msg)

    if uid not in reply_counts:
        reply_counts[uid] = 0

    if reply_counts[uid] < AUTOREPLY_MAX_COUNT:
        try:
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            await asyncio.sleep(1.5)
            await message.reply(settings.get("pesan", DEFAULT_AUTOREPLY_MSG))
            reply_counts[uid] += 1
        except Exception as e:
            print(f"[ERROR] Autoreply error: {e}")

async def set_on(client, message):
    settings = load_settings()
    settings["aktif"] = True
    stopped_users.clear()
    reply_counts.clear()
    save_settings(settings)
    await message.edit("✅ Auto-Reply Aktif")

async def set_off(client, message):
    settings = load_settings()
    settings["aktif"] = False
    stopped_users.clear()
    reply_counts.clear()
    save_settings(settings)
    await message.edit("❌ Auto-Reply Mati")

async def set_reply(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ Format: .setreply <pesan>")

    settings = load_settings()
    new_pesan = message.text.split(None, 1)[1]
    settings["pesan"] = new_pesan
    save_settings(settings)
    await message.edit("✅ **Auto-Reply diubah!**")

async def monitor_loop(client):
    await asyncio.sleep(INITIAL_MONITOR_DELAY)

    known_groups = set()

    try:
        async for dialog in client.get_dialogs():
            if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                known_groups.add(dialog.chat.id)
    except Exception as e:
        print(f"[ERROR] Monitor initial scan: {e}")

    while True:
        try:
            settings = load_settings()
            if not settings.get("monitor_active", False):
                await asyncio.sleep(MONITOR_CHECK_INTERVAL)
                continue

            current_groups = set()

            async for dialog in client.get_dialogs():
                if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                    current_groups.add(dialog.chat.id)

            new_groups = current_groups - known_groups
            for chat_id in new_groups:
                try:
                    chat = await client.get_chat(chat_id)
                    chat_name = chat.title or "Grup"
                    chat_username = chat.username or ""

                    log_db.add_join_log(
                        user_id=client.me.id,
                        user_name=client.me.first_name,
                        user_username=client.me.username or "",
                        chat_id=chat.id,
                        chat_name=chat_name,
                        chat_username=chat_username,
                        is_self=True
                    )

                    log_text = (
                        "✅ **SAYA JOIN GRUP BARU (Monitor)**\n"
                        "━━━━━━━━━━━━━━━━━━\n"
                        f"👥 **Grup:** {chat_name}\n"
                        f"🔗 **Username:** @{chat_username if chat_username else 'Tidak ada'}\n"
                        f"🆔 **Chat ID:** `{chat.id}`\n"
                        f"🕐 **Waktu:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                    await send_log(client, log_text)
                except Exception as e:
                    print(f"[ERROR] Monitor processing new group {chat_id}: {e}")

            left_groups = known_groups - current_groups
            for chat_id in left_groups:
                try:
                    logs = log_db.get_join_leave_logs(limit=100)
                    chat_name = "Unknown Group"
                    for log in logs:
                        if log.get("chat_id") == chat_id:
                            chat_name = log.get("chat_name", "Unknown Group")
                            break

                    log_db.add_leave_log(
                        user_id=client.me.id,
                        user_name=client.me.first_name,
                        user_username=client.me.username or "",
                        chat_id=chat_id,
                        chat_name=chat_name,
                        chat_username="",
                        is_self=True
                    )

                    log_text = (
                        "🚪 **SAYA KELUAR DARI GRUP (Monitor)**\n"
                        "━━━━━━━━━━━━━━━━━━\n"
                        f"👥 **Grup:** {chat_name}\n"
                        f"🆔 **Chat ID:** `{chat_id}`\n"
                        f"🕐 **Waktu:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                    await send_log(client, log_text)
                except Exception as e:
                    print(f"[ERROR] Monitor processing left group {chat_id}: {e}")

            known_groups = current_groups

            await asyncio.sleep(MONITOR_CHECK_INTERVAL)

        except Exception as e:
            print(f"[ERROR] Monitor loop error: {e}")
            await asyncio.sleep(MONITOR_CHECK_INTERVAL)

async def set_av_handler(client, message):
    cmd = message.command
    if len(cmd) < 2:
        return await message.edit("❌ Gunakan: `.av on` atau `.av off`")
    
    action = cmd[1].lower()
    settings = load_settings()
    
    if action == "on":
        settings["anti_view_once"] = True
        save_settings(settings)
        settings["anti_view_once"] = True
        save_settings(settings)
        await message.edit("✅ **Anti View-Once Aktif!**\n\nSiap maling pap yang ada timer-nya. 😎\nHasil akan dikirim ke Assistant Bot (jika ada) atau Saved Messages.")
    elif action == "off":
        settings["anti_view_once"] = False
        save_settings(settings)
        await message.edit("❌ **Anti View-Once Dimatikan.**")
    else:
        await message.edit("❌ Gunakan: `.av on` atau `.av off`")

async def anti_view_once_watcher(client, message):
    try:
        settings = load_settings()
        if not settings.get("anti_view_once", False):
            return

        is_protected = message.has_protected_content
        if not (message.photo or message.video or message.voice or message.video_note):
            return
        
        if is_protected:
            download_path = await message.download()
            if not download_path:
                return
            
            sender_name = message.from_user.first_name if message.from_user else "Unknown"
            caption = (
                f"🕵️‍♂️ **MALING VIEW ONCE**\n"
                f"👤 **Dari:** {sender_name} (`{message.from_user.id}`)\n"
                f"🕐 **Waktu:** {datetime.now().strftime('%H:%M:%S')}"
            )
            
            if hasattr(client, 'inline_manager'):
                target = client.inline_manager.bot_username
            else:
                target = "me"

            if message.photo:
                await client.send_photo(target, download_path, caption=caption)
            elif message.video:
                await client.send_video(target, download_path, caption=caption)
            elif message.voice:
                await client.send_voice(target, download_path, caption=caption)
            elif message.video_note:
                await client.send_video_note(target, download_path)
                await client.send_message(target, caption)
                
            if os.path.exists(download_path):
                os.remove(download_path)
                
    except Exception as e:
        print(f"[ERROR] AV Watcher: {e}")


def install_ubot_handlers(ubot):
    m = MessageHandler
    me = filters.me

    print("[INFO] Installing handlers...")

    ubot.add_handler(m(ping_ubot, filters.command("ping", prefixes=".") & me))
    ubot.add_handler(m(alive_inline_handler, filters.command("alive", prefixes=".") & me))
    ubot.add_handler(m(help_inline_handler, filters.command("help", prefixes=".") & me))
    
    ubot.add_handler(m(status_ubot, filters.command("status", prefixes=".") & me))
    ubot.add_handler(m(cek_id_handler, filters.command("cekid", prefixes=".") & me))
    ubot.add_handler(m(stop_action, filters.command("stop", prefixes=".") & me))
    ubot.add_handler(m(restart_ubot, filters.command("restart", prefixes=".") & me))
    ubot.add_handler(m(dspam_handler, filters.command("dspam", prefixes=".") & me))

    ubot.add_handler(m(superdino_anim, filters.command("dino", prefixes=".") & me))
    ubot.add_handler(m(lucu_anim, filters.command("lucu", prefixes=".") & me))
    ubot.add_handler(m(keren_anim, filters.command("keren", prefixes=".") & me))
    ubot.add_handler(m(marah_anim, filters.command("marah", prefixes=".") & me))
    ubot.add_handler(m(sedih_anim, filters.command("sedih", prefixes=".") & me))
    ubot.add_handler(m(ketawa_anim, filters.command("ketawa", prefixes=".") & me))
    ubot.add_handler(m(heart_anim, filters.command("heart", prefixes=".") & me))
    ubot.add_handler(m(load_anim, filters.command("loading", prefixes=".") & me))
    ubot.add_handler(m(moon_anim, filters.command("moon", prefixes=".") & me))
    ubot.add_handler(m(clock_anim, filters.command("clock", prefixes=".") & me))
    

    ubot.add_handler(m(bomb_anim, filters.command("bomb", prefixes=".") & me))
    ubot.add_handler(m(rocket_anim, filters.command("roket", prefixes=".") & me))
    ubot.add_handler(m(police_anim, filters.command("police", prefixes=".") & me))
    ubot.add_handler(m(airplane_anim, filters.command("pesawat", prefixes=".") & me))
    ubot.add_handler(m(car_anim, filters.command("mobil", prefixes=".") & me))
    ubot.add_handler(m(bike_anim, filters.command("motor", prefixes=".") & me))
    ubot.add_handler(m(ufo_anim, filters.command("ufo", prefixes=".") & me))
    ubot.add_handler(m(ghost_anim, filters.command("hantu", prefixes=".") & me))
    ubot.add_handler(m(cat_anim, filters.command("kucing", prefixes=".") & me))
    ubot.add_handler(m(dog_anim, filters.command("anjing", prefixes=".") & me))
    ubot.add_handler(m(monkey_anim, filters.command("monyet", prefixes=".") & me))
    ubot.add_handler(m(dragon_anim, filters.command("naga", prefixes=".") & me))
    ubot.add_handler(m(rain_anim, filters.command("hujan", prefixes=".") & me))
    ubot.add_handler(m(snow_anim, filters.command("salju", prefixes=".") & me))
    ubot.add_handler(m(thunder_anim, filters.command("petir", prefixes=".") & me))
    ubot.add_handler(m(earth_anim, filters.command("bumi", prefixes=".") & me))
    ubot.add_handler(m(star_anim, filters.command("bintang", prefixes=".") & me))
    ubot.add_handler(m(fire_anim, filters.command("api", prefixes=".") & me))
    ubot.add_handler(m(money_anim, filters.command("duit", prefixes=".") & me))
    ubot.add_handler(m(beer_anim, filters.command("mabuk", prefixes=".") & me))
    ubot.add_handler(m(food_anim, filters.command("makan", prefixes=".") & me))
    ubot.add_handler(m(boxing_anim, filters.command("tinju", prefixes=".") & me))
    ubot.add_handler(m(ball_anim, filters.command("bola", prefixes=".") & me))
    ubot.add_handler(m(music_anim, filters.command("musik", prefixes=".") & me))
    ubot.add_handler(m(dance_anim, filters.command("dance", prefixes=".") & me))
    ubot.add_handler(m(robot_anim, filters.command("robot", prefixes=".") & me))
    ubot.add_handler(m(phone_anim, filters.command("telpon", prefixes=".") & me))
    ubot.add_handler(m(letter_anim, filters.command("surat", prefixes=".") & me))
    ubot.add_handler(m(key_anim, filters.command("kunci", prefixes=".") & me))
    ubot.add_handler(m(firework_anim, filters.command("kembangapi", prefixes=".") & me))
    ubot.add_handler(m(bday_anim, filters.command("ulangtahun", prefixes=".") & me))
    ubot.add_handler(m(sleep_anim, filters.command("tidur", prefixes=".") & me))
    ubot.add_handler(m(ninja_anim, filters.command("ninja", prefixes=".") & me))
    ubot.add_handler(m(uub_anim, filters.command("uub", prefixes=".") & me))
    ubot.add_handler(m(wave_anim, filters.command("pantai", prefixes=".") & me))
    ubot.add_handler(m(tree_anim, filters.command("pohon", prefixes=".") & me))
    ubot.add_handler(m(sun_anim, filters.command("matahari", prefixes=".") & me))
    ubot.add_handler(m(ocean_anim, filters.command("laut", prefixes=".") & me))
    ubot.add_handler(m(game_anim, filters.command("game", prefixes=".") & me))
    ubot.add_handler(m(tv_anim, filters.command("televisi", prefixes=".") & me))
    ubot.add_handler(m(tools_anim, filters.command("tools", prefixes=".") & me))
    ubot.add_handler(m(microscope_anim, filters.command("microscope", prefixes=".") & me))
    ubot.add_handler(m(space_anim, filters.command("space", prefixes=".") & me))
    ubot.add_handler(m(medical_anim, filters.command("medical", prefixes=".") & me))
    ubot.add_handler(m(workout_anim, filters.command("gym", prefixes=".") & me))
    ubot.add_handler(m(travel_anim, filters.command("travel", prefixes=".") & me))
    ubot.add_handler(m(magic_anim, filters.command("sulap", prefixes=".") & me))
    ubot.add_handler(m(weather_anim, filters.command("cuaca", prefixes=".") & me))
    ubot.add_handler(m(flags_anim, filters.command("bendera", prefixes=".") & me))
    ubot.add_handler(m(colors_anim, filters.command("warna", prefixes=".") & me))

    ubot.add_handler(m(scan_groups_handler, filters.command("scangroups", prefixes=".") & me))
    ubot.add_handler(m(list_groups_handler, filters.command("listgroups", prefixes=".") & me))
    ubot.add_handler(m(jaseball_handler, filters.command("jaseball", prefixes=".") & me))
    ubot.add_handler(m(gcast_handler, filters.command("gcast", prefixes=".") & me))
    ubot.add_handler(m(gucast_handler, filters.command("gucast", prefixes=".") & me))
    ubot.add_handler(m(monitor_group_handler, filters.command("monitor", prefixes=".") & me))
    ubot.add_handler(m(show_logs_handler, filters.command("logs", prefixes=".") & me))
    ubot.add_handler(m(clear_logs_handler, filters.command("clearlogs", prefixes=".") & me))

    ubot.add_handler(m(set_on, filters.command("seton", prefixes=".") & me))
    ubot.add_handler(m(set_off, filters.command("setoff", prefixes=".") & me))
    ubot.add_handler(m(set_reply, filters.command("setreply", prefixes=".") & me))
    ubot.add_handler(m(stop_autoreply_handler, filters.command("stoppm", prefixes=".") & me))
    ubot.add_handler(m(unstop_autoreply_handler, filters.command("unstoppm", prefixes=".") & me))
    ubot.add_handler(m(list_stopped_pm_handler, filters.command("listpm", prefixes=".") & me))
    ubot.add_handler(m(clear_stopped_pm_handler, filters.command("clearpm", prefixes=".") & me))
    ubot.add_handler(m(set_pay_handler, filters.command("setpay", prefixes=".") & me))
    ubot.add_handler(m(del_pay_handler, filters.command("delpay", prefixes=".") & me))
    ubot.add_handler(m(pay_handler, filters.command("pay", prefixes=".") & me))
    ubot.add_handler(m(add_blacklist_handler, filters.command("addbl", prefixes=".") & me))
    ubot.add_handler(m(remove_blacklist_handler, filters.command("offbl", prefixes=".") & me))
    ubot.add_handler(m(list_blacklist_handler, filters.command("listbl", prefixes=".") & me))
    

    ubot.add_handler(m(adzan_handler, filters.command("adzan", prefixes=".") & me))
    ubot.add_handler(m(quran_handler, filters.command("quran", prefixes=".") & me))
    ubot.add_handler(m(jadwal_sholat_handler, filters.command("jadwal", prefixes=".") & me))
    ubot.add_handler(m(doa_handler, filters.command("doa", prefixes=".") & me))
    ubot.add_handler(m(hadits_handler, filters.command("hadits", prefixes=".") & me))
    ubot.add_handler(m(asmaul_husna_handler, filters.command(["asma", "isma"], prefixes=".") & me))
    ubot.add_handler(m(quotes_islami_handler, filters.command(["quotes", "motivasi"], prefixes=".") & me))
    ubot.add_handler(m(kisah_nabi_handler, filters.command("kisah", prefixes=".") & me))
    ubot.add_handler(m(rukun_islam_handler, filters.command(["rukunislam", "rislam"], prefixes=".") & me))
    ubot.add_handler(m(rukun_iman_handler, filters.command(["rukuniman", "riman"], prefixes=".") & me))
    

    ubot.add_handler(m(alkitab_handler, filters.command(["alkitab", "bible"], prefixes=".") & me))
    ubot.add_handler(m(renungan_handler, filters.command("renungan", prefixes=".") & me))
    ubot.add_handler(m(quotes_kristen_handler, filters.command("kquote", prefixes=".") & me))
    ubot.add_handler(m(kidung_handler, filters.command("kidung", prefixes=".") & me))
    ubot.add_handler(m(kisah_rasul_handler, filters.command("rasul", prefixes=".") & me))

    ubot.add_handler(m(gemini_handler, filters.command("gemini", prefixes=".") & me))
    ubot.add_handler(m(gpt_handler, filters.command(["gpt", "chatgpt"], prefixes=".") & me))
    ubot.add_handler(m(claude_handler, filters.command("claude", prefixes=".") & me))
    ubot.add_handler(m(perplexity_handler, filters.command(["pplx", "perplexity"], prefixes=".") & me))

    ubot.add_handler(m(kick_handler, filters.command("kick", prefixes=".") & me))
    ubot.add_handler(m(ban_handler, filters.command("ban", prefixes=".") & me))
    ubot.add_handler(m(mute_handler, filters.command("mute", prefixes=".") & me))
    ubot.add_handler(m(unmute_handler, filters.command("unmute", prefixes=".") & me))
    ubot.add_handler(m(zombie_handler, filters.command("zombie", prefixes=".") & me))
    ubot.add_handler(m(tagall_handler, filters.command("tagall", prefixes=".") & me))

    ubot.add_handler(m(toxic_handler, filters.command("toxic", prefixes=".") & me))
    ubot.add_handler(m(pantun_handler, filters.command("pantun", prefixes=".") & me))
    ubot.add_handler(m(quotes_handler, filters.command("quotes", prefixes=".") & me))
    ubot.add_handler(m(percentage_handler, filters.command(["gay", "lesbi", "ganteng", "cantik", "jelek"], prefixes=".") & me))
    ubot.add_handler(m(siapa_handler, filters.command("siapa", prefixes=".") & me))
    ubot.add_handler(m(dl_handler, filters.command("dl", prefixes=".") & me))
    ubot.add_handler(m(kang_handler, filters.command(["kang", "s", "stiker"], prefixes=".") & me))
    ubot.add_handler(m(toimg_handler, filters.command("toimg", prefixes=".") & me))

    ubot.add_handler(m(set_av_handler, filters.command("av", prefixes=".") & me))
    ubot.add_handler(m(anti_view_once_watcher, filters.private & ~filters.me & (filters.photo | filters.video | filters.voice | filters.video_note)))

    print("[INFO] Installing join/leave handlers...")
    ubot.add_handler(m(new_chat_members_handler, filters.new_chat_members & filters.group))
    ubot.add_handler(m(left_chat_member_handler, filters.left_chat_member & filters.group))

    ubot.add_handler(m(tag_log_handler, (filters.mentioned | filters.reply) & filters.group & ~filters.me))
    ubot.add_handler(m(autoreply_handler, filters.private & ~filters.me & ~filters.bot))

    print("[INFO] Starting background loops...")
    asyncio.create_task(monitor_loop(ubot))

    print("[INFO] All handlers installed successfully!")




