import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
from supabase import create_client
import pandas as pd

# --- 1. الإعدادات ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. التنسيق والواجهة ---
st.set_page_config(page_title="AI Career Portal", layout="wide")
lang = st.sidebar.selectbox("🌐 اختر اللغة", ["العربية", "English"])

# تنسيق CSS لضبط الاتجاهات والجماليات
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    [data-testid="stSidebar"] { direction: rtl; }
    .job-card { background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-right: 5px solid #1E3A8A; }
    .stButton>button { width: 100%; background-color: #1E3A8A; color: white; }
    </style>
    """ if lang == "العربية" else """
    <style>
    .stApp { direction: ltr; text-align: left; }
    .job-card { background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #1E3A8A; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. دالة الـ AI الاحترافية ---
def get_ai_cv(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {'Content-Type': 'application/json', 'x-goog-api-key': GEMINI_API_KEY}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(url, headers=headers, json=data).json()
        return response['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"خطأ في الاتصال: {e}"

# --- 4. المحتوى ---
st.title("بوابة التوظيف الذكية 🚀")

with st.form("cv_form"):
    col1, col2 = st.columns(2)
    name = col1.text_input("الاسم الكامل")
    job_title = col2.text_input("المسمى الوظيفي")
    experience = st.text_area("الخبرات المهنية")
    skills = st.text_input("المهارات")
    submitted = st.form_submit_button("توليد السيرة الذاتية")

if submitted:
    tab1, tab2 = st.tabs(["✨ السيرة الذاتية", "🎯 الوظائف المقترحة"])
    with tab1:
        st.markdown(get_ai_cv(f"أنت خبير توظيف. اكتب سيرة ذاتية احترافية لـ {name} في {job_title} بناءً على: {experience} و {skills}"))
    with tab2:
        try:
            url = f"https://wuzzuf.net/search/jobs/?q={urllib.parse.quote(job_title)}"
            soup = BeautifulSoup(requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text, "html.parser")
            for job in soup.find_all("div", class_="css-1gatmva", limit=5):
                st.markdown(f'<div class="job-card">{job.text.strip()}</div>', unsafe_allow_html=True)
        except:
            st.warning("تعذر جلب الوظائف.")
