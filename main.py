import asyncio
import sys
import os
import signal
import subprocess
from pyrogram import Client
from userbot.handlers import install_ubot_handlers
from helper.bot import HelperManager

API_ID = 31874382
API_HASH = "b9c499220c85a8a51a10c15bf2565e96"
BOT_TOKEN = "8389698571:AAHxIN-uKPvN4S94omKjhi1X_hftDwG-qYM"

def check_imports():
    try:
        from userbot.handlers import install_ubot_handlers
        from helper.bot import HelperManager
        return True
    except Exception as e:
        print(f"[ERROR] Import failed: {e}")
        return False

def check_environment():
    print("[INIT] Detecting environment...")
    is_termux = os.path.exists("/data/data/com.termux/files/usr/bin/python")
    if is_termux:
        print("[INIT] 📱 Termux platform detected")
    
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[INIT] ✅ FFmpeg found")
    except FileNotFoundError:
        print("[WARN] ⚠️ FFmpeg NOT found!")
        if is_termux:
            print("[TIP] Please run: pkg install ffmpeg")
        else:
            print("[TIP] Please install FFmpeg for sticker & video features")
    
    return is_termux

helper = None

async def main():
    global helper
    
    is_termux = check_environment()
    os.environ["IS_TERMUX"] = "1" if is_termux else "0"
    
    try:
        print("[STEP 1/5] Initializing HelperManager...")
        helper = HelperManager()
        print("[STEP 1/5] ✅ HelperManager initialized")
    except Exception as e:
        print(f"[ERROR] Failed to initialize HelperManager: {e}")
        import traceback
        traceback.print_exc()
        return

    try:
        print("[STEP 2/5] Initializing database...")
        helper.init_db()
        print("[STEP 2/5] ✅ Database initialized")
    except Exception as e:
        print(f"[ERROR] Failed to initialize database: {e}")
        print("[TIP] Try deleting database folder and restart if error persists")
        import traceback
        traceback.print_exc()
        return

    try:
        print("[STEP 3/5] Setting up helper bot handlers...")
        helper.setup_handlers()
        print("[STEP 3/5] ✅ Handlers configured")
    except Exception as e:
        print(f"[ERROR] Failed to setup handlers: {e}")
        import traceback
        traceback.print_exc()
        return

    try:
        print("[STEP 4/5] Starting Helper Bot...")
        await helper.bot.start()
        me = await helper.bot.get_me()
        print(f"[STEP 4/5] ✅ Helper Bot online as @{me.username}")
    except Exception as e:
        print(f"[ERROR] Failed to start Helper Bot: {e}")
        print("[TIP] Check your BOT_TOKEN is valid")
        import traceback
        traceback.print_exc()
        return

    try:
        print("[STEP 5/5] Starting all registered userbots...")
        await helper.start_all_userbots()
        print(f"[STEP 5/5] ✅ {len(helper.active_userbots)} userbot(s) started")
    except Exception as e:
        print(f"[ERROR] Failed to start userbots: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*50)
    print("🚀 KENXI USERBOT IS NOW RUNNING!")
    print("="*50)
    print(f"📱 Helper Bot: @{me.username if 'me' in locals() else 'Unknown'}")
    print(f"👥 Active Userbots: {len(helper.active_userbots)}")
    print("💡 Type /start in the bot to begin")
    print("⚠️  Press Ctrl+C to stop")
    print("="*50 + "\n")
    
    try:
        while True:
            await asyncio.sleep(3600)
    except (asyncio.CancelledError, KeyboardInterrupt):
        print("\n[INFO] Shutting down...")
        if helper:
            for phone, ubot in list(helper.active_userbots.items()):
                try:
                    await ubot.stop()
                except:
                    pass
            await helper.bot.stop()

if __name__ == "__main__":
    print("\n")
    print("╔════════════════════════════════════════════╗")
    print("║        KENXI USERBOT - @kenxiubot          ║")
    print("║              King of Ubot                  ║")
    print("╚════════════════════════════════════════════╝")
    print("\n")
    
    if not check_imports():
        print("\n[FATAL] Import check failed. Please install requirements:")
        print("        pip install -r requirements.txt")
        sys.exit(1)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n")
        print("="*50)
        print("👋 SHUTDOWN COMPLETE")
        print("="*50)
        print("✅ Helper Bot stopped")
        print("✅ All userbots stopped")
        print("✅ Database connections closed")
        print("\nThank you for using KENXI Userbot!")
        print("="*50)
    except Exception as e:
        print("\n")
        print("="*50)
        print("❌ CRITICAL ERROR")
        print("="*50)
        print(f"Error: {e}")
        print("\nFull traceback:")
        import traceback
        traceback.print_exc()
        print("\n[TIP] Common solutions:")
        print("  1. Delete 'database' folder and restart")
        print("  2. Check your API credentials")
        print("  3. Ensure no other instances are running")
        print("  4. Reinstall: pip install -r requirements.txt")
        print("="*50)
        sys.exit(1)