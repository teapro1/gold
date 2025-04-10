import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Thông tin cấu hình
TELEGRAM_TOKEN = "7693032578:AAHIfmBIzhSklkKgP5VhsVFy8PLioPxj5IQ"
CHAT_ID = "6998063684"

# Cấu hình proxy
PROXIES = {
    "http": "http://118.69.7.30:15604",
    "https": "http://118.69.7.30:15604"
}

# Khởi tạo bot Telegram
bot = Bot(token=TELEGRAM_TOKEN)

def get_sjc_price():
    try:
        url = "https://sjc.com.vn/"
        response = requests.get(url, proxies=PROXIES, timeout=10)  # Sử dụng proxy
        soup = BeautifulSoup(response.text, "html.parser")

        # Tìm bảng giá vàng
        table = soup.find("table", class_="sjc-table-show-price")
        if not table:
            return "Không tìm thấy bảng giá vàng SJC."

        rows = table.find_all("tr")

        # Tìm giá mua và bán cho "Vàng SJC 1L, 10L, 1KG" tại Hồ Chí Minh
        for row in rows:
            cells = row.find_all("td")
            if len(cells) == 3 and "Vàng SJC 1L, 10L, 1KG" in cells[0].text:
                price_buy = cells[1].text.strip()
                price_sell = cells[2].text.strip()
                return f"Mua: {price_buy} VNĐ, Bán: {price_sell} VNĐ"

        return "Không tìm thấy thông tin giá vàng SJC."
    except Exception as e:
        return f"Lỗi khi lấy giá vàng SJC: {e}"

def get_pnj_price():
    try:
        url = "https://www.pnj.com.vn/"
        response = requests.get(url, timeout=10)  # Không sử dụng proxy
        soup = BeautifulSoup(response.text, "html.parser")

        # Tìm vị trí chứa giá vàng PNJ (cần xác định đúng class từ HTML thực tế)
        price_buy = soup.find("span", class_="price_buy_class").text.strip()
        price_sell = soup.find("span", class_="price_sell_class").text.strip()

        return f"Mua: {price_buy} VNĐ, Bán: {price_sell} VNĐ"
    except Exception as e:
        return f"Lỗi khi lấy giá vàng PNJ: {e}"

async def send_gold_prices():
    try:
        sjc_price = get_sjc_price()
        pnj_price = get_pnj_price()

        # Soạn nội dung tin nhắn
        message = f"📈 Giá vàng hôm nay:\n\n"
        message += f"🏅 SJC:\n{sjc_price}\n\n"
        message += f"🏅 PNJ:\n{pnj_price}\n"

        # Gửi tin nhắn qua Telegram
        await bot.send_message(chat_id=CHAT_ID, text=message)
        print("Đã gửi thông báo Telegram!")
    except Exception as e:
        print(f"Lỗi khi gửi tin nhắn: {e}")

async def main():
    print("Đang lấy giá vàng và gửi thông báo...")

    # Tạo lịch chạy định kỳ
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_gold_prices, 'interval', minutes=5)  # Lặp lại mỗi 5 phút

    # Bắt đầu scheduler trong event loop hiện tại
    scheduler.start()

    # Giữ chương trình chạy mãi
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())  # Sử dụng asyncio.run để khởi động event loop
    except KeyboardInterrupt:
        print("Chương trình đã bị hủy.")
