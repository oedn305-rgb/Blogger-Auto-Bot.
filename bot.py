import os
import smtplib
import sys
import time
from email.mime.text import MIMEText
from google import genai
from google.genai import types

def run_pro_trend_bot():
    try:
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        target_email = "oedn305.trnd20266@blogger.com"

        if not all([api_key, sender_email, app_password]):
            print("❌ نقص في البيانات السرية (Secrets)")
            sys.exit(1)

        client = genai.Client(api_key=api_key)
        
        prompt = "ابحث عن ترند حالي في السعودية والخليج الآن، واكتب مقال HTML احترافي SEO يتجاوز 900 كلمة."

        # التصحيح النهائي لاسم الأداة وفقاً لتحديث 2026
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())] 
            )
        )
        
        content = response.text.replace('```html', '').replace('```', '').strip()
        
        # استخراج العنوان
        lines = content.split('\n')
        title = [l for l in lines if '<h1>' in l]
        subject = title[0].replace('<h1>', '').replace('</h1>', '').strip() if title else "ترند اليوم في السعودية"

        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = target_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print(f"🚀 تم بنجاح! العنوان: {subject}")

    except Exception as e:
        if "429" in str(e):
            print("⚠️ تم تجاوز الحصة المؤقتة. انتظر دقيقة ثم حاول مرة أخرى.")
        else:
            print(f"❌ خطأ تقني: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_pro_trend_bot()
