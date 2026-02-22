import os
import smtplib
from email.mime.text import MIMEText
import google.generativeai as genai
import sys

def run():
    try:
        # 1. جلب البيانات
        api_key = os.getenv("GEMINI_KEY")
        sender = os.getenv("MY_EMAIL")
        password = os.getenv("EMAIL_PASS")
        target = "oedn305.trnd20266@blogger.com"

        print(f"Checking keys... Email: {sender}")

        # 2. توليد المحتوى
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        print("Connecting to Gemini...")
        response = model.generate_content("اكتب مقال ترند عربي تقني قصير جدا بتنسيق HTML")
        article_html = response.text
        print("Article generated successfully!")

        # 3. إعداد الإيميل
        msg = MIMEText(article_html, 'html', 'utf-8')
        msg['Subject'] = "مقال ترند تلقائي"
        msg['From'] = sender
        msg['To'] = target

        # 4. الإرسال
        print("Connecting to Gmail Server...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        
        print("✅ SUCCESS: Post sent to Blogger!")

    except Exception as e:
        print(f"❌ ERROR FOUND: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run()
