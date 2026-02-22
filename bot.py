import os
import smtplib
from email.mime.text import MIMEText
import google.generativeai as genai

# إعداد جيمناي
genai.configure(api_key=os.getenv("GEMINI_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# صياغة المقال (تقدر تغير البرومبت هنا)
prompt = "اكتب مقال ترند عربي احترافي ومنسق بـ HTML"
response = model.generate_content(prompt)
html_content = response.text

# إعداد الإيميل السري
to_email = "oedn305.trnd20266@blogger.com" # هذا إيميلك السري اللي رتبناه
msg = MIMEText(html_content, 'html')
msg['Subject'] = "مقال جديد من بوت الترند"
msg['From'] = os.getenv("MY_EMAIL")
msg['To'] = to_email

# الإرسال
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(os.getenv("MY_EMAIL"), os.getenv("EMAIL_PASS"))
        server.send_message(msg)
    print("Success: Post sent to Blogger!")
except Exception as e:
    print(f"Error: {e}")
