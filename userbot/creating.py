import os
import io
import asyncio
import re
from pyrogram import filters, enums, raw
from pyrogram.types import Message
from pyrogram.errors import StickersetInvalid, PeerIdInvalid
from PIL import Image
import yt_dlp

def get_yt_dlp_options(output_path):
    return {
        'format': 'best[ext=mp4]/best',
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
    }

async def dl_handler(client, message):
    args = message.text.split(None, 1)
    if len(args) < 2:
        return await message.edit("❌ Silakan berikan link video (TikTok/YT/IG).")
    
    url = args[1].strip()
    await message.edit("📥 **Sedang memproses unduhan (High Compatibility)...**")
    
    output_file = f"download_{message.id}.mp4"
    
    try:
        loop = asyncio.get_event_loop()
        ydl_opts = get_yt_dlp_options(output_file)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await loop.run_in_executor(None, lambda: ydl.download([url]))
            
        if not os.path.exists(output_file):
            return await message.edit("❌ Gagal mendownload video. Link mungkin tidak didukung atau terjadi kesalahan.")
            
        await message.edit("📤 **Sedang mengirim video...**")
        await client.send_video(
            message.chat.id, 
            output_file, 
            caption=f"✅ Berhasil diunduh!\n\n🔗 [Link Asli]({url})"
        )
        await message.delete()
        
    except Exception as e:
        await message.edit(f"❌ Error: {str(e)}")
    finally:
        if os.path.exists(output_file):
            os.remove(output_file)

async def kang_handler(client, message):
    replied = message.reply_to_message
    if not replied or not (replied.photo or replied.sticker or replied.document):
        return await message.edit("❌ Balas ke foto atau stiker untuk ditambahkan ke pack.")
    
    await message.edit("🎨 **Sedang memproses stiker ke pack Anda...**")
    
    try:
        me = await client.get_me()
        pack_name = f"k{me.id}_by_{me.username or 'kenxi'}"
        pack_title = f"Pack Stiker @{me.username or me.first_name}"
        
        path = await client.download_media(replied)
        if not path:
            return await message.edit("❌ Gagal mendownload media.")
            
        sticker_path = f"kang_{message.id}.webp"
        img = Image.open(path)
        
        if img.mode != "RGBA":
            img = img.convert("RGBA")
            
        width, height = img.size
        if width > height:
            new_width = 512
            new_height = int(height * (512 / width))
        else:
            new_height = 512
            new_width = int(width * (512 / height))
            
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        img.save(sticker_path, "WebP")
        
        uploaded_file = await client.save_file(sticker_path)
        
        emoji = "✨"
        if replied.sticker and replied.sticker.emoji:
            emoji = replied.sticker.emoji
            
        media = await client.invoke(
            raw.functions.messages.UploadMedia(
                peer=raw.types.InputPeerSelf(),
                media=raw.types.InputMediaUploadedDocument(
                    file=uploaded_file,
                    mime_type="image/webp",
                    attributes=[
                        raw.types.DocumentAttributeSticker(
                            alt=emoji,
                            stickerset=raw.types.InputStickerSetEmpty()
                        ),
                        raw.types.DocumentAttributeImageSize(w=new_width, h=new_height)
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
            
        await message.edit(f"✅ **Stiker berhasil ditambahkan!**\n\n🖼️ [Lihat Pack Anda](https://t.me/addstickers/{pack_name})")
        
        if os.path.exists(sticker_path):
            os.remove(sticker_path)
        if os.path.exists(path):
            os.remove(path)
            
    except Exception as e:
        await message.edit(f"❌ Error: {str(e)}")

async def toimg_handler(client, message):
    replied = message.reply_to_message
    if not replied or not replied.sticker:
        return await message.edit("❌ Balas ke stiker untuk mengubahnya menjadi foto.")
    
    if replied.sticker.is_animated or replied.sticker.is_video:
        return await message.edit("❌ Fitur ini hanya untuk stiker statis (bukan animasi/video).")
    
    await message.edit("🖼️ **Sedang mengubah stiker ke foto...**")
    
    try:
        path = await client.download_media(replied)
        if not path:
            return await message.edit("❌ Gagal mendownload stiker.")
        
        img = Image.open(path).convert("RGB")
        img_io = io.BytesIO()
        img.save(img_io, "JPEG")
        img_io.seek(0)
        
        await client.send_photo(message.chat.id, img_io, caption="✅ Stiker berhasil diubah menjadi foto!")
        
        if os.path.exists(path):
            os.remove(path)
        await message.delete()
    except Exception as e:
        await message.edit(f"❌ Error: {str(e)}")
