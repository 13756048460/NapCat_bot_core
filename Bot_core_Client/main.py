import asyncio
from dotenv import load_dotenv
import os

from Bot_core_Client import Bot

load_dotenv()
URL = os.getenv('URL')
TOKEN = os.getenv('TOKEN')
# URL=ws://127.0.0.1:3001
# URL=ws://172.16.0.2:3001

async def main():
    """主函数"""
    if not URL:
        print("Error: URL not found in environment variables.")
        return

    bot = Bot(url=URL, token=TOKEN, plugin_dir="plugins")
    await bot.run()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("程序已退出")
