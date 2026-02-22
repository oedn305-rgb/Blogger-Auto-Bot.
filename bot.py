import os
import smtplib
import sys
from email.mime.text import MIMEText
import google.generativeai as genai

def run_blogger_bot():
    try:
        # 1. جلب البيانات من الخزنة
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        target_email = "oedn305.trnd20266@blogger.com"

        print(f"--- بدء الاتصال بحساب: {sender_email} ---")

        # 2. إعداد الذكاء الاصطناعي (النسخة المستقرة عالمياً)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.0-pro')
        
        print("جاري توليد مقال الترند...")
        prompt = "اكتب مقالاً إخبارياً عربياً قصيراً ومنسقاً بـ HTML (استخدم h2 و p). ابدأ بالعنوان مباشرة."
        response = model.generate_content(prompt)
        
        # تنظيف النص من أي زوائد
        content = response.text.replace('```html', '').replace('```', '').strip()

        # 3. إعداد رسالة الإيميل
        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = "تحديث تلقائي للمدونة"
        msg['From'] = sender_email
        msg['To'] = target_email

        # 4. الإرسال عبر Gmail
        print("جاري محاولة الإرسال إلى بلوجر...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print("✅ تم النشر بنجاح!")

    except Exception as e:
        print(f"❌ حدث خطأ: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_blogger_bot()
