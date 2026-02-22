import os
import smtplib
import sys
import random
from email.mime.text import MIMEText
from google import genai

def run_blogger_bot():
    try:
        # 1. جلب البيانات من الأسرار (Secrets) التي حدثتها
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        target_email = "oedn305.trnd20266@blogger.com"

        if not api_key or not sender_email or not app_password:
            print("❌ خطأ: تأكد من إعداد Secrets في GitHub بشكل صحيح!")
            sys.exit(1)

        # 2. الاتصال بذكاء Gemini
        client = genai.Client(api_key=api_key)
        
        # 3. اختيار مجال عشوائي لمدونتك لتنويع المحتوى
        categories = ["تقنية", "رياضة", "اقتصاد", "صحة وجمال", "سيارات 2026"]
        selected_category = random.choice(categories)

        # 4. طلب المقال (أمر احترافي لـ SEO)
        prompt = f"""
        اكتب مقالاً طويلاً (أكثر من 1000 كلمة) بتنسيق HTML حول موضوع ترند في مجال ({selected_category}) لعام 2026.
        - استخدم H1 للعنوان الرئيسي.
        - استخدم H2 و H3 للعناوين الفرعية.
        - اجعل الأسلوب جذاباً ومناسباً للقارئ السعودي والخليجي.
        - ضع مقدمة قوية، فقرات مفصلة، وخاتمة.
        - المقال يجب أن يكون جاهزاً للنشر فوراً في بلوجر.
        """

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        
        # تنظيف الكود الناتج
        content = response.text.replace('```html', '').replace('```', '').strip()
        
        # استخراج العنوان للرسالة
        lines = content.split('\n')
        subject = f"جديد اليوم في {selected_category}: تحديثات 2026"
        for line in lines:
            if '<h1>' in line:
                subject = line.replace('<h1>', '').replace('</h1>', '').strip()
                break

        # 5. إعداد وإرسال الإيميل
        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = f"ناشر المحتوى الذكي <{sender_email}>"
        msg['To'] = target_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print(f"🚀 تم بنجاح! تم نشر مقال بعنوان: {subject}")

    except Exception as e:
        print(f"❌ حدث خطأ: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_blogger_bot()
