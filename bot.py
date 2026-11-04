import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai

# Khởi tạo Gemini Client
client = genai.Client(api_key="AQ.Ab8RN6JxFrYOSvhyK3YSmb1KJ6k2FIkGH9YHG7v74UrlxeFhUg")

SYSTEM_INSTRUCTION = """
Bạn là một trợ lý dịch thuật thông minh, chuyên nghiệp và am hiểu sâu sắc văn hóa giao tiếp giữa người Việt và người Trung Quốc.
Nhiệm vụ của bạn:
1. Nếu người dùng gửi tiếng Việt -> Hãy dịch sang tiếng Trung (Trung Quốc đại lục, văn phong tự nhiên, hiện đại, đúng ngữ cảnh giao tiếp hàng ngày hoặc kinh doanh tùy câu).
2. Nếu người dùng gửi tiếng Trung -> Hãy dịch sang tiếng Việt (văn phong tự nhiên, trôi chảy, đúng ngữ cảnh đối thoại giữa người với người).
3. KHÔNG dịch máy móc từng từ. Hãy giữ nguyên sắc thái cảm xúc, ý nghĩa ẩn sau câu chữ và ngữ cảnh.
4. Chỉ trả về kết quả dịch trực tiếp, không kèm theo giải thích dài dòng trừ khi người dùng yêu cầu đặc biệt.
"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not user_text:
        return

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
            config={
                'system_instruction': SYSTEM_INSTRUCTION,
                'temperature': 0.3,
            }
        )
        
        translated_text = response.text
        await update.message.reply_text(translated_text)
        
    except Exception as e:
        await update.message.reply_text(f"⚠️ Có lỗi xảy ra khi dịch: {str(e)}")

if __name__ == '__main__':
    TOKEN = "9290671112:AAHCqdIXXHcmHfYKPTLtYs3FzrJHSXGTxM"
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("🤖 Bot dịch thuật thông minh đang chạy...")
    app.run_polling()
