import asyncio
import sys
import os
from pyrogram import Client
from userbot.handlers import install_ubot_handlers
from helper.bot import HelperManager

API_ID = 31874382
API_HASH = "b9c499220c85a8a51a10c15bf2565e96"
BOT_TOKEN = "8389698571:AAHxIN-uKPvN4S94omKjhi1X_hftDwG-qYM"

IS_TERMUX = os.path.exists('/data/data/com.termux')
if IS_TERMUX:
    os.environ['SSL_CERT_FILE'] = '/data/data/com.termux/files/usr/etc/tls/cert.pem'
    print("[INFO] Running in Termux environment")

def suppress_pyrogram_errors(loop, context):
    """Suppress peer resolution errors from Pyrogram"""
    exception = context.get('exception')
    if exception:
        error_msg = str(exception)
        if 'ID not found' in error_msg or 'Peer id invalid' in error_msg:
            return
    
    # Log other errors normally
    if 'message' in context:
        print(f"[ASYNC ERROR] {context['message']}")
    if exception:
        print(f"[EXCEPTION] {exception}")

def check_imports():
    try:
        print("[INIT] Checking imports...")
        from userbot.handlers import install_ubot_handlers
        from helper.bot import HelperManager
        print("[INIT] ✅ All imports successful")
        return True
    except Exception as e:
        print(f"[ERROR] Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

helper = None

async def main():
    global helper
    
    try:
        print("[STEP 1/4] Initializing HelperManager...")
        helper = HelperManager()
        helper.init_db()
        print("[STEP 1/4] ✅ Manager & Database Ready")
    except Exception as e:
        print(f"[ERROR] Init failed: {e}")
        return

    try:
        print("[STEP 2/4] Setting up bot handlers...")
        helper.setup_handlers()
        print("[STEP 2/4] ✅ Handlers Configured")
    except Exception as e:
        print(f"[ERROR] Handlers failed: {e}")
        return

    try:
        print("[STEP 3/4] Starting Helper Bot...")
        await helper.bot.start()
        me = await helper.bot.get_me()
        print(f"[STEP 3/4] ✅ Assistant: @{me.username}")
    except Exception as e:
        print(f"[ERROR] Helper Bot failed: {e}")
        return

    try:
        print("[STEP 4/4] Parallel Booting Userbots...")
        # start_all_userbots now handles its own summary logging
        await helper.start_all_userbots()
    except Exception as e:
        print(f"[ERROR] Userbot boot failed: {e}")

    print("\n" + "="*50)
    print("🚀 KENXI USERBOT IS NOW RUNNING!")
    print("="*50)
    print("� Command support: /start in Assistant Bot")
    print("⚠️  Press Ctrl+C to stop")
    print("="*50 + "\n")
    
    try:
        await asyncio.sleep(float('inf'))
    except asyncio.CancelledError:
        print("\n[INFO] Shutting down...")

if __name__ == "__main__":
    # Optimize for Windows (Proactor support for more socket handles)
    if os.name == 'nt' and hasattr(asyncio, 'WindowsProactorEventLoopPolicy'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    print("\n")
    print("╔════════════════════════════════════════════╗")
    print("║        KENXI USERBOT - @kenxiubot          ║")
    print("║              King of Ubot                  ║")
    print("╚════════════════════════════════════════════╝")
    print("\n")
    
    if not check_imports():
        print("\n[FATAL] Import check failed.")
        sys.exit(1)
    
    try:
        loop = asyncio.get_event_loop()
        loop.set_exception_handler(suppress_pyrogram_errors)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Goodbye!")
    except Exception as e:
        print(f"\n[FATAL] {e}")
        sys.exit(1)
