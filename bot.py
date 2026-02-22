import os
import smtplib
import sys
import random
from email.mime.text import MIMEText
import google.generativeai as genai

def run_mega_profit_bot():
    try:
        # 1. جلب البيانات من Secrets
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        target_email = "oedn305.trnd20266@blogger.com"

        # 2. تهيئة الذكاء الاصطناعي واختيار الموديل المتاح
        genai.configure(api_key=api_key)
        all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = all_models[0] if all_models else 'gemini-1.5-flash'
        model = genai.GenerativeModel(model_name)

        # 3. قائمة المجالات الأكثر ربحاً في أدسينس (High CPC)
        niches = [
            "طرق مبتكرة للربح من الإنترنت 2026",
            "أسرار خفية في هواتف أندرويد وآيفون",
            "تحليل ترندات التقنية والذكاء الاصطناعي",
            "كيفية استثمار الأموال الصغيرة للمبتدئين",
            "أفضل الأدوات الرقمية لزيادة الإنتاجية"
        ]
        topic = random.choice(niches)

        # 4. هندسة الأمر (Prompt) لضمان محتوى بشري 100% وSEO قوي
        prompt = f"""
        بصفتك خبير سيكولوجي وكاتب محتوى SEO محترف:
        اكتب مقالاً طويلاً (أكثر من 600 كلمة) عن موضوع: ({topic}).
        
        استخدم الاستراتيجية التالية:
        - ابدأ مباشرة بالعنوان (بدون مقدمات برمجية).
        - العنوان يجب أن يكون H1 جذاب ومثير للفضول.
        - مقدمة مشوقة تجذب القارئ وتدفعه للتمرير.
        - قسم المحتوى إلى 4 فقرات رئيسية تحت عناوين H2.
        - استخدم القوائم النقطية (Bullet points) بكثرة.
        - أضف فقرة "الأسئلة الشائعة" في النهاية.
        - التنسيق: HTML فقط. اللغة: عربية فخمة وسلسة.
        - ممنوع تماماً ذكر أنك ذكاء اصطناعي.
        """

        response = model.generate_content(prompt)
        raw_text = response.text.replace('```html', '').replace('```', '').strip()

        # 5. نظام توزيع المساحات الإعلانية الاحترافي (لا يزعج الزائر)
        ad_code = '<div style="margin:25px 0; padding:15px; border-top:1px dashed #ccc; border-bottom:1px dashed #ccc; text-align:center; background-color:#fcfcfc;"><span style="color:#aaa; font-size:11px; display:block; margin-bottom:5px;">إعلان مقترح</span></div>'

        # تقسيم النص لزرع الإعلانات بعد العناوين الفرعية
        sections = raw_text.split('</h2>')
        if len(sections) > 2:
            final_content = sections[0] + '</h2>' + ad_code + sections[1] + '</h2>' + sections[2] + '</h2>' + ad_code + "".join(sections[3:])
        else:
            final_content = raw_text.replace('</h2>', '</h2>' + ad_code, 1)

        # 6. نظام ذكي لاستخراج العنوان ومنع ظهور الأكواد في Subject الإيميل
        lines = [l.strip() for l in raw_text.split('\n') if l.strip() and '<' not in l[:10]]
        subject_text = lines[0] if lines else "موضوع اليوم المثير للاهتمام"
        # تنظيف إضافي للعنوان
        final_subject = subject_text.replace('<h1>', '').replace('</h1>', '').replace('<h2>', '').replace('</h2>', '').strip()

        # 7. إعداد وإرسال الإيميل
        msg = MIMEText(final_content, 'html', 'utf-8')
        msg['Subject'] = final_subject[:80] # تحديد طول العنوان
        msg['From'] = f"بوابة المعرفة <{sender_email}>"
        msg['To'] = target_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print(f"✅ SUCCESS: تم النشر بعنوان: {final_subject}")

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_mega_profit_bot()
