import os
import asyncio
import subprocess
from pyrogram import raw
from pyrogram.errors import StickersetInvalid
import yt_dlp

def get_yt_dlp_options(output_path):
    return {
        "format": "best[ext=mp4]/best",
        "outtmpl": output_path,
        "quiet": True,
        "no_warnings": True,
        "nocheckcertificate": True,
    }

async def run_ffmpeg_convert_webp(input_file, output_file):
    pass
    cmd = [
        "ffmpeg", "-y", "-i", input_file,
        "-vf", "scale=w=512:h=512:force_original_aspect_ratio=decrease",
        "-c:v", "libwebp", "-lossless", "0", "-quality", "75",
        output_file
    ]
    process = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL
    )
    await process.wait()
    return os.path.exists(output_file)

async def run_ffmpeg_convert_png(input_file, output_file):
    cmd = [
        "ffmpeg", "-y", "-i", input_file,
        output_file
    ]
    process = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL
    )
    await process.wait()
    return os.path.exists(output_file)

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

    path = None
    sticker_path = f"kang_{message.id}.webp"
    
    try:
        me = await client.get_me()
        user_username = me.username if me.username else "kenxi"
        pack_name = f"k{me.id}_by_{user_username}"
        pack_title = f"Pack @{user_username}"

        path = await client.download_media(replied)
        if not path:
            return await message.edit("❌ Gagal download media.")

        pass
        success = await run_ffmpeg_convert_webp(path, sticker_path)
        if not success:
            return await message.edit("❌ Gagal konversi ke WebP (FFmpeg Error).")

        uploaded = await client.save_file(sticker_path)

        emoji = "✨"
        if replied.sticker and replied.sticker.emoji:
            emoji = replied.sticker.emoji

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

    await message.edit("🎨 Konversi ke gambar...")
    
    path = None
    output_path = f"img_{message.id}.png"

    try:
        path = await client.download_media(replied)
        if not path:
            return await message.edit("❌ Gagal download stiker.")

        pass
        success = await run_ffmpeg_convert_png(path, output_path)
        if not success:
            return await message.edit("❌ Gagal konversi gambar.")

        await client.send_photo(
            message.chat.id,
            output_path,
            reply_to_message_id=replied.id
        )
        await message.delete()

    except Exception as e:
        await message.edit(f"❌ Error: {e}")

    finally:
        for f in (path, output_path):
            if f and os.path.exists(f):
                os.remove(f)
