import os
import smtplib
import sys
import time
import random
from email.mime.text import MIMEText
from google import genai

def run_stabilized_bot():
    try:
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        target_email = "oedn305.trnd20266@blogger.com"

        if not api_key:
            print("❌ GEMINI_KEY مفقود!")
            sys.exit(1)

        # إعداد الاتصال
        client = genai.Client(api_key=api_key)
        
        # اختيار موضوع متنوع
        topics = [
            "أفضل تطبيقات الذكاء الاصطناعي لعام 2026",
            "دليل السياحة في نيوم والوجهات الجديدة بالسعودية",
            "كيف تبدأ مشروعاً إلكترونياً ناجحاً في الخليج"
        ]
        chosen_topic = random.choice(topics)

        print(f"⏳ جاري العمل على موضوع: {chosen_topic}...")
        
        # 4. طلب المحتوى (تعديل اسم الموديل ليتوافق مع V1Beta)
        prompt = f"اكتب مقالاً طويلاً بتنسيق HTML حول: {chosen_topic}. استخدم H1 و H2 وتنسيق SEO قوي."

        # جربنا gemini-1.5-flash، إذا لم يعمل نستخدم الموديل الأساسي المضمون
        response = client.models.generate_content(
            model='gemini-1.5-flash', 
            contents=prompt
        )
        
        content = response.text.replace('```html', '').replace('```', '').strip()
        
        # 5. استخراج العنوان
        subject = f"تحديث 2026: {chosen_topic}"

        # 6. إرسال الإيميل
        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = target_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print(f"✅ تم النشر بنجاح: {subject}")

    except Exception as e:
        # إذا فشل 1.5 فلاش، سأعطيك كوداً بديلاً هنا فوراً
        print(f"❌ حدث خطأ: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_stabilized_bot()
