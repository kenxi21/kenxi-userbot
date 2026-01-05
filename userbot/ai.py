import aiohttp
import urllib.parse

async def fetch_ai(url, prompt, extra_params=None):
    params = {"text": prompt}
    if extra_params:
        params.update(extra_params)

    query = urllib.parse.urlencode(params)
    full_url = f"{url}?{query}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(full_url, timeout=30) as resp:
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

async def gpt_handler(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ Gunakan: `.gpt [pertanyaan]`")

    prompt = message.text.split(None, 1)[1]
    await message.edit("🤖 GPT-5 sedang berpikir...")

    response = await fetch_ai(
        "https://api.gimita.id/api/ai/gpt5",
        prompt
    )

    await message.edit(f"🤖 GPT-5\n━━━━━━━━━━━━━━━━━━\n\n{response}")

async def gemini_handler(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ Gunakan: `.gemini [pertanyaan]`")

    prompt = message.text.split(None, 1)[1]
    await message.edit("🤖 Gemini sedang berpikir...")

    response = await fetch_ai(
        "https://api.gimita.id/api/ai/gemini",
        prompt
    )

    await message.edit(f"🤖 GEMINI AI\n━━━━━━━━━━━━━━━━━━\n\n{response}")

async def claude_handler(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ Gunakan: `.claude [pertanyaan]`")

    prompt = message.text.split(None, 1)[1]
    await message.edit("🤖 Claude sedang berpikir...")

    response = await fetch_ai(
        "https://api.gimita.id/api/ai/claude",
        prompt
    )

    await message.edit(f"🤖 CLAUDE AI\n━━━━━━━━━━━━━━━━━━\n\n{response}")

async def perplexity_handler(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ Gunakan: `.pplx [pertanyaan]`")

    prompt = message.text.split(None, 1)[1]
    await message.edit("🤖 Perplexity sedang mencari jawaban...")

    response = await fetch_ai(
        "https://api.gimita.id/api/ai/chatai",
        prompt,
        {"model": "perplexity"}
    )

    await message.edit(f"🤖 PERPLEXITY AI\n━━━━━━━━━━━━━━━━━━\n\n{response}")
