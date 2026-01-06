import aiohttp
import asyncio
from pyrogram import filters
from datetime import datetime

async def get_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try:
                return await response.json()
            except Exception as e:
                return None

async def adzan_handler(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ **Gunakan:** `.adzan [nama kota]`\nContoh: `.adzan Jakarta`")

    kota = message.text.split(None, 1)[1]
    await message.edit(f"🔍 **Mencari jadwal sholat untuk:** `{kota}`...")

    url = f"http://api.aladhan.com/v1/timingsByCity?city={kota}&country=Indonesia&method=11"
    
    data = await get_json(url)
    
    if not data or data.get('code') != 200:
        return await message.edit(f"❌ **Kota tidak ditemukan!**\nCoba nama kota lain (misal: Jakarta, Surabaya, Bandung)")

    timings = data['data']['timings']
    date = data['data']['date']['readable']
    hijri = data['data']['date']['hijri']
    
    text = (
        f"🕌 **JADWAL SHOLAT**\n"
        f"📍 **Kota:** {kota.title()}\n"
        f"📅 **Tanggal:** {date}\n"
        f"🗓 **Hijriyah:** {hijri['day']} {hijri['month']['en']} {hijri['year']}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🤲 **Imsak:** `{timings['Imsak']}`\n"
        f"🌅 **Subuh:** `{timings['Fajr']}`\n"
        f"🌄 **Terbit:** `{timings['Sunrise']}`\n"
        f"🌞 **Dzuhur:** `{timings['Dhuhr']}`\n"
        f"🌤 **Ashar:** `{timings['Asr']}`\n"
        f"🌇 **Maghrib:** `{timings['Maghrib']}`\n"
        f"🌙 **Isya:** `{timings['Isha']}`\n"
        f"━━━━━━━━━━━━━━━━━━"
    )
    
    await message.edit(text)

async def quran_handler(client, message):
    if len(message.command) < 3:
        return await message.edit("❌ **Gunakan:** `.quran [nomor surat] [nomor ayat]`\nContoh: `.quran 1 1` (Al-Fatihah ayat 1)")

    try:
        surah = int(message.command[1])
        ayah = int(message.command[2])
    except ValueError:
        return await message.edit("❌ **Nomor surat dan ayat harus angka!**")

    await message.edit(f"📖 **Mencari Surat ke-{surah} Ayat {ayah}...**")

    url = f"http://api.alquran.cloud/v1/ayah/{surah}:{ayah}/id.indonesian"
    url_ar = f"http://api.alquran.cloud/v1/ayah/{surah}:{ayah}"
    
    data = await get_json(url)
    data_ar = await get_json(url_ar)
    
    if not data or data.get('code') != 200:
        return await message.edit("❌ **Ayat tidak ditemukan!**\nPastikan nomor surat dan ayat benar.")

    text_ar = data_ar['data']['text']
    text_id = data['data']['text']
    surah_name = data['data']['surah']['englishName']
    surah_name_ar = data['data']['surah']['name']
    
    result = (
        f"📖 **AL-QUR'AN**\n"
        f"☪️ **{surah_name} ({surah_name_ar}) : {ayah}**\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"**ٱلسَّلَامُ عَلَيْكُمْ**\n\n"
        f"{text_ar}\n\n"
        f"**Artinya:**\n_{text_id}_"
    )
    
    await message.edit(result)

async def jadwal_sholat_handler(client, message):
    await adzan_handler(client, message)

async def doa_handler(client, message):
    cmd = message.command
    await message.edit("🔄 **Memuat Doa...**")
    
    url = "https://doa-doa-api-ahmadramadhan.fly.dev/api"
    data = await get_json(url)
    
    if not data:
        return await message.edit("❌ **Gagal mengambil data doa.**")

    target_doa = None
    
    if len(cmd) > 1:
        keyword = " ".join(cmd[1:]).lower()
        results = [d for d in data if keyword in d['doa'].lower()]
        if results:
            target_doa = results[0]
        else:
            return await message.edit(f"❌ **Doa tidak ditemukan untuk kata kunci:** `{keyword}`")
    else:
        import random
        target_doa = random.choice(data)

    if target_doa:
        result = (
            f"🤲 **DOA HARIAN**\n"
            f"📜 **Judul:** {target_doa['doa']}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"{target_doa['ayat']}\n\n"
            f"**Latin:** {target_doa['latin']}\n\n"
            f"**Artinya:**\n_{target_doa['artinya']}_"
        )
        await message.edit(result)

async def hadits_handler(client, message):
    await message.edit("🔄 **Memuat Hadits...**")
    

    import random
    book = random.choice(books)
    
    
    range_start = random.randint(1, 2000)
    range_end = range_start + 1
    url = f"https://api.hadith.gading.dev/books/{book}?range={range_start}-{range_start}" 
    
    data = await get_json(url)
    
    if not data or not data.get("data") or not data["data"]["hadiths"]:
        url = f"https://api.hadith.gading.dev/books/{book}?range=1-1"
        data = await get_json(url)
        
    if not data or not data.get("data"):
         return await message.edit("❌ **Gagal mengambil hadits.**")
    
    hadith = data["data"]["hadiths"][0]
    
    result = (
        f"📜 **HADITS HARIAN**\n"
        f"📚 **Riwayat:** HR. {book.title().replace('-', ' ')}\n"
        f"🔢 **Nomor:** {hadith['number']}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"{hadith['arab']}\n\n"
        f"**Artinya:**\n_{hadith['id']}_"
    )
    
    await message.edit(result)

async def asmaul_husna_handler(client, message):
    await message.edit("🔄 **Memuat Asmaul Husna...**")
    
    url = "https://api.aladhan.com/v1/asmaAlHusna"
    data = await get_json(url)
    
    if not data or data.get('code') != 200:
         return await message.edit("❌ **Gagal mengambil Asmaul Husna.**")
         

    import random
    asma = random.choice(data['data'])
    
    result = (
        f"🆔 **ASMAUL HUSNA**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"**{asma['name']}**\n"
        f"({asma['transliteration']})\n\n"

    )
    
    await message.edit(result)

async def quotes_islami_handler(client, message):
    quotes = [
        "Janganlah kamu berduka cita, sesungguhnya Allah bersama kita. (QS. At-Taubah: 40)",
        "Allah tidak membebani seseorang melainkan sesuai dengan kesanggupannya. (QS. Al-Baqarah: 286)",
        "Maka sesungguhnya bersama kesulitan ada kemudahan. (QS. Al-Insyirah: 5)",
        "Dunia ini adalah perhiasan, dan sebaik-baik perhiasan dunia adalah wanita sholehah. (HR. Muslim)",
        "Barangsiapa yang menempuh jalan untuk menuntut ilmu, Allah akan mudahkan baginya jalan menuju surga. (HR. Muslim)",
        "Senyummu di hadapan saudaramu adalah sedekah. (HR. Tirmidzi)",
        "Kebersihan adalah sebagian dari iman.",
        "Solat itu tiang agama.",
        "Orang yang paling kuat adalah orang yang mampu menahan amarahnya.",
        "Sebaik-baik manusia adalah yang paling bermanfaat bagi orang lain.",
        "Sabar itu separuh iman.",
        "Bertaqwalah kepada Allah dimanapun engkau berada.",
        "Setiap amal tergantung pada niatnya.",
        "Tangan di atas lebih baik daripada tangan di bawah.",
        "Jauhilah dengki, karena dengki memakan kebaikan sebagaimana api memakan kayu bakar."
    ]
    import random
    selected = random.choice(quotes)
    await message.edit(f"💡 **QUOTE ISLAMI**\n━━━━━━━━━━━━━━━━━━\n\n_{selected}_")

from pyrogram import Client, filters

def split_text(text, max_len=3900):
    parts = []
    while len(text) > max_len:
        split_at = text.rfind("\n", 0, max_len)
        if split_at == -1:
            split_at = max_len
        parts.append(text[:split_at])
        text = text[split_at:]
    parts.append(text)
    return parts

KISAH_NABI = {
    "adam": {
        "nabi": "Adam",
        "tahun_kelahiran": "Awal penciptaan manusia",
        "tempat_kelahiran": "Surga",
        "usia": "930 tahun",
        "kisah": (
            "Nabi Adam adalah manusia pertama yang diciptakan oleh Allah SWT dari tanah.\n\n"
            "Allah mengajarkan kepadanya nama-nama segala sesuatu dan menjadikannya khalifah di bumi.\n\n"
            "Karena godaan iblis, Nabi Adam dan Hawa melanggar larangan Allah dan diturunkan ke bumi. "
            "Namun Nabi Adam segera bertaubat dan Allah menerima taubatnya."
        )
    },
    "idris": {
        "nabi": "Idris",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "Babilonia",
        "usia": "-",
        "kisah": (
            "Nabi Idris dikenal sebagai nabi yang cerdas dan tekun dalam ibadah.\n\n"
            "Beliau mengajarkan tulisan, ilmu pengetahuan, dan perhitungan kepada umatnya.\n\n"
            "Allah mengangkat derajat Nabi Idris ke tempat yang tinggi sebagai bentuk kemuliaan."
        )
    },
    "nuh": {
        "nabi": "Nuh",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "Mesopotamia",
        "usia": "950 tahun",
        "kisah": (
            "Nabi Nuh diutus untuk menyeru kaumnya agar menyembah Allah dan meninggalkan berhala.\n\n"
            "Karena kaumnya ingkar, Allah memerintahkan Nabi Nuh membuat bahtera.\n\n"
            "Banjir besar datang dan hanya Nabi Nuh serta orang-orang beriman yang selamat."
        )
    },
    "hud": {
        "nabi": "Hud",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "Ahqaf",
        "usia": "-",
        "kisah": (
            "Nabi Hud diutus kepada kaum Ad yang sombong dan kuat.\n\n"
            "Karena mereka menolak dakwah, Allah menurunkan azab berupa angin topan yang menghancurkan mereka."
        )
    },
    "shalih": {
        "nabi": "Shalih",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "Hijr",
        "usia": "-",
        "kisah": (
            "Nabi Shalih diutus kepada kaum Tsamud.\n\n"
            "Allah memberi mukjizat berupa unta betina, namun kaum Tsamud membunuhnya.\n\n"
            "Akibatnya mereka dibinasakan oleh azab Allah."
        )
    },
    "ibrahim": {
        "nabi": "Ibrahim",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "Ur, Babilonia",
        "usia": "175 tahun",
        "kisah": (
            "Nabi Ibrahim adalah bapak para nabi dan teladan tauhid.\n\n"
            "Beliau menghancurkan berhala dan diuji dengan perintah menyembelih putranya.\n\n"
            "Karena ketaatan, Allah menggantinya dengan seekor domba."
        )
    },
    "luth": {
        "nabi": "Luth",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "Sodom",
        "usia": "-",
        "kisah": (
            "Nabi Luth diutus kepada kaum yang melakukan perbuatan keji.\n\n"
            "Karena mereka ingkar, Allah membinasakan kaum tersebut kecuali Nabi Luth dan pengikutnya."
        )
    },
    "ismail": {
        "nabi": "Ismail",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "Makkah",
        "usia": "137 tahun",
        "kisah": (
            "Nabi Ismail adalah putra Nabi Ibrahim yang sangat taat kepada Allah.\n\n"
            "Beliau membantu membangun Ka'bah bersama ayahnya."
        )
    },
    "ishaq": {
        "nabi": "Ishaq",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "Kan'an",
        "usia": "180 tahun",
        "kisah": (
            "Nabi Ishaq adalah putra Nabi Ibrahim.\n\n"
            "Beliau meneruskan dakwah tauhid kepada kaumnya."
        )
    },
    "yaqub": {
        "nabi": "Ya'qub",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "Kan'an",
        "usia": "147 tahun",
        "kisah": (
            "Nabi Ya'qub dikenal dengan kesabaran dan kasih sayangnya.\n\n"
            "Beliau adalah ayah dari Nabi Yusuf."
        )
    },
    "yusuf": {
        "nabi": "Yusuf",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "Kan'an",
        "usia": "110 tahun",
        "kisah": (
            "Nabi Yusuf dikenal karena ketampanan dan kesabarannya.\n\n"
            "Ia dibuang ke sumur, dijual sebagai budak, hingga menjadi pejabat Mesir.\n\n"
            "Beliau memaafkan saudara-saudaranya."
        )
    },
    "ayyub": {
        "nabi": "Ayyub",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "-",
        "usia": "-",
        "kisah": (
            "Nabi Ayyub diuji dengan penyakit dan kehilangan harta.\n\n"
            "Namun beliau tetap sabar dan Allah mengembalikan nikmatnya."
        )
    },
    "syuaib": {
        "nabi": "Syuaib",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "Madyan",
        "usia": "-",
        "kisah": (
            "Nabi Syuaib diutus kepada kaum Madyan yang curang dalam berdagang.\n\n"
            "Karena ingkar, mereka dibinasakan."
        )
    },
    "musa": {
        "nabi": "Musa",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "Mesir",
        "usia": "120 tahun",
        "kisah": (
            "Nabi Musa diutus kepada Fir'aun yang zalim.\n\n"
            "Dengan mukjizat tongkat, beliau membebaskan Bani Israil."
        )
    },
    "harun": {
        "nabi": "Harun",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "Mesir",
        "usia": "-",
        "kisah": (
            "Nabi Harun adalah saudara Nabi Musa.\n\n"
            "Beliau membantu Nabi Musa dalam berdakwah."
        )
    },
    "dzulkifli": {
        "nabi": "Dzulkifli",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "-",
        "usia": "-",
        "kisah": (
            "Nabi Dzulkifli dikenal sebagai nabi yang sabar dan adil dalam memimpin umatnya."
        )
    },
    "daud": {
        "nabi": "Daud",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "Palestina",
        "usia": "100 tahun",
        "kisah": (
            "Nabi Daud adalah raja sekaligus nabi.\n\n"
            "Beliau diberi kitab Zabur dan suara yang merdu."
        )
    },
    "sulaiman": {
        "nabi": "Sulaiman",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "Palestina",
        "usia": "-",
        "kisah": (
            "Nabi Sulaiman diberi kekuasaan atas jin, manusia, dan hewan.\n\n"
            "Beliau adalah raja yang sangat adil."
        )
    },
    "ilyas": {
        "nabi": "Ilyas",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "-",
        "usia": "-",
        "kisah": (
            "Nabi Ilyas menyeru kaumnya untuk meninggalkan penyembahan berhala Baal."
        )
    },
    "ilyasa": {
        "nabi": "Ilyasa",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "-",
        "usia": "-",
        "kisah": (
            "Nabi Ilyasa melanjutkan dakwah Nabi Ilyas dengan penuh kesabaran."
        )
    },
    "yunus": {
        "nabi": "Yunus",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "Niniwe",
        "usia": "-",
        "kisah": (
            "Nabi Yunus meninggalkan kaumnya dan ditelan ikan besar.\n\n"
            "Setelah bertaubat, Allah menyelamatkannya."
        )
    },
    "zakaria": {
        "nabi": "Zakaria",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "Palestina",
        "usia": "-",
        "kisah": (
            "Nabi Zakaria memohon keturunan di usia tua.\n\n"
            "Allah mengabulkan dengan kelahiran Nabi Yahya."
        )
    },
    "yahya": {
        "nabi": "Yahya",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "Palestina",
        "usia": "-",
        "kisah": (
            "Nabi Yahya dikenal sebagai nabi yang suci dan taat sejak kecil."
        )
    },
    "isa": {
        "nabi": "Isa",
        "tahun_kelahiran": "-",
        "tempat_kelahiran": "Betlehem",
        "usia": "-",
        "kisah": (
            "Nabi Isa lahir tanpa ayah atas izin Allah.\n\n"
            "Beliau diberi mukjizat menyembuhkan penyakit dan menghidupkan orang mati."
        )
    },
    "muhammad": {
        "nabi": "Muhammad",
        "tahun_kelahiran": "570 M",
        "tempat_kelahiran": "Makkah",
        "usia": "63 tahun",
        "kisah": (
            "Nabi Muhammad SAW adalah nabi terakhir dan penutup para nabi.\n\n"
            "Beliau menerima Al-Qur'an sebagai pedoman hidup umat manusia.\n\n"
            "Akhlaknya menjadi teladan terbaik sepanjang masa."
        )
    }
}

@Client.on_message(filters.command("kisah", prefixes=".") & filters.me)
async def kisah_nabi_handler(client, message):
    if len(message.command) < 2:
        return await message.edit(
            "❌ **Gunakan:** `.kisah [nama nabi]`\n"
            "Contoh: `.kisah yusuf`"
        )

    nama_nabi = message.command[1].lower()

    if nama_nabi not in KISAH_NABI:
        return await message.edit(
            f"❌ **Kisah Nabi {nama_nabi.capitalize()} belum tersedia.**"
        )

    data = KISAH_NABI[nama_nabi]

    header = (
        f"📜 **KISAH NABI {data['nabi'].upper()}**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👶 **Tahun Kelahiran:** {data['tahun_kelahiran']}\n"
        f"📍 **Tempat Kelahiran:** {data['tempat_kelahiran']}\n"
        f"⏳ **Usia:** {data['usia']}\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
    )

    parts = split_text(data["kisah"])

    await message.edit(header + parts[0])

    for i, part in enumerate(parts[1:], start=2):
        await message.reply(f"📖 **Lanjutan ({i}/{len(parts)})**\n\n{part}")
    await message.edit(header + parts[0])

    for i, part in enumerate(parts[1:], start=2):
        await message.reply(
            f"📖 **Lanjutan ({i}/{len(parts)})**\n\n{part}"
        )

async def rukun_islam_handler(client, message):
    text = (
        "🕌 **RUKUN ISLAM**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "1️⃣ **Syahadat**\n"
        "   (Bersaksi tiada Tuhan selain Allah dan Nabi Muhammad utusan Allah)\n\n"
        "2️⃣ **Shalat**\n"
        "   (Mendirikan shalat 5 waktu)\n\n"
        "3️⃣ **Zakat**\n"
        "   (Menunaikan zakat bagi yang mampu)\n\n"
        "4️⃣ **Puasa**\n"
        "   (Berpuasa di bulan Ramadhan)\n\n"
        "5️⃣ **Haji**\n"
        "   (Pergi haji bagi yang mampu)"
    )
    await message.edit(text)

async def rukun_iman_handler(client, message):
    text = (
        "✨ **RUKUN IMAN**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "1️⃣ **Iman kepada Allah**\n\n"
        "2️⃣ **Iman kepada Malaikat-Malaikat Allah**\n\n"
        "3️⃣ **Iman kepada Kitab-Kitab Allah**\n\n"
        "4️⃣ **Iman kepada Rasul-Rasul Allah**\n\n"
        "5️⃣ **Iman kepada Hari Kiamat**\n\n"
        "6️⃣ **Iman kepada Qada dan Qadar**"
    )
    await message.edit(text)



