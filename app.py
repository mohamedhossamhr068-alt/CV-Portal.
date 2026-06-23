import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
from supabase import create_client, Client
import pandas as pd

# --- 1. الإعدادات والمفاتيح ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. إدارة اللغة والمظهر ---
st.set_page_config(page_title="AI Career Portal", page_icon="💼", layout="wide")
lang = st.sidebar.selectbox("🌐 اختر اللغة / Choose Language", ["العربية", "English"])

# --- CSS للتنسيق ---
st.markdown("""
    <style>
    .job-card { background-color: #F8FAFC; padding: 15px; border-radius: 8px; border-left: 5px solid #1E3A8A; margin-bottom: 10px; }
    .stButton>button { background-color: #1E3A8A; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- 3. الدوال البرمجية ---
def get_ai_cv(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        if 'candidates' in result:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"خطأ من جوجل: {result.get('error', {}).get('message', 'خطأ غير معروف')}"
    except Exception as e:
        return f"حدث خطأ في الاتصال: {str(e)}"

# --- 4. منطق التطبيق (تسجيل الدخول والواجهة) ---
if 'user' not in st.session_state: st.session_state.user = None

if st.session_state.user is None:
    st.title("تسجيل الدخول / Login")
    with st.form("login"):
        email = st.text_input("البريد الإلكتروني")
        password = st.text_input("كلمة المرور", type="password")
        if st.form_submit_button("دخول"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.rerun()
            except:
                st.error("فشل تسجيل الدخول")
else:
    st.title("بوابة التوظيف الذكية 🚀")
    
    with st.form("cv_form"):
        name = st.text_input("الاسم الكامل")
        job_title = st.text_input("المسمى الوظيفي المستهدف")
        experience = st.text_area("الخبرات المهنية")
        skills = st.text_input("أهم المهارات")
        submitted = st.form_submit_button("توليد السيرة الذاتية والبحث عن وظائف")

    if submitted:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("✨ السيرة الذاتية المطورة")
            with st.spinner("جاري صياغة الـ CV..."):
                prompt = f"أنت خبير HR محترف. قم بصياغة سيرة ذاتية ATS-friendly لـ {name} في مجال {job_title} بناءً على خبرات: {experience} ومهارات: {skills}."
                st.markdown(get_ai_cv(prompt))
        
        with col2:
            st.subheader("🎯 وظائف مقترحة")
            try:
                query = urllib.parse.quote(f"{job_title}")
                url = f"https://wuzzuf.net/search/jobs/?q={query}"
                res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
                soup = BeautifulSoup(res.text, "html.parser")
                jobs = soup.find_all("div", class_="css-1gatmva", limit=5)
                for job in jobs:
                    st.markdown(f'<div class="job-card">{job.text.strip()}</div>', unsafe_allow_html=True)
            except:
                st.warning("تعذر جلب الوظائف حالياً.")
