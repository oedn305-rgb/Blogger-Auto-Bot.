import os
import smtplib
import sys
from email.mime.text import MIMEText
import google.generativeai as genai

def run_blogger_bot():
    try:
        # 1. جلب البيانات السرية
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        target_email = "oedn305.trnd20266@blogger.com"

        if not all([api_key, sender_email, app_password]):
            print("❌ خطأ: تأكد من إضافة جميع المفاتيح في Secrets (GEMINI_KEY, MY_EMAIL, EMAIL_PASS)")
            return

        print(f"--- جاري بدء العملية للحساب: {sender_email} ---")

        # 2. إعداد جيمناي (استخدام الموديل المستقر لتجنب خطأ 404)
        genai.configure(api_key=api_key)
        
        # استخدام gemini-1.5-flash-latest كخيار أول أو gemini-pro كبديل
        try:
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            print("تم اختيار موديل: Gemini 1.5 Flash Latest")
        except:
            model = genai.GenerativeModel('gemini-pro')
            print("تم اختيار موديل البديل: Gemini Pro")

        # 3. أمر توليد المقال
        prompt = "اكتب مقالاً إخبارياً عربياً قصيراً عن ترند اليوم بتنسيق HTML (استخدم h2 و p فقط). لا تكتب علامات ```html"
        
        print("جاري توليد المحتوى...")
        response = model.generate_content(prompt)
        
        # تنظيف النص
        content = response.text.replace('```html', '').replace('```', '').strip()

        # 4. تجهيز الإيميل
        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = "مقال جديد: " + response.text[:30].strip() + "..."
        msg['From'] = sender_email
        msg['To'] = target_email

        # 5. الإرسال
        print("جاري الاتصال بسيرفر Gmail...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print("✅ تم النشر بنجاح في مدونة بلوجر!")

    except Exception as e:
        print(f"❌ ERROR FOUND: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_blogger_bot()
