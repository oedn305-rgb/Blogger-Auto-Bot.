import os
import smtplib
import sys

# تثبيت المكتبة لضمان العمل
os.system('pip install -q google-generativeai')

import google.generativeai as genai
from email.mime.text import MIMEText

def run_smart_bot():
    try:
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        target_email = "oedn305.trnd20266@blogger.com"

        genai.configure(api_key=api_key)

        # --- الجزء الذكي: البحث عن الموديل المتاح ---
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        print(f"🔎 الموديلات المتاحة في حسابك: {available_models}")
        
        # اختيار أول موديل متاح (غالباً سيكون gemini-1.5-flash-latest أو مشابه)
        if not available_models:
            print("❌ لم يتم العثور على أي موديل متاح في هذا المفتاح!")
            return
            
        selected_model = available_models[0] 
        print(f"🚀 سيتم استخدام الموديل: {selected_model}")
        
        model = genai.GenerativeModel(selected_model)
        # -------------------------------------------

        topic = "الذكاء الاصطناعي وتطوره في 2026"
        response = model.generate_content(f"اكتب مقال HTML احترافي عن: {topic}")
        
        content = response.text.replace('```html', '').replace('```', '').strip()

        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = f"تحديث تقني: {topic}"
        msg['From'] = sender_email
        msg['To'] = target_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print("✅ نجحت العملية! تم النشر باستخدام الموديل المتاح.")

    except Exception as e:
        print(f"❌ خطأ تقني: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_smart_bot()
