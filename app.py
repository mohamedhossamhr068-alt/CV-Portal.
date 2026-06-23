import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import urllib.parse
from supabase import create_client, Client

# --- 1. الإعدادات والمفاتيح (مخفية للآمان) ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# تهيئة الاتصال بالسيرفرات
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="المنصة الذكية للتوظيف", page_icon="💼", layout="wide")

# حفظ حالة تسجيل الدخول للمستخدم
if 'user' not in st.session_state:
    st.session_state.user = None

# --- 2. نظام تسجيل الدخول وإنشاء الحساب ---
if st.session_state.user is None:
    st.title("تسجيل الدخول للمنصة 🔐")
    st.info("قم بإنشاء حساب جديد أو تسجيل الدخول للبدء في استخدام المنصة.")
    
    with st.form("login_form"):
        email = st.text_input("البريد الإلكتروني")
        password = st.text_input("كلمة المرور", type="password")
        col1, col2 = st.columns(2)
        with col1:
            login_btn = st.form_submit_button("تسجيل الدخول")
        with col2:
            signup_btn = st.form_submit_button("إنشاء حساب جديد")
            
    if signup_btn:
        try:
            res = supabase.auth.sign_up({"email": email, "password": password})
            st.success("تم إنشاء الحساب بنجاح! يرجى الضغط على 'تسجيل الدخول' الآن.")
            if res.user:
               supabase.table("user_profiles").insert({"id": res.user.id, "email": email}).execute()
        except Exception as e:
            st.error("تأكد من كتابة إيميل صحيح وكلمة مرور لا تقل عن 6 أحرف.")
            
    if login_btn:
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            st.session_state.user = res.user
            st.rerun() 
        except Exception as e:
            st.error("خطأ في تسجيل الدخول. تأكد من البريد الإلكتروني وكلمة المرور.")

# --- 3. الواجهة الرئيسية (بعد تسجيل الدخول) ---
else:
    col_a, col_b = st.columns([8, 2])
    with col_a:
        st.title("بوابة صياغة السيرة الذاتية وترشيحات الوظائف 🚀")
    with col_b:
        if st.button("تسجيل الخروج", use_container_width=True):
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

    st.info(f"👤 مرحباً: {st.session_state.user.email} | 📊 استخدمت النظام: {usage_count} مرات من أصل 3 محاولات مجانية.")

    if usage_count >= 3 and role != 'admin':
        st.error("⛔ لقد استنفدت الحد الأقصى للمحاولات المجانية. يرجى التواصل مع الإدارة للترقية.")
    else:
        with st.form("cv_form"):
            st.subheader("أدخل بياناتك المهنية:")
            name = st.text_input("الاسم الكامل")
            job_title = st.text_input("المسمى الوظيفي (مثال: HR Consultant)")
            location = st.text_input("المنطقة (مثال: Upper Egypt Fayoum)")
            experience = st.text_area("الخبرات العملية باختصار")
            skills = st.text_area("أهم المهارات")
            
            submitted = st.form_submit_button("توليد السيرة الذاتية والبحث عن وظائف")

        if submitted and name and job_title:
            new_count = usage_count + 1
            supabase.table("user_profiles").update({"usage_count": new_count}).eq("id", st.session_state.user.id).execute()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.success("جاري صياغة السيرة الذاتية...")
                prompt = f"""
                أنت خبير موارد بشرية. أعد صياغة هذه البيانات لسيرة ذاتية احترافية:
                الاسم: {name} | الوظيفة: {job_title} | الخبرات: {experience} | المهارات: {skills}
                نسقها في نقاط واضحة (الملخص، الخبرات، المهارات).
                """
                try:
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error("حدث خطأ في الذكاء الاصطناعي.")

            with col2:
                st.success("جاري البحث عن وظائف مطابقة...")
                try:
                    linkedin_query = urllib.parse.quote(job_title)
                    linkedin_loc = urllib.parse.quote(location)
                    linkedin_link = f"https://www.linkedin.com/jobs/search/?keywords={linkedin_query}&location={linkedin_loc}"
                    st.markdown(f"**[💼 اضغط هنا لعرض وظائف {job_title} على LinkedIn]({linkedin_link})**")
                    
                    st.write("---")
                    st.write("**وظائف مقترحة من Wuzzuf:**")
                    
                    query = urllib.parse.quote(f"{job_title} {location}")
                    url = f"https://wuzzuf.net/search/jobs/?q={query}&a=hpb"
                    headers = {"User-Agent": "Mozilla/5.0"}
                    res = requests.get(url, headers=headers)
                    soup = BeautifulSoup(res.text, "html.parser")
                    
                    job_cards = soup.find_all("div", class_="css-1gatmva e1v1l3u10", limit=5)
                    if not job_cards:
                        st.warning("لم نجد وظائف مطابقة حالياً على وظف.")
                    
                    for card in job_cards:
                        title_elem = card.find("h2", class_="css-m604qf")
                        company_elem = card.find("a", class_="css-17s97q8")
                        link_elem = title_elem.find("a") if title_elem else None
                        
                        if title_elem and company_elem and link_elem:
                            job_link = "https://wuzzuf.net" + link_elem["href"]
                            st.markdown(f"- [{title_elem.text.strip()}]({job_link}) - *{company_elem.text.strip().replace(' -', '')}*")
                            
                except Exception as e:
                    st.error("حدث خطأ أثناء جلب الوظائف.")
