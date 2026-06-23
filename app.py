import streamlit as st
import requests
from streamlit_option_menu import option_menu
from supabase import create_client

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Professional AI Portal", layout="wide")

# --- الإعدادات ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- القائمة الجانبية الاحترافية ---
with st.sidebar:
    selected = option_menu(
        "القائمة الرئيسية", ["السيرة الذاتية", "وظائف مقترحة", "لوحة الإدارة"],
        icons=['file-earmark-text', 'search', 'gear'], menu_icon="cast", default_index=0
    )

# --- دالة الذكاء الاصطناعي ---
def generate_cv(name, job, exp, skills):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {'x-goog-api-key': GEMINI_API_KEY, 'Content-Type': 'application/json'}
    prompt = f"قم بصياغة سيرة ذاتية احترافية جداً لـ {name} لمسمى {job}. الخبرات: {exp}. المهارات: {skills}."
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        res = requests.post(url, headers=headers, json=data).json()
        return res['candidates'][0]['content']['parts'][0]['text']
    except:
        return "حدث خطأ في الاتصال بالسيرفر، يرجى المحاولة لاحقاً."

# --- منطق الصفحات ---
if selected == "السيرة الذاتية":
    st.title("✨ صياغة سيرة ذاتية احترافية")
    with st.form("cv_form"):
        col1, col2 = st.columns(2)
        name = col1.text_input("الاسم الكامل")
        job = col2.text_input("المسمى الوظيفي")
        exp = st.text_area("الخبرات المهنية")
        skills = st.text_input("المهارات")
        submit = st.form_submit_button("توليد الـ CV")
    
    if submit:
        with st.spinner("جاري الإبداع..."):
            st.markdown(generate_cv(name, job, exp, skills))

elif selected == "وظائف مقترحة":
    st.title("🎯 فرص العمل الحالية")
    st.info("جاري فحص السوق بناءً على ملفك الشخصي...")
    # هنا يمكنك إضافة كود الـ BeautifulSoup لسحب الوظائف

elif selected == "لوحة الإدارة":
    st.title("⚙️ لوحة تحكم الإدارة")
    st.write("إحصائيات المنصة والمستخدمين ستظهر هنا.")
