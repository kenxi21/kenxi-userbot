from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
from userbot.help_texts import HELP_TEXTS, CATEGORY_MENUS, ANIM_GROUPS

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
    
    def create_category_menu(self, category_name, commands_list):
        buttons = []
        row = []
        for label, callback in commands_list:
            row.append(InlineKeyboardButton(label, callback_data=callback))
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)
        
        buttons.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")])
        buttons.append([InlineKeyboardButton("❌ Close", callback_data="close")])
        
        return InlineKeyboardMarkup(buttons)

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

    def get_help_content(self):
        text = (
            "📚 **KENXI USERBOT - HELP MENU**\n\n"
            "Pilih kategori untuk melihat command:\n"
            f"Total: **100+ Commands**"
        )
        markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⚡ Basic", callback_data="help_basic"),
                InlineKeyboardButton("📢 Spam", callback_data="help_spam")
            ],
            [
                InlineKeyboardButton("🎭 Animations", callback_data="help_anim"),
                InlineKeyboardButton("👮 Admin", callback_data="help_admin")
            ],
            [
                InlineKeyboardButton("🕌 Islamic", callback_data="help_islamic"),
                InlineKeyboardButton("✝️ Christian", callback_data="help_christian")
            ],
            [
                InlineKeyboardButton("🤖 AI", callback_data="help_ai"),
                InlineKeyboardButton("🎮 Fun", callback_data="help_fun")
            ],
            [
                InlineKeyboardButton("📥 Media", callback_data="help_media"),
                InlineKeyboardButton("⚙️ Settings", callback_data="help_settings")
            ],
            [
                InlineKeyboardButton("❌ Close", callback_data="close")
            ]
        ])
        return text, markup

    def get_ai_help_content(self):
        text = (
            "📖 **KENXI USERBOT HELP MENU (Pag. 2)**\n\n"
            "Fitur Artificial Intelligence (AI):"
        )
        markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🤖 Gemini", callback_data="help_ai_gemini"),
                InlineKeyboardButton("🤖 ChatGPT", callback_data="help_ai_gpt")
            ],
            [
                InlineKeyboardButton("🤖 Claude", callback_data="help_ai_claude"),
                InlineKeyboardButton("🤖 Perplexity", callback_data="help_ai_pplx")
            ],
            [
                InlineKeyboardButton("⬅️", callback_data="help_back"),
                InlineKeyboardButton("❌", callback_data="close"),
                InlineKeyboardButton("➡️", callback_data="help_next2")
            ]
        ])
        return text, markup

    def get_extra_help_content(self):
        text = (
            "📖 **KENXI USERBOT HELP MENU (Pag. 3)**\n\n"
            "Fitur tambahan dan hiburan:"
        )
        markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🚀 Utility", callback_data="help_util"),
                InlineKeyboardButton("🎉 Fun", callback_data="help_fun")
            ],
            [
                InlineKeyboardButton("🕌 Islami", callback_data="help_islamic"),
                InlineKeyboardButton("✝️ Kristiani", callback_data="help_christian")
            ],
            [
                InlineKeyboardButton("⬅️", callback_data="help_back2"),
                InlineKeyboardButton("❌", callback_data="close"),
                InlineKeyboardButton("➡️", callback_data="help_next3")
            ]
        ])
        return text, markup

    def get_anim_p1_help_content(self):
        text = (
            "📖 **KENXI USERBOT HELP MENU (Pag. 4)**\n\n"
            "Animasi & Desain (Bagian 1):"
        )
        markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎬 Anim 1", callback_data="help_anim_1"),
                InlineKeyboardButton("🎬 Anim 2", callback_data="help_anim_2")
            ],
            [
                InlineKeyboardButton("🎬 Anim 3", callback_data="help_anim_3"),
                InlineKeyboardButton("🎨 Creating", callback_data="help_creating")
            ],
            [
                InlineKeyboardButton("⬅️", callback_data="help_back3"),
                InlineKeyboardButton("❌", callback_data="close"),
                InlineKeyboardButton("➡️", callback_data="help_next4")
            ]
        ])
        return text, markup

    def get_anim_p2_help_content(self):
        text = (
            "📖 **KENXI USERBOT HELP MENU (Pag. 5)**\n\n"
            "Koleksi animasi (Bagian 2):"
        )
        markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎬 Anim 4", callback_data="help_anim_4"),
                InlineKeyboardButton("🎬 Anim 5", callback_data="help_anim_5")
            ],
            [
                InlineKeyboardButton("🎬 Anim 6", callback_data="help_anim_6")
            ],
            [
                InlineKeyboardButton("⬅️", callback_data="help_back4"),
                InlineKeyboardButton("❌", callback_data="close")
            ]
        ])
        return text, markup

    async def send_alive_msg(self, chat_id):
        text, markup = self.get_alive_content()
        await self.bot.send_message(chat_id, text, reply_markup=markup)

    async def send_help_msg(self, chat_id):
        text, markup = self.get_help_content()
        await self.bot.send_message(chat_id, text, reply_markup=markup)

    def install_handlers(self):
        @self.bot.on_inline_query()
        async def inline_handler(client, inline_query):
            query = inline_query.query.lower()
            results = []
            
            if query == "alive":
                text, markup = self.get_alive_content()
                results.append(
                    InlineQueryResultArticle(
                        title="Alive Check",
                        description="Status Userbot & Assistant",
                        input_message_content=InputTextMessageContent(text),
                        reply_markup=markup
                    )
                )

            elif query == "help":
                text, markup = self.get_help_content()
                results.append(
                    InlineQueryResultArticle(
                        title="Help Menu",
                        description="Buka Menu Bantuan Lengkap",
                        input_message_content=InputTextMessageContent(text),
                        reply_markup=markup
                    )
                )
            
            await inline_query.answer(results=results, cache_time=0)

        @self.bot.on_callback_query()
        async def callback_handler(client, callback_query):
            data = callback_query.data
            
            if data == "close":
                try:
                    await callback_query.edit_message_text("❌ **Menu Ditutup.**", reply_markup=None)
                except:
                    pass
                return
            
            if data == "back_to_main":
                text, markup = self.get_help_content()
                await callback_query.edit_message_text(text, reply_markup=markup)
                return
            
            if data == "help_basic":
                text = "⚡ **BASIC COMMANDS**\n\nPilih command untuk detail:"
                markup = self.create_category_menu("basic", CATEGORY_MENUS["basic"])
                await callback_query.edit_message_text(text, reply_markup=markup)
                return
            
            if data == "help_spam":
                text = "📢 **SPAM & BROADCAST**\n\nPilih command untuk detail:"
                markup = self.create_category_menu("spam", CATEGORY_MENUS["spam"])
                await callback_query.edit_message_text(text, reply_markup=markup)
                return
            
            if data == "help_admin":
                text = "👮 **GROUP ADMIN**\n\nPilih command untuk detail:"
                markup = self.create_category_menu("admin", CATEGORY_MENUS["admin"])
                await callback_query.edit_message_text(text, reply_markup=markup)
                return
            
            if data == "help_ai":
                text = "🤖 **AI FEATURES**\n\nPilih AI model:"
                markup = self.create_category_menu("ai", CATEGORY_MENUS["ai"])
                await callback_query.edit_message_text(text, reply_markup=markup)
                return
            
            if data == "help_media":
                text = "📥 **MEDIA COMMANDS**\n\nPilih command untuk detail:"
                markup = self.create_category_menu("media", CATEGORY_MENUS["media"])
                await callback_query.edit_message_text(text, reply_markup=markup)
                return
            
            if data == "help_anim":
                text = "🎭 **ANIMATIONS (56 total!)**\n\nPilih grup animasi:"
                markup = self.create_category_menu("anim", CATEGORY_MENUS["anim"])
                await callback_query.edit_message_text(text, reply_markup=markup)
                return
            
            if data.startswith("cmd_"):
                if data in HELP_TEXTS:
                    back_button = InlineKeyboardMarkup([
                        [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")],
                        [InlineKeyboardButton("❌ Close", callback_data="close")]
                    ])
                    await callback_query.edit_message_text(HELP_TEXTS[data], reply_markup=back_button)
                return
            
            if data.startswith("anim_"):
                if data in ANIM_GROUPS:
                    back_button = InlineKeyboardMarkup([
                        [InlineKeyboardButton("⬅️ Back to Animations", callback_data="help_anim")],
                        [InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")],
                        [InlineKeyboardButton("❌ Close", callback_data="close")]
                    ])
                    await callback_query.edit_message_text(ANIM_GROUPS[data], reply_markup=back_button)
                return
            
            if data == "help_islamic":
                text = (
                    "🕌 **ISLAMIC FEATURES**\n\n"
                    "`.adzan [kota]` - Jadwal sholat\n"
                    "`.quran [surat] [ayat]` - Baca Quran\n"
                    "`.doa [keyword]` - Doa harian\n"
                    "`.hadits` - Hadits random\n"
                    "`.asma` - Asmaul Husna\n"
                    "`.quotes` - Quotes Islami\n"
                    "`.kisah [nabi]` - Kisah Nabi\n"
                    "`.rukunislam` - Rukun Islam\n"
                    "`.rukuniman` - Rukun Iman"
                )
                back_button = InlineKeyboardMarkup([
                    [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")],
                    [InlineKeyboardButton("❌ Close", callback_data="close")]
                ])
                await callback_query.edit_message_text(text, reply_markup=back_button)
                return
            
            if data == "help_christian":
                text = (
                    "✝️ **CHRISTIAN FEATURES**\n\n"
                    "`.alkitab [kitab pasal:ayat]` - Baca Alkitab\n"
                    "`.bible` - Alias alkitab\n"
                    "`.renungan` - Renungan harian\n"
                    "`.kquote` - Quotes Kristen\n"
                    "`.kidung [nomor]` - Kidung Jemaat\n"
                    "`.rasul [nama]` - Kisah Rasul"
                )
                back_button = InlineKeyboardMarkup([
                    [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")],
                    [InlineKeyboardButton("❌ Close", callback_data="close")]
                ])
                await callback_query.edit_message_text(text, reply_markup=back_button)
                return
            
            if data == "help_fun":
                text = (
                    "🎮 **FUN COMMANDS**\n\n"
                    "`.toxic` - Random toxic text\n"
                    "`.pantun` - Random pantun\n"
                    "`.quotes` - Random quotes\n\n"
                    "**Percentage Check:**\n"
                    "`.gay` `.lesbi` `.ganteng` `.cantik` `.jelek`\n\n"
                    "`.siapa [pertanyaan]` - Random member"
                )
                back_button = InlineKeyboardMarkup([
                    [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")],
                    [InlineKeyboardButton("❌ Close", callback_data="close")]
                ])
                await callback_query.edit_message_text(text, reply_markup=back_button)
                return
            
            if data == "help_settings":
                text = (
                    "⚙️ **SETTINGS & MANAGEMENT**\n\n"
                    "**Auto-Reply:**\n"
                    "`.seton` `.setoff` `.setreply [text]`\n"
                    "`.stoppm` `.unstoppm` `.listpm`\n\n"
                    "**Monitoring:**\n"
                    "`.monitor [on/off]` `.logs` `.clearlogs`\n\n"
                    "**Anti View-Once:**\n"
                    "`.av on` `.av off`\n\n"
                    "**Payment:**\n"
                    "`.setpay` `.delpay` `.pay`\n\n"
                    "**Blacklist:**\n"
                    "`.addbl` `.offbl` `.listbl`"
                )
                back_button = InlineKeyboardMarkup([
                    [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")],
                    [InlineKeyboardButton("❌ Close", callback_data="close")]
                ])
                await callback_query.edit_message_text(text, reply_markup=back_button)
                return
            data = callback_query.data
            
            if data == "close":
                try:
                    await callback_query.edit_message_text("❌ **Menu Ditutup.**", reply_markup=None)
                except:
                    pass
            
            elif data == "help_next":
                text, markup = self.get_ai_help_content()
                await callback_query.edit_message_text(text, reply_markup=markup)

            elif data == "help_back":
                text, markup = self.get_help_content()
                await callback_query.edit_message_text(text, reply_markup=markup)

            elif data == "help_next2":
                text, markup = self.get_extra_help_content()
                await callback_query.edit_message_text(text, reply_markup=markup)

            elif data == "help_back2":
                text, markup = self.get_ai_help_content()
                await callback_query.edit_message_text(text, reply_markup=markup)

            elif data == "help_next3":
                text, markup = self.get_anim_p1_help_content()
                await callback_query.edit_message_text(text, reply_markup=markup)

            elif data == "help_back3":
                text, markup = self.get_extra_help_content()
                await callback_query.edit_message_text(text, reply_markup=markup)

            elif data == "help_next4":
                text, markup = self.get_anim_p2_help_content()
                await callback_query.edit_message_text(text, reply_markup=markup)

            elif data == "help_back4":
                text, markup = self.get_anim_p1_help_content()
                await callback_query.edit_message_text(text, reply_markup=markup)

            elif data == "help_ai_gemini":
                text = (
                    "🤖 **GEMINI AI**\n\n"
                    "AI canggih dari Google untuk tanya jawab, coding, dan analisis teks.\n\n"
                    "🔹 **Perintah:** `.gemini [pertanyaan]`\n\n"
                    "🔹 **Contoh:** `.gemini Apa itu black hole?`"
                )
                await callback_query.edit_message_text(text, reply_markup=self.back_to_p2())

            elif data == "help_ai_gpt":
                text = (
                    "🤖 **CHATGPT**\n\n"
                    "Model bahasa populer dari OpenAI untuk asisten percakapan.\n\n"
                    "🔹 **Perintah:** `.gpt [pertanyaan]`\n\n"
                    "🔹 **Contoh:** `.gpt buatkan puisi cinta`"
                )
                await callback_query.edit_message_text(text, reply_markup=self.back_to_p2())

            elif data == "help_ai_claude":
                text = (
                    "🤖 **CLAUDE AI**\n\n"
                    "AI dari Anthropic yang dikenal lebih aman dan bernuansa alami.\n\n"
                    "🔹 **Perintah:** `.claude [pertanyaan]`\n\n"
                    "🔹 **Contoh:** `.claude ringkas teks ini: [teks]`"
                )
                await callback_query.edit_message_text(text, reply_markup=self.back_to_p2())

            elif data == "help_ai_pplx":
                text = (
                    "🤖 **PERPLEXITY AI**\n\n"
                    "AI yang fokus pada pencarian informasi real-time dengan sumber terpercaya.\n\n"
                    "🔹 **Perintah:** `.pplx [pertanyaan]`\n\n"
                    "🔹 **Contoh:** `.pplx berita terbaru hari ini`"
                )
                await callback_query.edit_message_text(text, reply_markup=self.back_to_p2())

            elif data == "help_anim_1":
                text = (
                    "🎬 **ANIMASI KATEGORI 1**\n\n"
                    "🔹 `.dino` | `.lucu` | `.keren`\n"
                    "🔹 `.marah` | `.sedih` | `.ketawa`\n"
                    "🔹 `.heart` | `.loading` | `.moon` | `.clock`"
                )
                await callback_query.edit_message_text(text, reply_markup=self.back_to_p4())

            elif data == "help_anim_2":
                text = (
                    "🎬 **ANIMASI KATEGORI 2**\n\n"
                    "🔹 `.bomb` | `.roket` | `.police`\n"
                    "🔹 `.pesawat` | `.mobil` | `.motor`\n"
                    "🔹 `.ufo` | `.hantu` | `.kucing` | `.anjing`"
                )
                await callback_query.edit_message_text(text, reply_markup=self.back_to_p4())

            elif data == "help_anim_3":
                text = (
                    "🎬 **ANIMASI KATEGORI 3**\n\n"
                    "🔹 `.monyet` | `.naga` | `.hujan`\n"
                    "🔹 `.salju` | `.petir` | `.bumi`\n"
                    "🔹 `.bintang` | `.api` | `.duit` | `.mabuk`"
                )
                await callback_query.edit_message_text(text, reply_markup=self.back_to_p4())

            elif data == "help_anim_4":
                text = (
                    "🎬 **ANIMASI KATEGORI 4**\n\n"
                    "🔹 `.makan` | `.tinju` | `.bola`\n"
                    "🔹 `.musik` | `.dance` | `.robot`\n"
                    "🔹 `.telpon` | `.surat` | `.kunci` | `.kembangapi`"
                )
                await callback_query.edit_message_text(text, reply_markup=self.back_to_p4())

            elif data == "help_anim_5":
                text = (
                    "🎬 **ANIMASI KATEGORI 5**\n\n"
                    "🔹 `.ulangtahun` | `.tidur` | `.ninja`\n"
                    "🔹 `.uub` | `.pantai` | `.pohon`\n"
                    "🔹 `.matahari` | `.laut` | `.game` | `.televisi`"
                )
                await callback_query.edit_message_text(text, reply_markup=self.back_to_p5())

            elif data == "help_anim_6":
                text = (
                    "🎬 **ANIMASI KATEGORI 6**\n\n"
                    "🔹 `.tools` | `.microscope` | `.space`\n"
                    "🔹 `.medical` | `.gym` | `.travel`\n"
                    "🔹 `.sulap` | `.cuaca` | `.bendera` | `.warna`"
                )
                await callback_query.edit_message_text(text, reply_markup=self.back_to_p5())

            elif data == "help_islamic":
                text = (
                    "🕌 **FITUR ISLAMI**\n\n"
                    "🔹 `.adzan` | `.quran` | `.jadwal`\n"
                    "🔹 `.doa` | `.hadits` | `.asma`\n"
                    "🔹 `.quotes` | `.kisah` | `.rislam` | `.riman`"
                )
                await callback_query.edit_message_text(text, reply_markup=self.back_to_p3())

            elif data == "help_christian":
                text = (
                    "✝️ **FITUR KRISTIANI**\n\n"
                    "🔹 `.alkitab` | `.renungan` | `.kquote`\n"
                    "🔹 `.kidung` | `.rasul`"
                )
                await callback_query.edit_message_text(text, reply_markup=self.back_to_p3())

            elif data == "help_admin":
                text = (
                    "🛡️ **FITUR ADMIN & GRUP**\n\n"
                    "🔹 `.kick` | `.ban` | `.mute` | `.unmute`\n"
                    "🔹 `.zombie` | `.tagall`"
                )
                await callback_query.edit_message_text(text, reply_markup=self.back_to_p1())

            elif data == "help_fun":
                text = (
                    "🎉 **FITUR HIBURAN (FUN)**\n\n"
                    "🔹 `.toxic` | `.pantun` | `.quotes` | `.siapa`\n"
                    "🔹 `.gay` | `.lesbi` | `.ganteng` | `.cantik` | `.jelek`"
                )
                await callback_query.edit_message_text(text, reply_markup=self.back_to_p3())

            elif data == "help_creating":
                text = (
                    "🎨 **CREATING & DOWNLOADING**\n\n"
                    "🔹 `.dl [link]` | `.kang` | `.toimg`"
                )
                await callback_query.edit_message_text(text, reply_markup=self.back_to_p4())

            elif data == "help_spam":
                text = (
                    "💣 **MENU SPAM**\n\n"
                    "🔹 `.dspam` | `.gcast` | `.gucast` | `.jaseball`"
                )
                await callback_query.edit_message_text(text, reply_markup=self.back_button())

            elif data == "help_tools":
                text = (
                    "🛠️ **FITUR TOOLS & LAINNYA**\n\n"
                    "🔹 `.seton` | `.setoff` | `.setreply` | `.stoppm`\n"
                    "🔹 `.addbl` | `.listbl` | `.monitor` | `.scangroups`\n"
                    "🔹 `.logs` | `.av` | `.pay` | `.cekid` | `.restart` | `.stop`"
                )
                await callback_query.edit_message_text(text, reply_markup=self.back_button())

            elif data == "help_util":
                text = (
                    "🚀 **UTILITY FEATURES**\n\n"
                    "🔹 `.ping` | `.status` | `.help`"
                )
                await callback_query.edit_message_text(text, reply_markup=self.back_to_p3())

    def back_button(self):
        return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️", callback_data="help_back")]])

    def back_to_p1(self):
        return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️", callback_data="help_back")]])

    def back_to_p2(self):
        return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️", callback_data="help_next")]])

    def back_to_p3(self):
        return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️", callback_data="help_next2")]])

    def back_to_p4(self):
        return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️", callback_data="help_next3")]])

    def back_to_p5(self):
        return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️", callback_data="help_next4")]])
