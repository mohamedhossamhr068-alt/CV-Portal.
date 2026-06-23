```python
import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
from supabase import create_client, Client
import pandas as pd
from fpdf import FPDF

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Career Portal", page_icon="💼", layout="wide", initial_sidebar_state="expanded")

# ─── Secrets ───────────────────────────────────────────────────────────────────
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ─── Language Selector ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌐 Language / اللغة")
    lang = st.radio("", ["العربية", "English"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("<div style='font-size:12px; color:#94A3B8; text-align:center;'>Powered by AI</div>", unsafe_allow_html=True)

is_rtl = lang == "العربية"
direction = "rtl" if is_rtl else "ltr"
text_align = "right" if is_rtl else "left"

# ─── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Inter:wght@400;500;600;700&display=swap');
html, body, [data-testid="stAppViewContainer"] {{
    direction: {direction};
    font-family: {"'Cairo'" if is_rtl else "'Inter'"}, sans-serif;
    background: #F0F4FF;
}}
[data-testid="stSidebar"] {{
    background: linear-gradient(160deg, #0F172A 0%, #1E3A8A 100%);
}}
[data-testid="stSidebar"] * {{ color: #E2E8F0 !important; }}
h1, h2, h3 {{ font-weight: 800; color: #0F172A; }}
.stButton > button {{
    background: linear-gradient(135deg, #1E3A8A, #3B82F6);
    color: #fff; border: none; border-radius: 10px;
    font-weight: 700; font-size: 15px; padding: 0.6rem 1.4rem;
}}
.stButton > button:hover {{
    background: linear-gradient(135deg, #1D4ED8, #60A5FA);
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(59,130,246,0.4);
}}
.stTextInput > div > div > input, .stTextArea > div > textarea {{
    direction: {direction}; text-align: {text_align};
    border-radius: 8px; border: 1.5px solid #CBD5E1;
    font-family: {"'Cairo'" if is_rtl else "'Inter'"}, sans-serif;
}}
.job-card {{
    background: #fff; padding: 16px 20px; border-radius: 12px;
    border-{"right" if is_rtl else "left"}: 4px solid #3B82F6;
    margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    direction: {direction}; text-align: {text_align};
}}
.hero-banner {{
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 60%, #3B82F6 100%);
    border-r```python
import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
from supabase import create_client, Client
import pandas as pd
from fpdf import FPDF

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Career Portal", page_icon="💼", layout="wide", initial_sidebar_state="expanded")

# ─── Secrets ───────────────────────────────────────────────────────────────────
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ─── Language Selector ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌐 Language / اللغة")
    lang = st.radio("", ["العربية", "English"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("<div style='font-size:12px; color:#94A3B8; text-align:center;'>Powered by AI</div>", unsafe_allow_html=True)

is_rtl = lang == "العربية"
direction = "rtl" if is_rtl else "ltr"
text_align = "right" if is_rtl else "left"

# ─── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Inter:wght@400;500;600;700&display=swap');
html, body, [data-testid="stAppViewContainer"] {{
    direction: {direction};
    font-family: {"'Cairo'" if is_rtl else "'Inter'"}, sans-serif;
    background: #F0F4FF;
}}
[data-testid="stSidebar"] {{
    background: linear-gradient(160deg, #0F172A 0%, #1E3A8A 100%);
}}
[data-testid="stSidebar"] * {{ color: #E2E8F0 !important; }}
h1, h2, h3 {{ font-weight: 800; color: #0F172A; }}
.stButton > button {{
    background: linear-gradient(135deg, #1E3A8A, #3B82F6);
    color: #fff; border: none; border-radius: 10px;
    font-weight: 700; font-size: 15px; padding: 0.6rem 1.4rem;
}}
.stButton > button:hover {{
    background: linear-gradient(135deg, #1D4ED8, #60A5FA);
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(59,130,246,0.4);
}}
.stTextInput > div > div > input, .stTextArea > div > textarea {{
    direction: {direction}; text-align: {text_align};
    border-radius: 8px; border: 1.5px solid #CBD5E1;
    font-family: {"'Cairo'" if is_rtl else "'Inter'"}, sans-serif;
}}
.job-card {{
    background: #fff; padding: 16px 20px; border-radius: 12px;
    border-{"right" if is_rtl else "left"}: 4px solid #3B82F6;
    margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    direction: {direction}; text-align: {text_align};
}}
.hero-banner {{
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 60%, #3B82F6 100%);
    border-radius: 16px; padding: 36px 40px; color: white;
    margin-bottom: 28px; direction: {direction}; text-align: {text_align};
}}
.hero-banner h1 {{ color: white; font-size: 2rem; margin-bottom: 6px; }}
.hero-banner p {{ color: #BAE6FD; font-size: 1rem; margin: 0; }}
.stat-badge {{
    display: inline-block; background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25); border-radius: 20px;
    padding: 4px 14px; font-size: 13px; color: #E0F2FE; margin-top: 14px;
}}
.section-card {{
    background: #fff; border-radius: 14px; padding: 28px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07); margin-bottom: 20px;
    direction: {direction}; text-align: {text_align};
}}
.resume-output {{
    background: #F8FAFF; border: 1px solid #DBEAFE; border-radius: 12px;
    padding: 24px; font-size: 15px; line-height: 1.9;
    direction: {direction}; text-align: {text_align};
}}
.linkedin-btn {{
    display: block; background: #0A66C2; color: white !important;
    text-decoration: none; text-align: center; padding: 14px;
    border-radius: 10px; font-weight: 700; margin-bottom: 20px;
}}
.quota-bar {{ background: #E0E7FF; border-radius: 20px; height: 8px; margin-top: 6px; overflow: hidden; }}
.quota-fill {{ height: 8px; border-radius: 20px; background: linear-gradient(90deg, #3B82F6, #6366F1); }}
</style>
""", unsafe_allow_html=True)

# ─── UI Text ───────────────────────────────────────────────────────────────────
ui = {
    "العربية": {
        "login_title": "مرحباً بك في بوابة التوظيف الذكية 💼",
        "login_sub": "سجّل الدخول أو أنشئ حسابًا جديدًا للبدء.",
        "email": "البريد الإلكتروني",
        "password": "كلمة المرور",
        "login_btn": "تسجيل الدخول",
        "signup_btn": "إنشاء حساب جديد",
        "logout": "خروج 🚪",
        "main_title": "بوابة التوظيف الذكية 🚀",
        "main_sub": "صيّغ سيرتك الذاتية باحترافية واعثر على أفضل الفرص الوظيفية",
        "welcome": "👤 {email}",
        "usage": "الاستخدام: {count} / 3 محاولات مجانية",
        "quota_error": "⛔ استنفدت حدّك المجاني.",
        "form_header": "أدخل بياناتك المهنية",
        "name": "الاسم الكامل",
        "job_title": "المسمى الوظيفي المستهدف",
        "location": "المنطقة / الموقع",
        "exp": "ملخص الخبرات العملية",
        "skills": "أبرز المهارات",
        "submit_btn": "✨ توليد السيرة والبحث عن وظائف",
        "loading_ai": "الذكاء الاصطناعي يصيغ سيرتك...",
        "loading_jobs": "جاري فحص سوق العمل...",
        "cv_header": "✨ السيرة الذاتية المطوّرة",
        "jobs_header": "🎯 الفرص الوظيفية المقترحة",
        "wuzzuf_header": "وظائف من منصة Wuzzuf:",
        "no_jobs": "لم نجد وظائف مطابقة حالياً.",
        "linkedin_btn": "💼 استعرض الوظائف على LinkedIn",
        "admin_title": "⚙️ لوحة تحكم المشرف",
        "validation_error": "⚠️ يرجى ملء جميع الحقول",
        "download_pdf": "📥 تحميل PDF",
        "ai_prompt": "اكتب سيرة ذاتية احترافية لهذا الشخص بالضبط بدون اختراع أي معلومات:\n\nالاسم: {name}\nالمسمى الوظيفي المستهدف: {job_title}\nالخبرا```python
import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
from supabase import create_client, Client
import pandas as pd
from fpdf import FPDF

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Career Portal", page_icon="💼", layout="wide", initial_sidebar_state="expanded")

# ─── Secrets ───────────────────────────────────────────────────────────────────
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ─── Language Selector ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌐 Language / اللغة")
    lang = st.radio("", ["العربية", "English"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("<div style='font-size:12px; color:#94A3B8; text-align:center;'>Powered by AI</div>", unsafe_allow_html=True)

is_rtl = lang == "العربية"
direction = "rtl" if is_rtl else "ltr"
text_align = "right" if is_rtl else "left"

# ─── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Inter:wght@400;500;600;700&display=swap');
html, body, [data-testid="stAppViewContainer"] {{
    direction: {direction};
    font-family: {"'Cairo'" if is_rtl else "'Inter'"}, sans-serif;
    background: #F0F4FF;
}}
[data-testid="stSidebar"] {{
    background: linear-gradient(160deg, #0F172A 0%, #1E3A8A 100%);
}}
[data-testid="stSidebar"] * {{ color: #E2E8F0 !important; }}
h1, h2, h3 {{ font-weight: 800; color: #0F172A; }}
.stButton > button {{
    background: linear-gradient(135deg, #1E3A8A, #3B82F6);
    color: #fff; border: none; border-radius: 10px;
    font-weight: 700; font-size: 15px; padding: 0.6rem 1.4rem;
}}
.stButton > button:hover {{
    background: linear-gradient(135deg, #1D4ED8, #60A5FA);
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(59,130,246,0.4);
}}
.stTextInput > div > div > input, .stTextArea > div > textarea {{
    direction: {direction}; text-align: {text_align};
    border-radius: 8px; border: 1.5px solid #CBD5E1;
    font-family: {"'Cairo'" if is_rtl else "'Inter'"}, sans-serif;
}}
.job-card {{
    background: #fff; padding: 16px 20px; border-radius: 12px;
    border-{"right" if is_rtl else "left"}: 4px solid #3B82F6;
    margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    direction: {direction}; text-align: {text_align};
}}
.hero-banner {{
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 60%, #3B82F6 100%);
    border-radius: 16px; padding: 36px 40px; color: white;
    margin-bottom: 28px; direction: {direction}; text-align: {text_align};
}}
.hero-banner h1 {{ color: white; font-size: 2rem; margin-bottom: 6px; }}
.hero-banner p {{ color: #BAE6FD; font-size: 1rem; margin: 0; }}
.stat-badge {{
    display: inline-block; background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25); border-radius: 20px;
    padding: 4px 14px; font-size: 13px; color: #E0F2FE; margin-top: 14px;
}}
.section-card {{
    background: #fff; border-radius: 14px; padding: 28px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07); margin-bottom: 20px;
    direction: {direction}; text-align: {text_align};
}}
.resume-output {{
    background: #F8FAFF; border: 1px solid #DBEAFE; border-radius: 12px;
    padding: 24px; font-size: 15px; line-height: 1.9;
    direction: {direction}; text-align: {text_align};
}}
.linkedin-btn {{
    display: block; background: #0A66C2; color: white !important;
    text-decoration: none; text-align: center; padding: 14px;
    border-radius: 10px; font-weight: 700; margin-bottom: 20px;
}}
.quota-bar {{ background: #E0E7FF; border-radius: 20px; ```python
import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
from supabase import create_client, Client
import pandas as pd
from fpdf import FPDF

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Career Portal", page_icon="💼", layout="wide", initial_sidebar_state="expanded")

# ─── Secrets ───────────────────────────────────────────────────────────────────
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ─── Language Selector ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌐 Language / اللغة")
    lang = st.radio("", ["العربية", "English"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("<div style='font-size:12px; color:#94A3B8; text-align:center;'>Powered by AI</div>", unsafe_allow_html=True)

is_rtl = lang == "العربية"
direction = "rtl" if is_rtl else "ltr"
text_align = "right" if is_rtl else "left"

# ─── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Inter:wght@400;500;600;700&display=swap');
html, body, [data-testid="stAppViewContainer"] {{
    direction: {direction};
    font-family: {"'Cairo'" if is_rtl else "'Inter'"}, sans-serif;
    background: #F0F4FF;
}}
[data-testid="stSidebar"] {{
    background: linear-gradient(160deg, #0F172A 0%, #1E3A8A 100%);
}}
[data-testid="stSidebar"] * {{ color: #E2E8F0 !important; }}
h1, h2, h3 {{ font-weight: 800; color: #0F172A; }}
.stButton > button {{
    background: linear-gradient(135deg, #1E3A8A, #3B82F6);
    color: #fff; border: none; border-radius: 10px;
    font-weight: 700; font-size: 15px; padding: 0.6rem 1.4rem;
}}
.stButton > button:hover {{
    background: linear-gradient(135deg, #1D4ED8, #60A5FA);
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(59,130,246,0.4);
}}
.stTextInput > div > div > input, .stTextArea > div > textarea {{
    direction: {direction}; text-align: {text_align};
    border-radius: 8px; border: 1.5px solid #CBD5E1;
    font-family: {"'Cairo'" if is_rtl else "'Inter'"}, sans-serif;
}}
.job-card {{
    background: #fff; padding: 16px 20px; border-radius: 12px;
    border-{"right" if is_rtl else "left"}: 4px solid #3B82F6;
    margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    direction: {direction}; text-align: {text_align};
}}
.hero-banner {{
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 60%, #3B82F6 100%);
    border-radius: 16px; padding: 36px 40px; color: white;
    margin-bottom: 28px; direction: {direction}; text-align: {text_align};
}}
.hero-banner h1 {{ color: white; font-size: 2rem; margin-bottom: 6px; }}
.hero-banner p {{ color: #BAE6FD; font-size: 1rem; margin: 0; }}
.stat-badge {{
    display: inline-block; background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25); border-radius: 20px;
    padding: 4px 14px; font-size: 13px; color: #E0F2FE; margin-top: 14px;
}}
.section-card {{
    background: #fff; border-radius: 14px; padding: 28px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07); margin-bottom: 20px;
    direction: {direction}; text-align: {text_align};
}}
.resume-output {{
    background: #F8FAFF; border: 1px solid #DBEAFE; border-radius: 12px;
    padding: 24px; font-size: 15px; line-height: 1.9;
    direction: {direction}; text-align: {text_align};
}}
.linkedin-btn {{
    display: block; background: #0A66C2; color: white !important;
    text-decoration: none; text-align: center; padding: 14px;
    border-radius: 10px; font-weight: 700; margin-bottom: 20px;
}}
.quota-bar {{ background: #E0E7FF; border-radius: 20px; height: 8px; margin-top: 6px; overflow: hidden; }}
.quota-fill {{ height: 8px; border-radius: 20px; background: linear-gradient(90deg, #3B82F6, #6366F1); }}
</style```python
import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
from supabase import create_client, Client
import pandas as pd
from fpdf import FPDF

st.set_page_config(page_title="AI Career Portal", page_icon="💼", layout="wide", initial_sidebar_state="expanded")

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

with st.sidebar:
    st.markdown("### 🌐 Language / اللغة")
    lang = st.radio("", ["العربية", "English"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("<div style='font-size:12px; color:#94A3B8; text-align:center;'>Powered by AI</div>", unsafe_allow_html=True)

is_rtl = lang == "العربية"
direction = "rtl" if is_rtl else "ltr"
text_align = "right" if is_rtl else "left"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Inter:wght@400;500;600;700&display=swap');
html, body, [data-testid="stAppViewContainer"] {{
    direction: {direction};
    font-family: {"'Cairo'" if is_rtl else "'Inter'"}, sans-serif;
    background: #F0F4FF;
}}
[data-testid="stSidebar"] {{
    background: linear-gradient(160deg, #0F172A 0%, #1E3A8A 100%);
}}
[data-testid="stSidebar"] * {{ color: #E2E8F0 !important; }}
h1, h2, h3 {{ font-weight: 800; color: #0F172A; }}
.stButton > button {{
    background: linear-gradient(135deg, #1E3A8A, #3B82F6);
    color: #fff; border: none; border-radius: 10px;
    font-weight: 700; font-size: 15px; padding: 0.6rem 1.4rem;
}}
.stButton > button:hover {{
    background: linear-gradient(135deg, #1D4ED8, #60A5FA);
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(59,130,246,0.4);
}}
.stTextInput > div > div > input, .stTextArea > div > textarea {{
    direction: {direction}; text-align: {text_align};
    border-radius: 8px; border: 1.5px solid #CBD5E1;
    font-family: {"'Cairo'" if is_rtl else "'Inter'"}, sans-serif;
}}
.job-card {{
    background: #fff; padding: 16px 20px; border-radius: 12px;
    border-{"right" if is_rtl else "left"}: 4px solid #3B82F6;
    margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    direction: {direction}; text-align: {text_align};
}}
.hero-banner {{
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 60%, #3B82F6 100%);
    border-radius: 16px; padding: 36px 40px; color: white;
    margin-bottom: 28px; direction: {direction}; text-align: {text_align};
}}
.hero-banner h1 {{ color: white; font-size: 2rem; margin-bottom: 6px; }}
.hero-banner p {{ color: #BAE6FD; font-size: 1rem; margin: 0; }}
.stat-badge {{
    display: inline-block; background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25); border-radius: 20px;
    padding: 4px 14px; font-size: 13px; color: #E0F2FE; margin-top: 14px;
}}
.section-card {{
    background: #fff; border-radius: 14px; padding: 28px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07); margin-bottom: 20px;
    direction: {direction}; text-align: {text_align};
}}
.resume-output {{
    background: #F8FAFF; border: 1px solid #DBEAFE; border-radius: 12px;
    padding: 24px; font-size: 15px; line-height: 1.9;
    direction: {direction}; text-align: {text_align};
}}
.linkedin-btn {{
    display: block; background: #0A66C2; color: white !important;
    text-decoration: none; text-align: center; padding: 14px;
    border-radius: 10px; font-weight: 700; margin-bottom: 20px;
}}
.quota-bar {{ background: #E0E7FF; border-radius: 20px; height: 8px; margin-top: 6px; overflow: hidden; }}
.quota-fill {{ height: 8px; border-radius: 20px; background: linear-gradient(90deg, #3B82F6, #6366F1); }}
</style>
""", unsafe_allow_html=True)
Your workspace has exhausted its trial use of AI.
