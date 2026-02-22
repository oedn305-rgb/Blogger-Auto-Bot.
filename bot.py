import os
import smtplib
import sys

# تثبيت المكتبة إجبارياً قبل البدء لضمان عدم حدوث ModuleNotFoundError
os.system('pip install -q google-generativeai')

import google.generativeai as genai
from email.mime.text import MIMEText

def run_final_stable():
    try:
        # 1. جلب البيانات من الأسرار (Secrets)
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        target_email = "oedn305.trnd20266@blogger.com"

        if not api_key:
            print("❌ GEMINI_KEY is missing!")
            return

        # 2. إعداد الموديل المستقر (gemini-pro)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # 3. طلب توليد المحتوى
        topic = "أفضل مشاريع التقنية والربح من الإنترنت 2026"
        prompt = f"اكتب مقال HTML احترافي وشامل عن: {topic}. استخدم H1 و H2."
        
        response = model.generate_content(prompt)
        
        # تنظيف النص الناتج
        content = response.text.replace('```html', '').replace('```', '').strip()

        # 4. إعداد الرسالة
        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = f"تحديث جديد: {topic}"
        msg['From'] = sender_email
        msg['To'] = target_email

        # 5. الإرسال عبر السيرفر
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print("✅ Success: The post has been published!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_final_stable()
