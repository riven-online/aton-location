import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, time, date

# ==========================================
# 1. تهيئة الصفحة والأنماط البصرية الحديثة (Modern POS UI)
# ==========================================
st.set_page_config(
    page_title="آتون لوكيشن | Aton Location POS",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تهيئة متغيرات الجلسة (Session State) للاسم والورديّة
if 'cashier_name' not in st.session_state:
    st.session_state.cashier_name = "إسلام محمد"

if 'session_name' not in st.session_state:
    st.session_state.session_name = "الوردية الصباحية ☀️"

if 'shift_start' not in st.session_state:
    st.session_state.shift_start = "09:00 AM"

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

    /* إخفاء القائمة الجانبية تماماً وأزرار التحكم بها */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* شريط الرأس المعنون والموسع في منتصف الصفحة */
    .pos-header-center {
        background: linear-gradient(135deg, #141824 0%, #0d1017 100%);
        border: 2px solid #d4af37;
        padding: 20px;
        border-radius: 16px;
        margin: 0 auto 20px auto;
        text-align: center !important;
        width: 100%;
        max-width: 900px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
    }
    .pos-title-center {
        font-size: 28px;
        font-weight: 900;
        color: #d4af37;
        letter-spacing: 1.5px;
        margin: 0;
        text-align: center !important;
    }

    /* بطاقات معلومات الكاشير والسيشن العلوية */
    .info-card {
        background: rgba(20, 24, 36, 0.85);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(212, 175, 55, 0.25);
        border-radius: 14px;
        padding: 14px 18px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .info-label {
        font-size: 12px;
        color: #94a3b8;
        margin-bottom: 4px;
        font-weight: 600;
    }
    .info-value {
        font-size: 16px;
        color: #f8fafc;
        font-weight: 800;
    }

    /* كروت الكاشير الرئيسية */
    .pos-card-button {
        background: linear-gradient(145deg, #161b26, #0f131c);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 16px;
        padding: 25px 15px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        margin-bottom: 12px;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .pos-card-title {
        color: #ffffff;
        font-size: 19px;
        font-weight: 800;
        margin-bottom: 6px;
    }
    .pos-card-desc {
        color: #94a3b8;
        font-size: 12px;
        margin: 0;
    }

    /* توسيط أزرار Streamlit بداخل كل العمود */
    .stButton {
        display: flex;
        justify-content: center;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%) !important;
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        width: 80% !important;
        margin: 0 auto !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.25);
    }

    /* تصميم الإيصال الطباعي */
    .receipt-container {
        max-width: 340px;
        margin: auto;
        padding: 22px;
        background-color: #ffffff;
        color: #000000;
        border-radius: 8px;
        font-family: 'Cairo', sans-serif;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
        border-top: 5px solid #d4af37;
    }
    .receipt-header {
        text-align: center;
        border-bottom: 2px dashed #222;
        padding-bottom: 12px;
        margin-bottom: 12px;
    }
    .receipt-title {
        font-size: 22px;
        font-weight: 900;
        color: #000000;
        margin: 0;
    }
    .receipt-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        font-size: 13px;
        color: #111111;
    }
    .receipt-total {
        border-top: 2px dashed #222;
        padding-top: 10px;
        margin-top: 12px;
        font-size: 16px;
        font-weight: 800;
    }

    @media print {
        body * {
            visibility: hidden;
        }
        .receipt-container, .receipt-container * {
            visibility: visible;
        }
        .receipt-container {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. الاتصال بقاعدة البيانات Supabase
# ==========================================
try:
    url = str(st.secrets["SUPABASE_URL"]).strip()
    key = str(st.secrets["SUPABASE_KEY"]).strip()
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error(f"خطأ في الاتصال بقاعدة البيانات: {e}")
    st.stop()

# ==========================================
# 3. الهيدر العلوي الموحد ومعلومات الكاشير والسيشن
# ==========================================
st.markdown("""
<div class="pos-header-center">
    <div class="pos-title-center">آتون لوكيشن | ATON LOCATION</div>
</div>
""", unsafe_allow_html=True)

# عرض بيانات الكاشير والسيشن الحالي في أعمدة أنيقة بأعلى الواجهة
c_info1, c_info2, c_info3, c_info4 = st.columns(4)

with c_info1:
    st.markdown(f"""
        <div class="info-card">
            <div class="info-label">👤 كاشير الشيفت الحالي</div>
            <div class="info-value">💼 {st.session_state.cashier_name}</div>
        </div>
    """, unsafe_allow_html=True)

with c_info2:
    st.markdown(f"""
        <div class="info-card">
            <div class="info-label">🕒 اسم السيشن / الورديّة</div>
            <div class="info-value">🔄 {st.session_state.session_name}</div>
        </div>
    """, unsafe_allow_html=True)

with c_info3:
    st.markdown(f"""
        <div class="info-card">
            <div class="info-label">⏰ وقت بدء الشيفت</div>
            <div class="info-value">⏱️ {st.session_state.shift_start}</div>
        </div>
    """, unsafe_allow_html=True)

with c_info4:
    st.markdown(f"""
        <div class="info-card">
            <div class="info-label">🟢 حالة النظام</div>
            <div class="info-value" style="color: #34d399;">✨ متصل وجاهز</div>
        </div>
    """, unsafe_allow_html=True)

if st.session_state.current_screen != 'dashboard':
    c_back1, c_back2, c_back3 = st.columns([1, 2, 1])
    with c_back2:
        if st.button("العودة للشاشة الرئيسية", key="back_to_home"):
            st.session_state.current_screen = 'dashboard'
            st.rerun()

st.divider()

# ==========================================
# 4. الشاشة الرئيسية (Dashboard - Centered Cards & Buttons)
# ==========================================
if st.session_state.current_screen == 'dashboard':
    st.markdown("<h3 style='text-align: center; color: #d4af37; margin-bottom: 30px;'>اختر القسم المطلوب للبدء</h3>", unsafe_allow_html=True)
    
    # الصف الأول: الحجوزات والتذاكر
    row1_1, row1_2 = st.columns(2)
    
    with row1_1:
        st.markdown("""
        <div class="pos-card-button">
            <div class="pos-card-title">📅 حجز سيشن وتقويم المواعيد</div>
            <div class="pos-card-desc">إضافة حجز جديد، طباعة العقد، وتتبع تقويم الأيام</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("دخول قسم الحجوزات", key="btn_nav_bookings"):
            st.session_state.current_screen = 'bookings'
            st.rerun()

    with row1_2:
        st.markdown("""
        <div class="pos-card-button">
            <div class="pos-card-title">🎟️ قطع تذاكر الأفراد</div>
            <div class="pos-card-desc">إصدار تذاكر الدخول الفورية وطباعة الإيصال فوراً</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("دخول كاشير التذاكر", key="btn_nav_tickets"):
            st.session_state.current_screen = 'tickets'
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # الصف الثاني: باقي الخدمات والأقسام الفرعية
    row2_1, row2_2, row2_3, row2_4 = st.columns(4)
    
    with row2_1:
        st.markdown("""
        <div class="pos-card-button">
            <div class="pos-card-title">📊 التقارير والميزانية</div>
            <div class="pos-card-desc">الحسابات والربحية</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("التقارير", key="btn_nav_reports"):
            st.session_state.current_screen = 'reports'
            st.rerun()

    with row2_2:
        st.markdown("""
        <div class="pos-card-button">
            <div class="pos-card-title">🛠️ إدارة العهدة والمعدات</div>
            <div class="pos-card-desc">تسليم واستلام المعدات</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("العهدة", key="btn_nav_equip"):
            st.session_state.current_screen = 'equip'
            st.rerun()

    with row2_3:
        st.markdown("""
        <div class="pos-card-button">
            <div class="pos-card-title">💸 المصروفات والنفقات</div>
            <div class="pos-card-desc">تسجيل المصاريف الإدارية</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("المصروفات", key="btn_nav_expenses"):
            st.session_state.current_screen = 'expenses'
            st.rerun()

    with row2_4:
        st.markdown("""
        <div class="pos-card-button">
            <div class="pos-card-title">👷 العمالة والحضور والسُلف</div>
            <div class="pos-card-desc">سجل الحضور اليومي والسُلف</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("العمالة", key="btn_nav_staff"):
            st.session_state.current_screen = 'staff'
            st.rerun()

# ==========================================
# 5. قسم كاشير تذاكر الأفراد
# ==========================================
elif st.session_state.current_screen == 'tickets':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>🎟️ قطع تذاكر دخول الأفراد</h3>", unsafe_allow_html=True)
    
    col_in, col_print = st.columns([1.1, 1])
    
    with col_in:
        st.subheader("📝 بيانات التذكرة")
        count = st.number_input("عدد الأفراد 👥", min_value=1, value=1, step=1, key="pos_t_count")
        price_per_ticket = st.number_input("سعر التذكرة للفرد (ج.م) 💵", min_value=1, value=50, step=10, key="pos_t_price")
        total_price = count * price_per_ticket
        
        st.markdown(f"""
        <div style="background: #141824; border:1px solid #d4af37; padding:15px; border-radius:10px; text-align:center; margin: 15px 0;">
            <div style="font-size: 14px; color:#94a3b8;">💰 الإجمالي المطلوب دفعه</div>
            <div style="font-size: 28px; font-weight:900; color:#d4af37;">{total_price:,.0f} ج.م</div>
        </div>
        """, unsafe_allow_html=True)
        
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button("✅ تأكيد وحفظ وطباعة"):
                try:
                    supabase.table("tickets").insert({
                        "count": count,
                        "price_per_ticket": price_per_ticket,
                        "total_price": total_price
                    }).execute()
                    
                    st.session_state.last_ticket = {
                        "time": datetime.now().strftime('%Y-%m-%d %H:%M'),
                        "count": count,
                        "price": price_per_ticket,
                        "total": total_price
                    }
                    st.success("تم الحفظ بنجاح! جاري طلب الطباعة...")
                    st.markdown("<script>window.print();</script>", unsafe_allow_html=True)
                except Exception as ex:
                    st.error(f"خطأ في العملية: {ex}")

        with btn_c2:
            if st.button("🔄 إعادة طباعة آخر تذكرة"):
                if st.session_state.last_ticket:
                    st.info("جاري إعادة طباعة آخر تذكرة دون تسجيلها مجدداً...")
                    st.markdown("<script>window.print();</script>", unsafe_allow_html=True)
                else:
                    st.warning("لا توجد تذكرة سابقة مسجلة في الجلسة لإعادة طباعتها.")

    with col_print:
        st.subheader("🖨️ معاينة الإيصال للطباعة")
        t_data = st.session_state.last_ticket if st.session_state.last_ticket else {
            "time": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "count": count,
            "price": price_per_ticket,
            "total": total_price
        }
        
        receipt_html = f"""
        <div class="receipt-container">
            <div class="receipt-header">
                <div class="receipt-title">آتون لوكيشن</div>
                <div style="font-size: 11px; font-weight: 700; color: #333; margin-top:5px;">🎟️ إيصال دخول أفراد</div>
            </div>
            <div class="receipt-row"><span>التاريخ والوقت:</span> <strong>{t_data['time']}</strong></div>
            <div class="receipt-row"><span>عدد الأفراد:</span> <strong>{t_data['count']} فرد</strong></div>
            <div class="receipt-row"><span>سعر الفرد:</span> <strong>{t_data['price']:,.0f} ج.م</strong></div>
            <hr style="border:0.5px dashed #444; margin:8px 0;">
            <div class="receipt-total receipt-row">
                <span>الإجمالي المدفوع:</span>
                <span>{t_data['total']:,.0f} ج.م</span>
            </div>
            <div style="text-align:center; font-size:10px; color:#555; margin-top:15px; font-weight:bold;">
                شكراً لزيارتكم آتون لوكيشن ✨
            </div>
        </div>
        """
        st.markdown(receipt_html, unsafe_allow_html=True)

# ==========================================
# 6. قسم حجوزات الأفراح والتقويم
# ==========================================
elif st.session_state.current_screen == 'bookings':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>📅 حجز سيشن وتقويم المواعيد</h3>", unsafe_allow_html=True)
    
    tab_new, tab_cal, tab_list = st.tabs(["حجز جديد وإيصال 📝", "تقويم الاستعلام 📅", "سجل الحجوزات 📋"])

    with tab_new:
        col_b_input, col_b_print = st.columns([1.2, 1])
        
        with col_b_input:
            client_name = st.text_input("اسم العريس / العروسة 👤", key="b_cname")
            phone = st.text_input("رقم الهاتف 📱", key="b_phone")
            
            session_type = st.selectbox(
                "نوع الجلسة / الباقة 🎬", 
                ["سيشن عادي", "سيشن مميز", "باقة الفرح الكامل", "فوتوسيشن خارجي", "تخصيص يدوي"],
                key="b_stype"
            )
            
            c1, c2 = st.columns(2)
            with c1:
                session_date = st.date_input("تاريخ السيشن 📅", value=date.today(), key="b_sdate")
                start_t = st.time_input("وقت البداية ⏰", value=time(15, 0), key="b_sstart")
                location_room = st.selectbox("اللوكيشن المطلوبة 📍", ["اللوكيشن الكلاسيك", "اللوكيشن المودرن", "غرفة التجهيز", "الاستوديو بالكامل"], key="b_sloc")
            with c2:
                end_t = st.time_input("وقت النهاية ⏱️", value=time(16, 0), key="b_send")
                total_agreed = st.number_input("إجمالي الاتفاق (ج.م) 💰", min_value=0, value=600, step=50, key="b_stotal")
                paid_amount = st.number_input("العربون المدفوع (ج.م) 💳", min_value=0, value=200, step=50, key="b_spaid")

            photographer_commission = st.number_input("عمولة المصور 📸", min_value=0, value=0, step=50, key="b_scomm")
            notes = st.text_area("ملاحظات 📝", key="b_snotes")

            b_btn1, b_btn2 = st.columns(2)
            with b_btn1:
                if st.button("✅ تأكيد وحفظ العقد وطباعة"):
                    if not client_name:
                        st.warning("يرجى إدخال اسم العميل أولاً.")
                    else:
                        payload = {
                            "client_name": client_name,
                            "phone": phone,
                            "session_date": str(session_date),
                            "session_type": session_type,
                            "total_agreed": total_agreed,
                            "paid_amount": paid_amount,
                            "start_time": str(start_t),
                            "end_time": str(end_t),
                            "location_room": location_room,
                            "photographer_commission": photographer_commission,
                            "notes": notes
                        }
                        try:
                            supabase.table("bookings").insert(payload).execute()
                            st.session_state.last_booking = payload
                            st.success("تم تأكيد الحجز وحفظه! جاري فتح الطباعة...")
                            st.markdown("<script>window.print();</script>", unsafe_allow_html=True)
                        except Exception as ex:
                            try:
                                payload["booking_date"] = payload.pop("session_date")
                                supabase.table("bookings").insert(payload).execute()
                                st.session_state.last_booking = payload
                                st.success("تم الحفظ بنجاح! جاري فتح الطباعة...")
                                st.markdown("<script>window.print();</script>", unsafe_allow_html=True)
                            except Exception as ex2:
                                st.error(f"خطأ في الحفظ: {ex2}")

            with b_btn2:
                if st.button("🔄 إعادة طباعة العقد الحالي"):
                    if st.session_state.last_booking:
                        st.info("جاري إعادة طباعة العقد الأخير...")
                        st.markdown("<script>window.print();</script>", unsafe_allow_html=True)
                    else:
                        st.warning("لا يوجد عقد محجوز مؤخراً لإعادة طباعته.")

        with col_b_print:
            st.subheader("🖨️ معاينة عقد الحجز")
            b_curr = st.session_state.last_booking if st.session_state.last_booking else {
                "client_name": client_name if client_name else '...................',
                "phone": phone if phone else '...................',
                "session_type": session_type,
                "location_room": location_room,
                "session_date": str(session_date),
                "start_time": str(start_t),
                "end_time": str(end_t),
                "total_agreed": total_agreed,
                "paid_amount": paid_amount
            }
            rem_calc = float(b_curr.get("total_agreed", 0)) - float(b_curr.get("paid_amount", 0))
            
            receipt_html = f"""
            <div class="receipt-container">
                <div class="receipt-header">
                    <div class="receipt-title">آتون لوكيشن</div>
                    <div style="font-size: 11px; font-weight: bold; color: #333; margin-top:5px;">📋 إيصال تأكيد موعد وحجز</div>
                </div>
                <div class="receipt-row"><span>العميل:</span> <strong>{b_curr.get('client_name')}</strong></div>
          