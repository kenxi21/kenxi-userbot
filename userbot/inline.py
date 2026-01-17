from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent

class InlineBotManager:
    def __init__(self, token, parent_client):
        self.token = token
        self.parent = parent_client 
        self.bot = Client(
            name=f"inline_{token.split(':')[0]}",
            api_id=parent_client.api_id,
            api_hash=parent_client.api_hash,
            bot_token=token,
            in_memory=True
        )
        self.install_handlers()

    async def start(self):
        print(f"[INFO] Starting Inline Bot: {self.token[:10]}...")
        await self.bot.start()

        self.bot_username = (await self.bot.get_me()).username
        self.parent.inline_bot_username = self.bot_username
        print(f"[INFO] Inline Bot Started: @{self.bot_username}")

    async def stop(self):
        await self.bot.stop()

    def get_alive_content(self):
        text = (
            "⚡ **USERBOT STATUS: ON**\n\n"
            "✅ **Sistem:** Normal\n"
            "✅ **Assistant:** Connected\n"
            "🐍 **Python:** 3.9+\n"
            "__Siap melayani Anda, Tuan!__ 😎"
        )
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Store", url="https://t.me/MARKET_BABEH"), InlineKeyboardButton("Support", url="https://t.me/MAU_BOBO")],
            [InlineKeyboardButton("Close", callback_data="close")]
        ])
        return text, markup

    def get_help_p1(self):
        text = (
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📖 **HELP MENU — PAGE 1/3**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "💠 *Silakan jelajahi modul utama kami di bawah ini:*"
        )
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("👨‍💻 OWNER SUPPORT", url="https://t.me/MAU_BOBO")],
            [
                InlineKeyboardButton("🛡️ Admin", callback_data="cat_admin"),
                InlineKeyboardButton("💣 Spam", callback_data="cat_spam")
            ],
            [
                InlineKeyboardButton("🛠️ Tools", callback_data="cat_tools"),
                InlineKeyboardButton("🚀 Utility", callback_data="cat_util")
            ],
            [
                InlineKeyboardButton("❌", callback_data="close"),
                InlineKeyboardButton("➡️", callback_data="help_p2")
            ]
        ])
        return text, markup

    def get_help_p2(self):
        text = (
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📖 **HELP MENU — PAGE 2/3**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "💠 *Fitur hiburan, religi, dan kecerdasan buatan:*"
        )
        markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🕌 Islami", callback_data="cat_islamic"),
                InlineKeyboardButton("✝️ Christian", callback_data="cat_christian")
            ],
            [
                InlineKeyboardButton("🤖 AI Chat", callback_data="cat_ai"),
                InlineKeyboardButton("🎉 Fun Menu", callback_data="cat_fun")
            ],
            [
                InlineKeyboardButton("🎨 Creating", callback_data="cat_creating")
            ],
            [
                InlineKeyboardButton("⬅️", callback_data="help_p1"),
                InlineKeyboardButton("❌", callback_data="close"),
                InlineKeyboardButton("➡️", callback_data="help_p3")
            ]
        ])
        return text, markup

    def get_help_p3(self):
        text = (
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📖 **HELP MENU — PAGE 3/3**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "💠 *Koleksi animasi seru untuk chat Anda:*"
        )
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎬 Anim 1", callback_data="anim_1"), InlineKeyboardButton("🎬 Anim 2", callback_data="anim_2")],
            [InlineKeyboardButton("🎬 Anim 3", callback_data="anim_3"), InlineKeyboardButton("🎬 Anim 4", callback_data="anim_4")],
            [InlineKeyboardButton("🎬 Anim 5", callback_data="anim_5"), InlineKeyboardButton("🎬 Anim 6", callback_data="anim_6")],
            [
                InlineKeyboardButton("⬅️", callback_data="help_p2"),
                InlineKeyboardButton("❌", callback_data="close")
            ]
        ])
        return text, markup

    def get_admin_help(self):
        text = "🛡️ **ADMIN & GRUP FEATURES**\nPilih perintah untuk melihat detailnya:"
        btns = [
            [InlineKeyboardButton("kick", callback_data="cmd_kick"), InlineKeyboardButton("ban", callback_data="cmd_ban")],
            [InlineKeyboardButton("mute", callback_data="cmd_mute"), InlineKeyboardButton("unmute", callback_data="cmd_unmute")],
            [InlineKeyboardButton("zombie", callback_data="cmd_zombie"), InlineKeyboardButton("tagall", callback_data="cmd_tagall")],
            [InlineKeyboardButton("⬅️ Back", callback_data="help_p1")]
        ]
        return text, InlineKeyboardMarkup(btns)

    def get_spam_help(self):
        text = "💣 **SPAM & BROADCAST**\nPilih perintah untuk melihat detailnya:"
        btns = [
            [InlineKeyboardButton("dspam", callback_data="cmd_dspam"), InlineKeyboardButton("gcast", callback_data="cmd_gcast")],
            [InlineKeyboardButton("gucast", callback_data="cmd_gucast"), InlineKeyboardButton("jaseball", callback_data="cmd_jaseball")],
            [InlineKeyboardButton("⬅️ Back", callback_data="help_p1")]
        ]
        return text, InlineKeyboardMarkup(btns)

    def get_ai_help(self):
        text = "🤖 **ARTIFICIAL INTELLIGENCE**\nPilih perintah untuk melihat detailnya:"
        btns = [
            [InlineKeyboardButton("gemini", callback_data="cmd_gemini"), InlineKeyboardButton("gpt", callback_data="cmd_gpt")],
            [InlineKeyboardButton("claude", callback_data="cmd_claude"), InlineKeyboardButton("perplexity", callback_data="cmd_pplx")],
            [InlineKeyboardButton("⬅️ Back", callback_data="help_p2")]
        ]
        return text, InlineKeyboardMarkup(btns)

    def get_fun_help(self):
        text = "🎉 **FUN & GAMES**\nPilih perintah untuk melihat detailnya:"
        btns = [
            [InlineKeyboardButton("toxic", callback_data="cmd_toxic"), InlineKeyboardButton("pantun", callback_data="cmd_pantun")],
            [InlineKeyboardButton("quotes", callback_data="cmd_quotes"), InlineKeyboardButton("siapa", callback_data="cmd_siapa")],
            [InlineKeyboardButton("gay/lesbi/...", callback_data="cmd_perc")],
            [InlineKeyboardButton("⬅️ Back", callback_data="help_p2")]
        ]
        return text, InlineKeyboardMarkup(btns)

    def get_util_help(self):
        text = "🚀 **UTILITY FEATURES**\nPilih perintah untuk melihat detailnya:"
        btns = [
            [InlineKeyboardButton("ping", callback_data="cmd_ping"), InlineKeyboardButton("status", callback_data="cmd_status")],
            [InlineKeyboardButton("help", callback_data="cmd_help")],
            [InlineKeyboardButton("⬅️ Back", callback_data="help_p1")]
        ]
        return text, InlineKeyboardMarkup(btns)

    def get_tools_help(self):
        text = "🛠️ **TOOLS & SYSTEM**\nPilih perintah untuk melihat detailnya:"
        btns = [
            [InlineKeyboardButton("seton", callback_data="cmd_seton"), InlineKeyboardButton("setoff", callback_data="cmd_setoff")],
            [InlineKeyboardButton("setreply", callback_data="cmd_setreply"), InlineKeyboardButton("stoppm", callback_data="cmd_stoppm")],
            [InlineKeyboardButton("addbl", callback_data="cmd_addbl"), InlineKeyboardButton("listbl", callback_data="cmd_listbl")],
            [InlineKeyboardButton("monitor", callback_data="cmd_monitor"), InlineKeyboardButton("scangroups", callback_data="cmd_scangroups")],
            [InlineKeyboardButton("logs", callback_data="cmd_logs"), InlineKeyboardButton("av", callback_data="cmd_av")],
            [InlineKeyboardButton("pay", callback_data="cmd_pay"), InlineKeyboardButton("cekid", callback_data="cmd_cekid")],
            [InlineKeyboardButton("restart", callback_data="cmd_restart"), InlineKeyboardButton("stop", callback_data="cmd_stop")],
            [InlineKeyboardButton("⬅️ Back", callback_data="help_p1")]
        ]
        return text, InlineKeyboardMarkup(btns)

    def get_islamic_help(self):
        text = "🕌 **ISLAMIC FEATURES**\nPilih perintah untuk melihat detailnya:"
        btns = [
            [InlineKeyboardButton("adzan", callback_data="cmd_adzan"), InlineKeyboardButton("quran", callback_data="cmd_quran")],
            [InlineKeyboardButton("jadwal", callback_data="cmd_jadwal"), InlineKeyboardButton("doa", callback_data="cmd_doa")],
            [InlineKeyboardButton("hadits", callback_data="cmd_hadits"), InlineKeyboardButton("asma", callback_data="cmd_asma")],
            [InlineKeyboardButton("quotes", callback_data="cmd_iquote"), InlineKeyboardButton("kisah", callback_data="cmd_kisah")],
            [InlineKeyboardButton("rislam", callback_data="cmd_rislam"), InlineKeyboardButton("riman", callback_data="cmd_riman")],
            [InlineKeyboardButton("⬅️ Back", callback_data="help_p2")]
        ]
        return text, InlineKeyboardMarkup(btns)

    def get_christian_help(self):
        text = "✝️ **CHRISTIAN FEATURES**\nPilih perintah untuk melihat detailnya:"
        btns = [
            [InlineKeyboardButton("alkitab", callback_data="cmd_alkitab"), InlineKeyboardButton("renungan", callback_data="cmd_renungan")],
            [InlineKeyboardButton("kquote", callback_data="cmd_kquote"), InlineKeyboardButton("kidung", callback_data="cmd_kidung")],
            [InlineKeyboardButton("rasul", callback_data="cmd_rasul")],
            [InlineKeyboardButton("⬅️ Back", callback_data="help_p2")]
        ]
        return text, InlineKeyboardMarkup(btns)

    def get_creating_help(self):
        text = "🎨 **CREATING & MEDIA**\nPilih perintah untuk melihat detailnya:"
        btns = [
            [InlineKeyboardButton("dl", callback_data="cmd_dl"), InlineKeyboardButton("kang", callback_data="cmd_kang")],
            [InlineKeyboardButton("stiker", callback_data="cmd_stiker"), InlineKeyboardButton("toimg", callback_data="cmd_toimg")],
            [InlineKeyboardButton("⬅️ Back", callback_data="help_p2")]
        ]
        return text, InlineKeyboardMarkup(btns)

    def back_to(self, target):
        return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data=target)]])

    def install_handlers(self):
        @self.bot.on_inline_query()
        async def inline_handler(client, inline_query):
            query = inline_query.query.lower()
            results = []
            if query == "alive":
                text, markup = self.get_alive_content()
                results.append(InlineQueryResultArticle(title="Alive", input_message_content=InputTextMessageContent(text), reply_markup=markup))
            elif query == "help":
                text, markup = self.get_help_p1()
                results.append(InlineQueryResultArticle(title="Help", input_message_content=InputTextMessageContent(text), reply_markup=markup))
            await inline_query.answer(results=results, cache_time=0)

        @self.bot.on_callback_query()
        async def callback_handler(client, callback_query):
            data = callback_query.data
            user_id = callback_query.from_user.id
            owner_id = self.parent.me.id

            if data == "close":
                if user_id != owner_id:
                    return await callback_query.answer("❌ Hanya pemilik userbot yang bisa menutup menu ini!", show_alert=True)
                await callback_query.edit_message_text("❌ **Menu Ditutup.**")
                return

            # Pages
            elif data == "help_p1":
                text, markup = self.get_help_p1()
                await callback_query.edit_message_text(text, reply_markup=markup)
            elif data == "help_p2":
                text, markup = self.get_help_p2()
                await callback_query.edit_message_text(text, reply_markup=markup)
            elif data == "help_p3":
                text, markup = self.get_help_p3()
                await callback_query.edit_message_text(text, reply_markup=markup)
            
            # Categories
            elif data == "cat_admin":
                text, markup = self.get_admin_help()
                await callback_query.edit_message_text(text, reply_markup=markup)
            elif data == "cat_spam":
                text, markup = self.get_spam_help()
                await callback_query.edit_message_text(text, reply_markup=markup)
            elif data == "cat_ai":
                text, markup = self.get_ai_help()
                await callback_query.edit_message_text(text, reply_markup=markup)
            elif data == "cat_fun":
                text, markup = self.get_fun_help()
                await callback_query.edit_message_text(text, reply_markup=markup)
            elif data == "cat_util":
                text, markup = self.get_util_help()
                await callback_query.edit_message_text(text, reply_markup=markup)
            elif data == "cat_tools":
                text, markup = self.get_tools_help()
                await callback_query.edit_message_text(text, reply_markup=markup)
            elif data == "cat_islamic":
                text, markup = self.get_islamic_help()
                await callback_query.edit_message_text(text, reply_markup=markup)
            elif data == "cat_christian":
                text, markup = self.get_christian_help()
                await callback_query.edit_message_text(text, reply_markup=markup)
            elif data == "cat_creating":
                text, markup = self.get_creating_help()
                await callback_query.edit_message_text(text, reply_markup=markup)

            # Details Mapping
            cmd_map = {
                "cmd_kick": ("🛡️ **KICK**\nFungsi: Mengeluarkan member dari grup.\nFormat: `.kick` (reply ke user)", "cat_admin"),
                "cmd_ban": ("🛡️ **BAN**\nFungsi: Memblokir member dari grup secara permanen.\nFormat: `.ban` (reply ke user)", "cat_admin"),
                "cmd_mute": ("🛡️ **MUTE**\nFungsi: Membisukan member di grup.\nFormat: `.mute` (reply ke user)", "cat_admin"),
                "cmd_unmute": ("🛡️ **UNMUTE**\nFungsi: Mengaktifkan kembali suara member.\nFormat: `.unmute` (reply ke user)", "cat_admin"),
                "cmd_zombie": ("🛡️ **ZOMBIE**\nFungsi: Membersihkan akun terhapus dari grup.\nFormat: `.zombie`", "cat_admin"),
                "cmd_tagall": ("🛡️ **TAG ALL**\nFungsi: Men-tag semua anggota grup.\nFormat: `.tagall [pesan]`", "cat_admin"),
                "cmd_dspam": ("💣 **DSPAM**\nFungsi: Bot akan mengirimkan pesan secara berulang.\nFormat: `.dspam [jumlah] [teks]`", "cat_spam"),
                "cmd_gcast": ("📡 **GCAST**\nFungsi: Mengirim pesan ke semua grup yang diikuti.\nFormat: `.gcast [teks]` (atau reply)", "cat_spam"),
                "cmd_gucast": ("📡 **GUCAST**\nFungsi: Mengirim pesan ke semua chat pribadi.\nFormat: `.gucast [teks]` (atau reply)", "cat_spam"),
                "cmd_jaseball": ("⚾ **JASEBALL**\nFungsi: Broadcast ke grup dengan delay agar aman.\nFormat: `.jaseball [teks]`", "cat_spam"),
                "cmd_gemini": ("🤖 **GEMINI**\nFungsi: Bertanya ke Google Gemini AI.\nFormat: `.gemini [pertanyaan]`", "cat_ai"),
                "cmd_gpt": ("🤖 **CHATGPT**\nFungsi: Bertanya ke OpenAI ChatGPT.\nFormat: `.gpt [pertanyaan]`", "cat_ai"),
                "cmd_claude": ("🤖 **CLAUDE**\nFungsi: Bertanya ke Claude AI.\nFormat: `.claude [pertanyaan]`", "cat_ai"),
                "cmd_pplx": ("🤖 **PERPLEXITY**\nFungsi: Bertanya ke Perplexity AI.\nFormat: `.pplx [pertanyaan]`", "cat_ai"),
                "cmd_toxic": ("🔥 **TOXIC**\nFungsi: Mengeluarkan kata-kata mutiara.\nFormat: `.toxic`", "cat_fun"),
                "cmd_pantun": ("🎑 **PANTUN**\nFungsi: Mengeluarkan pantun random.\nFormat: `.pantun`", "cat_fun"),
                "cmd_quotes": ("💬 **QUOTES**\nFungsi: Mengeluarkan kutipan bijak random.\nFormat: `.quotes`", "cat_fun"),
                "cmd_siapa": ("🤔 **SIAPA**\nFungsi: Menentukan siapa yang dimaksud.\nFormat: `.siapa [teks]`", "cat_fun"),
                "cmd_perc": ("📊 **PERCENTAGE**\nFungsi: Cek persentase gay, ganteng, dll.\nFormat: `.gay` | `.ganteng` | `.jelek`", "cat_fun"),
                "cmd_ping": ("🚀 **PING**\nFungsi: Cek kecepatan respon bot.\nFormat: `.ping`", "cat_util"),
                "cmd_status": ("📊 **STATUS**\nFungsi: Cek status akun userbot Anda.\nFormat: `.status`", "cat_util"),
                "cmd_help": ("📖 **HELP**\nFungsi: Menampilkan menu bantuan ini.\nFormat: `.help`", "cat_util"),
                "cmd_seton": ("🛠️ **SETON**\nFungsi: Mengaktifkan auto-reply.\nFormat: `.seton`", "cat_tools"),
                "cmd_setoff": ("🛠️ **SETOFF**\nFungsi: Mematikan auto-reply.\nFormat: `.setoff`", "cat_tools"),
                "cmd_setreply": ("🛠️ **SETREPLY**\nFungsi: Mengubah pesan auto-reply.\nFormat: `.setreply [teks]`", "cat_tools"),
                "cmd_stoppm": ("🛠️ **STOPPM**\nFungsi: Mematikan auto-reply untuk user tertentu.\nFormat: `.stoppm` (reply)", "cat_tools"),
                "cmd_addbl": ("🛠️ **ADDBL**\nFungsi: Menambah grup ke daftar blacklist broadcast.\nFormat: `.addbl`", "cat_tools"),
                "cmd_listbl": ("🛠️ **LISTBL**\nFungsi: Melihat daftar grup yang di-blacklist.\nFormat: `.listbl`", "cat_tools"),
                "cmd_monitor": ("🛠️ **MONITOR**\nFungsi: Monitoring join/leave grup.\nFormat: `.monitor on/off`", "cat_tools"),
                "cmd_scangroups": ("🛠️ **SCANGROUPS**\nFungsi: Scan semua grup untuk database.\nFormat: `.scangroups`", "cat_tools"),
                "cmd_logs": ("🛠️ **LOGS**\nFungsi: Melihat log aktivitas bot.\nFormat: `.logs [type]`", "cat_tools"),
                "cmd_av": ("🛠️ **AV**\nFungsi: Anti View-Once (maling pap timer).\nFormat: `.av on/off`", "cat_tools"),
                "cmd_pay": ("🛠️ **PAY**\nFungsi: Menampilkan info pembayaran.\nFormat: `.pay`", "cat_tools"),
                "cmd_cekid": ("🛠️ **CEKID**\nFungsi: Cek ID user atau chat.\nFormat: `.cekid`", "cat_tools"),
                "cmd_restart": ("🛠️ **RESTART**\nFungsi: Me-restart akun userbot.\nFormat: `.restart`", "cat_tools"),
                "cmd_stop": ("🛠️ **STOP**\nFungsi: Menghentikan bot sementara.\nFormat: `.stop`", "cat_tools"),
                "cmd_adzan": ("🕌 **ADZAN**\nFungsi: Cek waktu adzan wilayah tertentu.\nFormat: `.adzan [kota]`", "cat_islamic"),
                "cmd_quran": ("🕌 **QURAN**\nFungsi: Mengambil ayat Al-Quran.\nFormat: `.quran [surah]`", "cat_islamic"),
                "cmd_jadwal": ("🕌 **JADWAL**\nFungsi: Cek jadwal sholat hari ini.\nFormat: `.jadwal [kota]`", "cat_islamic"),
                "cmd_doa": ("🕌 **DOA**\nFungsi: Mengambil doa-doa harian.\nFormat: `.doa [nama doa]`", "cat_islamic"),
                "cmd_hadits": ("🕌 **HADITS**\nFungsi: Mengambil hadits random.\nFormat: `.hadits`", "cat_islamic"),
                "cmd_asma": ("🕌 **ASMAUL HUSNA**\nFungsi: Mengambil asmaul husna.\nFormat: `.asma`", "cat_islamic"),
                "cmd_iquote": ("🕌 **ISLAMIC QUOTES**\nFungsi: Kutipan islami penyejuk hati.\nFormat: `.quotes`", "cat_islamic"),
                "cmd_kisah": ("🕌 **KISAH NABI**\nFungsi: Membaca kisah nabi.\nFormat: `.kisah [nabi]`", "cat_islamic"),
                "cmd_rislam": ("🕌 **RUKUN ISLAM**\nFungsi: Menampilkan rukun islam.\nFormat: `.rislam`", "cat_islamic"),
                "cmd_riman": ("🕌 **RUKUN IMAN**\nFungsi: Menampilkan rukun iman.\nFormat: `.riman`", "cat_islamic"),
                "cmd_alkitab": ("✝️ **ALKITAB**\nFungsi: Mengambil ayat Alkitab.\nFormat: `.alkitab [nomer]`", "cat_christian"),
                "cmd_renungan": ("✝️ **RENUNGAN**\nFungsi: Renungan harian Kristen.\nFormat: `.renungan`", "cat_christian"),
                "cmd_kquote": ("✝️ **CHRISTIAN QUOTES**\nFungsi: Kutipan penyemangat Kristen.\nFormat: `.kquote`", "cat_christian"),
                "cmd_kidung": ("✝️ **KIDUNG**\nFungsi: Lirik lagu Kidung Jemaat.\nFormat: `.kidung`", "cat_christian"),
                "cmd_rasul": ("✝️ **KISAH RASUL**\nFungsi: Membaca kisah para rasul.\nFormat: `.rasul`", "cat_christian"),
                "cmd_dl": ("🎨 **DL**\nFungsi: Download video dari link.\nFormat: `.dl [link]`", "cat_creating"),
                "cmd_kang": ("🎨 **KANG**\nFungsi: Menambah stiker ke pack Anda.\nFormat: `.kang` (reply)", "cat_creating"),
                "cmd_stiker": ("🎨 **STIKER**\nFungsi: Membuat stiker dari foto.\nFormat: `.s` | `.stiker` (reply)", "cat_creating"),
                "cmd_toimg": ("🎨 **TOIMG**\nFungsi: Mengubah stiker statis ke foto.\nFormat: `.toimg` (reply)", "cat_creating"),
            }

            if data in cmd_map:
                text, target = cmd_map[data]
                await callback_query.edit_message_text(text, reply_markup=self.back_to(target))

            # Anim Categories
            anim_map = {
                "anim_1": ("🎬 **ANIMASI 1**\n🔹 `.dino` | `.lucu` | `.keren`\n🔹 `.marah` | `.sedih` | `.ketawa`\n🔹 `.heart` | `.loading` | `.moon` | `.clock`", "help_p3"),
                "anim_2": ("🎬 **ANIMASI 2**\n🔹 `.bomb` | `.roket` | `.police`\n🔹 `.pesawat` | `.mobil` | `.motor`\n🔹 `.ufo` | `.hantu` | `.kucing` | `.anjing`", "help_p3"),
                "anim_3": ("🎬 **ANIMASI 3**\n🔹 `.monyet` | `.naga` | `.hujan`\n🔹 `.salju` | `.petir` | `.bumi`\n🔹 `.bintang` | `.api` | `.duit` | `.mabuk`", "help_p3"),
                "anim_4": ("🎬 **ANIMASI 4**\n🔹 `.makan` | `.tinju` | `.bola`\n🔹 `.musik` | `.dance` | `.robot`\n🔹 `.telpon` | `.surat` | `.kunci` | `.kembangapi`", "help_p3"),
                "anim_5": ("🎬 **ANIMASI 5**\n🔹 `.ulangtahun` | `.tidur` | `.ninja`\n🔹 `.uub` | `.pantai` | `.pohon`\n🔹 `.matahari` | `.laut` | `.game` | `.televisi`", "help_p3"),
                "anim_6": ("🎬 **ANIMASI 6**\n🔹 `.tools` | `.microscope` | `.space`\n🔹 `.medical` | `.gym` | `.travel`\n🔹 `.sulap` | `.cuaca` | `.bendera` | `.warna`", "help_p3"),
            }

            if data in anim_map:
                text, target = anim_map[data]
                await callback_query.edit_message_text(text, reply_markup=self.back_to(target))
