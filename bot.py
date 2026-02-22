import os
import smtplib
import sys
from email.mime.text import MIMEText
import google.generativeai as genai

def run_blogger_bot():
    try:
        # 1. سحب البيانات السرية من GitHub Secrets
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        # إيميل بلوجر السري الخاص بك
        target_email = "oedn305.trnd20266@blogger.com"

        print(f"--- Starting Process for: {sender_email} ---")

        # 2. إعداد ذكاء Gemini الاصطناعي
        if not api_key:
            raise ValueError("GEMINI_KEY is missing!")
            
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # 3. أمر توليد المقال (Prompt)
        prompt = """اكتب مقالاً إخبارياً عربياً قصيراً وحصرياً عن ترند اليوم. 
        استخدم تنسيق HTML بسيط (فقط <h2> و <p>). 
        ممنوع وضع علامات مثل ```html أو أي أكواد برمجية، ابدأ بالمقال مباشرة."""
        
        print("Generating content from Gemini...")
        response = model.generate_content(prompt)
        
        # تنظيف النص الناتج من أي شوائب برمجية
        clean_html = response.text.replace('```html', '').replace('```', '').strip()

        # 4. تجهيز رسالة الإيميل
        msg = MIMEText(clean_html, 'html', 'utf-8')
        msg['Subject'] = "تحديث إخباري جديد - " + sender_email.split('@')[0]
        msg['From'] = sender_email
        msg['To'] = target_email

        # 5. الاتصال بسيرفر Gmail والإرسال
        print("Connecting to Gmail server...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print("✅ DONE! The article has been sent to your Blogger email.")

    except Exception as e:
        print(f"❌ ERROR FOUND: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_blogger_bot()
