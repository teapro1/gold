import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot
import requests

# Cấu hình
GOLD_API_KEY = "goldapi-1223k519m9b4ams6-io"
TELEGRAM_TOKEN = "7693032578:AAHIfmBIzhSklkKgP5VhsVFy8PLioPxj5IQ"
CHAT_ID = "6998063684"
TARGET_PRICE_VND = 80000000
CHECK_INTERVAL_MINUTES = 1  # Kiểm tra mỗi phút
EXCHANGE_RATE = 23500  # Tỷ giá USD -> VNĐ

# API URLs
GOLD_API_URL = "https://www.goldapi.io/api/XAU/USD"

# Tạo bot Telegram
bot = Bot(token=TELEGRAM_TOKEN)

async def get_gold_price():
    headers = {"x-access-token": GOLD_API_KEY, "Content-Type": "application/json"}
    try:
        response = requests.get(GOLD_API_URL, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("price", None)
    except Exception as e:
        print(f"Lỗi khi lấy giá vàng: {e}")
        return None

async def send_telegram_message(message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"Lỗi khi gửi thông báo Telegram: {e}")

async def check_gold_price():
    price_usd = await get_gold_price()
    if price_usd:
        price_vnd = price_usd * EXCHANGE_RATE
        print(f"Giá vàng hiện tại: {price_vnd:,.0f} VNĐ")
        if price_vnd <= TARGET_PRICE_VND:
            await send_telegram_message(f"⚠️ Giá vàng đã giảm xuống: {price_vnd:,.0f} VNĐ!")

async def main():
    print("Dịch vụ đang chạy...")
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_gold_price, 'interval', minutes=CHECK_INTERVAL_MINUTES)
    scheduler.start()

    # Giữ chương trình chạy
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
