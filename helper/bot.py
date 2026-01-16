import asyncio
import sqlite3
import os
import sys
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded, AuthKeyInvalid, UserDeactivated, SessionRevoked
from userbot.handlers import install_ubot_handlers

API_ID = 31874382
API_HASH = "b9c499220c85a8a51a10c15bf2565e96"
BOT_TOKEN = "8389698571:AAHxIN-uKPvN4S94omKjhi1X_hftDwG-qYM"
OWNER_ID = 7003481257
OWNER_USERNAME = "MAU_BOBO"
DB_PATH = "database/userbot_sessions.db"

class HelperManager:
    def __init__(self):
        self.bot = Client(
            "helper_bot", 
            api_id=API_ID, 
            api_hash=API_HASH, 
            bot_token=BOT_TOKEN, 
            workdir="database",
            ipv6=False,
            sleep_threshold=60,
            max_concurrent_transmissions=1,
            no_updates=False,
            workers=4
        )
        self.active_userbots = {}
        self.user_data = {}
        self.cleanup_task = None

    def init_db(self):
        os.makedirs("database", exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.execute("CREATE TABLE IF NOT EXISTS sessions (phone TEXT PRIMARY KEY, api_id INTEGER, api_hash TEXT, session_string TEXT, expiry_date TEXT, owner_id INTEGER, bot_token TEXT)")
        conn.execute("CREATE TABLE IF NOT EXISTS admins (user_id INTEGER PRIMARY KEY)")
        

        try:
            conn.execute("ALTER TABLE sessions ADD COLUMN bot_token TEXT DEFAULT NULL")
        except:
            pass
            
        conn.commit()
        conn.close()

    def is_admin(self, user_id):
        if user_id == OWNER_ID: return True
        conn = sqlite3.connect(DB_PATH)
        res = conn.execute("SELECT user_id FROM admins WHERE user_id = ?", (user_id,)).fetchone()
        conn.close()
        return True if res else False

    async def start_all_userbots(self):
        conn = sqlite3.connect(DB_PATH)
        try:
            rows = conn.execute("SELECT * FROM sessions").fetchall()
        finally:
            conn.close()
        
        now = datetime.now()
        to_boot = []
        expired_phones = []

        for row in rows:
            # Handle different schema versions safely
            if len(row) == 5:
                phone, aid, ahash, sess, exp = row
                owner_id, bot_token = 0, None
            elif len(row) == 6:
                phone, aid, ahash, sess, exp, owner_id = row
                bot_token = None
            else:
                phone, aid, ahash, sess, exp, owner_id, bot_token = row
            
            try:
                exp_date = datetime.strptime(exp, "%Y-%m-%d")
            except:
                continue

            if now > exp_date:
                expired_phones.append(phone)
                continue
            
            if bot_token and str(bot_token).lower() in ["null", "none"]: 
                bot_token = None
                
            to_boot.append((phone, aid, ahash, sess, bot_token))
        
        # Fast cleanup of expired
        if expired_phones:
            conn = sqlite3.connect(DB_PATH)
            for p in expired_phones:
                conn.execute("DELETE FROM sessions WHERE phone = ?", (p,))
            conn.commit()
            conn.close()

        total = len(to_boot)
        if total == 0:
            print("[INFO] No userbots to start.")
            return

        print(f"[BOOT] Starting {total} userbots in parallel batches...")
        
        BATCH_SIZE = 50
        started = 0
        failed = 0
        
        for i in range(0, total, BATCH_SIZE):
            batch = to_boot[i:i+BATCH_SIZE]
            tasks = [self.boot_userbot(*args) for args in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for res in results:
                if res is True: started += 1
                else: failed += 1
            
            # Concise summary line as requested
            sys.stdout.write(f"\r[BOOT] Status: {started}/{total} online | {failed} failed {' '*10}")
            sys.stdout.flush()
            
            if i + BATCH_SIZE < total:
                await asyncio.sleep(1) # Small pause for OS stability

        print(f"\n[DONE] Kenxi Userbot initialized: {started} active.")
        
        if not self.cleanup_task:
            self.cleanup_task = asyncio.create_task(self.check_expired_sessions())

    async def boot_userbot(self, phone, aid, ahash, sess, bot_token=None):
        try:
            if phone in self.active_userbots:
                try: 
                    old_ubot = self.active_userbots[phone]
                    if hasattr(old_ubot, 'inline_manager'):
                        await old_ubot.inline_manager.stop()
                    await old_ubot.stop()
                    print(f"🔄 Userbot {phone} di-stop sebelum restart.")
                except Exception as e:
                    print(f"⚠️ Gagal stop {phone}: {e}")

            ubot = Client(
                name=f"u_{phone}",
                api_id=aid,
                api_hash=ahash,
                session_string=sess,
                in_memory=True,
                app_version="@MARKET_BABEH",
                device_model="Kenxi Userbot",
                system_version="Gacor",
                ipv6=False,
                sleep_threshold=60,
                max_concurrent_transmissions=1,
                no_updates=False,
                workers=4
            )
            
            pass
            if bot_token:
                try:
                    from userbot.inline import InlineBotManager
                    inline_mgr = InlineBotManager(bot_token, ubot)
                    ubot.inline_manager = inline_mgr
                    await inline_mgr.start()
                except Exception as e:
                    print(f"⚠️ Gagal start Assistant Bot untuk {phone}: {e}")
            
            install_ubot_handlers(ubot)
            await ubot.start()
            self.active_userbots[phone] = ubot
            print(f"✅ Userbot {phone} berhasil di-boot!")
            return True
        except Exception as e:
            print(f"❌ Gagal boot {phone}: {e}")
            return False

    async def stop_userbot(self, phone):
        if phone in self.active_userbots:
            try:
                await self.active_userbots[phone].stop()
                del self.active_userbots[phone]
                print(f"🛑 Userbot {phone} berhasil di-stop.")
                return True
            except Exception as e:
                print(f"❌ Gagal stop userbot {phone}: {e}")
                return False
        return False

    async def check_expired_sessions(self):
        while True:
            try:
                await asyncio.sleep(3600)
                
                conn = sqlite3.connect(DB_PATH)
                try:
                    rows = conn.execute("SELECT phone, expiry_date, owner_id FROM sessions").fetchall()
                except:
                    rows = conn.execute("SELECT phone, expiry_date FROM sessions").fetchall()
                    rows = [(r[0], r[1], 0) for r in rows]
                
                now = datetime.now()
                expired_sessions = []
                
                for phone, exp_str, owner_id in rows:
                    exp_date = datetime.strptime(exp_str, "%Y-%m-%d")
                    if now > exp_date:
                        expired_sessions.append((phone, owner_id))
                
                for phone, owner_id in expired_sessions:
                    print(f"⏰ Session {phone} kadaluarsa, menghapus...")
                    
                    await self.stop_userbot(phone)
                    
                    conn.execute("DELETE FROM sessions WHERE phone = ?", (phone,))
                    conn.commit()
                    
                    try:
                        if owner_id and owner_id != 0:
                            await self.bot.send_message(
                                owner_id,
                                f"⚠️ **NOTIFIKASI KADALUARSA**\n\n"
                                f"Userbot `{phone}` telah kadaluarsa dan dihapus otomatis dari sistem.\n\n"
                                f"Jika ingin menggunakan kembali, silakan login ulang dengan `/add`"
                            )
                    except Exception as e:
                        print(f"⚠️ Gagal kirim notifikasi ke owner {owner_id}: {e}")
                    
                    print(f"✅ Session {phone} berhasil dihapus dari database")
                
                conn.close()
                
            except Exception as e:
                print(f"❌ Error saat check expired sessions: {e}")
                await asyncio.sleep(60)

    def setup_handlers(self):
        @self.bot.on_message(filters.command("start") & filters.private)
        async def start_cmd(c, m):
            uid = m.from_user.id
            
            if not self.is_admin(uid):
                # Ambil foto owner
                photos = []
                async for photo in c.get_chat_photos(OWNER_USERNAME, limit=1):
                    photos.append(photo.file_id)
                
                photo_id = photos[0] if photos else None
                
                caption = (
                    "👋 **Halo! Tertarik dengan Userbot ini?**\n\n"
                    "Ini adalah **Assistant Bot** dari Kenxi Userbot. "
                    "Bot ini Private dan hanya bisa digunakan oleh Owner.\n\n"
                    "💡 **Mau punya Userbot canggih kayak gini?**\n"
                    "Bisa deploy sendiri atau beli jadi (terima beres)!\n\n"
                    "✅ **Fitur Lengkap** (100+ Commands)\n"
                    "✅ **Anti Banned** & **Aman**\n"
                    "✅ **Support Termux & VPS**\n\n"
                    "👇 **Klik tombol di bawah untuk info lengkap:**"
                )
                
                buttons = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🛒 Store", url="https://t.me/MARKET_BABEH"), InlineKeyboardButton("👤 Owner", url=f"https://t.me/{OWNER_USERNAME}")],
                    [InlineKeyboardButton("💰 Pricelist", url="https://t.me/MARKET_BABEH/123"), InlineKeyboardButton("💬 Testimoni", url="https://t.me/TESTI_MARKET_BABEH")]
                ])
                
                if photo_id:
                    return await m.reply_photo(photo_id, caption=caption, reply_markup=buttons)
                else:
                    return await m.reply(caption, reply_markup=buttons, disable_web_page_preview=True)
            
            if uid == OWNER_ID:
                menu = (
                    "🚀 **Kenxi Manager (OWNER)**\n\n"
                    "• `/add` - Login Userbot\n"
                    "• `/cek` - Pantau Semua Userbot\n"
                    "• `/restart` <nomor> - Restart Akun\n"
                    "• `/renew` - Perpanjang Session (Custom Durasi)\n"
                    "• `/delete` <nomor> - Hapus Session Permanent\n"
                    "• `/admin` - Tambah Admin\n"
                    "• `/unadmin` <id> - Hapus Admin\n"
                    "• `/listadmin` - Lihat Daftar Admin"
                )
            else:
                menu = (
                    "🚀 **Kenxi Manager (ADMIN)**\n\n"
                    "• `/add` - Login Userbot Baru\n"
                    "• `/cek` - Cek Status Userbot Saya\n"
                    "• `/restart` <nomor> - Restart Userbot Saya"
                )
            await m.reply(menu)

        @self.bot.on_message(filters.command("promo_admin") & filters.private)
        async def promo_admin_cmd(c, m):
            promo_admin = (
                "👑 **JADI ADMIN KENXI USERBOT - UNTUNG BANGET!** 👑\n\n"
                "Bosan jadi member biasa? Yuk jadi ADMIN aja! 💰\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "🎯 **APA ITU ADMIN KENXI?**\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Admin adalah partner terpercaya yang punya akses untuk:\n"
                "✅ Menjual paket Kenxi Userbot ke member\n"
                "✅ Mendapat KOMISI dari setiap penjualan\n"
                "✅ Support teknis penuh dari Owner\n"
                "✅ Update terbaru tanpa biaya\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "💰 **KEUNTUNGAN JADI ADMIN:**\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "💵 **Komisi Menggiurkan**\n"
                "    └ Setiap penjualan = $ untuk kamu\n"
                "    └ Semakin banyak jual = semakin kaya!\n\n"
                "🎁 **Bonus & Insentif Rutin**\n"
                "    └ Top seller = bonus ekstra\n"
                "    └ Event spesial = reward tambahan\n\n"
                "📈 **Passive Income Potential**\n"
                "    └ Recruit member baru = komisi berlanjut\n"
                "    └ Skalabilitas unlimited\n\n"
                "🤝 **Status & Prestise**\n"
                "    └ Jadi bagian ekosistem Kenxi\n"
                "    └ Network dengan admin lain\n"
                "    └ Community support kuat\n\n"
                "🎓 **Training & Materi Marketing**\n"
                "    └ Template promosi siap pakai\n"
                "    └ Guidance dari Owner\n"
                "    └ Tips & trick selling\n\n"
                "⏰ **Fleksibilitas Waktu**\n"
                "    └ Kerja dari mana saja\n"
                "    └ Jadwal sesuai keinginan kamu\n"
                "    └ Part-time atau full-time\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "📊 **CONTOH EARNING POTENTIAL:**\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Jika setiap paket = Rp 100rb (contoh)\n"
                "Komisi kamu = 20% per penjualan\n\n"
                "💸 1 penjualan/hari = Rp 600rb/bulan\n"
                "💸 5 penjualan/hari = Rp 3jt/bulan\n"
                "💸 10 penjualan/hari = Rp 6jt/bulan\n\n"
                "Passive income = terus jalan! 🚀\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "✨ **SYARAT JADI ADMIN:**\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "✅ Minimal 18 tahun\n"
                "✅ Punya Telegram aktif\n"
                "✅ Komitmen untuk promote Kenxi\n"
                "✅ Punya cara pembayaran (untuk member)\n"
                "✅ Komunikasi lancar dengan Owner\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "🎯 **GIMANA CARA DAFTAR ADMIN?**\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Sangat mudah! Cukup hubungi Owner:\n\n"
                "👉 **@{}**\n\n"
                "Bilang: \"Saya tertarik jadi ADMIN Kenxi\"\n\n"
                "Lalu Owner akan:\n"
                "1️⃣ Jelaskan detail komisi & bonus\n"
                "2️⃣ Training singkat tentang produk\n"
                "3️⃣ Kasih materi marketing siap pakai\n"
                "4️⃣ Aktifasi status admin kamu\n"
                "5️⃣ Mulai earning dari hari pertama!\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "⚡ **KENAPA PILIH KENXI?**\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "🏆 Product terbaik di kelasnya\n"
                "📈 High conversion rate (orang senang beli)\n"
                "💎 Support Owner responsif 24/7\n"
                "🌟 Komunitas admin solid & supportif\n"
                "💪 Growing market = opportunity besar\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "🚀 **JANGAN LEWATKAN KESEMPATAN INI!**\n\n"
                "Slot admin terbatas. Semakin cepat daftar,\n"
                "semakin cepat earning! 💰\n\n"
                "👉 **Hubungi: @{}**\n\n"
                "Admin kami banyak yg already passive income 6 digit! 🔥\n"
                "Ini legit bukan scam, lihat sendiri! 💯"
            ).format(OWNER_USERNAME, OWNER_USERNAME)
            await m.reply(promo_admin)

        @self.bot.on_message(filters.command("admin") & filters.private)
        async def add_admin(c, m):
            if m.from_user.id != OWNER_ID: 
                return await m.reply("❌ Command ini hanya untuk Owner!")
            
            if len(m.command) > 1:
                try:
                    target_id = int(m.command[1])
                except ValueError:
                    return await m.reply("❌ ID harus berupa angka!")
            else:
                self.user_data[m.from_user.id] = {"step": "admin_id"}
                return await m.reply("👤 **Tambah Admin**\n\nMasukkan ID Telegram user yang ingin dijadikan admin:")
            
            try:
                conn = sqlite3.connect(DB_PATH)
                conn.execute("INSERT OR IGNORE INTO admins VALUES (?)", (target_id,))
                conn.commit()
                conn.close()
                await m.reply(f"✅ User `{target_id}` berhasil menjadi Admin (Hanya akses /add).")
                
                try:
                    await c.send_message(
                        target_id, 
                        "🎉 **SELAMAT!** 🎉\n\n"
                        "Akun Anda telah diangkat menjadi **Admin** di bot ini.\n"
                        "Sekarang Anda sudah bisa menggunakan fitur `/add` untuk login userbot.\n\n"
                        "Silakan ketik `/start` untuk melihat menu."
                    )
                except Exception as e:
                    print(f"⚠️ Tidak bisa kirim notifikasi ke {target_id}: {e}")
            except Exception as e:
                await m.reply(f"❌ Terjadi error: {e}")

        @self.bot.on_message(filters.command("unadmin") & filters.private)
        async def del_admin(c, m):
            if m.from_user.id != OWNER_ID: 
                return await m.reply("❌ Command ini hanya untuk Owner!")
            
            try:
                target_id = int(m.command[1])
                
                if target_id == OWNER_ID:
                    return await m.reply("❌ Owner tidak bisa dihapus dari admin!")
                
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.execute("SELECT user_id FROM admins WHERE user_id = ?", (target_id,))
                if not cursor.fetchone():
                    conn.close()
                    return await m.reply(f"❌ User `{target_id}` tidak terdaftar sebagai admin.")
                
                conn.execute("DELETE FROM admins WHERE user_id = ?", (target_id,))
                conn.commit()
                conn.close()
                await m.reply(f"✅ User `{target_id}` dihapus dari Admin.")
                
                try:
                    await c.send_message(
                        target_id, 
                        "⚠️ **PEMBERITAHUAN**\n\n"
                        "Masa jabatan Admin Anda telah berakhir atau dicabut.\n"
                        "Anda tidak lagi memiliki akses ke fitur `/add`.\n\n"
                        "Hubungi Owner jika ada pertanyaan."
                    )
                except Exception as e:
                    print(f"⚠️ Tidak bisa kirim notifikasi ke {target_id}: {e}")
            except (IndexError, ValueError):
                await m.reply("❌ Format salah!\nGunakan: `/unadmin <id_user>`")
            except Exception as e:
                await m.reply(f"❌ Terjadi error: {e}")

        @self.bot.on_message(filters.command("listadmin") & filters.private)
        async def list_admin(c, m):
            if m.from_user.id != OWNER_ID:
                return await m.reply("❌ Command ini hanya untuk Owner!")
            
            conn = sqlite3.connect(DB_PATH)
            admins = conn.execute("SELECT user_id FROM admins").fetchall()
            conn.close()
            
            if not admins:
                return await m.reply("📋 **Daftar Admin:**\n\nBelum ada admin yang terdaftar.")
            
            text = "📋 **Daftar Admin:**\n\n"
            for idx, (admin_id,) in enumerate(admins, 1):
                try:
                    user = await c.get_users(admin_id)
                    name = user.first_name or "Unknown"
                    username = f"@{user.username}" if user.username else "-"
                    text += f"{idx}. **{name}** ({username})\n   ID: `{admin_id}`\n\n"
                except:
                    text += f"{idx}. ID: `{admin_id}` (User tidak ditemukan)\n\n"
            
            await m.reply(text)

        @self.bot.on_message(filters.command("renew") & filters.private)
        async def renew_bot(c, m):
            if m.from_user.id != OWNER_ID: 
                return await m.reply("❌ Command ini hanya untuk Owner!")
            
            if len(m.command) > 1:
                phone = m.command[1]
                days = int(m.command[2]) if len(m.command) > 2 else None
                
                if days:
                    conn = sqlite3.connect(DB_PATH)
                    row = conn.execute("SELECT expiry_date FROM sessions WHERE phone = ?", (phone,)).fetchone()
                    
                    if not row:
                        conn.close()
                        return await m.reply(f"❌ Nomor `{phone}` tidak ditemukan di database.")
                    
                    old_exp = datetime.strptime(row[0], "%Y-%m-%d")
                    base_date = max(datetime.now(), old_exp)
                    new_exp = (base_date + timedelta(days=days)).strftime("%Y-%m-%d")
                    
                    conn.execute("UPDATE sessions SET expiry_date = ? WHERE phone = ?", (new_exp, phone))
                    conn.commit()
                    conn.close()
                    
                    return await m.reply(
                        f"✅ **Berhasil Perpanjang Session!**\n\n"
                        f"📱 Nomor: `{phone}`\n"
                        f"⏰ Ditambah: {days} hari\n"
                        f"📅 Kadaluarsa baru: `{new_exp}`"
                    )
                else:
                    self.user_data[m.from_user.id] = {"step": "renew_days", "phone": phone}
                    return await m.reply("⏰ **Durasi Perpanjangan**\n\nMasukkan jumlah hari yang ingin ditambahkan:")
            else:
                self.user_data[m.from_user.id] = {"step": "renew_phone"}
                return await m.reply("📱 **Perpanjang Session**\n\nMasukkan nomor HP userbot yang ingin diperpanjang:")

        @self.bot.on_message(filters.command("delete") & filters.private)
        async def delete_session(c, m):
            if m.from_user.id != OWNER_ID:
                return await m.reply("❌ Command ini hanya untuk Owner!")
            
            try:
                phone = m.command[1]
                
                conn = sqlite3.connect(DB_PATH)
                row = conn.execute("SELECT phone FROM sessions WHERE phone = ?", (phone,)).fetchone()
                
                if not row:
                    conn.close()
                    return await m.reply(f"❌ Nomor `{phone}` tidak ditemukan di database.")
                
                await self.stop_userbot(phone)
                
                conn.execute("DELETE FROM sessions WHERE phone = ?", (phone,))
                conn.commit()
                conn.close()
                
                await m.reply(
                    f"🗑️ **Session Berhasil Dihapus!**\n\n"
                    f"📱 Nomor: `{phone}`\n"
                    f"✅ Session telah dihapus permanent dari database.\n"
                    f"⚠️ User harus daftar ulang jika ingin menggunakan userbot kembali."
                )
            except IndexError:
                await m.reply("❌ Format salah!\nGunakan: `/delete <nomor>`")
            except Exception as e:
                await m.reply(f"❌ Terjadi error: {e}")

        @self.bot.on_message(filters.command("cek") & filters.private)
        async def check_monitoring(c, m):
            uid = m.from_user.id
            
            if uid == OWNER_ID:
                conn = sqlite3.connect(DB_PATH)
                try:
                    rows = conn.execute("SELECT phone, expiry_date, owner_id FROM sessions").fetchall()
                except:
                    rows = conn.execute("SELECT phone, expiry_date FROM sessions").fetchall()
                    rows = [(r[0], r[1], 0) for r in rows]
                conn.close()
                
                if not rows: 
                    return await m.reply("📊 **Monitoring Userbot:**\n\nDatabase kosong, belum ada session terdaftar.")
                
                text = "📊 **Monitoring Semua Userbot:**\n\n"
                now = datetime.now()
                
                for phone, exp_str, owner_id in rows:
                    exp_date = datetime.strptime(exp_str, "%Y-%m-%d")
                    days_left = (exp_date - now).days
                    
                    if phone in self.active_userbots:
                        status = "🟢 Aktif"
                    else:
                        status = "🔴 Offline"
                    
                    if days_left < 0:
                        status += " (Kadaluarsa)"
                    elif days_left <= 3:
                        status += f" (⚠️ {days_left} hari lagi)"
                    
                    owner_info = f"Owner ID: `{owner_id}`" if owner_id else "Owner: Unknown"
                    
                    text += f"📱 `{phone}`\n"
                    text += f"Status: {status}\n"
                    text += f"Expired: `{exp_str}`\n"
                    text += f"{owner_info}\n\n"
                
                await m.reply(text)
            
            elif self.is_admin(uid):
                conn = sqlite3.connect(DB_PATH)
                try:
                    rows = conn.execute("SELECT phone, expiry_date FROM sessions WHERE owner_id = ?", (uid,)).fetchall()
                except:
                    rows = []
                conn.close()
                
                if not rows:
                    return await m.reply("📊 **Status Userbot Anda:**\n\nAnda belum memiliki userbot yang terdaftar.")
                
                text = "📊 **Status Userbot Anda:**\n\n"
                now = datetime.now()
                
                for phone, exp_str in rows:
                    exp_date = datetime.strptime(exp_str, "%Y-%m-%d")
                    days_left = (exp_date - now).days
                    
                    if phone in self.active_userbots:
                        status = "🟢 Aktif"
                    else:
                        status = "🔴 Offline"
                    
                    if days_left < 0:
                        status += " (Kadaluarsa)"
                    elif days_left <= 3:
                        status += f" (⚠️ {days_left} hari lagi)"
                    
                    text += f"📱 `{phone}`\n"
                    text += f"Status: {status}\n"
                    text += f"Expired: `{exp_str}`\n\n"
                
                await m.reply(text)
            else:
                await m.reply("❌ Command ini hanya untuk Owner & Admin!")

        @self.bot.on_message(filters.command("restart") & filters.private)
        async def restart_spesifik(c, m):
            uid = m.from_user.id
            
            if not self.is_admin(uid):
                return await m.reply("❌ Command ini hanya untuk Owner & Admin!")
            
            if len(m.command) < 2:
                if uid == OWNER_ID:
                    return await m.reply("❌ Format salah!\nGunakan: `/restart <nomor>`")
                else:
                    conn = sqlite3.connect(DB_PATH)
                    try:
                        rows = conn.execute("SELECT phone FROM sessions WHERE owner_id = ?", (uid,)).fetchall()
                    except:
                        rows = []
                    conn.close()
                    
                    if not rows:
                        return await m.reply("❌ Anda belum memiliki userbot yang terdaftar.")
                    
                    text = "📱 **Pilih Userbot untuk Restart:**\n\n"
                    for idx, (phone,) in enumerate(rows, 1):
                        status = "🟢 Aktif" if phone in self.active_userbots else "🔴 Offline"
                        text += f"{idx}. `{phone}` - {status}\n"
                    text += f"\nGunakan: `/restart <nomor>`"
                    return await m.reply(text)
            
            target_phone = m.command[1]
            
            conn = sqlite3.connect(DB_PATH)
            try:
                if uid == OWNER_ID:
                    row = conn.execute("SELECT * FROM sessions WHERE phone = ?", (target_phone,)).fetchone()
                else:
                    row = conn.execute("SELECT * FROM sessions WHERE phone = ? AND owner_id = ?", (target_phone, uid)).fetchone()
            except:
                row = None
            conn.close()
            
            if not row:
                if uid == OWNER_ID:
                    return await m.reply(f"❌ Nomor `{target_phone}` tidak ditemukan di database.")
                else:
                    return await m.reply(f"❌ Nomor `{target_phone}` tidak ditemukan atau bukan milik Anda.")
            
            if len(row) == 5:
                phone, aid, ahash, sess, exp = row
                bot_token = None
            elif len(row) == 6:
                phone, aid, ahash, sess, exp, owner_id = row
                bot_token = None
            else:
                 phone, aid, ahash, sess, exp, owner_id, bot_token = row
            
            exp_date = datetime.strptime(exp, "%Y-%m-%d")
            
            if datetime.now() > exp_date:
                return await m.reply(f"❌ Session `{target_phone}` sudah kadaluarsa!\nGunakan `/renew` untuk memperpanjang (Owner only) atau login ulang dengan `/add`")
            
            await m.reply(f"🔄 Restarting userbot `{target_phone}`...")
            
            if await self.boot_userbot(phone, aid, ahash, sess, bot_token):
                await m.reply(f"✅ Userbot `{target_phone}` berhasil di-restart dan sekarang aktif!")
            else:
                await m.reply(f"❌ Gagal restart userbot `{target_phone}`. Periksa log untuk detail.")

        @self.bot.on_message(filters.command("status") & filters.private)
        async def check_user_status(c, m):
            uid = m.from_user.id
            if not self.is_admin(uid):
                return await m.reply("❌ Anda tidak memiliki akses ke bot ini.")
            
            conn = sqlite3.connect(DB_PATH)
            try:
                rows = conn.execute("SELECT phone, expiry_date FROM sessions WHERE owner_id = ?", (uid,)).fetchall()
            except:
                rows = []
            conn.close()
            
            if not rows:
                return await m.reply("📊 **Status Userbot:**\n\nAnda belum memiliki userbot yang terdaftar.")
            
            text = "📊 **Status Userbot Anda:**\n\n"
            now = datetime.now()
            
            for phone, exp_str in rows:
                exp_date = datetime.strptime(exp_str, "%Y-%m-%d")
                days_left = (exp_date - now).days
                
                if phone in self.active_userbots:
                    status = "🟢 Aktif"
                else:
                    status = "🔴 Offline"
                
                if days_left < 0:
                    status += " (Kadaluarsa)"
                elif days_left <= 3:
                    status += f" (⚠️ {days_left} hari lagi)"
                
                text += f"📱 `{phone}`\n"
                text += f"Status: {status}\n"
                text += f"Expired: `{exp_str}`\n\n"
            
            await m.reply(text)

        @self.bot.on_message(filters.command("add") & filters.private)
        async def add_cmd(c, m):
            if not self.is_admin(m.from_user.id): 
                return await m.reply("❌ Anda tidak memiliki akses untuk menggunakan command ini.")
            
            self.user_data[m.from_user.id] = {"step": "bot_token_start"}
            await m.reply(
                "🤖 **SETUP ASSISTANT BOT - STEP 1**\n\n"
                "kami butuh **Bot Token**.\n"
                "Buat bot baru di @BotFather, lalu kirim tokennya ke sini.\n\n"
            )

        @self.bot.on_message(filters.text & filters.private)
        async def login_flow(c, m):
            uid = m.from_user.id
            if uid not in self.user_data: return
            
            data = self.user_data[uid]
            step, text = data["step"], m.text.strip()
            
            try:
                if step == "bot_token_start":
                    if text.lower() == "/skip":
                        data["bot_token"] = None
                    else:
                        if ":" not in text or len(text) < 20: 
                             return await m.reply("❌ **Token Invalid!**\nFormat salah (harus ada ':').\nKirim token yang benar atau ketik `/skip`.")
                        data["bot_token"] = text
                    
                    data["step"] = "api_id"
                    await m.reply(
                        "🔐 **LOGIN USERBOT - STEP 2**\n\n"
                        "Masukkan **API ID** Anda:\n\n"
                        "ℹ️ Dapatkan API ID & Hash dari: https://my.telegram.org"
                    )
                    return
                
                if step == "admin_id":
                    try:
                        target_id = int(text)
                        conn = sqlite3.connect(DB_PATH)
                        conn.execute("INSERT OR IGNORE INTO admins VALUES (?)", (target_id,))
                        conn.commit()
                        conn.close()
                        await m.reply(f"✅ User `{target_id}` berhasil menjadi Admin (Hanya akses /add).")
                        
                        try:
                            await c.send_message(
                                target_id, 
                                "🎉 **SELAMAT!** 🎉\n\n"
                                "Akun Anda telah diangkat menjadi **Admin** di bot ini.\n"
                                "Sekarang Anda sudah bisa menggunakan fitur `/add` untuk login userbot.\n\n"
                                "Silakan ketik `/start` untuk melihat menu."
                            )
                        except:
                            pass
                        del self.user_data[uid]
                    except ValueError:
                        await m.reply("❌ ID harus berupa angka!\nSilakan kirim ID yang benar:")
                    return
                
                if step == "renew_phone":
                    phone = text
                    conn = sqlite3.connect(DB_PATH)
                    row = conn.execute("SELECT expiry_date FROM sessions WHERE phone = ?", (phone,)).fetchone()
                    
                    if not row:
                        conn.close()
                        await m.reply(f"❌ Nomor `{phone}` tidak ditemukan.\nSilakan masukkan nomor yang benar:")
                        return
                    
                    conn.close()
                    data["phone"] = phone
                    data["step"] = "renew_days"
                    await m.reply("⏰ **Durasi Perpanjangan**\n\nMasukkan jumlah hari yang ingin ditambahkan:")
                    return
                
                if step == "renew_days":
                    try:
                        days = int(text)
                        if days <= 0:
                            await m.reply("❌ Jumlah hari harus lebih dari 0!\nSilakan masukkan angka yang valid:")
                            return
                        
                        phone = data["phone"]
                        conn = sqlite3.connect(DB_PATH)
                        row = conn.execute("SELECT expiry_date FROM sessions WHERE phone = ?", (phone,)).fetchone()
                        
                        old_exp = datetime.strptime(row[0], "%Y-%m-%d")
                        base_date = max(datetime.now(), old_exp)
                        new_exp = (base_date + timedelta(days=days)).strftime("%Y-%m-%d")
                        
                        conn.execute("UPDATE sessions SET expiry_date = ? WHERE phone = ?", (new_exp, phone))
                        conn.commit()
                        conn.close()
                        
                        await m.reply(
                            f"✅ **Berhasil Perpanjang Session!**\n\n"
                            f"📱 Nomor: `{phone}`\n"
                            f"⏰ Ditambah: {days} hari\n"
                            f"📅 Kadaluarsa baru: `{new_exp}`"
                        )
                        del self.user_data[uid]
                    except ValueError:
                        await m.reply("❌ Durasi harus berupa angka!\nSilakan masukkan jumlah hari:")
                    return
                
                if step == "api_id":
                    try:
                        api_id_val = int(text)
                        data.update({"api_id": api_id_val, "step": "api_hash"})
                        await m.reply(
                            "🔐 **LOGIN USERBOT - STEP 3**\n\n"
                            "Masukkan **API HASH** Anda:"
                        )
                    except ValueError:
                        await m.reply("❌ API ID harus berupa angka!\nSilakan kirim ulang API ID yang benar:")
                
                elif step == "api_hash":
                    data.update({"api_hash": text, "step": "phone"})
                    await m.reply(
                        "📱 **LOGIN USERBOT - STEP 4**\n\n"
                        "Masukkan **Nomor HP** dengan format internasional:\n\n"
                        "Contoh: +6281234567890"
                    )
                
                elif step == "phone":
                    data["phone"] = text
                    temp_c = Client(name="temp", api_id=data["api_id"], api_hash=data["api_hash"], in_memory=True)
                    await temp_c.connect()
                    code = await temp_c.send_code(text)
                    data.update({"hash": code.phone_code_hash, "client": temp_c, "step": "code"})
                    await m.reply(
                        "📩 **LOGIN USERBOT - STEP 5**\n\n"
                        "Kode OTP telah dikirim ke akun Telegram Anda.\n"
                        "Masukkan **kode OTP** (contoh: 12345):"
                    )
                
                elif step == "code":
                    try: 
                        await data["client"].sign_in(data["phone"], data["hash"], text.replace(" ", ""))
                    except SessionPasswordNeeded:
                        data["step"] = "2fa"
                        return await m.reply(
                            "🔐 **VERIFIKASI 2FA - STEP 6**\n\n"
                            "Akun Anda dilindungi 2FA.\n"
                            "Masukkan **Password 2FA** Anda:"
                        )
                    await self.finish_login(data, uid, m)
                
                elif step == "2fa":
                    await data["client"].check_password(text)
                    await self.finish_login(data, uid, m)
            
            except Exception as e:
                await m.reply(f"❌ Error: {e}")
                del self.user_data[uid]

    async def finish_login(self, data, uid, m):
        try:
            user = await data["client"].get_me()
            sess = await data["client"].export_session_string()
            await data["client"].disconnect()
            
            exp = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            
            bot_token = data.get("bot_token")
            
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT OR REPLACE INTO sessions (phone, api_id, api_hash, session_string, expiry_date, owner_id, bot_token) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                         (data["phone"], data["api_id"], data["api_hash"], sess, exp, uid, bot_token))
            conn.commit()
            conn.close()
            
            pass
            await self.boot_userbot(data["phone"], data["api_id"], data["api_hash"], sess, bot_token)
            
            token_status = "✅ Assistant Bot Aktif" if bot_token else "⚠️ Assistant Bot Tidak Aktif"
            
            await m.reply(
                f"✅ **LOGIN BERHASIL!**\n\n"
                f"👤 Akun: `{user.first_name}`\n"
                f"📱 Nomor: `{data['phone']}`\n"
                f"📅 Expired: `{exp}` (30 hari)\n"
                f"{token_status}\n\n"
                f"Ketik `.ping` di akun userbot untuk test."
            )
            del self.user_data[uid]
        except Exception as e:
            await m.reply(f"❌ Error saat finish login: {e}")