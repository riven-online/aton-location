import streamlit as st
import pandas as pd
from datetime import datetime, time, date

# ==========================================
# 1. إعداد الصفحة والأنماط البصرية
# ==========================================
st.set_page_config(
    page_title="آتون لوكيشن | Aton Location POS",
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
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        text-align: right;
        background-color: #0b0d12;
        color: #f8fafc;
    }
    
    .stApp {
        background-color: #0b0d12;
    }

    /* إخفاء القائمة الجانبية تماماً */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    
    /* تأثير النيون الذهبي للهيدر */
    @keyframes goldNeonGlow {
        0% { box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6), inset 0 0 15px rgba(212, 175, 55, 0.15); }
        50% { box-shadow: 0 8px 35px rgba(212, 175, 55, 0.3), inset 0 0 25px rgba(212, 175, 55, 0.3); }
        100% { box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6), inset 0 0 15px rgba(212, 175, 55, 0.15); }
    }

    .pos-header-center {
        background: linear-gradient(135deg, #141824 0%, #0d1017 100%);
        border: 2px solid #d4af37;
        padding: 16px;
        border-radius: 16px;
        margin: 0px auto 15px auto;
        text-align: center !important;
        width: 100%;
        max-width: 800px;
        animation: goldNeonGlow 3s infinite ease-in-out;
    }
    .pos-title-center {
        font-size: 26px;
        font-weight: 900;
        color: #fce181;
        letter-spacing: 2px;
        margin: 0;
    }

    /* هيكل الكارت البصري الثابت */
    .card-visual-box {
        background: linear-gradient(145deg, #161b26, #0f131c);
        border: 1px solid rgba(212, 175, 55, 0.35);
        border-radius: 16px;
        padding: 18px 12px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        min-height: 125px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-bottom: 8px;
    }
    .card-title-text {
        color: #ffffff;
        font-size: 16px;
        font-weight: 800;
        margin-bottom: 4px;
    }
    .card-desc-text {
        color: #94a3b8;
        font-size: 11px;
        margin: 0;
        line-height: 1.3;
    }

    /* أزرار الاستريمليت التفاعلية بتصميم نيون ذهبي متناسق تحت الكروت */
    .stButton>button {
        background: linear-gradient(145deg, #161b26, #0f131c) !important;
        border: 1px solid #d4af37 !important;
        color: #fce181 !important;
        width: 100% !important;
        border-radius: 12px !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        padding: 8px 12px !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.4) !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        background: linear-gradient(145deg, #1f2736, #141925) !important;
        border-color: #fce181 !important;
        color: #ffffff !important;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.5) !important;
        transform: translateY(-2px) !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. الهيدر العلوي وزر العودة
# ==========================================
st.markdown("""
<div class="pos-header-center">
    <div class="pos-title-center">آتون لوكيشن | ATON LOCATION</div>
</div>
""", unsafe_allow_html=True)

if st.session_state.current_screen != 'dashboard':
    col_back1, col_back2, col_back3 = st.columns([1, 2, 1])
    with col_back2:
        if st.button("← العودة للشاشة الرئيسية", key="back_to_home"):
            st.session_state.current_screen = 'dashboard'
            st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 3. الشاشة الرئيسية (Dashboard)
# ==========================================
if st.session_state.current_screen == 'dashboard':
    st.markdown("<h4 style='text-align: center; color: #d4af37; margin-bottom: 20px; font-weight: 700;'>اختر القسم المطلوب للبدء</h4>", unsafe_allow_html=True)
    
    # الصف الأول: حجز السيشن وقطع التذاكر
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.markdown("""
        <div class="card-visual-box">
            <div class="card-title-text">حجز سيشن وتقويم المواعيد</div>
            <div class="card-desc-text">إضافة حجز جديد، طباعة العقد المالي، وتتبع جدول المواعيد</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("دخول قسم الحجوزات", key="nav_bookings"):
            st.session_state.current_screen = 'bookings'
            st.rerun()

    with col2:
        st.markdown("""
        <div class="card-visual-box">
            <div class="card-title-text">قطع تذاكر الأفراد</div>
            <div class="card-desc-text">إصدار تذاكر الدخول الفورية وطباعة الإيصالات المالية فوراً</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("دخول قسم التذاكر", key="nav_tickets"):
            st.session_state.current_screen = 'tickets'
            st.rerun()

    st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

    # الصف الثاني: الأقسام الأربعة الفرعية
    col3, col4, col5, col6 = st.columns(4, gap="small")
    
    with col3:
        st.markdown("""
        <div class="card-visual-box">
            <div class="card-title-text">العمالة</div>
            <div class="card-desc-text">الحضور والسُلف</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("إدارة الععمالة", key="nav_staff"):
            st.session_state.current_screen = 'staff'
            st.rerun()

    with col4:
        st.markdown("""
        <div class="card-visual-box">
            <div class="card-title-text">المصروفات</div>
            <div class="card-desc-text">النفقات الإدارية</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("سجل المصروفات", key="nav_expenses"):
            st.session_state.current_screen = 'expenses'
            st.rerun()

    with col5:
        st.markdown("""
        <div class="card-visual-box">
            <div class="card-title-text">العهدة</div>
            <div class="card-desc-text">المعدات والأجهزة</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("إدارة العهدة", key="nav_equip"):
            st.session_state.current_screen = 'equip'
            st.rerun()

    with col6:
        st.markdown("""
        <div class="card-visual-box">
            <div class="card-title-text">التقارير</div>
            <div class="card-desc-text">الحسابات والربحية</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("عرض التقارير", key="nav_reports"):
            st.session_state.current_screen = 'reports'
            st.rerun()

# ==========================================
# 4. محتوى الأقسام الفرعية التفاعلية
# ==========================================
elif st.session_state.current_screen == 'tickets':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>قطع تذاكر دخول الأفراد</h3>", unsafe_allow_html=True)
    st.info("هنا يتم إصدار وطباعة تذاكر الأفراد بشكل فوري.")
    count = st.number_input("عدد الأفراد", min_value=1, value=1)
    price = st.number_input("سعر التذكرة للفرد", min_value=1, value=50)
    st.write(f"الإجمالي: {count * price} ج.م")
    if st.button("طباعة التذكرة", key="print_t_action"):
        st.success("تم إصدار التذكرة بنجاح!")

elif st.session_state.current_screen == 'bookings':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>حجز سيشن وتقويم المواعيد</h3>", unsafe_allow_html=True)
    st.info("هنا يتم تسجيل وإدارة حجوزات السيشن والعقود.")
    c_name = st.text_input("اسم العميل")
    b_date = st.date_input("تاريخ السيشن", value=date.today())
    if st.button("حفظ الحجز", key="save_b_action"):
        st.success("تم حفظ حجز السيشن بنجاح!")

elif st.session_state.current_screen == 'staff':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>إدارة الععمالة (الحضور والسُلف)</h3>", unsafe_allow_html=True)
    st.info("قسم متابعة حضور وانصراف الموظفين وسُلف العمالة.")

elif st.session_state.current_screen == 'expenses':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>سجل المصروفات والنفقات الإدارية</h3>", unsafe_allow_html=True)
    st.info("قسم تسجيل وإدارة المصروفات اليومية.")

elif st.session_state.current_screen == 'equip':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>إدارة العهدة والمعدات والأجهزة</h3>", unsafe_allow_html=True)
    st.info("قسم تتبع وتسجيل الأجهزة ومعدات اللوكيشن.")

elif st.session_state.current_screen == 'reports':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>التقارير والحسابات والربحية</h3>", unsafe_allow_html=True)
    st.info("قسم عرض ملخص الأرباح والتقارير المالية.")