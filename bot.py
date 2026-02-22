import os
import smtplib
import sys
import google.generativeai as genai
from email.mime.text import MIMEText

def run_final_stable_bot():
    try:
        # جلب البيانات
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        target_email = "oedn305.trnd20266@blogger.com"

        # إعداد الموديل بالطريقة المستقرة (Legacy Method)
        genai.configure(api_key=api_key)
        
        # استخدام موديل gemini-1.5-flash (أقوى وأضمن موديل مستقر حالياً)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        topic = "أفضل فرص الاستثمار والعمل الحر في السعودية 2026"
        
        # توليد المحتوى
        prompt = f"اكتب مقال SEO احترافي بتنسيق HTML حول: {topic}. استخدم H1 و H2."
        response = model.generate_content(prompt)
        
        content = response.text.replace('```html', '').replace('```', '').strip()
        
        # إرسال الإيميل
        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = topic
        msg['From'] = sender_email
        msg['To'] = target_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print("✅ مبروك! البوت اشتغل والمقال نُشر بنجاح.")

    except Exception as e:
        print(f"❌ خطأ تقني: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_final_stable_bot()
