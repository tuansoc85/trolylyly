import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
import google.generativeai as genai

# **QUAN TRỌNG:** Thay thế bằng API key của bot nina_votv_bot
TELEGRAM_BOT_TOKEN = "7679384872:AAHqaPmCyrwKSxy6buDbJBAokQ6aoVAU3CY"
# API key của Gemini sẽ được lấy từ biến môi trường trên Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Kiểm tra xem GEMINI_API_KEY có tồn tại không
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY environment variable not set. Gemini functionality will not work.")
    model = None  # Đặt model thành None nếu không có API key
else:
    # Khởi tạo mô hình Gemini
    genai.configure(api_key=GEMINI_API_KEY)
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        print(f"Error initializing Gemini model: {e}")
        model = None

async def start(update, context):
    await update.message.reply_text('Chào mừng bạn đến với bot Nina!')

async def handle_message(update, context):
    user_message = update.message.text
    chat_id = update.message.chat_id

    if model:
        try:
            response = model.generate_content(user_message)
            await context.bot.send_message(chat_id=chat_id, text=response.text)
        except Exception as e:
            print(f"Lỗi khi gọi Gemini API: {e}")
            await context.bot.send_message(chat_id=chat_id, text='Đã xảy ra lỗi khi xử lý yêu cầu của bạn.')
    else:
        await context.bot.send_message(chat_id=chat_id, text='Chức năng Gemini chưa được kích hoạt.')

async def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
