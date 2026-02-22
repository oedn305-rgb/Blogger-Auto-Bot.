import os
import smtplib
import sys
import google.generativeai as genai
from email.mime.text import MIMEText

def run_final():
    try:
        # 1. جلب البيانات من الأسرار
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        target_email = "oedn305.trnd20266@blogger.com"

        # 2. إعداد جوجل (المكتبة المستقرة)
        genai.configure(api_key=api_key)
        
        # 3. اختيار الموديل (فلاش 1.5 هو الأكثر استقراراً الآن)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 4. توليد المقال
        topic = "مستقبل التكنولوجيا والعمل عن بعد في السعودية 2026"
        response = model.generate_content(f"اكتب مقال HTML طويل واحترافي عن: {topic}")
        
        content = response.text.replace('```html', '').replace('```', '').strip()

        # 5. إعداد وإرسال الإيميل
        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = topic
        msg['From'] = sender_email
        msg['To'] = target_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print("✅ أخيراً! تم النشر بنجاح.")

    except Exception as e:
        print(f"❌ خطأ: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_final()
