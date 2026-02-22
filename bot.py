import os
import smtplib
import sys
from email.mime.text import MIMEText
import google.generativeai as genai

def run_blogger_bot():
    try:
        # 1. جلب البيانات من Secrets
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        target_email = "oedn305.trnd20266@blogger.com"

        if not api_key:
            print("❌ GEMINI_KEY is missing!")
            return

        print(f"--- الاتصال بالحساب: {sender_email} ---")

        # 2. إعداد جيمناي وفحص الموديلات المتاحة تلقائياً
        genai.configure(api_key=api_key)
        
        # كود ذكي لجلب الموديل الشغال فعلياً في حسابك
        model_to_use = 'gemini-1.5-flash' # الافتراضي
        try:
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if models:
                # نختار أول موديل مستقر متاح (يفضل flash أو pro)
                model_to_use = models[0]
                print(f"✅ تم العثور على الموديل النشط: {model_to_use}")
        except Exception as e:
            print(f"⚠️ فشل فحص الموديلات، سأحاول استخدام الموديل القياسي: {e}")

        model = genai.GenerativeModel(model_to_use)

        # 3. توليد المحتوى
        print("جاري إنشاء المقال...")
        prompt = "اكتب مقال ترند عربي قصير جداً وحصري. استخدم HTML بسيط (h2, p). لا تضع علامات أكواد برمجية."
        
        response = model.generate_content(prompt)
        
        if not response.text:
            raise Exception("Empty response from AI")

        # تنظيف النص
        content = response.text.replace('```html', '').replace('```', '').strip()

        # 4. إعداد وإرسال الإيميل
        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = "تحديث ترند تلقائي"
        msg['From'] = sender_email
        msg['To'] = target_email

        print("جاري الإرسال إلى بلوجر...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print("✅ نجحت العملية! تم النشر في المدونة.")

    except Exception as e:
        print(f"❌ حدث خطأ فني: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_blogger_bot()
