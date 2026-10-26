import os
import random
import asyncio
from datetime import datetime
import threading
requests = __import__('requests')
from google import genai
from flask import Flask

# إعداد سيرفر ويب وهمي لإرضاء متطلبات منصة Render المجانية
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Telegram AI Bot is running smoothly!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# سحب المفاتيح بأمان
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"خطأ في إرسال الرسالة: {e}")

def generate_smart_prompt():
    prompt = (
        "أنت صديق ذكي ومقرب ومبرمج محترف. "
        "مهمتك أن ترسل رسالة قصيرة تفقدية لصديقك (وهو شاب مهتم بالبرمجة وأنظمة لينكس والتقنية). "
        "نوع في الأساليب: مرة اسأله عن مشروعه البرمجي الحالي، مرة اطرح عليه تحدي برمجي بسيط، ومرة تفقد أحواله بيومه بلطافة. "
        "اكتب الرسالة باللهجة العامية اللطيفة والمحفزة، وبدون مقدمات طويلة."
    )
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"خطأ في توليد الذكاء الاصطناعي: {e}")
        return "ها يا وحش، كيف ماشي نهارك؟ شو انجزت اليوم بالبرمجة؟"

async def smart_scheduler():
    print("🤖 بوت الاستفقاد الذكي بدأ بالعمل...")
    while True:
        now = datetime.now()
        current_hour = now.hour
        
        if 10 <= current_hour <= 23:
            message = generate_smart_prompt()
            send_telegram_message(message)
            print(f"تم إرسال رسالة تفقدية في الساعة {now.strftime('%H:%M')}")
            
            wait_time = random.randint(7200, 14400) 
            await asyncio.sleep(wait_time)
        else:
            await asyncio.sleep(3600)

if __name__ == "__main__":
    # تشغيل سيرفر الويب في خلفية مستقلة لكي لا يغلق البوت
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()
    
    # تشغيل البوت الأساسي
    asyncio.run(smart_scheduler())
