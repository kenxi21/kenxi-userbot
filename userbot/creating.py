import os
import subprocess
from PIL import Image
import lottie

def _open_image(path):
    try:
        return Image.open(path)
    except Exception:
        return None

def _tgs_to_png(path, out="tgs_frame.png"):
    try:
        anim = lottie.importers.tgs.parse_tgs(path)
        frame = anim.render_frame(0)
        frame.save(out)
        return out
    except Exception:
        return None

def _webm_to_png(path, out="webm_frame.png"):
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", path, "-vframes", "1", out],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if os.path.exists(out):
            return out
        return None
    except Exception:
        return None

def open_sticker_as_image(path):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".webp":
        return _open_image(path)

    if ext == ".tgs":
        png = _tgs_to_png(path)
        if png:
            return _open_image(png)

    if ext == ".webm":
        png = _webm_to_png(path)
        if png:
            return _open_image(png)

    return None

async def toimg_handler(event):
    reply = await event.get_reply_message()
    if not reply:
        return await event.reply("❌ Reply sticker dulu.")

    path = await reply.download_media()
    if not path:
        return await event.reply("❌ Gagal download sticker.")

    img = open_sticker_as_image(path)
    if not img:
        return await event.reply("❌ Sticker ini tidak bisa diubah jadi foto.")

    out = "toimg.png"
    img.convert("RGBA").save(out)
    await event.reply(file=out)

async def kang_handler(event):
    reply = await event.get_reply_message()
    if not reply:
        return await event.reply("❌ Reply foto dulu.")

    path = await reply.download_media()
    if not path:
        return await event.reply("❌ Gagal download foto.")

    img = _open_image(path)
    if not img:
        return await event.reply("❌ File ini bukan foto.")

    img = img.convert("RGBA")
    img.thumbnail((512, 512))

    out = "kang.webp"
    img.save(out, "WEBP")
    await event.reply(file=out)
