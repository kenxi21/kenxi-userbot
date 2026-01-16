import os
import io
import asyncio
from pyrogram import raw
from pyrogram.errors import StickersetInvalid
from PIL import Image
import yt_dlp

def get_yt_dlp_options(output_path):
    return {
        "format": "best[ext=mp4]/best",
        "outtmpl": output_path,
        "quiet": True,
        "no_warnings": True,
        "nocheckcertificate": True,
    }

async def dl_handler(client, message):
    args = message.text.split(None, 1)
    if len(args) < 2:
        return await message.edit("❌ Silakan berikan link video.")

    url = args[1].strip()
    await message.edit("📥 Sedang mengunduh video...")

    output_file = f"download_{message.id}.mp4"

    try:
        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(get_yt_dlp_options(output_file)) as ydl:
            await loop.run_in_executor(None, lambda: ydl.download([url]))

        if not os.path.exists(output_file):
            return await message.edit("❌ Gagal mengunduh video.")

        await client.send_video(
            message.chat.id,
            output_file,
            caption=f"✅ Berhasil diunduh\n{url}"
        )
        await message.delete()

    except Exception as e:
        await message.edit(f"❌ Error: {e}")

    finally:
        if os.path.exists(output_file):
            os.remove(output_file)

async def kang_handler(client, message):
    replied = message.reply_to_message
    if not replied or not (replied.photo or replied.sticker or replied.document):
        return await message.edit("❌ Balas ke foto atau stiker.")

    await message.edit("🎨 Memproses stiker...")

    try:
        me = await client.get_me()
        pack_name = f"k{me.id}_by_{me.username or 'kenxi'}"
        pack_title = f"Pack @{me.username or me.first_name}"

        path = await client.download_media(replied)
        if not path:
            return await message.edit("❌ Gagal download media.")

        sticker_path = f"kang_{message.id}.webp"

        img = Image.open(path)
        img.load()

        if img.mode not in ("RGBA", "RGB"):
            img = img.convert("RGBA")
        else:
            img = img.convert("RGBA")

        w, h = img.size
        scale = 512 / max(w, h)
        new_size = (int(w * scale), int(h * scale))

        img = img.resize(new_size, Image.Resampling.LANCZOS)
        img.save(sticker_path, format="WEBP")

        uploaded = await client.save_file(sticker_path)

        emoji = replied.sticker.emoji if replied.sticker and replied.sticker.emoji else "✨"

        media = await client.invoke(
            raw.functions.messages.UploadMedia(
                peer=raw.types.InputPeerSelf(),
                media=raw.types.InputMediaUploadedDocument(
                    file=uploaded,
                    mime_type="image/webp",
                    attributes=[
                        raw.types.DocumentAttributeSticker(
                            alt=emoji,
                            stickerset=raw.types.InputStickerSetEmpty()
                        ),
                        raw.types.DocumentAttributeImageSize(
                            w=new_size[0],
                            h=new_size[1]
                        )
                    ]
                )
            )
        )

        doc = media.document

        try:
            await client.invoke(
                raw.functions.stickers.AddStickerToSet(
                    stickerset=raw.types.InputStickerSetShortName(short_name=pack_name),
                    sticker=raw.types.InputStickerSetItem(
                        document=raw.types.InputDocument(
                            id=doc.id,
                            access_hash=doc.access_hash,
                            file_reference=doc.file_reference
                        ),
                        emoji=emoji
                    )
                )
            )
        except StickersetInvalid:
            await client.invoke(
                raw.functions.stickers.CreateStickerSet(
                    user_id=await client.resolve_peer(me.id),
                    title=pack_title,
                    short_name=pack_name,
                    stickers=[
                        raw.types.InputStickerSetItem(
                            document=raw.types.InputDocument(
                                id=doc.id,
                                access_hash=doc.access_hash,
                                file_reference=doc.file_reference
                            ),
                            emoji=emoji
                        )
                    ]
                )
            )

        await message.edit(
            f"✅ Stiker ditambahkan\nhttps://t.me/addstickers/{pack_name}"
        )

    except Exception as e:
        await message.edit(f"❌ Error: {e}")

    finally:
        for f in (path, sticker_path):
            if f and os.path.exists(f):
                os.remove(f)

async def toimg_handler(client, message):
    replied = message.reply_to_message
    if not replied or not replied.sticker:
        return await message.edit("❌ Balas ke stiker.")

    if replied.sticker.is_animated or replied.sticker.is_video:
        return await message.edit("❌ Hanya stiker statis.")

    await message.edit("🖼 Mengubah ke foto...")

    try:
        path = await client.download_media(replied)
        if not path:
            return await message.edit("❌ Gagal download stiker.")

        img = Image.open(path)
        img.load()
        img = img.convert("RGB")

        bio = io.BytesIO()
        bio.name = "sticker.jpg"
        img.save(bio, "JPEG")
        bio.seek(0)

        await client.send_photo(message.chat.id, bio)
        await message.delete()

    except Exception as e:
        await message.edit(f"❌ Error: {e}")

    finally:
        if path and os.path.exists(path):
            os.remove(path)
