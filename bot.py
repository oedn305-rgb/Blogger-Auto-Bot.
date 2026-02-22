import os
import smtplib
import sys
import random

# تثبيت المكتبة لضمان العمل
os.system('pip install -q google-generativeai')

import google.generativeai as genai
from email.mime.text import MIMEText

def run_smart_bot():
    try:
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        target_email = "oedn305.trnd20266@blogger.com"

        genai.configure(api_key=api_key)

        # البحث عن الموديل المتاح
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if not available_models:
            print("❌ لا يوجد موديل متاح")
            return
            
        selected_model = available_models[0] 
        model = genai.GenerativeModel(selected_model)

        # --- قائمة مواضيع متنوعة (تتغير تلقائياً في كل مرة يعمل فيها البوت) ---
        topics = [
            "أسرار الربح من العمل الحر في السعودية 2026",
            "أفضل تطبيقات الذكاء الاصطناعي التي ستغير حياتك هذا العام",
            "كيف تبني مشروعاً إلكترونياً ناجحاً بأقل التكاليف",
            "مستقبل السياحة في نيوم والوجهات السعودية الجديدة",
            "أدوات تقنية لا غنى عنها لأصحاب الأعمال الصغيرة",
            "تطور العمل عن بعد وتأثيره على سوق العمل السعودي",
            "دليل شامل للاستثمار في العملات الرقمية والتقنيات الناشئة"
        ]
        
        # اختيار موضوع عشوائي من القائمة
        chosen_topic = random.choice(topics)
        print(f"🚀 الموضوع المختار اليوم: {chosen_topic}")

        # صياغة الأمر لمنع الحقوق الوهمية
        prompt = (
            f"اكتب مقال HTML احترافي وشامل عن: {chosen_topic}. "
            "ملاحظات هامة:\n"
            "1. لا تذكر أي اسم موقع مثل 'رادار السعودية' أو أي جهة أخرى.\n"
            "2. لا تضع روابط خارجية أو جملة 'جميع الحقوق محفوظة' لأي طرف ثالث.\n"
            "3. استخدم تنسيق SEO قوي (H1, H2, Bullet points).\n"
            "4. اجعل المقال مفيداً وموجهاً للجمهور السعودي والخليجي."
        )
        
        response = model.generate_content(prompt)
        content = response.text.replace('```html', '').replace('```', '').strip()

        # إرسال الإيميل
        msg = MIMEText(content, 'html', 'utf-8')
        msg
