import streamlit as st
import pandas as pd
from datetime import datetime, date

# ==========================================
# 1. إعداد الصفحة والأنماط البصرية (نيون ذهبي)
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
if 'booked_dates' not in st.session_state:
    # الأيام المحجوزة افتراضياً لتجربة التقويم
    st.session_state.booked_dates = [date(2026, 8, 15), date(2026, 8, 20)]

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
    
    .stApp { background-color: #0b0d12; }

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

    /* هيكل الكارت البصري الثابت (كروت الشاشة الكبيرة) */
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

    /* أزرار الاستريمليت التفاعلية بتصميم نيون ذهبي */
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
# 3. الشاشة الرئيسية (Dashboard - كروت الشاشة الكبيرة)
# ==========================================
if st.session_state.current_screen == 'dashboard':
    st.markdown("<h4 style='text-align: center; color: #d4af37; margin-bottom: 20px; font-weight: 700;'>اختر القسم المطلوب للبدء</h4>", unsafe_allow_html=True)
    
    # الصف الأول: كروت الشاشة الرئيسية الكبيرة (الحجوزات والتذاكر)
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.markdown("""
        <div class="card-visual-box">
            <div class="card-title-text">حجز سيشن وتقويم المواعيد</div>
            <div class="card-desc-text">إضافة حجز جديد، فحص اليوم الفاضي، طباعة العقد المالي وإكرامية المصور</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("دخول قسم الحجوزات", key="nav_bookings"):
            st.session_state.current_screen = 'bookings'
            st.rerun()

    with col2:
        st.markdown("""
        <div class="card-visual-box">
            <div class="card-title-text">قطع تذاكر الأفراد</div>
            <div class="card-desc-text">إصدار تذاكر الدخول الفورية وطباعة الإيصالات المالية فوراً وإعادة الطباعة</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("دخول قسم التذاكر", key="nav_tickets"):
            st.session_state.current_screen = 'tickets'
            st.rerun()

    st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

    # الصف الثاني: الأقسام الأربعة الفرعية الإدارية
    col3, col4, col5, col6 = st.columns(4, gap="small")
    
    with col3:
        st.markdown("""
        <div class="card-visual-box">
            <div class="card-title-text">العمالة</div>
            <div class="card-desc-text">الحضور والسُلف</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("إدارة العمالة", key="nav_staff"):
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
# 4. تفاصيل الأقسام والخدمات الكاملة
# ==========================================

# --- قسم حجوزات الأفراح والسيشن + التقويم التفاعلي وفاتورة الحجز الكاملة وإكرامية المصور ---
elif st.session_state.current_screen == 'bookings':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>التقويم التفاعلي وحجوزات السيشن والأفراح</h3>", unsafe_allow_html=True)
    
    tab_cal, tab_form = st.tabs(["📅 التقويم التفاعلي (اليوم الفاضي)", "📝 فاتورة الحجز الكاملة وإكرامية المصور"])
    
    with tab_cal:
        st.markdown("#### فحص المواعيد المتاحة والمحجوزة")
        selected_calendar_date = st.date_input("اختر التاريخ للتأكد من التوافر", value=date.today(), key="cal_checker")
        
        if selected_calendar_date in st.session_state.booked_dates:
            st.error(f"❌ عذراً، يوم {selected_calendar_date} محجوز بالكامل (غير متاح).")
        else:
            st.success(f"✅ يوم {selected_calendar_date} متاح (يوم فاضي وجاهز للحجز).")
            
        st.markdown("---")
        st.markdown("##### قائمة التواريخ المحجوزة حالياً في النظام:")
        if st.session_state.booked_dates:
            for d in sorted(st.session_state.booked_dates):
                st.write(f"- 🔴 محجوز بتاريخ: {d}")
        else:
            st.info("لا توجد تواريخ محجوزة حالياً.")

    with tab_form:
        st.markdown("#### تسجيل حجز جديد وإصدار الفاتورة الشاملة")
        col_b1, col_b2 = st.columns(2)
        
        with col_b1:
            client_name = st.text_input("اسم العميل / العروسين")
            client_phone = st.text_input("رقم الهاتف")
            booking_date = st.date_input("تاريخ الحجز المطلوب", value=date.today(), key="form_b_date")
            session_type = st.selectbox("نوع الحجز", ["سيشن تصوير", "حفل زفاف / فرح", "خطوبة", "مؤتمر / فعالية"])
            
        with col_b2:
            package_price = st.number_input("قيمة الباقة الأساسية (ج.م)", min_value=0, value=2000, step=100)
            photographer_tip = st.number_input("إكرامية المصور (ج.م)", min_value=0, value=200, step=50)
            extra_services = st.number_input("خدمات إضافية / إضاءة / ائتمان (ج.م)", min_value=0, value=0, step=50)
            paid_deposit = st.number_input("المبلغ المدفوع مقدماً (العربون)", min_value=0, value=500, step=100)

        total_invoice = package_price + photographer_tip + extra_services
        remaining_amount = total_invoice - paid_deposit
        
        st.markdown("---")
        st.markdown("### 🧾 ملخص فاتورة الحجز الكاملة:")
        col_res1, col_res2, col_res3 = st.columns(3)
        col_res1.metric("إجمالي الفاتورة", f"{total_invoice} ج.م")
        col_res2.metric("المبلغ المدفوع (العربون)", f"{paid_deposit} ج.م")
        col_res3.metric("المبلغ المتبقي للاستلام", f"{remaining_amount} ج.م", delta_color="inverse")
        
        if st.button("حفظ وتأكيد الحجز بالتقويم وإصدار العقد", key="confirm_full_booking"):
            if booking_date in st.session_state.booked_dates:
                st.error("⚠️ عذراً هذا التاريخ تم حجزه مسبقاً، يرجى اختيار يوم آخر!")
            else:
                st.session_state.booked_dates.append(booking_date)
                st.session_state.last_booking = {
                    "client": client_name,
                    "date": booking_date,
                    "total": total_invoice,
                    "tip": photographer_tip,
                    "remaining": remaining_amount
                }
                st.success(f"🎉 تم حجز يوم {booking_date} بنجاح للعميل {client_name} وإضافته لقائمة الحجوزات!")

        if st.session_state.last_booking:
            if st.button("🖨️ طباعة إيصال الحجز والعقد المالي"):
                b_info = st.session_state.last_booking
                st.info(f"جاري طباعة إيصال العميل: {b_info['client']} | التاريخ: {b_info['date']} | الإجمالي: {b_info['total']} ج.م (شامل إكرامية المصور: {b_info['tip']} ج.م)")

# --- قسم تذاكر الأفراد ---
elif st.session_state.current_screen == 'tickets':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>قطع تذاكر دخول الأفراد الفورية</h3>", unsafe_allow_html=True)
    st.info("إصدار تذاكر الدخول وطباعة الإيصالات الفورية وإعادة الطباعة عند الحاجة.")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        t_count = st.number_input("عدد الأفراد", min_value=1, value=1, step=1)
        t_price = st.number_input("سعر التذكرة للفرد الواحد (ج.م)", min_value=1, value=50, step=10)
        total_t_price = t_count * t_price
        st.write(f"**إجمالي مبلغ التذاكر:** {total_t_price} ج.م")
        
        if st.button("إصدار وطباعة التذكرة", key="print_ticket_action"):
            st.session_state.last_ticket = {"count": t_count, "total": total_t_price, "time": datetime.now().strftime("%Y-%m-%d %H:%M")}
            st.success("✅ تم إصدار التذكرة بنجاح وتسجيلها في النظام!")
            
    with col_t2:
        st.markdown("#### آخر تذكرة مُصدرة / إعادة الطباعة")
        if st.session_state.last_ticket:
            lt = st.session_state.last_ticket
            st.write(f"عدد الأفراد: {lt['count']}")
            st.write(f"الإجمالي: {lt['total']} ج.م")
            st.write(f"وقت الإصدار: {lt['time']}")
            if st.button("🖨️ إعادة طباعة التذكرة الأخيرة", key="reprint_t"):
                st.info("جاري إعادة طباعة التذكرة...")
        else:
            st.warning("لا توجد تذاكر مُصدرة في هذه الجلسة حتى الآن.")

# --- باقي الأقسام الإدارية ---
elif st.session_state.current_screen == 'staff':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>إدارة الععمالة (الحضور والسُلف)</h3>", unsafe_allow_html=True)
    st.info("قسم متابعة حضور وانصراف الموظفين وسُلف العمالة الشهرية وتوثيقها.")
    staff_name = st.text_input("اسم الموظف / العامل")
    advance_val = st.number_input("قيمة السلفة (ج.م)", min_value=0, value=0)
    if st.button("تسجيل السلفة أو الحضور"):
        st.success(f"تم تسجيل البيانات بنجاح للموظف: {staff_name}")

elif st.session_state.current_screen == 'expenses':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>سجل المصروفات والنفقات الإدارية</h3>", unsafe_allow_html=True)
    st.info("قسم تسجيل النفقات اليومية ومصاريف التشغيل والصيانة.")
    exp_desc = st.text_input("بند المصروف (مثال: صيانة، ضيافة، كهرباء)")
    exp_cost = st.number_input("المبلغ المدفوع (ج.م)", min_value=0, value=0)
    if st.button("حفظ المصروف"):
        st.success("تم تسجيل المصروف في الدفتر المالي بنجاح.")

elif st.session_state.current_screen == 'equip':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>إدارة العهدة والمعدات والأجهزة</h3>", unsafe_allow_html=True)
    st.info("قسم تتبع وتسجيل كاميرات التصوير، إضاءات اللوكيشن، والأجهزة المسلمة للعهدة.")
    eq_name = st.text_input("اسم المعدة أو الجهاز")
    eq_status = st.selectbox("حالة العهدة", ["متاحة بالاستوديو", "مع عهدة المصور", "تحت الصيانة"])
    if st.button("تحديث حالة العهدة"):
        st.success("تم تحديث السجل بنجاح.")

elif st.session_state.current_screen == 'reports':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>التقارير والحسابات والربحية</h3>", unsafe_allow_html=True)
    st.info("قسم عرض ملخص المبيعات، إجمالي الحجوزات، المصروفات، وصصافي الربحية للوكيشن.")
    st.metric("إجمالي الإيرادات العامة", "0.00 ج.م")
    st.metric("صافي الأرباح", "0.00 ج.م")