import os
import smtplib
import sys
# تثبيت المكتبة برمجياً للتأكد 100% من وجودها
try:
    import google.generativeai as genai
except ImportError:
    os.system('pip install -q google-generativeai')
    import google.generativeai as genai

from email.mime.text import MIMEText

def run_bot():
    try:
        # جلب البيانات
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        target_email = "oedn305.trnd20266@blogger.com"

        # إعداد الموديل
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # توليد محتوى سريع
        response = model.generate_content("اكتب مقال HTML عن أهمية التقنية في 2026")
        
        # إرسال الإيميل
        msg = MIMEText(response.text, 'html', 'utf-8')
        msg['Subject'] = "تحديث تقني جديد"
        msg['From'] = sender_email
        msg['To'] = target_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print("✅ تم التشغيل والنشر بنجاح!")

    except Exception as e:
        print(f"❌ خطأ: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_bot()
