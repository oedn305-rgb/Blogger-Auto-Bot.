import os
import smtplib
import sys
import random
from email.mime.text import MIMEText
# استخدام المكتبة الجديدة كلياً لضمان عدم توقف البوت مستقبلاً
from google import genai
from google.genai import types

def run_future_bot():
    try:
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        target_email = "oedn305.trnd20266@blogger.com"

        # إعداد العميل الجديد (New Client SDK)
        client = genai.Client(api_key=api_key)
        
        niches = [
            "أسرار الربح من تطبيقات الذكاء الاصطناعي 2026",
            "كيف تختار هاتفك القادم بمواصفات خيالية وسعر رخيص",
            "تحليل أعمق لترندات جوجل والسوشيال ميديا اليوم",
            "خطوات عملية لاحتراف العمل الحر من المنزل",
            "تقنيات مذهلة ستغير شكل العالم في السنوات القادمة"
        ]
        selected_topic = random.choice(niches)

        prompt = f"""
        اكتب مقالاً احترافياً طويلاً (700 كلمة) لمدونة تقنية عن: {selected_topic}.
        التنسيق: HTML فقط.
        ابدأ بالعنوان H1 مباشرة.
        استخدم H2 للعناوين الفرعية.
        اجعل الأسلوب بشرياً، مشوقاً، ومناسباً لتصدر نتائج جوجل الأولى.
        لا تذكر أي معلومات عن الذكاء الاصطناعي في النص.
        """

        # توليد المحتوى باستخدام الموديل الأحدث
        response = client.models.generate_content(
            model='gemini-2.0-flash', # استخدام أحدث إصدار متاح مستقر
            contents=prompt
        )
        
        raw_text = response.text.strip()

        # نظام توزيع الإعلانات الذكي
        ad_code = '<div style="margin:20px 0; padding:15px; border:1px dashed #ccc; text-align:center; background:#f9f9f9;"><small>إعلان مقترح</small></div>'
        
        sections = raw_text.split('</h2>')
        if len(sections) > 2:
            final_content = sections[0] + '</h2>' + ad_code + sections[1] + '</h2>' + sections[2] + '</h2>' + ad_code + "".join(sections[3:])
        else:
            final_content = raw_text.replace('</h2>', '</h2>' + ad_code, 1)

        # استخراج العنوان النظيف (بدون أكواد)
        lines = [l.strip() for l in raw_text.split('\n') if l.strip() and '<' not in l[:5]]
        clean_title = lines[0].replace('<h1>', '').replace('</h1>', '')[:80]

        # إرسال الرسالة
        msg = MIMEText(final_content, 'html', 'utf-8')
        msg['Subject'] = clean_title
        msg['From'] = f"بوابة الترند العالمية <{sender_email}>"
        msg['To'] = target_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print(f"🚀 تم النشر بنجاح باستخدام التقنية الجديدة: {clean_title}")

    except Exception as e:
        print(f"❌ خطأ في النظام الجديد: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_future_bot()
