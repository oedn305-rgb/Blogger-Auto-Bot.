import os
import smtplib
import sys
import random
from email.mime.text import MIMEText
import google.generativeai as genai

def run_mega_profit_bot():
    try:
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        target_email = "oedn305.trnd20266@blogger.com"

        genai.configure(api_key=api_key)
        all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = all_models[0] if all_models else 'gemini-1.5-flash'
        model = genai.GenerativeModel(model_name)

        # مواضيع تهم الجمهور وتجعلهم يقرأون للنهاية
        niches = ["قصص نجاح في العمل الحر", "أسرار تقنية مخفية", "مقارنات صادمة بين الهواتف", "كيف تسبق الجميع في الذكاء الاصطناعي"]
        topic = random.choice(niches)

        prompt = f"""
        بصفتك كاتب محتوى سيكولوجي وخبير أرباح أدسينس:
        اكتب مقالاً طويلاً جداً ومقسماً بشكل احترافي عن: ({topic}).
        
        استخدم الاستراتيجية التالية لزيادة بقاء الزائر:
        1. ابدأ بـ H1 يحتوي على رقم (مثلاً: 10 أسرار... أو 5 طرق...) لأنها تجذب الزوار.
        2. اكتب مقدمة غامضة قليلاً تشجع الزائر على التمرير للأسفل.
        3. قسم المقال إلى 4 أقسام رئيسية (H2).
        4. بين كل قسم وقسم، اترك مساحة إعلانية واضحة.
        5. استخدم أسلوب "التعداد النقطي" بكثرة لأنه يسهل القراءة على الموبايل.
        6. في المنتصف، أضف جملة "اقرأ أيضاً: [موضوع مقترح]" لزيادة التنقل الداخلي.
        7. الخاتمة يجب أن تحتوي على نصيحة عملية تجعل الزائر يحفظ رابط موقعك.
        
        التنسيق: HTML فقط، لغة عربية فخمة، لا تذكر الذكاء الاصطناعي نهائياً.
        """

        response = model.generate_content(prompt)
        raw_text = response.text.replace('```html', '').replace('```', '').strip()

        # تصميم مساحات إعلانية "ناعمة" لا تزعج العين (Native Ads Style)
        ad_code = '<div style="margin:25px 0; padding:15px; border-top:1px solid #eee; border-bottom:1px solid #eee; text-align:center; background-color:#fafafa;"><span style="color:#999; font-size:12px; display:block; margin-bottom:5px;">إعلان</span></div>'

        # توزيع الإعلانات بذكاء (بعد الفقرة الأولى، وفي المنتصف، وقبل الخاتمة)
        sections = raw_text.split('</h2>')
        if len(sections) > 3:
            final_content = sections[0] + '</h2>' + ad_code + sections[1] + '</h2>' + sections[2] + '</h2>' + ad_code + "".join(sections[3:])
        else:
            final_content = raw_text.replace('</h2>', '</h2>' + ad_code, 1)

        subject = [l for l in raw_text.split('\n') if l.strip()][0].replace('<h1>', '').replace('</h1>', '')[:80]

        msg = MIMEText(final_content, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = f"مجلة التميز <{sender_email}>"
        msg['To'] = target_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print(f"✅ تم نشر المقال السيكولوجي: {subject}")

    except Exception as e:
        print(f"❌ خطأ: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_mega_profit_bot()
