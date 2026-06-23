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

# --- 2. إدارة اللغتين والتحكم في المظهر الاحترافي ---
st.set_page_config(page_title="AI Career Portal", page_icon="💼", layout="wide")

lang = st.sidebar.selectbox("🌐 اختر اللغة / Choose Language", ["العربية", "English"])

if lang == "العربية":
    direction = "rtl"
    text_align = "right"
    align_css = """
    <style>
    body, .stApp { direction: rtl; text-align: right; }
    .stTextInput > div > div > input, .stTextArea > div > textarea { text-align: right; direction: rtl; }
    div[data-baseweb="input"] { text-align: right; }
    .stAlert { direction: rtl; text-align: right; }
    </style>
    """
else:
    direction = "ltr"
    text_align = "left"
    align_css = """
    <style>
    body, .stApp { direction: ltr; text-align: left; }
    .stTextInput > div > div > input, .stTextArea > div > textarea { text-align: left; direction: ltr; }
    div[data-baseweb="input"] { text-align: left; }
    .stAlert { direction: ltr; text-align: left; }
    </style>
    """

st.markdown(align_css, unsafe_allow_html=True)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [data-testid="stMarkdownContainer"] { font-family: 'Inter', sans-serif; }
    h1, h2, h3 { color: #1E3A8A; font-weight: 700; }
    .stButton>button { background-color: #1E3A8A; color: white; border-radius: 8px; font-weight: 600; }
    .stButton>button:hover { background-color: #1D4ED8; color: white; }
    .job-card { background-color: #F8FAFC; padding: 15px; border-radius: 8px; border-left: 5px solid #1E3A8A; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

ui_text = {
    "العربية": {
        "login_title": "تسجيل الدخول للمنصة 🔐",
        "login_info": "قم بإنشاء حساب جديد أو تسجيل الدخول للبدء في استخدام المنصة.",
        "email": "البريد الإلكتروني",
        "password": "كلمة المرور",
        "login_btn": "تسجيل الدخول",
        "signup_btn": "إنشاء حساب جديد",
        "logout": "تسجيل الخروج",
        "main_title": "بوابة صياغة السيرة الذاتية وترشيحات الوظائف 🚀",
        "welcome": "👤 مرحباً: {email} | 📊 الاستخدام: {count}/3 محاولات مجانية.",
        "quota_error": "⛔ لقد استنفدت الحد الأقصى للمحاولات المجانية. يرجى التواصل مع الإدارة.",
        "form_header": "أدخل بياناتك المهنية الحالية:",
        "name": "الاسم الكامل",
        "job_title": "المسمى الوظيفي المستهدف (مثال: Production Manager)",
        "location": "المنطقة الحالية أو المستهدفة (مثال: Cairo)",
        "exp": "الخبرات العملية باختصار (أماكن العمل السابقة والمهام)",
        "skills": "أهم المهارات التي تتقنها",
        "submit_btn": "توليد السيرة الذاتية الذكية والبحث عن وظائف",
        "loading_ai": "جاري صياغة وتحسين السيرة الذاتية بواسطة الذكاء الاصطناعي...",
        "loading_jobs": "جاري فحص سوق العمل وسحب الوظائف الحالية...",
        "wuzzuf_header": "وظائف مقترحة لك من منصة Wuzzuf:",
        "no_jobs": "لم نجد وظائف مطابقة حالياً على وظف.",
        "linkedin_btn": "💼 عرض الوظائف المتاحة مباشرة على LinkedIn",
        "admin_title": "⚙️ لوحة تحكم الإدارة (Admin Dashboard)",
        "ai_prompt": "أنت خبير موارد بشرية محترف ومستشار تطوير مؤسسي. قم بإعادة صياغة وتنظيم البيانات التالية لتكوين سيرة ذاتية احترافية وجذابة للغاية ومجهزة لأنظمة الـ ATS باللغة العربية.\nالاسم: {name}\nالمسمى الوظيفي: {job_title}\nالخبرات: {experience}\nالمهارات: {skills}\nنسقها في نقاط احترافية وركز على الكلمات المفتاحية القوية."
    },
    "English": {
        "login_title": "Platform Login 🔐",
        "login_info": "Create a new account or log in to start using the platform.",
        "email": "Email Address",
        "password": "Password",
        "login_btn": "Log In",
        "signup_btn": "Register New Account",
        "logout": "Log Out",
        "main_title": "AI-Powered Career Portal & Job Recommender 🚀",
        "welcome": "👤 Welcome: {email} | 📊 Usage: {count}/3 free attempts.",
        "quota_error": "⛔ You have exhausted your free attempts. Please contact admin for upgrade.",
        "form_header": "Enter your professional details:",
        "name": "Full Name",
        "job_title": "Target Job Title (e.g., Production Manager)",
        "location": "Location (e.g., Quesna, Menofia)",
        "exp": "Brief Work Experience (Previous companies and roles)",
        "skills": "Key Skills & Core Competencies",
        "submit_btn": "Generate Smart CV & Find Jobs",
        "loading_ai": "AI is crafting and optimizing your professional resume...",
        "loading_jobs": "Scanning the job market and fetching live openings...",
        "wuzzuf_header": "Recommended Openings from Wuzzuf:",
        "no_jobs": "No matching jobs found on Wuzzuf at the moment.",
        "linkedin_btn": "💼 View Live Job Openings on LinkedIn",
        "admin_title": "⚙️ Admin Dashboard",
        "ai_prompt": "You are an elite HR Expert and Executive Recruiter. Rewrite and optimize the following raw details into a world-class, ATS-friendly corporate resume in English.\nName: {name}\nJob Title: {job_title}\nExperience: {experience}\nSkills: {skills}\nFormat it beautifully using clean bullet points and powerful action verbs."
    }
}[lang]

if 'user' not in st.session_state:
    st.session_state.user = None

# --- 3. شاشة تسجيل الدخول ---
if st.session_state.user is None:
    st.title(ui_text["login_title"])
    st.info(ui_text["login_info"])
    
    with st.form("login_form"):
        email = st.text_input(ui_text["email"])
        password = st.text_input(ui_text["password"], type="password")
        col1, col2 = st.columns(2)
        with col1:
            login_btn = st.form_submit_button(ui_text["login_btn"])
        with col2:
            signup_btn = st.form_submit_button(ui_text["signup_btn"])
            
    if signup_btn:
        try:
            res = supabase.auth.sign_up({"email": email, "password": password})
            st.success("Success! Account created. Please click Log In now.")
            if res.user:
               supabase.table("user_profiles").insert({"id": res.user.id, "email": email}).execute()
        except Exception as e:
            st.error("Error creating account. Ensure valid email and min 6 characters password.")
            
    if login_btn:
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            st.session_state.user = res.user
            st.rerun() 
        except Exception as e:
            st.error("Authentication failed. Please check your credentials.")

# --- 4. الشاشة الرئيسية بعد الدخول ---
else:
    col_a, col_b = st.columns([8, 2])
    with col_a:
        st.title(ui_text["main_title"])
    with col_b:
        if st.button(ui_text["logout"], use_container_width=True):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()

    try:
        profile = supabase.table("user_profiles").select("*").eq("id", st.session_state.user.id).execute()
        usage_count = profile.data[0]['usage_count']
        role = profile.data[0]['role']
    except Exception as e:
        usage_count = 0
        role = 'user'

    st.info(ui_text["welcome"].format(email=st.session_state.user.email, count=usage_count))

    if role == 'admin':
        st.write("---")
        st.subheader(ui_text["admin_title"])
        users_data = supabase.table("user_profiles").select("*").execute()
        if users_data.data:
            df = pd.DataFrame(users_data.data)
            df = df[['email', 'role', 'usage_count', 'created_at']]
            df.columns = ['Email', 'Role', 'Usage Count', 'Registration Date']
            st.dataframe(df, use_container_width=True)
        st.write("---")

    if usage_count >= 3 and role != 'admin':
        st.error(ui_text["quota_error"])
    else:
        with st.form("cv_form"):
            st.subheader(ui_text["form_header"])
            name = st.text_input(ui_text["name"])
            job_title = st.text_input(ui_text["job_title"])
            location = st.text_input(ui_text["location"])
            experience = st.text_area(ui_text["exp"])
            skills = st.text_area(ui_text["skills"])
            submitted = st.form_submit_button(ui_text["submit_btn"])

        if submitted and name and job_title:
            new_count = usage_count + 1
            supabase.table("user_profiles").update({"usage_count": new_count}).eq("id", st.session_state.user.id).execute()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("✨ Optimized Resume / السيرة الذاتية المطورة")
                with st.spinner(ui_text["loading_ai"]):
                    prompt = ui_text["ai_prompt"].format(name=name, job_title=job_title, experience=experience, skills=skills)
                    try:
                        # استدعاء مباشر لـ REST API الخاص بجوجل لتخطي أخطاء المكتبة مع مفاتيح AQ
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
                        headers = {'Content-Type': 'application/json'}
                        data = {
                            "contents": [{"parts": [{"text": prompt}]}]
                        }
                        response = requests.post(url, headers=headers, json=data)
                        result = response.json()
                        
                        if 'error' in result:
                            st.error(f"خطأ من جوجل: {result['error']['message']}")
                        else:
                            ai_text = result['candidates'][0]['content']['parts'][0]['text']
                            st.markdown(ai_text)
                    except Exception as e:
                        st.error(f"حدث خطأ في الاتصال: {str(e)}")

            with col2:
                st.subheader("🎯 Job Opportunities / الفرص المتاحة")
                with st.spinner(ui_text["loading_jobs"]):
                    try:
                        linkedin_query = urllib.parse.quote(job_title)
                        linkedin_loc = urllib.parse.quote(location)
                        linkedin_link = f"https://www.linkedin.com/jobs/search/?keywords={linkedin_query}&location={linkedin_loc}"
                        st.markdown(f'<a href="{linkedin_link}" target="_blank"><button style="width:100%; background-color:#0A66C2; color:white; border:none; padding:12px; border-radius:8px; font-weight:bold; cursor:pointer; margin-bottom:20px;">{ui_text["linkedin_btn"]}</button></a>', unsafe_allow_html=True)
                        
                        st.markdown(f"<h5>{ui_text['wuzzuf_header']}</h5>", unsafe_allow_html=True)
                        
                        query = urllib.parse.quote(f"{job_title} {location}")
                        url = f"https://wuzzuf.net/search/jobs/?q={query}&a=hpb"
                        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
                        soup = BeautifulSoup(res.text, "html.parser")
                        
                        job_cards = soup.find_all("div", class_="css-1gatmva e1v1l3u10", limit=5)
                        if not job_cards:
                            st.warning(ui_text["no_jobs"])
                        else:
                            for card in job_cards:
                                title_elem = card.find("h2", class_="css-m604qf")
                                company_elem = card.find("a", class_="css-17s97q8")
                                if title_elem and company_elem:
                                    job_link = "https://wuzzuf.net" + title_elem.find("a")["href"]
                                    st.markdown(f"""
                                        <div class="job-card">
                                            <a href="{job_link}" target="_blank" style="color:#1E3A8A; font-weight:bold; text-decoration:none;">{title_elem.text.strip()}</a>
                                            <div style="color:#64748B; font-size:13px; margin-top:5px;">🏢 {company_elem.text.strip().replace(' -', '')}</div>
                                        </div>
                                    """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error("Market Scraping Error.")
