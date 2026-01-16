# Help text untuk setiap command individual
HELP_TEXTS = {
    # Basic Commands
    "cmd_ping": "⚡ **PING**\n\nCek latency bot\n\n**Command:** `.ping`\n\n**Output:** Ping response dalam ms",
    
    "cmd_alive": "⚡ **ALIVE**\n\nCek status userbot\n\n**Command:** `.alive`\n\n**Keterangan:** Menampilkan status bot via inline",
    
    "cmd_help": "⚡ **HELP**\n\nMenu bantuan lengkap\n\n**Command:** `.help`\n\n**Keterangan:** Menampilkan semua kategori command",
    
    "cmd_status": "⚡ **STATUS**\n\nInfo profil userbot\n\n**Command:** `.status`\n\n**Keterangan:** Tampilkan info akun, auto-reply, dll",
    
    "cmd_cekid": "⚡ **CEK ID**\n\nCek ID chat/user\n\n**Command:** `.cekid`\n\n**Keterangan:** Tampilkan chat ID dan user ID",
    
    "cmd_stop": "⚡ **STOP**\n\nStop spam/animation\n\n**Command:** `.stop`\n\n**Keterangan:** Hentikan semua proses spam dan animasi",
    
    "cmd_restart": "⚡ **RESTART**\n\nRestart userbot\n\n**Command:** `.restart`\n\n**Keterangan:** Restart bot (Termux compatible)",
    
    # Spam Commands
    "cmd_dspam": "📢 **DELAYED SPAM**\n\n**Command:** `.dspam [delay] [count] [text]`\n\n**Contoh:** `.dspam 1.5 10 Hello World`\n\n**Keterangan:** Spam dengan delay custom per pesan",
    
    "cmd_fwd": "📢 **AUTO FORWARD**\n\n**Command:** `.fwd [delay] [count]`\n\n**Cara 1:** Balas pesan lalu `.fwd 2 10`\n**Cara 2:** `.fwd 2 10 https://t.me/channel/123`\n\n**Keterangan:** Forward pesan dengan delay",
    
    "cmd_scangroups": "📢 **SCAN GROUPS**\n\n**Command:** `.scangroups`\n\n**Keterangan:** Scan dan list semua grup yang diikuti",
    
    "cmd_listgroups": "📢 **LIST GROUPS**\n\n**Command:** `.listgroups`\n\n**Keterangan:** Tampilkan daftar lengkap semua grup dengan ID",
    
    "cmd_jaseball": "📢 **JASEBALL**\n\n**Command:** `.jaseball [pesan]`\n**Test Mode:** `.jaseball test [pesan]`\n\n**Contoh:** `.jaseball Halo semua!`\n\n**Keterangan:** Broadcast ke semua grup dengan delay otomatis",
    
    "cmd_gcast": "📢 **GROUP CAST**\n\n**Command:** `.gcast [pesan]`\n\n**Atau:** Balas media lalu `.gcast`\n\n**Keterangan:** Broadcast ke semua grup (text/media)",
    
    "cmd_gucast": "📢 **USER CAST**\n\n**Command:** `.gucast [pesan]`\n\n**Keterangan:** Broadcast ke semua private chat",
    
    # Admin Commands  
    "cmd_kick": "👮 **KICK USER**\n\n**Command:** `.kick [user]`\n\n**Cara pakai:** Balas pesan user atau `.kick @username`\n\n**Keterangan:** Kick user dari grup",
    
    "cmd_ban": "👮 **BAN USER**\n\n**Command:** `.ban [user]`\n\n**Cara pakai:** Balas pesan user atau `.ban @username`\n\n**Keterangan:** Ban user permanen",
    
    "cmd_mute": "👮 **MUTE USER**\n\n**Command:** `.mute [user]`\n\n**Keterangan:** Mute user (tidak bisa kirim pesan)",
    
    "cmd_unmute": "👮 **UNMUTE USER**\n\n**Command:** `.unmute [user]`\n\n**Keterangan:** Unmute user",
    
    "cmd_zombie": "👮 **ZOMBIE CLEANER**\n\n**Command:** `.zombie`\n\n**Keterangan:** Hapus semua akun deleted dari grup",
    
    "cmd_tagall": "👮 **TAG ALL**\n\n**Command:** `.tagall [pesan]`\n\n**Contoh:** `.tagall Meeting dimulai!`\n\n**Keterangan:** Tag semua member grup (batch 5 per pesan)",
    
    # AI Commands
    "cmd_gemini": "🤖 **GEMINI AI**\n\n**Command:** `.gemini [pertanyaan]`\n\n**Contoh:** `.gemini Jelaskan black hole`\n\n**Keterangan:** AI dari Google untuk berbagai topik",
    
    "cmd_gpt": "🤖 **CHATGPT**\n\n**Command:** `.gpt [pertanyaan]`\n\n**Contoh:** `.gpt Buat kode Python hello world`\n\n**Keterangan:** ChatGPT untuk coding, tanya jawab, dll",
    
    "cmd_claude": "🤖 **CLAUDE AI**\n\n**Command:** `.claude [pertanyaan]`\n\n**Keterangan:** Claude dari Anthropic untuk analisis mendalam",
    
    "cmd_perplexity": "🤖 **PERPLEXITY AI**\n\n**Command:** `.pplx [pertanyaan]`\n\n**Keterangan:** Perplexity AI dengan real-time search",
    
    # Media Commands
    "cmd_dl": "📥 **DOWNLOADER**\n\n**Command:** `.dl [link]`\n\n**Support:**\n- YouTube\n- TikTok  \n- Instagram\n- Twitter/X\n- Facebook\n\n**Contoh:** `.dl https://youtu.be/xxx`",
    
    "cmd_kang": "📥 **KANG STICKER**\n\n**Command:** `.kang` / `.s` / `.stiker`\n\n**Cara pakai:** Balas sticker/foto lalu `.kang`\n\n**Keterangan:** Tambahkan ke sticker pack pribadi",
    
    "cmd_toimg": "📥 **TO IMAGE**\n\n**Command:** `.toimg`\n\n**Cara pakai:** Balas sticker lalu `.toimg`\n\n**Keterangan:** Convert sticker animated/static ke image",
}

# Category menus dengan button per command
CATEGORY_MENUS = {
    "basic": [
        ("⚡ Ping", "cmd_ping"), ("⚡ Alive", "cmd_alive"),
        ("⚡ Help", "cmd_help"), ("⚡ Status", "cmd_status"),
        ("⚡ Cek ID", "cmd_cekid"), ("⚡ Stop", "cmd_stop"),
        ("⚡ Restart", "cmd_restart")
    ],
    
    "spam": [
        ("📢 DSpam", "cmd_dspam"), ("📢 Forward", "cmd_fwd"),
        ("📢 Scan Groups", "cmd_scangroups"), ("📢 List Groups", "cmd_listgroups"),
        ("📢 Jaseball", "cmd_jaseball"), ("📢 GCast", "cmd_gcast"),
        ("📢 GUCast", "cmd_gucast")
    ],
    
    "admin": [
        ("👮 Kick", "cmd_kick"), ("👮 Ban", "cmd_ban"),
        ("👮 Mute", "cmd_mute"), ("👮 Unmute", "cmd_unmute"),
        ("👮 Zombie", "cmd_zombie"), ("👮 TagAll", "cmd_tagall")
    ],
    
    "ai": [
        ("🤖 Gemini", "cmd_gemini"), ("🤖 ChatGPT", "cmd_gpt"),
        ("🤖 Claude", "cmd_claude"), ("🤖 Perplexity", "cmd_perplexity")
    ],
    
    "media": [
        ("📥 Download", "cmd_dl"), ("📥 Kang", "cmd_kang"),
        ("📥 To Image", "cmd_toimg")
    ],
    
    "anim": [
        ("🎭 Anim 1", "anim_1"), ("🎭 Anim 2", "anim_2"),
        ("🎭 Anim 3", "anim_3"), ("🎭 Anim 4", "anim_4"),
        ("🎭 Anim 5", "anim_5"), ("🎭 Anim 6", "anim_6")
    ]
}

# Animation groups
ANIM_GROUPS = {
    "anim_1": "🎭 **ANIMATIONS 1 - Emoji**\n\n`.dino` `.lucu` `.keren` `.marah` `.sedih` `.ketawa` `.heart` `.loading` `.moon` `.clock`",
    
    "anim_2": "🎭 **ANIMATIONS 2 - Transport**\n\n`.bomb` `.roket` `.police` `.pesawat` `.mobil` `.motor` `.ufo`",
    
    "anim_3": "🎭 **ANIMATIONS 3 - Animal**\n\n`.hantu` `.kucing` `.anjing` `.monyet` `.naga`",
    
    "anim_4": "🎭 **ANIMATIONS 4 - Weather & Nature**\n\n`.hujan` `.salju` `.petir` `.bumi` `.bintang` `.api` `.pantai` `.pohon` `.matahari` `.laut`",
    
    "anim_5": "🎭 **ANIMATIONS 5 - Fun & Food**\n\n`.duit` `.mabuk` `.makan` `.tinju` `.bola` `.musik` `.dance` `.tidur` `.ninja` `.uub`",
    
    "anim_6": "🎭 **ANIMATIONS 6 - Tech & Misc**\n\n`.robot` `.telpon` `.surat` `.kunci` `.kembangapi` `.ulangtahun` `.game` `.televisi` `.tools` `.microscope` `.space` `.medical` `.gym` `.travel` `.sulap` `.cuaca` `.bendera` `.warna`"
}
