import feedparser
import google.generativeai as genai
import requests
import os

# إعدادات المفاتيح (سنجعلها سرية في GitHub لاحقاً)
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
BLOG_ID = os.getenv("BLOG_ID")
BLOGGER_TOKEN = os.getenv("BLOGGER_TOKEN")
RSS_URL = "https://feeds.bbci.co.uk/arabic/rss.xml"

def get_latest_news():
    feed = feedparser.parse(RSS_URL)
    item = feed.entries[0]
    return item.title, item.summary

def rephrase_with_gemini(title, description):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"خبير سيو. أعد صياغة هذا الخبر بأسلوب احترافي وحصري: \nالعنوان: {title}\nالتفاصيل: {description}"
    response = model.generate_content(prompt)
    return response.text

def post_to_blogger(content):
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {"Authorization": f"Bearer {BLOGGER_TOKEN}"}
    payload = {
        "kind": "blogger#post",
        "title": "مقال تقني جديد", # جيمناي سيعدل العنوان داخل المحتوى
        "content": content
    }
    r = requests.post(url, json=payload, headers=headers)
    return r.status_code

# تشغيل البوت
title, desc = get_latest_news()
new_content = rephrase_with_gemini(title, desc)
status = post_to_blogger(new_content)
print(f"Status: {status}")
