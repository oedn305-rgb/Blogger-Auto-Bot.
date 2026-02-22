import os
import smtplib
import sys
import time
import random
from email.mime.text import MIMEText
from google import genai

def run_stabilized_bot():
    try:
        # 1. جلب البيانات من Secrets
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        target_email = "oedn305.trnd20266@blogger.com"

        if not api_key:
            print("❌ GEMINI_KEY مفقود!")
            sys.exit(1)

        # 2. إعداد الاتصال
        client = genai.Client(api_key=api_key)
        
        # 3. اختيار موضوع متنوع
        topics = [
            "أفضل تطبيقات الذكاء الاصطناعي لعام 2026",
            "دليل السياحة في نيوم والوجهات الجديدة بالسعودية",
            "كيف تبدأ مشروعاً إلكترونياً ناجحاً في الخليج",
            "مراجعة لأحدث السيارات الكهربائية في السوق السعودي"
        ]
        chosen_topic = random.choice(topics)

        print(f"⏳ جاري العمل على موضوع: {chosen_topic}...")
        # انتظار بسيط لتهدئة السيرفر وتجنب خطأ 429
        time.sleep(5)

        # 4. طلب المحتوى باستخدام الموديل المستقر 1.5
        prompt = f"اكتب مقالاً طويلاً (1000 كلمة) بتنسيق HTML احترافي حول: {chosen_topic}. استخدم H1 و H2 وتنسيق SEO قوي."

        response = client.models.generate_content(
            model='gemini-1.5-flash', # هذا هو الموديل الذي اتفقنا عليه
            contents=prompt
        )
        
        content = response.text.replace('```html', '').replace('```', '').strip()
        
        # 5. استخراج العنوان
        lines = content.split('\n')
        subject = f"حصري: {chosen_topic}"
        for line in lines:
            if '<h1>' in line:
                subject = line.replace('<h1>', '').replace('</h1>', '').strip()
                break

        # 6. إرسال الإيميل
        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = f"الناشر الآلي <{sender_email}>"
        msg['To'] = target_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print(f"✅ تم النشر بنجاح: {subject}")

    except Exception as e:
        print(f"❌ حدث خطأ: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_stabilized_bot()
