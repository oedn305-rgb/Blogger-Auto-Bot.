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
        
        if not available_models:
            print("❌ لم يتم العثور على أي موديل متاح في هذا المفتاح!")
            return
            
        selected_model = available_models[0] 
        model = genai.GenerativeModel(selected_model)
        # -------------------------------------------

        # اختيار موضوع متنوع في كل مرة (أو يمكنك تركه ثابتاً)
        topic = "ثورة الذكاء الاصطناعي في 2026 والتحولات الكبرى"
        
        # --- التعديل الجذري على الأوامر (البرومبت) لمنع الحقوق الوهمية ---
        prompt = (
            f"اكتب مقال HTML احترافي وشامل عن: {topic}. "
            "ملاحظات هامة جداً:\n"
            "1. لا تذكر أي اسم موقع مثل 'رادار السعودية' أو أي جهة إخبارية أخرى.\n"
            "2. لا تضع روابط خارجية أو جملة 'جميع الحقوق محفوظة' لأي طرف ثالث.\n"
            "3. اجعل المقال ينتهي بعبارة 'حقوق النشر محفوظة لمدونتنا' فقط.\n"
            "4. استخدم تنسيق SEO قوي مع H1 و H2."
        )
        
        response = model.generate_content(prompt)
        
        content = response.text.replace('```html', '').replace('```', '').strip()

        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = f"تحديث حصري: {topic}"
        msg['From'] = sender_email
        msg['To'] = target_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print(f"✅ نجحت العملية! تم النشر باستخدام الموديل: {selected_model}")

    except Exception as e:
        print(f"❌ خطأ تقني: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_smart_bot()
