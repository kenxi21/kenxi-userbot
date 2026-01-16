import random
from pyrogram import filters, enums
from pyrogram.types import Message

TOXIC_LIST = [
    "Muka lo kek pantat panci gosong.",
    "Otak lo di dengkul ya? Pantesan bego.",
    "Gaya selangit, saku sesempit sempak.",
    "Lo tuh kek daki, gak berguna tapi ada terus.",
    "Cermin mana cermin? Ngaca dulu sebelum ngomong.",
    "Bacot lo kek knalpot racing, berisik doang gak ada isinya.",
    "Mending diem daripada malu-maluin nenek moyang lo.",
    "Muka pas-pasan, kelakuan kek setan.",
    "Lo tuh unik, kek kesalahan pabrik.",
    "Capek liat lo, kek nungguin gajah bertelur."
]

PANTUN_LIST = [
    "Masak air biar mateng, Kalo udah mateng jangan lupa ditaruh. Muka lo emang ganteng, Tapi sayang dompet lo keruh.",
    "Makan nasi pake tempe, Tempenya digoreng pake tepung. Jangan suka maen hape, Nanti matanya jadi juling.",
    "Buah nanas buah manggis, Segar rasanya dimakan pagi. Janganlah engkau menangis, Mending kita nyanyi lagi."
]

QUOTES_LIST = [
    "Hiduplah seolah-olah kamu akan mati besok. Belajarlah seolah-olah kamu akan hidup selamanya.",
    "Kegagalan adalah kunci kesuksesan.",
    "Jangan pernah menyerah pada apa yang benar-benar kamu inginkan.",
    "Waktu adalah uang.",
    "Kebahagiaan bukan sesuatu yang sudah jadi. Itu berasal dari tindakanmu sendiri."
]

async def toxic_handler(client, message):
    await message.edit(random.choice(TOXIC_LIST))

async def pantun_handler(client, message):
    await message.edit(random.choice(PANTUN_LIST))

async def quotes_handler(client, message):
    await message.edit(random.choice(QUOTES_LIST))

async def percentage_handler(client, message):
    cmd = message.command[0].lower()
    label = {
        "gay": "Gay",
        "lesbi": "Lesbi",
        "ganteng": "Ganteng",
        "cantik": "Cantik",
        "jelek": "Jelek"
    }.get(cmd, cmd.capitalize())
    
    perc = random.randint(0, 100)
    await message.edit(f"📊 **Cek {label}**\n\nHasilnya: **{perc}%**")

async def siapa_handler(client, message):
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.edit("❌ Fitur ini hanya untuk grup.")
    
    args = message.text.split(None, 1)
    prompt = args[1] if len(args) > 1 else "akan beruntung hari ini?"
    
    members = []
    async for member in client.get_chat_members(message.chat.id):
        if not member.user.is_bot and not member.user.is_deleted:
            members.append(member.user)
    
    if not members:
        return await message.edit("❌ Tidak ada anggota yang ditemukan.")
    
    target = random.choice(members)
    await message.edit(f"🔍 **Pertanyaan:** Siapa {prompt}\n\n👉 **Jawaban:** {target.mention()}")
