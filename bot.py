import os
import smtplib
import sys
import random

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

        if not api_key:
            print("❌ GEMINI_KEY is missing!")
            return

        genai.configure(api_key=api_key)

        # البحث عن الموديل المتاح
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if not available_models:
            print("❌ No models found!")
            return
            
        selected_model = available_models[0] 
        model = genai.GenerativeModel(selected_model)

        # قائمة المواضيع
        topics = [
            "أسرار الربح من العمل الحر في السعودية 2026",
            "أفضل تطبيقات الذكاء الاصطناعي التي ستغير حياتك هذا العام",
            "كيف تبني مشروعاً إلكترونياً ناجحاً بأقل التكاليف",
            "مستقبل السياحة في نيوم والوجهات السعودية الجديدة",
            "أدوات تقنية لا غنى عنها لأصحاب الأعمال الصغيرة"
        ]
        
        chosen_topic = random.choice(topics)
        
        prompt = (
            f"اكتب مقال HTML احترافي وشامل عن: {chosen_topic}. "
            "ملاحظات هامة: لا تذكر أسماء مواقع وهمية، لا تضع حقوق ملكية لغيري، "
            "استخدم وسم H1 للعنوان و H2 للعناوين الفرعية."
        )
        
        response = model.generate_content(prompt)
        content = response.text.replace('```html', '').replace('```', '').strip()

        # إعداد الرسالة
        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = chosen_topic
        msg['From'] = sender_email
        msg['To'] = target_email

        # إرسال الإيميل
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print(f"✅ تم النشر بنجاح: {chosen_topic}")

    except Exception as e:
        print(f"❌ خطأ تقني: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_smart_bot()
