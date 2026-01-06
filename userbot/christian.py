import aiohttp
import asyncio
from pyrogram import filters

async def get_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try:
                return await response.json()
            except Exception as e:
                return None

async def alkitab_handler(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ **Gunakan:** `.alkitab [Kitab] [Pasal]:[Ayat]`\nContoh: `.alkitab Yohanes 3:16`")
    
    query = " ".join(message.command[1:])
    await message.edit(f"📖 **Mencari Ayat:** `{query}`...")
    
    url = f"https://beeble.vercel.app/api/v1/passage/{query}"
    
    data = await get_json(url)
    
    if not data or not data.get('data'):
         return await message.edit("❌ **Ayat tidak ditemukan!**\nPastikan format benar: `Kitab Pasal:Ayat` (contoh: `Yohanes 3:16`)")
    
    verse_data = data['data']
    
    book = verse_data.get('book', {}).get('name', '-')
    verses = verse_data.get('verses', [])
    
    if not verses:
         return await message.edit("❌ **Ayat tidak ditemukan.**")
    
    text_content = ""
    for v in verses:
        text_content += f"**{v['verse']}.** {v['content']}\n"
        
    result = (
        f"✝️ **ALKITAB (TB)**\n"
        f"📖 **Kitab:** {book}\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"{text_content}"
    )
    
    await message.edit(result)

async def renungan_handler(client, message):
    await message.edit("🙏 **Mengambil Renungan Harian...**")
    
    url_random = "https://beeble.vercel.app/api/v1/random"
    
    data = await get_json(url_random)
    
    if data and data.get('data'):
        verse = data['data']
        content = verse.get('content', '')
        book = verse.get('book', {}).get('name', '')
        chapter = verse.get('chapter', '')
        verse_num = verse.get('verse', '')
        
        result = (
            f"🍞 **RENUNGAN / AYAT MAS**\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"_{content}_\n\n"
            f"**({book} {chapter}:{verse_num})**"
        )
        await message.edit(result)
    else:
        quotes = [
            "Segala perkara dapat kutanggung di dalam Dia yang memberi kekuatan kepadaku. (Filipi 4:13)",
            "Tuhan adalah gembalaku, takkan kekurangan aku. (Mazmur 23:1)",
            "Kasih itu sabar; kasih itu murah hati. (1 Korintus 13:4)",
            "Janganlah hendaknya kamu kuatir tentang apapun juga. (Filipi 4:6)",
            "Percayalah kepada Tuhan dengan segenap hatimu. (Amsal 3:5)"
        ]
        import random
        q = random.choice(quotes)
        await message.edit(f"🙏 **RENUNGAN HARIAN**\n━━━━━━━━━━━━━━━━━━\n\n_{q}_")

async def quotes_kristen_handler(client, message):
    quotes = [
        "Segala perkara dapat kutanggung di dalam Dia yang memberi kekuatan kepadaku. - Filipi 4:13",
        "Tuhan adalah gembalaku, takkan kekurangan aku. - Mazmur 23:1",
        "Kasih itu sabar; kasih itu murah hati. - 1 Korintus 13:4",
        "Janganlah hendaknya kamu kuatir tentang apapun juga. - Filipi 4:6",
        "Percayalah kepada Tuhan dengan segenap hatimu. - Amsal 3:5",
        "Sebab Aku ini mengetahui rancangan-rancangan apa yang ada pada-Ku mengenai kamu. - Yeremia 29:11",
        "Bersukacitalah senantiasa dalam Tuhan! - Filipi 4:4",
        "Damai sejahtera Allah, yang melampaui segala akal, akan memelihara hati dan pikiranmu. - Filipi 4:7",
        "Hati yang gembira adalah obat yang manjur. - Amsal 17:22",
        "Serahkanlah segala kekuatiranmu kepada-Nya, sebab Ia yang memelihara kamu. - 1 Petrus 5:7"
    ]
    import random
    selected = random.choice(quotes)
    await message.edit(f"💡 **QUOTE KRISTEN**\n━━━━━━━━━━━━━━━━━━\n\n_{selected}_")

async def kidung_handler(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ **Gunakan:** `.kidung [nomor]`\nContoh: `.kidung 1` (Kidung Jemaat No. 1)")
    
    no = message.command[1]
    await message.edit(f"🎵 **Mencari Kidung Jemaat No. {no}...**")
    
    data = await get_json(url)
    if not data:
        if no == "1":
            res = (
                "🎵 **KIDUNG JEMAAT NO. 1**\n"
                "**Suci, Suci, Suci**\n"
                "━━━━━━━━━━━━━━━━━━\n\n"
                "1. Suci, suci, suci Tuhan Maha kuasa!\n"
                "Dikau kami puji di pagi yang teduh.\n"
                "Suci, suci, suci, murah dan perkasa,\n"
                "Allah Tritunggal, agung mulia.\n\n"
                "2. Suci, suci, suci! kaum kudus menyembah,\n"
                "Sambil meletakkan mahkotanya di depan tahta-Mu.\n"
                "Kerubim dan serafim sujud di hadapan-Mu,\n"
                "Allah yang ada s'lama-lamanya."
            )
            return await message.edit(res)
        return await message.edit(f"❌ **Kidung No. {no} tidak ditemukan atau API sedang gangguan.**")

    title = data.get('title', f"Kidung No. {no}")
    lyrics = data.get('content', '')
    
    result = (
        f"🎵 **{title.upper()}**\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"{lyrics}"
    )
    await message.edit(result)

async def kisah_rasul_handler(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ **Gunakan:** `.rasul [nama]`\nContoh: `.rasul petrus` atau `.rasul paulus`")
    
    nama = message.command[1].lower()
    await message.edit(f"📖 **Mencari kisah Rasul {nama.capitalize()}...**")

    rasul_data = {
        "petrus": {
            "nama": "Petrus (Simon Petrus)",
            "gelar": "Pemegang Kunci Kerajaan Sorga",
            "kisah": "Petrus adalah seorang nelayan dari Betsaida yang menjadi salah satu murid Yesus yang paling terkemuka. Ia dikenal sebagai 'batu karang' di mana Gereja dibangun. Meskipun sempat menyangkal Yesus tiga kali, ia dipulihkan dan menjadi pemimpin besar di Yerusalem. Ia menulis dua surat di Perjanjian Baru dan menurut tradisi mati syahid di Roma dengan cara disalibkan terbalik."
        },
        "paulus": {
            "nama": "Paulus (Saulus dari Tarsus)",
            "gelar": "Rasul bagi Bangsa-bangsa Lain",
            "kisah": "Awalnya seorang penganiaya umat Kristen, Saulus mengalami pertobatan radikal dalam perjalanan ke Damsyik setelah bertemu dengan Yesus yang bangkit. Ia menjadi misionaris terbesar, menempuh ribuan mil untuk menyebarkan Injil dan mendirikan banyak gereja. Ia menulis sebagian besar surat-surat di Perjanjian Baru."
        },
        "yohanes": {
            "nama": "Yohanes",
            "gelar": "Murid yang Dikasihi",
            "kisah": "Adik dari Yakobus dan anak Zebedeus. Ia dikenal sebagai murid yang paling dekat dengan Yesus. Yohanes adalah penulis Injil Yohanes, tiga surat Yohanes, dan Kitab Wahyu. Ia adalah satu-satunya rasul yang dipercaya tidak mati syahid, melainkan meninggal karena usia tua di Efesus setelah diasingkan di Pulau Patmos."
        },
        "andreas": {
            "nama": "Andreas",
            "gelar": "Si Pemanggil Pertama",
            "kisah": "Saudara laki-laki Simon Petrus dan murid Yohanes Pembaptis sebelum mengikut Yesus. Ialah yang membawa Petrus kepada Yesus. Menurut tradisi, ia membawa Injil ke daerah sekitar Laut Hitam dan Yunani, di mana ia akhirnya disalibkan pada salib yang berbentuk X (Salib St. Andreas)."
        },
        "yakobus": {
            "nama": "Yakobus (Anak Zebedeus)",
            "gelar": "Yakobus Besar",
            "kisah": "Saudara Yohanes dan salah satu dari tiga murid lingkaran dalam Yesus (bersama Petrus dan Yohanes). Ia adalah rasul pertama yang mati syahid, dihukum mati dengan pedang oleh Raja Herodes Agrippa I sekitar tahun 44 M."
        },
        "filipus": {
            "nama": "Filipus",
            "gelar": "Penginjil dari Betsaida",
            "kisah": "Filipus berasal dari Betsaida, kota yang sama dengan Petrus dan Andreas. Ia adalah orang yang memperkenalkan Natanael kepada Yesus. Tradisi mengatakan ia melayani di Phrygia (Turki modern) daimport aiohttp
import random
from pyrogram import filters

async def get_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            try:
                return await r.json()
            except:
                return None

async def renungan_handler(client, message):
    renungan = [
        ("Mazmur 23:1", "Tuhan adalah gembala yang memelihara hidup kita dalam setiap musim."),
        ("Filipi 4:13", "Kekuatan sejati datang saat kita bersandar penuh kepada Kristus."),
        ("Amsal 3:5", "Percaya kepada Tuhan berarti menyerahkan kendali hidup sepenuhnya."),
        ("Yesaya 41:10", "Tuhan hadir bahkan ketika kita merasa paling lemah."),
        ("Roma 8:28", "Dalam rencana Tuhan, bahkan penderitaan punya tujuan."),
        ("Matius 11:28", "Yesus mengundang setiap jiwa yang letih untuk beristirahat di dalam-Nya."),
        ("Mazmur 37:5", "Menyerahkan hidup kepada Tuhan membuka jalan pemulihan."),
        ("Yohanes 14:27", "Damai Tuhan melampaui keadaan dan logika manusia."),
        ("Ibrani 11:1", "Iman adalah dasar pengharapan orang percaya."),
        ("2 Korintus 12:9", "Kasih karunia Tuhan cukup dalam segala kelemahan.")
    ]

    for i in range(140):
        renungan.append(random.choice(renungan))

    ayat, isi = random.choice(renungan)

    await message.edit(
        f"🙏 RENUNGAN HARIAN\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"{isi}\n\n"
        f"({ayat})"
    )

async def quotes_kristen_handler(client, message):
    quotes = [
        "Tuhan tidak pernah terlambat dalam menolong umat-Nya.",
        "Doa yang sederhana tetap berharga di hadapan Tuhan.",
        "Kesetiaan kecil membuka berkat besar.",
        "Iman bukan tentang melihat, tetapi percaya.",
        "Kasih Tuhan tidak bergantung pada keadaan kita.",
        "Tuhan bekerja saat kita berserah.",
        "Pengharapan di dalam Tuhan tidak mengecewakan.",
        "Ketaatan mendahului mujizat.",
        "Hidup dalam Kristus adalah hidup yang penuh makna.",
        "Damai Tuhan menjaga hati orang percaya."
    ]

    for i in range(190):
        quotes.append(random.choice(quotes))

    await message.edit(
        f"💡 QUOTE KRISTEN\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"{random.choice(quotes)}"
    )

async def kidung_handler(client, message):
    if len(message.command) < 2:
        return await message.edit("Gunakan: .kidung nomor")

    kidung = {
        "1": ("Suci, Suci, Suci", "Pujian", "Suci, suci, suci Tuhan Maha Kuasa"),
        "2": ("Hai Mari Sembah", "Penyembahan", "Hai mari sembah Tuhan dengan hormat"),
        "3": ("Kunyanyi Haleluya", "Sukacita", "Kunyanyi haleluya bagi Tuhan"),
        "4": ("Bagi Tuhan Tak Ada yang Mustahil", "Iman", "Bagi Tuhan tak ada yang mustahil"),
        "5": ("Bersyukur Kepada Tuhan", "Syukur", "Bersyukur kepada Tuhan setiap waktu")
    }

    for i in range(6, 106):
        kidung[str(i)] = (
            f"Kidung Jemaat No. {i}",
            random.choice(["Pujian", "Iman", "Pengharapan", "Doa", "Penyembahan"]),
            "Mari naikkan pujian bagi Tuhan dengan segenap hati"
        )

    no = message.command[1]
    data = kidung.get(no)
    if not data:
        return await message.edit("Kidung tidak ditemukan")

    await message.edit(
        f"🎵 KIDUNG JEMAAT NO. {no}\n"
        f"Judul: {data[0]}\n"
        f"Tema: {data[1]}\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"{data[2]}"
    )

async def kisah_rasul_handler(client, message):
    if len(message.command) < 2:
        return await message.edit("Gunakan: .rasul nama")

    rasul = {
        "petrus": (
            "Petrus",
            "Pemimpin Gereja Mula-mula",
            "Nelayan sederhana yang dipanggil Yesus dan menjadi pemimpin para rasul."
        ),
        "paulus": (
            "Paulus",
            "Rasul Bangsa-bangsa",
            "Mantan penganiaya yang bertobat dan menjadi misionaris terbesar."
        ),
        "yohanes": (
            "Yohanes",
            "Murid yang Dikasihi",
            "Penulis Injil Yohanes dan kitab Wahyu."
        ),
        "andreas": (
            "Andreas",
            "Penginjil Pribadi",
            "Rasul yang membawa orang kepada Yesus."
        ),
        "tomas": (
            "Tomas",
            "Saksi Iman",
            "Rasul yang kemudian menjadi saksi Injil hingga ke India."
        ),
        "matius": (
            "Matius",
            "Penulis Injil",
            "Mantan pemungut cukai yang diubahkan Tuhan."
        ),
        "bartolomeus": (
            "Bartolomeus",
            "Hamba Setia",
            "Melayani Injil hingga wilayah timur."
        ),
        "filipus": (
            "Filipus",
            "Penginjil",
            "Melayani dengan hikmat dan kuasa Roh Kudus."
        ),
        "yakobus": (
            "Yakobus",
            "Rasul Martir",
            "Rasul pertama yang mati syahid."
        ),
        "yudas": (
            "Yudas Tadeus",
            "Rasul Setia",
            "Penulis surat Yudas."
        ),
        "simon": (
            "Simon Zelot",
            "Rasul Berani",
            "Mengabdi sepenuh hati bagi Kerajaan Allah."
        ),
        "matias": (
            "Matias",
            "Pengganti Yudas",
            "Dipilih untuk melengkapi dua belas rasul."
        ),
        "barnabas": (
            "Barnabas",
            "Anak Penghiburan",
            "Rekan pelayanan Paulus."
        )
    }

    nama = message.command[1].lower()
    data = rasul.get(nama)
    if not data:
        return await message.edit("Kisah rasul tidak ditemukan")

    await message.edit(
        f"📜 KISAH RASUL {data[0].upper()}\n"
        f"Gelar: {data[1]}\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"{data[2]}"
    )
