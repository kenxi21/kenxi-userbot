from pyrogram import Client, filters
from pyrogram.types import Message

async def send_smart_response(client, message, query_type):
    try:
        if not hasattr(client, 'inline_manager'):
            return await message.edit("⚠️ **Assistant Bot Tidak Aktif!**\n\nSilakan login ulang dengan `/add` di Helper Bot.")

        bot_username = client.inline_manager.bot_username
        
        pass
        status = await message.edit(f"🔄 **Memanggil Menu...**")
        
        try:
            pass
            results = await client.get_inline_bot_results(bot_username, query_type)
            
            if results.results:
                await message.delete()
                
                pass
                await client.send_inline_bot_result(
                    message.chat.id, 
                    results.query_id, 
                    results.results[0].id
                )
            else:
                await status.edit("❌ **Error:** Tidak ada respon dari Assistant Bot.")
                
        except Exception as e:
             await status.edit(f"❌ **Gagal:** {e}")

    except Exception as e:
        await message.edit(f"❌ **Error Sistem:** {str(e)}")



async def alive_inline_handler(client, message):
    await send_smart_response(client, message, "alive")

async def help_inline_handler(client, message):
    await send_smart_response(client, message, "help")
