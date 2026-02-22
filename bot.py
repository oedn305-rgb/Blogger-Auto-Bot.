import os
import smtplib
import sys
import time
import random
from email.mime.text import MIMEText
from google import genai

def run_final_bot():
    api_key = os.getenv("GEMINI_KEY")
    sender_email = os.getenv("MY_EMAIL")
    app_password = os.getenv("EMAIL_PASS")
    target_email = "oedn305.trnd20266@blogger.com"

    # قائمة تصنيفات لتنويع المحتوى
    categories = ["الذكاء الاصطناعي", "أخبار التقنية في السعودية", "العملات الرقمية", "موسم الرياض وفعاليات الخليج"]
    chosen = random.choice(categories)

    client = genai.Client(api_key=api_key)

    # نظام المحاولات المتكررة (في حال وجود ضغط على السيرفر)
    for attempt in range(3): 
        try:
            print(f"🔄 محاولة توليد المقال (محاولة رقم {attempt + 1})...")
            
            prompt = f"اكتب مقال SEO احترافي جداً وطويل باللغة العربية حول {chosen} لعام 2026. استخدم تنسيق HTML كامل (h1, h2, p, ul). المقال موجه للجمهور السعودي والخليجي."

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            
            content = response.text.replace('```html', '').replace('```', '').strip()
            
            # إرسال الإيميل
            msg = MIMEText(content, 'html', 'utf-8')
            msg['Subject'] = f"جديد اليوم: {chosen} (تحديث 2026)"
            msg['From'] = sender_email
            msg['To'] = target_email

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, app_password)
                server.send_message(msg)
            
            print(f"🚀 تم النشر بنجاح بعد {attempt + 1} محاولات!")
            return # إنهاء البرنامج بنجاح

        except Exception as e:
            if "429" in str(e):
                print(f"⚠️ السيرفر مشغول (Quota). سأنتظر 30 ثانية ثم أحاول مجدداً...")
                time.sleep(30) # انتظار 30 ثانية قبل المحاولة التالية
            else:
                print(f"❌ خطأ غير متوقع: {str(e)}")
                break

    sys.exit(1) # إذا فشلت كل المحاولات

if __name__ == "__main__":
    run_final_bot()
