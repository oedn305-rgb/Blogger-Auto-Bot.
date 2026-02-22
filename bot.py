import os
import smtplib
import sys
from email.mime.text import MIMEText
from google import genai
from google.genai import types

def run_pro_trend_bot():
    # تعديل الأسماء لتطابق الموجود في GitHub Secrets عندك
    api_key = os.getenv("GEMINI_KEY")
    sender_email = os.getenv("MY_EMAIL")
    app_password = os.getenv("EMAIL_PASS")
    # ملاحظة: سنستخدم target_email الثابت كما في المرة السابقة
    target_email = "oedn305.trnd20266@blogger.com"

    if not api_key or not sender_email or not app_password:
        print(f"❌ خطأ: أحد الأسرار مفقود! GEMINI_KEY: {'موجود' if api_key else 'ناقص'}, MY_EMAIL: {'موجود' if sender_email else 'ناقص'}, EMAIL_PASS: {'موجود' if app_password else 'ناقص'}")
        sys.exit(1)

    try:
        client = genai.Client(api_key=api_key)
        
        prompt = """
        ابحث عن ترند حالي في السعودية والخليج واكتب عنه مقال HTML احترافي طويل (800 كلمة).
        استخدم العناوين الفرعية H2 و H3 واجعل المحتوى حصري ومفيد جداً.
        """

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config=types.GenerateContentConfig(tools=[{'google_search': {}}])
        )
        
        content = response.text.replace('```html', '').replace('```', '')
        
        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = "تحديث الترند اليومي الحصري"
        msg['From'] = sender_email
        msg['To'] = target_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print("🚀 تم النشر بنجاح!")

    except Exception as e:
        print(f"❌ حدث خطأ تقني: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_pro_trend_bot()
