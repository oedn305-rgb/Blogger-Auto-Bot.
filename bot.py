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

        if not all([api_key, sender_email, app_password]):
            print("❌ نقص في إعدادات Secrets")
            return

        print(f"--- بدء الاتصال بحساب: {sender_email} ---")

        # 2. إعداد جيمناي والبحث عن الموديل المتاح
        genai.configure(api_key=api_key)
        
        # البحث عن موديل متاح (تجاوز خطأ 404)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if not available_models:
            raise Exception("No supported models found for this API Key")
        
        # اختيار أول موديل متاح (غالباً سيكون gemini-pro أو gemini-1.5-flash)
        model_name = available_models[0]
        print(f"✅ تم العثور على الموديل المتاح: {model_name}")
        model = genai.GenerativeModel(model_name)

        # 3. توليد المحتوى
        print("جاري توليد المقال...")
        prompt = "اكتب مقال ترند تقني عربي بأسلوب جذاب. استخدم HTML (h2, p). لا تضع علامات ```."
        response = model.generate_content(prompt)
        
        if not response.text:
            raise Exception("Gemini returned empty text")

        content = response.text.replace('```html', '').replace('```', '').strip()

        # 4. إعداد الإيميل
        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = "تحديث تلقائي للمدونة"
        msg['From'] = sender_email
        msg['To'] = target_email

        # 5. الإرسال
        print("جاري الإرسال إلى بلوجر...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print("✅ تم النشر بنجاح!")

    except Exception as e:
        print(f"❌ حدث خطأ: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_blogger_bot()
