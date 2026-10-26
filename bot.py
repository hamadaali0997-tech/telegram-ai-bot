import os
import random
import asyncio
from datetime import datetime
import requests
from google import genai

# جلب المفاتيح من متغيرات البيئة (Environment Variables) في المنصة
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# تهيئة عميل Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

def send_telegram_message(text):
    """إرسال رسالة تليجرام باستخدام Bot API"""
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
    """توليد سؤال ذكي وعميق ومتجدد عبر نموذج Gemini"""
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
    """حلقة ذكية تفحص الوقت وتختار أوقات عشوائية خلال النهار للبعث"""
    print("🤖 بوت الاستفقاد الذكي بدأ بالعمل...")
    while True:
        now = datetime.now()
        current_hour = now.hour
        
        # إرسال رسائل خلال ساعات النهار (من 10 صباحاً لـ 11 ليلاً)
        if 10 <= current_hour <= 23:
            message = generate_smart_prompt()
            send_telegram_message(message)
            print(f"تم إرسال رسالة تفقدية في الساعة {now.strftime('%H:%M')}")
            
            # الانتظار لمدة عشوائية بين ساعتين إلى 4 ساعات تقريباً (بالثواني)
            wait_time = random.randint(7200, 14400) 
            await asyncio.sleep(wait_time)
        else:
            # إذا كان الوقت ليلاً، انتظر ساعة ورجع افحص الوقت
            await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(smart_scheduler())
