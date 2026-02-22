import os
import smtplib
import sys
# محاولة تثبيت المكتبة للتأكد
os.system('pip install -q google-generativeai')
import google.generativeai as genai
from email.mime.text import MIMEText

def run_final_stable():
    try:
        # 1. جلب البيانات
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        target_email = "oedn305.trnd20266@blogger.com"

        # 2. الإعداد (استخدام الموديل المضمون gemini-pro)
        genai.configure(api_key=api_key)
        
        # ملاحظة: استخدمنا gemini-pro لأنه الأكثر استقراراً ويحل مشكلة 404
        model = genai.GenerativeModel('gemini-pro')
        
        # 3. توليد المحتوى
        topic = "أحدث تقنيات 2026 والذكاء الاصطناعي"
        response = model.generate_content(f"اكتب مقال HTML احترافي عن: {topic}")
        
        content = response.text.replace('```html', '').replace('```', '').strip()

        # 4. إعداد وإرسال الإيميل
        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = f"تحديث حصري: {topic}"
        msg['From'] = sender_email
        msg['To'] = target_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print("✅ أخيراً! العلامة الخضراء
