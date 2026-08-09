import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, date

# تهيئة الصفحة
st.set_page_config(page_title="آتون لوكيشن | النظام المتكامل", layout="wide")

# الاتصال بـ Supabase
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

# إدارة التنقل
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'dashboard'

# تنسيق CSS الموحد
st.markdown("""
<style>
    .pos-card-container { background: #161b26; border: 1px solid #d4af37; border-radius: 15px; padding: 20px; text-align: center; }
    .stButton>button { width: 100%; border-radius: 10px; background: #d4af37; color: black; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# الهيدر
st.title("🎬 آتون لوكيشن | نظام الإدارة المتكامل")

# الشاشة الرئيسية
if st.session_state.current_screen == 'dashboard':
    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)
    
    with col1:
        if st.button("حجز السيشن"): st.session_state.current_screen = 'bookings'; st.rerun()
    with col2:
        if st.button("تذاكر الأفراد"): st.session_state.current_screen = 'tickets'; st.rerun()
    with col3:
        if st.button("شؤون الموظفين"): st.session_state.current_screen = 'staff'; st.rerun()
    with col4:
        if st.button("المصروفات والخزينة"): st.session_state.current_screen = 'expenses'; st.rerun()
    with col5:
        if st.button("التقارير والإحصائيات"): st.session_state.current_screen = 'reports'; st.rerun()

# --- وظائف الأقسام (مثال لربطها بـ Supabase) ---

def show_back_button():
    if st.button("⬅️ عودة للرئيسية"): st.session_state.current_screen = 'dashboard'; st.rerun()

# 1. قسم الحجوزات
if st.session_state.current_screen == 'bookings':
    show_back_button()
    st.header("إدارة الحجوزات")
    # مثال إدخال
    name = st.text_input("اسم العميل")
    if st.button("حفظ الحجز"):
        supabase.table("bookings").insert({"client_name": name, "date": str(date.today())}).execute()
        st.success("تم حفظ الحجز!")
    # عرض البيانات
    data = supabase.table("bookings").select("*").execute().data
    st.dataframe(pd.DataFrame(data))

# 2. قسم التذاكر
elif st.session_state.current_screen == 'tickets':
    show_back_button()
    st.header("كاشير التذاكر")
    # ... (ضع كود التذاكر هنا)

# 3. قسم الموظفين
elif st.session_state.current_screen == 'staff':
    show_back_button()
    st.header("شؤون الموظفين")
    emp_name = st.text_input("اسم الموظف")
    role = st.text_input("الوظيفة")
    if st.button("إضافة موظف"):
        supabase.table("staff").insert({"name": emp_name, "role": role}).execute()
        st.success("تم إضافة الموظف!")
    data = supabase.table("staff").select("*").execute().data
    st.dataframe(pd.DataFrame(data))

# 4. قسم المصروفات
elif st.session_state.current_screen == 'expenses':
    show_back_button()
    st.header("المصروفات والخزينة")
    amount = st.number_input("المبلغ")
    desc = st.text_input("البيان")
    if st.button("تسجيل مصروف"):
        supabase.table("expenses").insert({"amount": amount, "description": desc}).execute()
        st.success("تم تسجيل المصروف!")
    data = supabase.table("expenses").select("*").execute().data
    st.dataframe(pd.DataFrame(data))

# 5. قسم التقارير
elif st.session_state.current_screen == 'reports':
    show_back_button()
    st.header("التقارير والإحصائيات")
    # يمكنك سحب البيانات من كل الجداول وعمل إحصائيات بـ pandas
    st.info("جارٍ معالجة تقارير النظام...")
