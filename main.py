import aiohttp
import asyncio
import aiogram
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.settings import settings
import os
import logging
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename="logs.log",
                    filemode="a",
                    )

logs = logging.getLogger(__name__)

@dp.message(CommandStart())
async def start_handler(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 GitHub", url="https://github.com/CleanInit")]
    ])
    await message.answer(f"Привет, {message.from_user.full_name}! Вы запустили бота по мониторингу статусов сайтов!", reply_markup=keyboard)

async def _fetch_status(session: aiohttp.ClientSession, page_url: str):
    try:
        async with session.get(page_url) as response:
            logs.debug(f"{page_url} - вернул статус {response.status}")
            
            return response.status
    except Exception as e:
        logs.error(f"Ошибка при попытке получить статус {page_url}\n{e}")
        return -1

async def _task_monitoring(page_urls: list, admin_id: int, schedule_seconds: int, error_status_send: bool, approved_status_send: bool, error_status: list, approved_status: list):
    async with aiohttp.ClientSession() as session:
        site_statuses = {}
        while True:
            for page_url in page_urls:
                status = await _fetch_status(session, page_url)
                
                if (site_statuses.get(page_url) != status) or (page_url not in site_statuses):
                    text = f"<blockquote>{page_url} - изменил статус на {status}!</blockquote>"
                    if status in error_status and error_status_send:
                        await bot.send_message(admin_id, text)
                    elif status in approved_status and approved_status_send:
                        await bot.send_message(admin_id, text)

                    site_statuses[page_url] = status
            await asyncio.sleep(schedule_seconds)

async def main():
    st = settings()
    setting = st._load_settings()
    page_urls = setting.get("page_urls")
    settings_status = setting.get("status")
    settings_bot = setting.get("bot")
    
    schedule_seconds = setting.get("schedule_seconds") 

    admin_id = settings_bot.get("admin_id")
    error_status_send = settings_bot.get("error_status_send")
    approved_status_send = settings_bot.get("approved_status_send")
    
    error_status = settings_status.get("error_status")
    approved_status = settings_status.get("approved_status")

    asyncio.create_task(_task_monitoring(
        page_urls=page_urls, 
        admin_id=admin_id, 
        schedule_seconds=schedule_seconds, 
        error_status_send=error_status_send, 
        approved_status_send=approved_status_send, 
        error_status=error_status, 
        approved_status=approved_status))

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logs.info(f"Завершение работы программы.")
        exit(0)
    except Exception as e:
        print(e)
