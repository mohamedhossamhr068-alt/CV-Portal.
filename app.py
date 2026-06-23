import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
from supabase import create_client, Client
import pandas as pd

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Career Portal",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Secrets ───────────────────────────────────────────────────────────────────
SUPABASE_URL  = st.secrets["SUPABASE_URL"]
SUPABASE_KEY  = st.secrets["SUPABASE_KEY"]
GEMINI_API_KEY = "AIzaSyA4WQJrIIbKAoflL1ty96qBZOz-12sRBpg"   # مفتاح Gemini

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ─── Language Selector ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌐 Language / اللغة")
    lang = st.radio("", ["العربية", "English"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown(
        "<div style='font-size:12px; color:#94A3B8; text-align:center;'>Powered by Gemini AI</div>",
        unsafe_allow_html=True
    )

is_rtl = lang == "العربية"

# ─── Global CSS ────────────────────────────────────────────────────────────────
direction   = "rtl" if is_rtl else "ltr"
text_align  = "right" if is_rtl else "left"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Inter:wght@400;500;600;700&display=swap');

/* ── Base ─────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {{
    direction: {direction};
    font-family: {"'Cairo'" if is_rtl else "'Inter'"}, sans-serif;
    background: #F0F4FF;
}}

/* ── Sidebar ─────────────────────────────────────── */
[data-testid="stSidebar"] {{
    background: linear-gradient(160deg, #0F172A 0%, #1E3A8A 100%);
}}
[data-testid="stSidebar"] * {{
    color: #E2E8F0 !important;
}}

/* ── Headings ────────────────────────────────────── */
h1, h2, h3 {{
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.5px;
}}

/* ── Buttons ─────────────────────────────────────── */
.stButton > button {{
    background: linear-gradient(135deg, #1E3A8A, #3B82F6);
    color: #fff;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    font-size: 15px;
    padding: 0.6rem 1.4rem;
    transition: all 0.2s;
    letter-spacing: 0.3px;
}}
.stButton > button:hover {{
    background: linear-gradient(135deg, #1D4ED8, #60A5FA);
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(59,130,246,0.4);
}}

/* ── Form inputs ─────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > textarea {{
    direction: {direction};
    text-align: {text_align};
    border-radius: 8px;
    border: 1.5px solid #CBD5E1;
    background: #fff;
    font-family: {"'Cairo'" if is_rtl else "'Inter'"}, sans-serif;
    font-size: 15px;
    padding: 10px 14px;
}}
.stTextInput > div > div > input:focus,
.stTextArea > div > textarea:focus {{
    border-color: #3B82F6;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15);
}}

/* ── Cards ───────────────────────────────────────── */
.job-card {{
    background: #fff;
    padding: 16px 20px;
    border-radius: 12px;
    border-{("right" if is_rtl else "left")}: 4px solid #3B82F6;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    transition: box-shadow 0.2s;
    direction: {direction};
    text-align: {text_align};
}}
.job-card:hover {{
    box-shadow: 0 4px 16px rgba(59,130,246,0.15);
}}

/* ── Hero banner ─────────────────────────────────── */
.hero-banner {{
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 60%, #3B82F6 100%);
    border-radius: 16px;
    padding: 36px 40px;
    color: white;
    margin-bottom: 28px;
    direction: {direction};
    text-align: {text_align};
}}
.hero-banner h1 {{
    color: white;
    font-size: 2rem;
    margin-bottom: 6px;
}}
.hero-banner p {{
    color: #BAE6FD;
    font-size: 1rem;
    margin: 0;
}}

/* ── Stat badge ─────────────────────────────────── */
.stat-badge {{
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 13px;
    color: #E0F2FE;
    margin-top: 14px;
}}

/* ── Section card ────────────────────────────────── */
.section-card {{
    background: #fff;
    border-radius: 14px;
    padding: 28px 28px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    margin-bottom: 20px;
    direction: {direction};
    text-align: {text_align};
}}

/* ── Resume output ───────────────────────────────── */
.resume-output {{
    background: #F8FAFF;
    border: 1px solid #DBEAFE;
    border-radius: 12px;
    padding: 24px;
    font-size: 15px;
    line-height: 1.9;
    direction: {direction};
    text-align: {text_align};
}}

/* ── Admin table ─────────────────────────────────── */
.dataframe {{ font-size: 14px; }}

/* ── Alerts ──────────────────────────────────────── */
.stAlert {{ direction: {direction}; text-align: {text_align}; border-radius: 10px; }}

/* ── LinkedIn button ─────────────────────────────── */
.linkedin-btn {{
    display: block;
    background: #0A66C2;
    color: white !important;
    text-decoration: none;
    text-align: center;
    padding: 14px;
    border-radius: 10px;
    font-weight: 700;
    font-size: 15px;
    margin-bottom: 20px;
    transition: background 0.2s;
}}
.linkedin-btn:hover {{ background: #004182; }}

/* ── Quota bar ───────────────────────────────────── */
.quota-bar {{
    background: #E0E7FF;
    border-radius: 20px;
    height: 8px;
    margin-top: 6px;
    overflow: hidden;
}}
.quota-fill {{
    height: 8px;
    border-radius: 20px;
    background: linear-gradient(90deg, #3B82F6, #6366F1);
    transition: width 0.4s;
}}
</style>
""", unsafe_allow_html=True)


# ─── UI Text ───────────────────────────────────────────────────────────────────
ui = {
    "العربية": {
        "login_title":   "مرحباً بك في بوابة التوظيف الذكية 💼",
        "login_sub":     "سجّل الدخول أو أنشئ حسابًا جديدًا للبدء.",
        "email":         "البريد الإلكتروني",
        "password":      "كلمة المرور",
        "login_btn":     "تسجيل الدخول",
        "signup_btn":    "إنشاء حساب جديد",
        "logout":        "خروج 🚪",
        "main_title":    "بوابة التوظيف الذكية 🚀",
        "main_sub":      "صيّغ سيرتك الذاتية باحترافية واعثر على أفضل الفرص الوظيفية",
        "welcome":       "👤 {email}",
        "usage":         "الاستخدام: {count} / 3 محاولات مجانية",
        "quota_error":   "⛔ استنفدت حدّك المجاني. تواصل مع الإدارة للحصول على المزيد.",
        "form_header":   "أدخل بياناتك المهنية",
        "name":          "الاسم الكامل",
        "job_title":     "المسمى الوظيفي المستهدف  (مثال: Production Manager)",
        "location":      "المنطقة / الموقع  (مثال: Cairo)",
        "exp":           "ملخص الخبرات العملية",
        "skills":        "أبرز المهارات التقنية والشخصية",
        "submit_btn":    "✨ توليد السيرة والبحث عن وظائف",
        "loading_ai":    "الذكاء الاصطناعي يصيغ سيرتك...",
        "loading_jobs":  "جاري فحص سوق العمل...",
        "cv_header":     "✨ السيرة الذاتية المطوّرة",
        "jobs_header":   "🎯 الفرص الوظيفية المقترحة",
        "wuzzuf_header": "وظائف من منصة Wuzzuf:",
        "no_jobs":       "لم نجد وظائف مطابقة حالياً.",
        "linkedin_btn":  "💼 استعرض الوظائف على LinkedIn",
        "admin_title":   "⚙️ لوحة تحكم المشرف",
        "ai_prompt": (
            "أنت خبير موارد بشرية محترف ومستشار مؤسسي متخصص في صياغة السير الذاتية. "
            "أعد صياغة وتنسيق البيانات التالية لتكوين سيرة ذاتية احترافية جاهزة لأنظمة ATS باللغة العربية.\n"
            "الاسم: {name}\n"
            "المسمى الوظيفي: {job_title}\n"
            "الخبرات: {experience}\n"
            "المهارات: {skills}\n\n"
            "استخدم نقاطًا احترافية، وأفعالًا قوية، وكلمات مفتاحية مؤثرة. رتّب الأقسام: الملخص المهني، الخبرات، المهارات."
        ),
    },
    "English": {
        "login_title":   "Welcome to the AI Career Portal 💼",
        "login_sub":     "Sign in or create an account to get started.",
        "email":         "Email Address",
        "password":      "Password",
        "login_btn":     "Log In",
        "signup_btn":    "Create Account",
        "logout":        "Log Out 🚪",
        "main_title":    "AI Career Portal 🚀",
        "main_sub":      "Craft a world-class résumé and discover top job opportunities",
        "welcome":       "👤 {email}",
        "usage":         "Usage: {count} / 3 free attempts",
        "quota_error":   "⛔ Free limit reached. Contact admin to unlock more attempts.",
        "form_header":   "Enter Your Professional Details",
        "name":          "Full Name",
        "job_title":     "Target Job Title  (e.g., Production Manager)",
        "location":      "Location  (e.g., Cairo, Egypt)",
        "exp":           "Work Experience Summary",
        "skills":        "Key Skills & Competencies",
        "submit_btn":    "✨ Generate Résumé & Find Jobs",
        "loading_ai":    "AI is crafting your résumé…",
        "loading_jobs":  "Scanning the job market…",
        "cv_header":     "✨ Optimised Résumé",
        "jobs_header":   "🎯 Recommended Opportunities",
        "wuzzuf_header": "Live openings on Wuzzuf:",
        "no_jobs":       "No matching jobs found on Wuzzuf right now.",
        "linkedin_btn":  "💼 View Jobs on LinkedIn",
        "admin_title":   "⚙️ Admin Dashboard",
        "ai_prompt": (
            "You are an elite HR Expert and Executive Recruiter. "
            "Rewrite the following details into a world-class, ATS-optimised résumé in English.\n"
            "Name: {name}\nJob Title: {job_title}\nExperience: {experience}\nSkills: {skills}\n\n"
            "Use clean bullet points, strong action verbs, and impactful keywords. "
            "Sections: Professional Summary, Work Experience, Skills."
        ),
    },
}[lang]

# ─── Session state ─────────────────────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None


# ═══════════════════════════════════════════════════════════════════════════════
#  LOGIN SCREEN
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.user is None:

    col_c, col_m, col_c2 = st.columns([1, 2, 1])
    with col_m:
        st.markdown(f"""
        <div class="section-card" style="margin-top:60px; text-align:center;">
            <div style="font-size:52px; margin-bottom:12px;">💼</div>
            <h1 style="font-size:1.6rem; margin-bottom:6px;">{ui["login_title"]}</h1>
            <p style="color:#64748B; margin-bottom:28px;">{ui["login_sub"]}</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            email    = st.text_input(ui["email"],    placeholder="you@example.com")
            password = st.text_input(ui["password"], type="password", placeholder="••••••••")
            c1, c2   = st.columns(2)
            with c1:
                login_btn  = st.form_submit_button(ui["login_btn"],  use_container_width=True)
            with c2:
                signup_btn = st.form_submit_button(ui["signup_btn"], use_container_width=True)

        if signup_btn and email:
            try:
                res = supabase.auth.sign_up({"email": email, "password": password})
                st.success("✅ Account created. Click Log In to continue.")
                if res.user:
                    supabase.table("user_profiles").insert({"id": res.user.id, "email": email}).execute()
            except Exception:
                st.error("Could not create account. Check email format and use ≥6-character password.")

        if login_btn and email:
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.rerun()
            except Exception:
                st.error("Login failed. Please verify your credentials.")


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN APP
# ═══════════════════════════════════════════════════════════════════════════════
else:
    # ── Load user profile ──────────────────────────────────────────────────────
    try:
        profile     = supabase.table("user_profiles").select("*").eq("id", st.session_state.user.id).execute()
        usage_count = profile.data[0]["usage_count"]
        role        = profile.data[0]["role"]
    except Exception:
        usage_count = 0
        role        = "user"

    # ── Hero Banner ────────────────────────────────────────────────────────────
    quota_pct = min(int(usage_count / 3 * 100), 100)
    st.markdown(f"""
    <div class="hero-banner">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
            <div>
                <h1>{ui["main_title"]}</h1>
                <p>{ui["main_sub"]}</p>
                <div class="stat-badge">{ui["welcome"].format(email=st.session_state.user.email)}</div>
            </div>
            <div style="min-width:180px;">
                <div style="font-size:13px; color:#BAE6FD; margin-bottom:4px;">{ui["usage"].format(count=usage_count)}</div>
                <div class="quota-bar"><div class="quota-fill" style="width:{quota_pct}%;"></div></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Logout in sidebar
    with st.sidebar:
        if st.button(ui["logout"], use_container_width=True):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()

    # ── Admin Dashboard ────────────────────────────────────────────────────────
    if role == "admin":
        with st.expander(ui["admin_title"], expanded=False):
            users_data = supabase.table("user_profiles").select("*").execute()
            if users_data.data:
                df = pd.DataFrame(users_data.data)[["email", "role", "usage_count", "created_at"]]
                df.columns = ["Email", "Role", "Usage", "Registered"]
                st.dataframe(df, use_container_width=True, hide_index=True)

    # ── Quota guard ────────────────────────────────────────────────────────────
    if usage_count >= 3 and role != "admin":
        st.error(ui["quota_error"])
        st.stop()

    # ── Input Form ─────────────────────────────────────────────────────────────
    st.markdown(f'<div class="section-card"><h3>📝 {ui["form_header"]}</h3>', unsafe_allow_html=True)
    with st.form("cv_form"):
        r1c1, r1c2 = st.columns(2)
        with r1c1:
            name      = st.text_input(ui["name"])
        with r1c2:
            job_title = st.text_input(ui["job_title"])

        location   = st.text_input(ui["location"])
        experience = st.text_area(ui["exp"],    height=130)
        skills     = st.text_area(ui["skills"], height=110)

        submitted = st.form_submit_button(ui["submit_btn"], use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Results ────────────────────────────────────────────────────────────────
    if submitted and name and job_title:
        new_count = usage_count + 1
        supabase.table("user_profiles").update({"usage_count": new_count}).eq("id", st.session_state.user.id).execute()

        col1, col2 = st.columns([1, 1], gap="large")

        # ── Left: AI Resume ──────────────────────────────────────────────────
        with col1:
            st.markdown(f'<div class="section-card"><h3>{ui["cv_header"]}</h3>', unsafe_allow_html=True)
            with st.spinner(ui["loading_ai"]):
                prompt = ui["ai_prompt"].format(
                    name=name, job_title=job_title,
                    experience=experience, skills=skills
                )
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
                    headers = {"Content-Type": "application/json"}
                    payload = {"contents": [{"parts": [{"text": prompt}]}]}

                    resp   = requests.post(url, headers=headers, json=payload, timeout=30)
                    result = resp.json()

                    if "error" in result:
                        st.error(f"Gemini error: {result['error'].get('message', 'Unknown error')}")
                    else:
                        ai_text = result["candidates"][0]["content"]["parts"][0]["text"]
                        st.markdown(
                            f'<div class="resume-output">{ai_text.replace(chr(10), "<br>")}</div>',
                            unsafe_allow_html=True
                        )
                except Exception as e:
                    st.error(f"Connection error: {e}")
            st.markdown("</div>", unsafe_allow_html=True)

        # ── Right: Jobs ──────────────────────────────────────────────────────
        with col2:
            st.markdown(f'<div class="section-card"><h3>{ui["jobs_header"]}</h3>', unsafe_allow_html=True)
            with st.spinner(ui["loading_jobs"]):
                # LinkedIn button
                li_q   = urllib.parse.quote(job_title)
                li_loc = urllib.parse.quote(location)
                li_url = f"https://www.linkedin.com/jobs/search/?keywords={li_q}&location={li_loc}"
                st.markdown(
                    f'<a class="linkedin-btn" href="{li_url}" target="_blank">{ui["linkedin_btn"]}</a>',
                    unsafe_allow_html=True
                )

                # Wuzzuf scraping
                st.markdown(f"<p style='font-weight:600; margin-bottom:10px;'>{ui['wuzzuf_header']}</p>", unsafe_allow_html=True)
                try:
                    q       = urllib.parse.quote(f"{job_title} {location}")
                    wurl    = f"https://wuzzuf.net/search/jobs/?q={q}&a=hpb"
                    wres    = requests.get(wurl, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
                    soup    = BeautifulSoup(wres.text, "html.parser")
                    cards   = soup.find_all("div", class_="css-1gatmva e1v1l3u10", limit=5)

                    if not cards:
                        st.info(ui["no_jobs"])
                    else:
                        for card in cards:
                            title_el   = card.find("h2", class_="css-m604qf")
                            company_el = card.find("a", class_="css-17s97q8")
                            if title_el and company_el:
                                job_link    = "https://wuzzuf.net" + title_el.find("a")["href"]
                                job_name    = title_el.text.strip()
                                company_name = company_el.text.strip().replace(" -", "")
                                st.markdown(f"""
                                <div class="job-card">
                                    <a href="{job_link}" target="_blank"
                                       style="color:#1E3A8A; font-weight:700; font-size:15px; text-decoration:none;">
                                        {job_name}
                                    </a>
                                    <div style="color:#64748B; font-size:13px; margin-top:6px;">🏢 {company_name}</div>
                                </div>
                                """, unsafe_allow_html=True)
                except Exception:
                    st.warning(ui["no_jobs"])
            st.markdown("</div>", unsafe_allow_html=True)
