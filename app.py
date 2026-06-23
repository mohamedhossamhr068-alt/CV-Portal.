import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
from supabase import create_client

# --- إعدادات ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- تنسيق احترافي ---
st.set_page_config(page_title="AI Career Portal", layout="wide")
lang = st.sidebar.selectbox("🌐 Language", ["العربية", "English"])

# منطق اللغة والاتجاهات
is_rtl = (lang == "العربية")
align = "right" if is_rtl else "left"
dir = "rtl" if is_rtl else "ltr"

st.markdown(f"""
    <style>
    .stApp {{ direction: {dir}; text-align: {align}; }}
    .job-card {{ background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-{ 'right' if is_rtl else 'left' }: 5px solid #1E3A8A; }}
    </style>
""", unsafe_allow_html=True)

# --- الدوال ---
def get_ai_cv(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {'x-goog-api-key': GEMINI_API_KEY, 'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(url, headers=headers, json=data).json()
        return response['candidates'][0]['content']['parts'][0]['text']
    except: return "خطأ في الاتصال بالذكاء الاصطناعي."

# --- الواجهة ---
st.title("بوابة التوظيف الذكية 🚀" if is_rtl else "AI Career Portal 🚀")

with st.form("cv_form"):
    col1, col2 = st.columns(2)
    name = col1.text_input("الاسم الكامل" if is_rtl else "Full Name")
    job_title = col2.text_input("المسمى الوظيفي" if is_rtl else "Job Title")
    experience = st.text_area("الخبرات" if is_rtl else "Experience")
    skills = st.text_input("المهارات" if is_rtl else "Skills")
    submitted = st.form_submit_button("توليد السيرة الذاتية" if is_rtl else "Generate CV")

if submitted:
    st.markdown("---")
    res = get_ai_cv(f"Write a professional CV for {name} targeting {job_title} with skills {skills}. Experience: {experience}")
    st.markdown(res)
