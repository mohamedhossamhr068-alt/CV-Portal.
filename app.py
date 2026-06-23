import streamlit as st
import requests
from supabase import create_client

# إعدادات الاتصال
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("بوابة صياغة السيرة الذاتية 🚀")

# النموذج
with st.form("cv_form"):
    name = st.text_input("الاسم الكامل")
    job_title = st.text_input("المسمى الوظيفي المستهدف")
    experience = st.text_area("الخبرات المهنية")
    skills = st.text_input("المهارات")
    submitted = st.form_submit_button("توليد السيرة الذاتية")

if submitted:
    with st.spinner("جاري التواصل مع ذكاء Gemini..."):
        # البرومبت المباشر
        prompt = f"أنت خبير توظيف. قم بكتابة سيرة ذاتية احترافية ATS-friendly لـ {name} في مجال {job_title} بناءً على خبرات: {experience} ومهارات: {skills}."
        
        # الاتصال بجوجل (REST API)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            response = requests.post(url, json=data).json()
            if 'candidates' in response:
                cv_result = response['candidates'][0]['content']['parts'][0]['text']
                st.markdown(cv_result)
            else:
                st.error(f"خطأ: {response}")
        except Exception as e:
            st.error(f"مشكلة في الاتصال: {e}")
