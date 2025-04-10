import requests

# URL API
api_url = "http://api.btmc.vn/api/BTMCAPI/getpricebtmc"
api_params = {
    "key": "3kd8ub1llcg9t45hnoh8hmn7t5kc2v"
}

# Telegram Bot Info
telegram_bot_token = "7693032578:AAHIfmBIzhSklkKgP5VhsVFy8PLioPxj5IQ"  # Thay bằng mã token của bạn
telegram_chat_id = "6998063684"  # Thay bằng ID chat hoặc nhóm Telegram của bạn

def send_to_telegram(message):
    """Gửi tin nhắn tới Telegram."""
    telegram_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    telegram_params = {
        "chat_id": telegram_chat_id,
        "text": message
    }
    response = requests.post(telegram_url, data=telegram_params)
    if response.status_code == 200:
        print("Tin nhắn đã được gửi đến Telegram.")
    else:
        print(f"Lỗi khi gửi tin nhắn: {response.status_code} - {response.text}")

try:
    # Gửi yêu cầu GET tới API
    response = requests.get(api_url, params=api_params)

    if response.status_code == 200:
        # Xử lý dữ liệu trả về
        data = response.json()
        messages = []

        for row in data.get("data", []):
            message = (
                f"Tên vàng: {row.get('n_1')}\n"
                f"Hàm lượng Kara: {row.get('k_1')}\n"
                f"Hàm lượng vàng: {row.get('h_1')}\n"
                f"Giá mua vào: {row.get('pb_1')}\n"
                f"Giá bán ra: {row.get('ps_1')}\n"
                f"Giá thế giới: {row.get('pt_1')}\n"
                f"Thời gian cập nhật: {row.get('d_1')}\n"
                "----------------------------------------"
            )
            messages.append(message)

        # Gửi từng tin nhắn tới Telegram
        for msg in messages:
            send_to_telegram(msg)

    else:
        print(f"Lỗi API: {response.status_code} - {response.text}")
        send_to_telegram(f"Lỗi API: {response.status_code} - Không thể lấy giá vàng.")

except Exception as e:
    error_message = f"Có lỗi xảy ra: {e}"
    print(error_message)
    send_to_telegram(error_message)
