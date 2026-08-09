import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="آتون لوكيشن | Aton Location", layout="wide")

# تهيئة Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# تهيئة الـ Session State
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'main'

# CSS المعتمد للواجهة
st.markdown("""
<style>
    .main-header { text-align: center; color: #d4af37; font-size: 40px; font-weight: bold; padding: 20px; border: 2px solid #d4af37; border-radius: 15px; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# الهيدر
st.markdown('<div class="main-header">آتون لوكيشن | ATON LOCATION</div>', unsafe_allow_html=True)
st.write("")

# التنقل
if st.session_state.current_screen != 'main':
    if st.button("⬅️ العودة للقائمة الرئيسية"):
        st.session_state.current_screen = 'main'
        st.rerun()

# منطق الشاشات
if st.session_state.current_screen == 'main':
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎟️ قطع تذاكر الأفراد"): st.session_state.current_screen = 'tickets'; st.rerun()
        if st.button("📊 التقارير والميزانية"): st.session_state.current_screen = 'reports'; st.rerun()
        if st.button("💸 المصروفات"): st.session_state.current_screen = 'expenses'; st.rerun()
    with col2:
        if st.button("📅 حجز سيشن"): st.session_state.current_screen = 'bookings'; st.rerun()
        if st.button("📦 إدارة العهدة"): st.session_state.current_screen = 'equip'; st.rerun()
        if st.button("👥 العمالة والحضور"): st.session_state.current_screen = 'staff'; st.rerun()

# --- قسم التذاكر ---
elif st.session_state.current_screen == 'tickets':
    st.subheader("🎟️ قسم تذاكر الأفراد")
    # ضع هنا كود التذاكر الخاص بك المربوط بجدول tickets

# --- قسم الحجوزات ---
elif st.session_state.current_screen == 'bookings':
    st.subheader("📅 قسم حجز المواعيد")
    # ضع هنا كود الحجوزات المربوط بجدول bookings

# --- قسم التقارير ---
elif st.session_state.current_screen == 'reports':
    st.subheader("📊 التقارير المالية")
    data = supabase.table("reports").select("*").execute().data
    if data: st.dataframe(pd.DataFrame(data))
    else: st.info("لا توجد بيانات")

# --- قسم العهدة ---
elif st.session_state.current_screen == 'equip':
    st.subheader("📦 إدارة العهدة والمعدات")
    data = supabase.table("equip").select("*").execute().data
    if data: st.dataframe(pd.DataFrame(data))
    else: st.info("لا توجد بيانات")

# --- قسم المصروفات ---
elif st.session_state.current_screen == 'expenses':
    st.subheader("💸 المصروفات اليومية")
    amount = st.number_input("المبلغ")
    desc = st.text_input("البيان")
    if st.button("تسجيل"):
        supabase.table("expenses").insert({"amount": amount, "description": desc}).execute()
        st.success("تم الحفظ")
    data = supabase.table("expenses").select("*").execute().data
    if data: st.dataframe(pd.DataFrame(data))

# --- قسم العمالة ---
elif st.session_state.current_screen == 'staff':
    st.subheader("👥 العمالة والحضور")
    data = supabase.table("staff").select("*").execute().data
    if data: st.dataframe(pd.DataFrame(data))
    else: st.info("لا توجد بيانات")