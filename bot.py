import os
import smtplib
import sys
from email.mime.text import MIMEText
from google import genai
from google.genai import types

def run_pro_trend_bot():
    try:
        # 1. جلب البيانات من الـ Secrets (تأكد أن الأسماء مطابقة لـ GitHub)
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        # إيميل بلوجر الخاص بك
        target_email = "oedn305.trnd20266@blogger.com"

        # التحقق من وجود الأسرار
        if not all([api_key, sender_email, app_password]):
            print("❌ خطأ: أحد الأسرار (Secrets) مفقود أو غير معرف بشكل صحيح في GitHub!")
            sys.exit(1)

        # 2. إعداد العميل مع ميزة البحث الحقيقي
        client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
        
        # 3. هندسة الأمر (الأمر الذي يجعله يبحث عن الترند)
        prompt = """
        بصفتك خبير SEO ورئيس تحرير موقع إخباري:
        1. ابحث الآن في Google Trends عن أكثر المواضيع بحثاً في (السعودية، الخليج، والعالم).
        2. اختر موضوعاً واحداً "ساخناً جداً" في أحد المجالات: (تقنية، اقتصاد، رياضة، منوعات).
        3. اكتب مقالاً احترافياً يتجاوز 900 كلمة بتنسيق HTML.
        4. الهيكلية المطلوبة:
           - ابدأ المقال بكلمة واحدة فقط هي اسم القسم بين قوسين مثل: (تقنية) أو (رياضة).
           - العنوان H1: جذاب جداً ويحتوي على الكلمات الأكثر بحثاً.
           - مقدمة، ثم عناوين فرعية H2 و H3، وقوائم نقطية.
           - أضف فقرة "تحليل الخبراء" وخاتمة.
        5. الإعلانات: ضع النص [AD_HERE] مرتين وسط المقال.
        6. اللغة: عربية فصحى بأسلوب بشري جذاب.
        """

        # 4. توليد المحتوى
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[{'google_search': {}}]
            )
        )
        
        raw_output = response.text.strip()
        clean_text = raw_output.replace('```html', '').replace('```', '').strip()
        
        # 5. استخراج القسم والعنوان
        lines = clean_text.split('\n')
        category = "عام"
        if '(' in lines[0] and ')' in lines[0]:
            category = lines[0].replace('(', '').replace(')', '').strip()
            clean_text = "\n".join(lines[1:])

        # إضافة كود المساحة الإعلانية
        ad_code = '<div style="margin:25px 0; padding:20px; border-radius:10px; border:1px solid #eee; background:#fefefe; text-align:center;"><small style="color:#999;">إعلان مخصص</small></div>'
        final_html = clean_text.replace('[AD_HERE]', ad_code)

        # استخراج العنوان للرسالة
        title_tag = [l for l in lines if '<h1>' in l]
        email_subject = title_tag[0].replace('<h1>', '').replace('</h1>', '').strip() if title_tag else "أخبار الترند اليوم"

        # 6. إرسال الإيميل
        msg = MIMEText(final_html, 'html', 'utf-8')
        msg['Subject'] = email_subject
        msg['From'] = sender_email
        msg['To'] = target_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print(f"🚀 تم بنجاح! القسم: {category} | العنوان: {email_subject}")

    except Exception as e:
        print(f"❌ حدث خطأ تقني: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_pro_trend_bot()
