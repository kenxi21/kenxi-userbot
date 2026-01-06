import random
import aiohttp

async def get_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            try:
                return await r.json()
            except:
                return None

async def alkitab_handler(client, message):
    if len(message.command) < 2:
        return await message.edit("Gunakan: .alkitab Kitab Pasal:Ayat")

    query = " ".join(message.command[1:])
    await message.edit("Mencari ayat...")

    url = f"https://beeble.vercel.app/api/v1/passage/{query}"
    data = await get_json(url)

    if not data or not data.get("data"):
        return await message.edit("Ayat tidak ditemukan")

    verses = data["data"].get("verses", [])
    book = data["data"].get("book", {}).get("name", "-")

    teks = ""
    for v in verses:
        teks += f"{v['verse']}. {v['content']}\n"

    await message.edit(
        f"ALKITAB\n"
        f"Kitab: {book}\n"
        f"━━━━━━━━━━━━━━\n\n"
        f"{teks}"
    )

async def renungan_handler(client, message):
    renungan = [
        ("Mazmur 23:1", "Tuhan memelihara hidup orang percaya dengan setia."),
        ("Filipi 4:13", "Kekuatan sejati datang dari Kristus."),
        ("Amsal 3:5", "Percaya Tuhan berarti menyerahkan kendali hidup."),
        ("Yesaya 41:10", "Tuhan hadir dalam setiap kelemahan."),
        ("Roma 8:28", "Segala sesuatu dipakai Tuhan untuk kebaikan.")
    ]

    for _ in range(150):
        renungan.append(random.choice(renungan))

    ayat, isi = random.choice(renungan)

    await message.edit(
        f"RENUNGAN HARIAN\n"
        f"━━━━━━━━━━━━━━\n\n"
        f"{isi}\n\n"
        f"({ayat})"
    )

async def quotes_kristen_handler(client, message):
    quotes = [
        "Tuhan setia menepati janji-Nya.",
        "Doa menguatkan iman orang percaya.",
        "Kasih Tuhan tidak pernah habis.",
        "Iman berjalan mendahului mujizat.",
        "Pengharapan di dalam Tuhan tidak mengecewakan."
    ]

    for _ in range(200):
        quotes.append(random.choice(quotes))

    await message.edit(
        f"QUOTE KRISTEN\n"
        f"━━━━━━━━━━━━━━\n\n"
        f"{random.choice(quotes)}"
    )

async def kidung_handler(client, message):
    if len(message.command) < 2:
        return await message.edit("Gunakan: .kidung nomor")

    kidung = {}

    for i in range(1, 101):
        kidung[str(i)] = (
            f"Kidung Jemaat No. {i}",
            random.choice(["Pujian", "Iman", "Doa", "Pengharapan"]),
            "Mari menaikkan pujian bagi Tuhan dengan segenap hati"
        )

    no = message.command[1]
    data = kidung.get(no)

    if not data:
        return await message.edit("Kidung tidak ditemukan")

    await message.edit(
        f"KIDUNG JEMAAT NO. {no}\n"
        f"Judul: {data[0]}\n"
        f"Tema: {data[1]}\n"
        f"━━━━━━━━━━━━━━\n\n"
        f"{data[2]}"
    )

async def kisah_rasul_handler(client, message):
    if len(message.command) < 2:
        return await message.edit("Gunakan: .rasul nama")

    rasul = {
        "petrus": (
            "Petrus",
            "Pemimpin Gereja",
            "Nelayan yang dipanggil Yesus dan menjadi pemimpin gereja mula-mula."
        ),
        "paulus": (
            "Paulus",
            "Rasul Bangsa-bangsa",
            "Mantan penganiaya yang bertobat dan memberitakan Injil ke banyak bangsa."
        ),
        "yohanes": (
            "Yohanes",
            "Murid yang Dikasihi",
            "Penulis Injil Yohanes dan Kitab Wahyu."
        ),
        "andreas": (
            "Andreas",
            "Penginjil",
            "Rasul yang membawa banyak orang kepada Yesus."
        ),
        "filipus": (
            "Filipus",
            "Penginjil Setia",
            "Filipus berasal dari Betsaida dan memperkenalkan Natanael kepada Yesus. "
            "Ia melayani di wilayah Asia Kecil menurut tradisi gereja."
        ),
        "tomas": (
            "Tomas",
            "Saksi Iman",
            "Rasul yang kemudian membawa Injil hingga ke India."
        ),
        "matius": (
            "Matius",
            "Penulis Injil",
            "Mantan pemungut cukai yang dipanggil Yesus."
        ),
        "barnabas": (
            "Barnabas",
            "Anak Penghiburan",
            "Rekan pelayanan Paulus dalam misi."
        ),
        "matias": (
            "Matias",
            "Rasul Pengganti",
            "Dipilih untuk menggantikan Yudas Iskariot."
        )
    }

    nama = message.command[1].lower()
    data = rasul.get(nama)

    if not data:
        return await message.edit("Kisah rasul tidak ditemukan")

    await message.edit(
        f"KISAH RASUL {data[0].upper()}\n"
        f"Gelar: {data[1]}\n"
        f"━━━━━━━━━━━━━━\n\n"
        f"{data[2]}"
    )
