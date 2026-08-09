import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, time, date

# ==========================================
# 1. تهيئة الصفحة والأنماط البصرية الحديثة
# ==========================================
st.set_page_config(
    page_title="آتون لوكيشن | Aton Location POS",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'dashboard'
if 'last_ticket' not in st.session_state:
    st.session_state.last_ticket = None
if 'last_booking' not in st.session_state:
    st.session_state.last_booking = None

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        text-align: right;
        background-color: #0b0d12;
        color: #f8fafc;
    }
    
    .stApp { background-color: #0b0d12; }
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    
    @keyframes goldNeonGlow {
        0% { text-shadow: 0 0 5px rgba(212, 175, 55, 0.4); box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6); }
        50% { text-shadow: 0 0 15px rgba(212, 175, 55, 0.8); box-shadow: 0 8px 35px rgba(212, 175, 55, 0.3); }
        100% { text-shadow: 0 0 5px rgba(212, 175, 55, 0.4); box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6); }
    }

    .pos-header-center {
        background: linear-gradient(135deg, #141824 0%, #0d1017 100%);
        border: 2px solid #d4af37;
        padding: 22px;
        border-radius: 16px;
        margin: 10px auto 30px auto;
        text-align: center !important;
        width: 100%;
        max-width: 800px;
        animation: goldNeonGlow 3s infinite ease-in-out;
    }
    .pos-title-center { font-size: 32px; font-weight: 900; color: #fce181; letter-spacing: 2px; }

    .pos-card-container {
        background: linear-gradient(145deg, #161b26, #0f131c);
        border: 1px solid rgba(212, 175, 55, 0.35);
        border-radius: 16px;
        padding: 24px 20px 20px 20px;
        text-align: center;
        margin-bottom: 12px;
        transition: all 0.3s ease;
    }
    .card-icon-circle {
        width: 50px; height: 50px;
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.2), rgba(212, 175, 55, 0.05));
        border: 1px solid #d4af37;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 12px auto;
    }
    .stButton>button {
        background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%) !important;
        color: #000000 !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        width: 100% !important;
    }
    .receipt-container {
        max-width: 340px; margin: auto; padding: 22px; background-color: #ffffff;
        color: #000000; border-radius: 8px; border-top: 5px solid #d4af37;
    }
</style>
""", unsafe_allow_html=True)

# الاتصال بـ Supabase
url = str(st.secrets["SUPABASE_URL"]).strip()
key = str(st.secrets["SUPABASE_KEY"]).strip()
supabase: Client = create_client(url, key)

# الهيدر
st.markdown('<div class="pos-header-center"><div class="pos-title-center">آتون لوكيشن | ATON LOCATION</div></div>', unsafe_allow_html=True)

if st.session_state.current_screen != 'dashboard':
    if st.button("⬅️ العودة للشاشة الرئيسية"):
        st.session_state.current_screen = 'dashboard'
        st.rerun()

st.divider()

# ==========================================
# الشاشات
# ==========================================

if st.session_state.current_screen == 'dashboard':
    col1, col2 = st.columns(2)
    with col1:
        if st.button("حجز سيشن وتقويم المواعيد"):
            st.session_state.current_screen = 'bookings'
            st.rerun()
    with col2:
        if st.button("قطع تذاكر الأفراد"):
            st.session_state.current_screen = 'tickets'
            st.rerun()
    
    col3, col4, col5, col6 = st.columns(4)
    if col3.button("التقارير"): st.session_state.current_screen = 'reports'; st.rerun()
    if col4.button("العهدة"): st.session_state.current_screen = 'equip'; st.rerun()
    if col5.button("المصروفات"): st.session_state.current_screen = 'expenses'; st.rerun()
    if col6.button("العمالة"): st.session_state.current_screen = 'staff'; st.rerun()

elif st.session_state.current_screen == 'tickets':
    # كود التذاكر (الذي اعتمدناه)
    pass 

elif st.session_state.current_screen == 'bookings':
    # كود الحجوزات (الذي اعتمدناه)
    pass

# الأقسام المفعّلة الآن:
elif st.session_state.current_screen == 'reports':
    st.subheader("📊 التقارير والميزانية")
    try:
        data = supabase.table("reports").select("*").execute().data
        st.dataframe(pd.DataFrame(data))
    except: st.warning("لا توجد بيانات في جدول التقارير.")

elif st.session_state.current_screen == 'equip':
    st.subheader("📦 إدارة العهدة")
    try:
        data = supabase.table("equip").select("*").execute().data
        st.dataframe(pd.DataFrame(data))
    except: st.warning("لا توجد بيانات في جدول العهدة.")

elif st.session_state.current_screen == 'expenses':
    st.subheader("💸 تسجيل المصروفات")
    # نموذج بسيط للإضافة
    amount = st.number_input("المبلغ")
    desc = st.text_input("البيان")
    if st.button("حفظ المصروف"):
        supabase.table("expenses").insert({"amount": amount, "description": desc}).execute()
        st.success("تم الحفظ")

elif st.session_state.current_screen == 'staff':
    st.subheader("👥 إدارة العمالة والسُلف")
    try:
        data = supabase.table("staff").select("*").execute().data
        st.dataframe(pd.DataFrame(data))
    except: st.warning("لا توجد بيانات في جدول العمالة.")