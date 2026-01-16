from pyrogram import filters, enums
from pyrogram.types import Message
import asyncio

async def get_user(message: Message, text: str):
    if message.reply_to_message:
        return message.reply_to_message.from_user
    if len(text.split()) > 1:
        user_info = text.split(None, 1)[1]
        try:
            return await message._client.get_users(user_info)
        except Exception:
            return None
    return None

async def kick_handler(client, message):
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.edit("❌ Fitur ini hanya untuk grup.")
    
    me = await client.get_chat_member(message.chat.id, "me")
    if not me.privileges or not me.privileges.can_restrict_members:
        return await message.edit("❌ Saya bukan admin atau tidak punya izin kick.")
    
    user = await get_user(message, message.text)
    if not user:
        return await message.edit("❌ Balas pesan user atau sebutkan ID/Username.")
    
    try:
        await client.ban_chat_member(message.chat.id, user.id)
        await client.unban_chat_member(message.chat.id, user.id)
        await message.edit(f"✅ **{user.first_name}** berhasil di-kick.")
    except Exception as e:
        await message.edit(f"❌ Gagal: {str(e)}")

async def ban_handler(client, message):
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.edit("❌ Fitur ini hanya untuk grup.")
    
    me = await client.get_chat_member(message.chat.id, "me")
    if not me.privileges or not me.privileges.can_restrict_members:
        return await message.edit("❌ Saya bukan admin atau tidak punya izin ban.")
    
    user = await get_user(message, message.text)
    if not user:
        return await message.edit("❌ Balas pesan user atau sebutkan ID/Username.")
    
    try:
        await client.ban_chat_member(message.chat.id, user.id)
        await message.edit(f"✅ **{user.first_name}** berhasil di-ban.")
    except Exception as e:
        await message.edit(f"❌ Gagal: {str(e)}")

async def mute_handler(client, message):
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.edit("❌ Fitur ini hanya untuk grup.")
    
    me = await client.get_chat_member(message.chat.id, "me")
    if not me.privileges or not me.privileges.can_restrict_members:
        return await message.edit("❌ Saya bukan admin atau tidak punya izin mute.")
    
    user = await get_user(message, message.text)
    if not user:
        return await message.edit("❌ Balas pesan user atau sebutkan ID/Username.")
    
    try:
        await client.restrict_chat_member(message.chat.id, user.id, enums.ChatPermissions())
        await message.edit(f"✅ **{user.first_name}** berhasil di-mute.")
    except Exception as e:
        await message.edit(f"❌ Gagal: {str(e)}")

async def unmute_handler(client, message):
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.edit("❌ Fitur ini hanya untuk grup.")
    
    me = await client.get_chat_member(message.chat.id, "me")
    if not me.privileges or not me.privileges.can_restrict_members:
        return await message.edit("❌ Saya bukan admin atau tidak punya izin unmute.")
    
    user = await get_user(message, message.text)
    if not user:
        return await message.edit("❌ Balas pesan user atau sebutkan ID/Username.")
    
    try:
        await client.unban_chat_member(message.chat.id, user.id)
        await message.edit(f"✅ **{user.first_name}** berhasil di-unmute.")
    except Exception as e:
        await message.edit(f"❌ Gagal: {str(e)}")

async def zombie_handler(client, message):
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.edit("❌ Fitur ini hanya untuk grup.")
    
    me = await client.get_chat_member(message.chat.id, "me")
    if not me.privileges or not me.privileges.can_restrict_members:
        return await message.edit("❌ Saya bukan admin atau tidak punya izin moderasi.")
    
    await message.edit("🔍 **Mencari akun terhapus...**")
    count = 0
    async for member in client.get_chat_members(message.chat.id):
        if member.user.is_deleted:
            try:
                await client.ban_chat_member(message.chat.id, member.user.id)
                await client.unban_chat_member(message.chat.id, member.user.id)
                count += 1
            except Exception:
                continue
    
    if count > 0:
        await message.edit(f"✅ Berhasil mengeluarkan **{count}** akun terhapus.")
    else:
        await message.edit("✅ Tidak ditemukan akun terhapus di grup ini.")

async def tagall_handler(client, message):
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.edit("❌ Fitur ini hanya untuk grup.")
    
    await message.delete()
    
    args = message.text.split(None, 1)
    tag_msg = args[1] if len(args) > 1 else "📢 Pemberitahuan!"
    
    members = []
    async for member in client.get_chat_members(message.chat.id):
        if not member.user.is_bot and not member.user.is_deleted:
            members.append(member.user.mention())
    
    for i in range(0, len(members), 5):
        chunk = members[i:i+5]
        mention_text = f"{tag_msg}\n\n" + " ".join(chunk)
        await client.send_message(message.chat.id, mention_text)
        await asyncio.sleep(1.5)
