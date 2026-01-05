import aiohttp
import urllib.parse
from pyrogram import filters

async def get_ai_response(model, prompt):
    base_url = "https://api.gimita.id/api/ai/gpt5"
    query = urllib.parse.urlencode({
        "text": prompt
    })
    url = f"{base_url}?{query}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=30) as resp:
                if resp.status != 200:
                    return "⚠️ AI tidak merespons."

                data = await resp.json()

                if isinstance(data, dict):
                    result = data.get("result") or data.get("response") or data.get("answer")
                    if not result:
                        return "⚠️ Respons AI kosong."

                    if len(result) > 4000:
                        result = result[:3990] + "..."

                    return result

                return "⚠️ Format respons tidak dikenali."

    except Exception as e:
        return f"⚠️ Gagal menghubungi AI: {e}"

async def gemini_handler(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ Gunakan: `.gemini [pertanyaan]`")

    prompt = message.text.split(None, 1)[1]
    await message.edit("🤖 Gemini sedang berpikir...")

    response = await get_ai_response("gemini", prompt)
    await message.edit(f"🤖 GEMINI AI\n━━━━━━━━━━━━━━━━━━\n\n{response}")

async def gpt_handler(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ Gunakan: `.gpt [pertanyaan]`")

    prompt = message.text.split(None, 1)[1]
    await message.edit("🤖 ChatGPT sedang berpikir...")

    response = await get_ai_response("gpt", prompt)
    await message.edit(f"🤖 CHATGPT\n━━━━━━━━━━━━━━━━━━\n\n{response}")

async def claude_handler(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ Gunakan: `.claude [pertanyaan]`")

    prompt = message.text.split(None, 1)[1]
    await message.edit("🤖 Claude sedang berpikir...")

    response = await get_ai_response("claude", prompt)
    await message.edit(f"🤖 CLAUDE AI\n━━━━━━━━━━━━━━━━━━\n\n{response}")

async def perplexity_handler(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ Gunakan: `.pplx [pertanyaan]`")

    prompt = message.text.split(None, 1)[1]
    await message.edit("🤖 Perplexity sedang mencari jawaban...")

    response = await get_ai_response("perplexity", prompt)
    await message.edit(f"🤖 PERPLEXITY AI\n━━━━━━━━━━━━━━━━━━\n\n{response}")
