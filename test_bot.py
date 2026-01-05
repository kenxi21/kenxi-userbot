import asyncio
import sys
from pyrogram import Client

print("Testing imports...")
try:
    from userbot.handlers import install_ubot_handlers
    print("✅ userbot.handlers imported successfully")
except Exception as e:
    print(f"❌ Error importing userbot.handlers: {e}")
    sys.exit(1)

try:
    from helper.bot import HelperManager
    print("✅ helper.bot imported successfully")
except Exception as e:
    print(f"❌ Error importing helper.bot: {e}")
    sys.exit(1)

print("\nTesting HelperManager initialization...")
try:
    helper = HelperManager()
    print("✅ HelperManager created successfully")
except Exception as e:
    print(f"❌ Error creating HelperManager: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nTesting database initialization...")
try:
    helper.init_db()
    print("✅ Database initialized successfully")
except Exception as e:
    print(f"❌ Error initializing database: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nTesting handler setup...")
try:
    helper.setup_handlers()
    print("✅ Handlers setup successfully")
except Exception as e:
    print(f"❌ Error setting up handlers: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ All tests passed! Bot should work fine.")
print("Now starting the actual bot...")
print()

async def main():
    print("[INFO] Starting Helper Bot...")
    try:
        await helper.bot.start()
        print("[INFO] ✅ Helper Bot is online!")
        
        print("[INFO] Starting all registered userbots...")
        await helper.start_all_userbots()
        print("[INFO] ✅ All userbots started!")
        
        print("\n[INFO] Bot is running. Press Ctrl+C to stop.")
        await asyncio.sleep(float('inf'))
    except Exception as e:
        print(f"[ERROR] Error during bot execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("╔════════════════════════════════════════════╗")
    print("║        KENXI USERBOT - @kenxiubot          ║")
    print("╚════════════════════════════════════════════╝\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[INFO] Shutdown signal received. Stopping gracefully...")
    except Exception as e:
        print(f"[ERROR] Critical error: {e}")
        import traceback
        traceback.print_exc()
