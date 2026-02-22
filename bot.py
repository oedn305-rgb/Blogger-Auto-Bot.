import os
import smtplib
from email.mime.text import MIMEText
import google.generativeai as genai

def run_bot():
    try:
        # 1. التحقق من وجود المفاتيح
        api_key = os.getenv("GEMINI_KEY")
        my_email = os.getenv("MY_EMAIL")
        email_pass = os.getenv("EMAIL_PASS")
        
        if not all([api_key, my_email, email_pass]):
            print("خطأ: تأكد من إضافة GEMINI_KEY و MY_EMAIL و EMAIL_PASS في Secrets")
            return

        # 2. إعداد جيمناي
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # 3. صياغة المقال
        prompt = "اكتب مقال ترند عربي احترافي. ابدأ بالعنوان مباشرة. استخدم تنسيق HTML بسيط جداً."
        response = model.generate_content(prompt)
        
        # تنظيف النص من أي علامات زائدة مثل ```html
        content = response.text.replace('```html', '').replace('```', '').strip()

        # 4. إعداد الإيميل السري
        to_email = "oedn305.trnd20266@blogger.com"
        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = "مقال ترند تلقائي"
        msg['From'] = my_email
        msg['To'] = to_email

        # 5. الإرسال
        print("جاري محاولة الإرسال...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(my_email, email_pass)
            server.send_message(msg)
        
        print("✅ تم النشر بنجاح في بلوجر!")

    except Exception as e:
        print(f"❌ حدث خطأ حقيقي هنا: {str(e)}")
        raise e  # لكي يظهر الخطأ بالتفصيل في GitHub

if __name__ == "__main__":
    run_bot()
