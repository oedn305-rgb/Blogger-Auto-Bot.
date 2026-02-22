import os
import smtplib
import sys
import random
from email.mime.text import MIMEText
from google import genai
from google.genai import types

def run_pro_publisher_bot():
    try:
        # 1. الإعدادات الأساسية
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        target_email = "oedn305.trnd20266@blogger.com"

        client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
        
        # 2. أمر الذكاء الاصطناعي لإنتاج محتوى عالي الجودة مع الأقسام
        prompt = """
        أنت الآن رئيس تحرير أكبر موقع إخباري في الخليج. 
        مهمتك:
        1. ابحث عن الترندات الحالية في السعودية والخليج والعالم باستخدام Google Search.
        2. اختر خبراً واحداً ذا قيمة عالية (تقنية، اقتصاد، رياضة، أو منوعات).
        3. اكتب مقالاً احترافياً يتجاوز 900 كلمة.
        4. التنسيق HTML: استخدم H1 للعنوان، H2 للعناوين الفرعية، H3 للتفاصيل، وقوائم نقطية.
        5. الأقسام (Labels): في السطر الأول من المقال، اكتب فقط كلمة واحدة تمثل القسم: 
           (تقنية، اقتصاد، رياضة، منوعات) بناءً على المحتوى.
        6. اجعل المقال يحتوي على مقدمة جذابة، تحليل للخبر، فقرة "رأي الخبراء"، وخاتمة قوية.
        7. اترك مساحة إعلانية [AD_SPACE] بعد الفقرة الثالثة والسادسة.
        """

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[{'google_search': {}}]
            )
        )
        
        full_output = response.text.strip()
        
        # 3. استخراج القسم (الكلمة الأولى) وتنظيف النص
        content_lines = full_output.split('\n')
        category = content_lines[0].replace('القسم:', '').strip()
        main_body = "\n".join(content_lines[1:]).replace('```html', '').replace('```', '')

        # 4. إضافة كود الإعلانات بشكل احترافي
        ad_code = '<div style="margin:30px 0; background:#fafafa; border:1px solid #eee; padding:20px; text-align:center; color:#999; border-radius:8px;">إعلان مخصص</div>'
        final_html = main_body.replace('[AD_SPACE]', ad_code)

        # 5. استخراج العنوان النظيف
        title_lines = [l.strip() for l in main_body.split('\n') if l.strip() and '<h1' in l]
        clean_title = title_lines[0].replace('<h1>', '').replace('</h1>', '').strip() if title_lines else "أحدث المستجدات العالمية"

        # 6. إرسال المقال مع "التصنيف" (Label)
        msg = MIMEText(final_html, 'html', 'utf-8')
        msg['Subject'] = f"{clean_title}" # بلوجر سيأخذ العنوان من هنا
        msg['From'] = f"بوابة الأخبار الذكية <{sender_email}>"
        msg['To'] = target_email

        # ملاحظة: لإضافة قسم (Label) في بلوجر عبر الإيميل، نضعه في حقل الكلمات المفتاحية إذا كان القالب يدعم ذلك، 
        # أو نتركه كأول سطر في المقال وبلوجر سيتعامل معه.
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print(f"✅ تم النشر بنجاح: {clean_title} في قسم {category}")

    except Exception as e:
        print(f"❌ خطأ: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_pro_publisher_bot()
