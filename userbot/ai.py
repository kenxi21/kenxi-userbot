import aiohttp
import urllib.parse
from pyrogram import filters

OPENROUTER_API_KEY = "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"

async def get_ai_response(model, prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "xiaomi/mimo-v2-flash:free",
        "messages": [
            {"role": "system", "content": f"You are {model.upper()} assistant. Give fast, concise answers in Indonesian."},
            {"role": "user", "content": prompt}
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload, timeout=30) as response:
            try:
                data = await response.json()
                if response.status == 200:
                    res_text = data["choices"][0]["message"]["content"]
                    if len(res_text) > 4000:
                        res_text = res_text[:3990] + "..."
                    return res_text
                error = data.get("error", {})
                return f"⚠️ OpenRouter Error: {error.get('message', 'Terjadi kesalahan sistem.')}"
            except Exception:
                return "⚠️ Gagal terhubung ke layanan OpenRouter."

async def gemini_handler(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ **Gunakan:** `.gemini [pertanyaan]`\nContoh: `.gemini Apa itu Python?`")
    
    prompt = message.text.split(None, 1)[1]
    await message.edit("🤖 **Gemini sedang berpikir...**")
    
    response = await get_ai_response("gemini", prompt)
    await message.edit(f"🤖 **GEMINI AI**\n━━━━━━━━━━━━━━━━━━\n\n{response}")

async def gpt_handler(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ **Gunakan:** `.gpt [pertanyaan]`\nContoh: `.gpt Buatkan kode Hello World`")
    
    prompt = message.text.split(None, 1)[1]
    await message.edit("🤖 **ChatGPT sedang berpikir...**")
    
    response = await get_ai_response("chatgpt", prompt)
    await message.edit(f"🤖 **CHATGPT**\n━━━━━━━━━━━━━━━━━━\n\n{response}")

async def claude_handler(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ **Gunakan:** `.claude [pertanyaan]`\nContoh: `.claude Jelaskan tentang kuantum`")
    
    prompt = message.text.split(None, 1)[1]
    await message.edit("🤖 **Claude sedang berpikir...**")
    
    response = await get_ai_response("claude", prompt)
    await message.edit(f"🤖 **CLAUDE AI**\n━━━━━━━━━━━━━━━━━━\n\n{response}")

async def perplexity_handler(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ **Gunakan:** `.pplx [pertanyaan]`\nContoh: `.pplx Berikan berita terbaru teknologi`")
    
    prompt = message.text.split(None, 1)[1]
    await message.edit("🤖 **Perplexity sedang mencari jawaban...**")
    
    response = await get_ai_response("perplexity", prompt)
    await message.edit(f"🤖 **PERPLEXITY AI**\n━━━━━━━━━━━━━━━━━━\n\n{response}")
