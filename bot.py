import os
import random
import asyncio
from datetime import datetime
import threading
import requests
from google import genai

# جلب المفاتيح وإعداد Gemini
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def send_telegram_message(text, target_chat_id=None):
    """إرسال رسالة تليجرام"""
    c_id = target_chat_id or CHAT_ID
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": c_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"خطأ في إرسال الرسالة: {e}")

def ask_gemini(prompt_text):
    """الذكاء الاصطناعي للرد وتوليد الرسائل بأسلوب ذكي ومقرب"""
    system_instruction = (
        "أنت مساعد شخصي ذكي جداً، مبرمج محترف، وصديق مقرب للشاب (مهتم بالبرمجة، لينكس، والتقنية). "
        "تتحدث باللهجة العامية اللطيفة والمحفزة، أسلوبك ذكي، عميق، وداعم دائماً."
    )
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=f"{system_instruction}\n\nالسياق/الرسالة: {prompt_text}"
        )
        return response.text
    except Exception as e:
        print(f"خطأ تفصيلي في توليد الذكاء الاصطناعي: {e}")
        return f"يا وحش، صار في خطأ تقني بالذكاء الاصطناعي: {str(e)}"

# نظام الإشعارات الذكية التلقائية (المبادرة بالتفقد)
async def smart_scheduler():
    print("🤖 نظام التفقد الذكي بدأ بالعمل...")
    while True:
        now = datetime.now()
        current_hour = now.hour
        
        if 10 <= current_hour <= 23:
            prompt = "ابعث رسالة قصيرة تفقدية لصديقك المبرمج، اسأله عن مشروعه أو ارمِ له فكرة تقنية بلطافة وبدون مقدمات طويلة."
            message = ask_gemini(prompt)
            send_telegram_message(message)
            
            wait_time = random.randint(7200, 14400) # بين ساعتين لـ 4 ساعات
            await asyncio.sleep(wait_time)
        else:
            await asyncio.sleep(3600)

# نظام الاستماع والرد الفوري (عندما تكلم البوت)
def listen_to_telegram():
    print("👀 نظام الرد الفوري يستمع لرسائلك...")
    offset = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset={offset}&timeout=30"
            response = requests.get(url).json()
            
            if "result" in response:
                for update in response["result"]:
                    offset = update["update_id"] + 1
                    
                    if "message" in update and "text" in update["message"]:
                        user_message = update["message"]["text"]
                        sender_chat_id = update["message"]["chat"]["id"]
                        
                        print(f"استلمت رسالة: {user_message}")
                        
                        # توليد رد ذكي باستخدام Gemini
                        ai_reply = ask_gemini(user_message)
                        
                        # الرد عليك مباشرة على نفس الشات
                        send_telegram_message(ai_reply, sender_chat_id)
        except Exception as e:
            print(f"خطأ في استقبال الرسائل: {e}")
        
        import time
        time.sleep(1)

if __name__ == "__main__":
    # تشغيل نظام الاستماع الفوري للرسائل في خلفية مستقلة
    t_listener = threading.Thread(target=listen_to_telegram)
    t_listener.daemon = True
    t_listener.start()
    
    # تشغيل المجدول الذكي للإشعارات
    asyncio.run(smart_scheduler())
