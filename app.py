import streamlit as st
import pandas as pd
from datetime import datetime, date

# ==========================================
# 1. إعداد الصفحة والأنماط البصرية
# ==========================================
st.set_page_config(page_title="آتون لوكيشن | Aton Location POS", layout="wide")

if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'dashboard'
# محاكاة لقاعدة بيانات الحجوزات
if 'booked_dates' not in st.session_state:
    st.session_state.booked_dates = [date(2026, 8, 15), date(2026, 8, 20)]

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif !important; direction: rtl; }
    .stApp { background-color: #0b0d12; color: #f8fafc; }
    [data-testid="stSidebar"] { display: none !important; }
    
    .pos-header {
        background: linear-gradient(135deg, #141824 0%, #0d1017 100%);
        border: 2px solid #d4af37;
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);
    }
    .card-box {
        background: #161b26;
        border: 1px solid #d4af37;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
    }
    .stButton>button {
        width: 100%; border-radius: 10px; border: 1px solid #d4af37;
        background: #0f131c; color: #fce181; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. الهيدر وزر العودة
# ==========================================
st.markdown("<div class='pos-header'><h1 style='color:#fce181;'>آتون لوكيشن | ATON LOCATION</h1></div>", unsafe_allow_html=True)

if st.session_state.current_screen != 'dashboard':
    if st.button("← العودة للشاشة الرئيسية"):
        st.session_state.current_screen = 'dashboard'
        st.rerun()

# ==========================================
# 3. الشاشة الرئيسية
# ==========================================
if st.session_state.current_screen == 'dashboard':
    st.subheader("لوحة التحكم الرئيسية")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("حجز سيشن وتقويم المواعيد"):
            st.session_state.current_screen = 'bookings'
            st.rerun()
    with c2:
        if st.button("قطع تذاكر الأفراد"):
            st.session_state.current_screen = 'tickets'
            st.rerun()
    
    st.write("---")
    c3, c4, c5, c6 = st.columns(4)
    if c3.button("إدارة العمالة"): st.session_state.current_screen = 'staff'; st.rerun()
    if c4.button("المصروفات"): st.session_state.current_screen = 'expenses'; st.rerun()
    if c5.button("العهدة"): st.session_state.current_screen = 'equip'; st.rerun()
    if c6.button("التقارير"): st.session_state.current_screen = 'reports'; st.rerun()

# ==========================================
# 4. منطق الأقسام
# ==========================================
elif st.session_state.current_screen == 'bookings':
    st.header("التقويم التفاعلي للمواعيد")
    
    col_l, col_r = st.columns([1, 1])
    with col_l:
        target_date = st.date_input("اختر التاريخ")
        if target_date in st.session_state.booked_dates:
            st.error(f"❌ يوم {target_date} محجوز بالكامل")
        else:
            st.success(f"✅ يوم {target_date} متاح (يوم فاضي)")
            
    with col_r:
        client = st.text_input("اسم العميل")
        if st.button("تأكيد الحجز"):
            st.session_state.booked_dates.append(target_date)
            st.success("تم تثبيت الحجز في التقويم!")
            st.rerun()

elif st.session_state.current_screen == 'tickets':
    st.header("نظام التذاكر")
    count = st.number_input("عدد الأفراد", 1, 100)
    if st.button("طباعة التذكرة"):
        st.success(f"تم طباعة {count} تذكرة بنجاح!")

else:
    st.info(f"قسم {st.session_state.current_screen} قيد التطوير...")
