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

async def kisah_nabi_handler(client, message):
    if len(message.command) < 2:
        return await message.edit(
            "❌ **Gunakan:** `.kisah [nama nabi]`\n"
            "Contoh: `.kisah yusuf`"
        )

    nama_nabi = message.command[1].lower()
    await message.edit(f"📖 **Mencari kisah Nabi {nama_nabi.capitalize()}...**")

    url = "https://raw.githubusercontent.com/zerodytrash/prophet-api/master/data.json"
    data = await get_json(url)

    if not data or not isinstance(data, list):
        return await message.edit("❌ **Gagal mengambil data kisah nabi.**")

    kisah = None
    for item in data:
        if item.get("nabi", "").lower() == nama_nabi:
            kisah = item
            break

    if not kisah:
        return await message.edit(
            f"❌ **Kisah Nabi {nama_nabi.capitalize()} tidak ditemukan.**"
        )

    name = kisah.get("nabi", nama_nabi).capitalize()
    birth = kisah.get("tahun_kelahiran", "-")
    place = kisah.get("tempat_kelahiran", "-")
    age = kisah.get("usia", "-")
    story = kisah.get("kisah", "-")

    header = (
        f"📜 **KISAH NABI {name.upper()}**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👶 **Tahun Kelahiran:** {birth}\n"
        f"📍 **Tempat Kelahiran:** {place}\n"
        f"⏳ **Usia:** {age}\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
    )

    parts = split_text(story)

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


