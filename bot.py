import os
import smtplib
import sys
from email.mime.text import MIMEText
from google import genai
from google.genai import types

def run_pro_trend_bot():
    try:
        # 1. جلب البيانات من الـ Secrets
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        target_email = "oedn305.trnd20266@blogger.com"

        if not all([api_key, sender_email, app_password]):
            print("❌ خطأ: أحد الأسرار (Secrets) مفقود!")
            sys.exit(1)

        # 2. إعداد العميل
        client = genai.Client(api_key=api_key)
        
        # 3. هندسة الأمر
        prompt = """
        ابحث في ترندات السعودية والخليج الآن. 
        اختر موضوعاً ساخناً واكتب عنه مقال HTML احترافي يتجاوز 900 كلمة.
        اجعل التنسيق ممتازاً مع عناوين فرعية H2 و H3.
        ضع كلمة (تقنية) أو (رياضة) أو (اقتصاد) في أول سطر حسب الموضوع.
        """

        # 4. توليد المحتوى (التعديل هنا لإصلاح خطأ الـ Tools)
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearchRetrieval())] # الطريقة الصحيحة والمحدثة
            )
        )
        
        raw_output = response.text.strip()
        clean_text = raw_output.replace('```html', '').replace('```', '').strip()
        
        # استخراج العنوان للرسالة
        lines = clean_text.split('\n')
        title_tag = [l for l in lines if '<h1>' in l]
        email_subject = title_tag[0].replace('<h1>', '').replace('</h1>', '').strip() if title_tag else "أخبار الترند اليوم"

        # 5. إرسال الإيميل
        msg = MIMEText(clean_text, 'html', 'utf-8')
        msg['Subject'] = email_subject
        msg['From'] = sender_email
        msg['To'] = target_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print(f"🚀 تم بنجاح! العنوان: {email_subject}")

    except Exception as e:
        print(f"❌ حدث خطأ تقني: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_pro_trend_bot()
