import streamlit as st

# إعداد الصفحة
st.set_page_config(layout="wide")

# CSS المخصص للتصميم الذهبي والأزرار التفاعلية
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        background-color: #0b0d12;
        color: white;
    }

    /* تصميم الكارت */
    .card-container {
        background: #141824;
        border: 1px solid #d4af37;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        transition: 0.3s;
    }
    
    /* تصميم زرار النيون الذهبي */
    div.stButton > button {
        background: transparent !important;
        border: 2px solid #d4af37 !important;
        color: #d4af37 !important;
        border-radius: 50px !important;
        padding: 10px 25px !important;
        font-weight: bold !important;
        transition: 0.3s !important;
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.2) !important;
    }
    
    div.stButton > button:hover {
        background: #d4af37 !important;
        color: #000 !important;
        box-shadow: 0 0 20px #d4af37 !important;
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown("<h1 style='text-align: center; color: #d4af37;'>آتون لوكيشن | ATON LOCATION</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; margin-bottom: 40px;'>اختر القسم المطلوب للبدء</h4>", unsafe_allow_html=True)

# دالة لإنشاء كارت تفاعلي
def create_card(title, description, button_text, key):
    with st.container():
        st.markdown(f"""
        <div class="card-container">
            <h3>{title}</h3>
            <p style='color: #888;'>{description}</p>
        </div>
        """, unsafe_allow_html=True)
        # الزرار التفاعلي تحت الكارت مباشرة
        if st.button(button_text, key=key, use_container_width=True):
            st.session_state.page = key
            st.rerun()

# توزيع الكروت في صفوف
col1, col2 = st.columns(2)

with col1:
    create_card("حجز سيشن وتقويم المواعيد", "إضافة حجز جديد، طباعة العقد المالي، وتتبع جدول المواعيد", "دخول لقسم الحجوزات", "bookings")

with col2:
    create_card("قطع تذاكر الأفراد", "إصدار تذاكر الدخول الفورية وطباعة الإيصالات المالية فوراً", "دخول لقسم التذاكر", "tickets")

st.markdown("<br>", unsafe_allow_html=True)

col3, col4, col5, col6 = st.columns(4)

with col3:
    create_card("التقارير", "الحسابات والربحية", "عرض التقارير", "reports")
with col4:
    create_card("العهدة", "المعدات والأجهزة", "إدارة العهدة", "equip")
with col5:
    create_card("المصروفات", "النفقات الإدارية", "سجل المصروفات", "expenses")
with col6:
    create_card("العمالة", "الحضور والسُلف", "إدارة الموظفين", "staff")

# التعامل مع الانتقالات
if 'page' not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page != "home":
    st.write(f"أنت الآن في صفحة: {st.session_state.page}")
    if st.button("← العودة للرئيسية"):
        st.session_state.page = "home"
        st.rerun()