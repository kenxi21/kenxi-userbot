import asyncio
import random
from pyrogram.errors import FloodWait

# Animation Speeds
ANIMATION_SPEED_FAST = 0.4
ANIMATION_SPEED_NORMAL = 0.3
ANIMATION_SPEED_SLOW = 0.2

stop_anim_tasks = {}

async def run_anim(client, message, frames, speed=0.5):
    user_id = client.me.id
    stop_anim_tasks[user_id] = False

    for frame in frames:
        if stop_anim_tasks.get(user_id):
            break

        try:
            await message.edit(frame)
            await asyncio.sleep(speed)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception as e:
            print(f"[ERROR] Animation error: {e}")
            break



async def superdino_anim(client, message):
    frames = [
        "🦖", "🦖💨", "💨🦖", "💨🦖💨", "🦖💨💨", "⚡🦖⚡", "✨🦖✨", "🔥🦖🔥",
        "💥🐲💥", "🔥🐲🔥", "✨🐲✨", "🐲☁️", "🐲☁️☁️", "🔥🔥🔥🐲", "🔥🔥🔥🔥🐲",
        "⚡🔥🐲🔥⚡", "✨⚡🐲⚡✨", "🏆🐲🏆", "✨🏆🐲🏆✨", "🎉✨🏆🐲🏆✨🎉"
    ]
    await run_anim(client, message, frames, speed=ANIMATION_SPEED_FAST)

async def lucu_anim(client, message):
    frames = ["🤪", "😜", "🤡", "👻", "🐵", "🤸", "🎈", "🤪✨"]
    await run_anim(client, message, frames, ANIMATION_SPEED_NORMAL)

async def keren_anim(client, message):
    frames = ["😎", "💎", "🔥", "⚡", "🎸", "🛸", "🕶️", "🔥✨"]
    await run_anim(client, message, frames, ANIMATION_SPEED_NORMAL)

async def marah_anim(client, message):
    frames = ["😠", "😡", "🤬", "💢", "💥", "💣", "🔥", "👹"]
    await run_anim(client, message, frames, ANIMATION_SPEED_NORMAL)

async def sedih_anim(client, message):
    frames = ["😔", "😢", "😭", "💔", "🌧️", "🥀", "😿", "💧"]
    await run_anim(client, message, frames, ANIMATION_SPEED_NORMAL)

async def ketawa_anim(client, message):
    frames = ["🙂", "😀", "😄", "😆", "😅", "😂", "🤣", "💀"]
    await run_anim(client, message, frames, ANIMATION_SPEED_NORMAL)

async def heart_anim(client, message):
    frames = ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎", "❤️"]
    await run_anim(client, message, frames, ANIMATION_SPEED_NORMAL)

async def load_anim(client, message):
    frames = [f"**Loading:** [{'■'*i}{'□'*(10-i)}] {i*10}%" for i in range(11)]
    frames.append("**LOADING COMPLETE!** ✅")
    await run_anim(client, message, frames, speed=ANIMATION_SPEED_SLOW)

async def moon_anim(client, message):
    frames = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
    await run_anim(client, message, frames, ANIMATION_SPEED_NORMAL)

async def clock_anim(client, message):
    frames = ["🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚", "🕛"]
    await run_anim(client, message, frames, ANIMATION_SPEED_SLOW)



async def bomb_anim(client, message):
    frames = ["💣", "💥", "🔥", "💨", "🌚"]
    await run_anim(client, message, frames, 0.4)

async def rocket_anim(client, message):
    frames = ["🚀", "🚀💨", "🚀☁️", "🚀✨", "🛸"]
    await run_anim(client, message, frames, 0.3)

async def police_anim(client, message):
    frames = ["🚓", "🚓💨", "🚓🚨", "🚨🚓", "🚔"]
    await run_anim(client, message, frames, 0.3)

async def airplane_anim(client, message):
    frames = ["✈️", "🛫", "🛬", "🛸", "🚀"]
    await run_anim(client, message, frames, 0.5)

async def car_anim(client, message):
    frames = ["🚗", "🚗💨", "🏎️", "🏎️💨", "🏁"]
    await run_anim(client, message, frames, 0.3)

async def bike_anim(client, message):
    frames = ["🚲", "🛵", "🏍️", "🏎️", "🚀"]
    await run_anim(client, message, frames, 0.4)

async def ufo_anim(client, message):
    frames = ["🛸", "🛸✨", "🛸👾", "👾", "☄️"]
    await run_anim(client, message, frames, 0.4)

async def ghost_anim(client, message):
    frames = ["👻", "💀", "🎃", "👻✨", "🧛"]
    await run_anim(client, message, frames, 0.4)

async def cat_anim(client, message):
    frames = ["🐱", "🐈", "🐾", "😽", "😻"]
    await run_anim(client, message, frames, 0.5)

async def dog_anim(client, message):
    frames = ["🐶", "🐕", "🐾", "🦴", "🐕‍🦺"]
    await run_anim(client, message, frames, 0.5)

async def monkey_anim(client, message):
    frames = ["🐵", "🐒", "🍌", "🙈", "🙉", "🙊"]
    await run_anim(client, message, frames, 0.4)

async def dragon_anim(client, message):
    frames = ["🐉", "🐲", "🔥", "🔥🐲🔥", "🐲💨"]
    await run_anim(client, message, frames, 0.4)

async def rain_anim(client, message):
    frames = ["☁️", "🌧️", "⛈️", "⛈️⚡", "🌈"]
    await run_anim(client, message, frames, 0.6)

async def snow_anim(client, message):
    frames = ["☁️", "🌨️", "❄️", "☃️", "🏔️"]
    await run_anim(client, message, frames, 0.6)

async def thunder_anim(client, message):
    frames = ["☁️", "⚡", "🌩️", "⛈️", "⚡⚡"]
    await run_anim(client, message, frames, 0.3)

async def earth_anim(client, message):
    frames = ["🌍", "🌎", "🌏", "🗺️", "🌑"]
    await run_anim(client, message, frames, 0.7)

async def star_anim(client, message):
    frames = ["⭐", "🌟", "✨", "💫", "🌠"]
    await run_anim(client, message, frames, 0.4)

async def fire_anim(client, message):
    frames = ["🔥", "💥", "☄️", "🌋", "☀️"]
    await run_anim(client, message, frames, 0.3)

async def money_anim(client, message):
    frames = ["💸", "💰", "💵", "💎", "💳", "🤑"]
    await run_anim(client, message, frames, 0.4)

async def beer_anim(client, message):
    frames = ["🍺", "🍻", "🥂", "🍷", "🍹", "🥴"]
    await run_anim(client, message, frames, 0.4)

async def food_anim(client, message):
    frames = ["🍕", "🍔", "🍟", "🌭", "🍣", "😋"]
    await run_anim(client, message, frames, 0.5)

async def boxing_anim(client, message):
    frames = ["🥊", "👊", "💥", "💢", "😵"]
    await run_anim(client, message, frames, 0.3)

async def ball_anim(client, message):
    frames = ["⚽", "🏀", "🏈", "🎾", "🏐", "🥅"]
    await run_anim(client, message, frames, 0.4)

async def music_anim(client, message):
    frames = ["🎵", "🎶", "🎸", "🎹", "🎺", "🎧"]
    await run_anim(client, message, frames, 0.4)

async def dance_anim(client, message):
    frames = ["💃", "🕺", "👯", "👯‍♂️", "✨"]
    await run_anim(client, message, frames, 0.4)

async def robot_anim(client, message):
    frames = ["🤖", "🦿", "🦾", "👾", "📡"]
    await run_anim(client, message, frames, 0.4)

async def phone_anim(client, message):
    frames = ["📱", "📲", "📞", "☎️", "📟"]
    await run_anim(client, message, frames, 0.5)

async def letter_anim(client, message):
    frames = ["✉️", "📩", "📧", "📨", "📬"]
    await run_anim(client, message, frames, 0.5)

async def key_anim(client, message):
    frames = ["🔑", "🗝️", "🔓", "🔒", "🔐"]
    await run_anim(client, message, frames, 0.5)

async def firework_anim(client, message):
    frames = ["🎆", "🎇", "✨", "🎉", "🎊"]
    await run_anim(client, message, frames, 0.4)

async def bday_anim(client, message):
    frames = ["🎂", "🍰", "🧁", "🎁", "🎈", "🥳"]
    await run_anim(client, message, frames, 0.5)

async def sleep_anim(client, message):
    frames = ["😴", "💤", "🛌", "🌚", "🌅"]
    await run_anim(client, message, frames, 0.8)

async def ninja_anim(client, message):
    frames = ["🥷", "🗡️", "⚔️", "💨", "👤"]
    await run_anim(client, message, frames, 0.4)

async def uub_anim(client, message):
    frames = ["👻", "👽", "👾", "🤖", "👹"]
    await run_anim(client, message, frames, 0.4)

async def wave_anim(client, message):
    frames = ["🌊", "🏄", "🏖️", "🏝️", "☀️"]
    await run_anim(client, message, frames, 0.5)

async def tree_anim(client, message):
    frames = ["🌱", "🌿", "🌳", "🌲", "🍂"]
    await run_anim(client, message, frames, 0.6)

async def sun_anim(client, message):
    frames = ["🌅", "☀️", "🌤️", "🌇", "🌆"]
    await run_anim(client, message, frames, 0.7)

async def ocean_anim(client, message):
    frames = ["🐳", "🐋", "🐬", "🐟", "🐠", "🐡"]
    await run_anim(client, message, frames, 0.5)

async def game_anim(client, message):
    frames = ["🎮", "🕹️", "👾", "👾💥", "🏆"]
    await run_anim(client, message, frames, 0.4)

async def tv_anim(client, message):
    frames = ["📺", "🎞️", "🎬", "🍿", "🎟️"]
    await run_anim(client, message, frames, 0.6)

async def tools_anim(client, message):
    frames = ["🔨", "🪚", "🔧", "🪛", "⚙️"]
    await run_anim(client, message, frames, 0.5)

async def microscope_anim(client, message):
    frames = ["🔬", "🧪", "🧬", "⚗️", "🎓"]
    await run_anim(client, message, frames, 0.5)

async def space_anim(client, message):
    frames = ["🪐", "🛸", "☄️", "🌠", "🌌"]
    await run_anim(client, message, frames, 0.5)

async def medical_anim(client, message):
    frames = ["🏥", "🚑", "🩺", "💉", "💊", "🩹"]
    await run_anim(client, message, frames, 0.5)

async def workout_anim(client, message):
    frames = ["🏋️", "🚴", "🏃", "🤾", "🛹"]
    await run_anim(client, message, frames, 0.4)

async def travel_anim(client, message):
    frames = ["🌍", "✈️", "🚢", "🏔️", "🗼", "🗽"]
    await run_anim(client, message, frames, 0.6)

async def magic_anim(client, message):
    frames = ["🪄", "✨", "🎩", "🐇", "🃏"]
    await run_anim(client, message, frames, 0.4)

async def weather_anim(client, message):
    frames = ["☀️", "🌤️", "☁️", "🌧️", "⛈️", "🌩️"]
    await run_anim(client, message, frames, 0.6)

async def flags_anim(client, message):
    frames = ["🏁", "🚩", "🏴", "🏳️", "🌈"]
    await run_anim(client, message, frames, 0.5)

async def colors_anim(client, message):
    frames = ["🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "⚪", "⚫"]
    await run_anim(client, message, frames, 0.4)
