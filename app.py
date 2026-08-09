import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, time, date

# ==========================================
# 0. بطاقة الذاكرة الدائمة (استخدمها عند فتح شات جديد لاحقاً)
# ==========================================
"""
مشروع: آتون لوكيشن | Aton Location POS
جداول Supabase المستخدمة: tickets, bookings, equipment, expenses, staff
الحالة العامة (Session States): current_screen, last_ticket, last_booking
"""

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

    /* إخفاء القائمة الجانبية تماماً وأزرار التحكم بها */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }
    
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
    .pos-title-center {
        font-size: 32px;
        font-weight: 900;
        color: #fce181;
        letter-spacing: 2px;
        margin: 0;
    }

    .pos-card-container {
        background: linear-gradient(145deg, #161b26, #0f131c);
        border: 1px solid rgba(212, 175, 55, 0.35);
        border-radius: 16px;
        padding: 24px 20px 20px 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 12px;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .card-icon-circle {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.2), rgba(212, 175, 55, 0.05));
        border: 1px solid #d4af37;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 12px;
    }
    .card-icon-circle i { font-size: 20px; color: #fce181; }

    .pos-card-title { color: #ffffff; font-size: 18px; font-weight: 800; margin-bottom: 6px; }
    .pos-card-desc { color: #94a3b8; font-size: 12px; margin: 0; }

    .stButton>button {
        background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%) !important;
        color: #000000 !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        padding: 10px 15px !important;
        width: 100% !important;
        max-width: 200px !important;
        margin: 0 auto !important;
    }

    .receipt-container {
        max-width: 340px;
        margin: auto;
        padding: 22px;
        background-color: #ffffff;
        color: #000000;
        border-radius: 8px;
        border-top: 5px solid #d4af37;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    }
    .receipt-header { text-align: center; border-bottom: 2px dashed #222; padding-bottom: 12px; margin-bottom: 12px; }
    .receipt-title { font-size: 22px; font-weight: 900; margin: 0; }
    .receipt-row { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 13px; color: #111; }
    .receipt-total { border-top: 2px dashed #222; padding-top: 10px; margin-top: 12px; font-size: 16px; font-weight: 800; }
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
# 3. الهيدر العلوي الموحد
# ==========================================
st.markdown("""
<div class="pos-header-center">
    <div class="pos-title-center">آتون لوكيشن | ATON LOCATION</div>
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
# 4. الشاشة الرئيسية (Dashboard)
# ==========================================
if st.session_state.current_screen == 'dashboard':
    st.markdown("<h3 style='text-align: center; color: #d4af37; margin-bottom: 25px;'>اختر القسم المطلوب للبدء</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="pos-card-container">
            <div class="card-icon-circle"><i class="fa-solid fa-calendar-days"></i></div>
            <div class="pos-card-title">حجز سيشن وتقويم المواعيد</div>
            <div class="pos-card-desc">إضافة حجز جديد، طباعة العقد، وتتبع تقويم الأيام</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("دخول قسم الحجوزات", key="btn_nav_bookings"):
            st.session_state.current_screen = 'bookings'
            st.rerun()

    with col2:
        st.markdown("""
        <div class="pos-card-container">
            <div class="card-icon-circle"><i class="fa-solid fa-ticket"></i></div>
            <div class="pos-card-title">قطع تذاكر الأفراد</div>
            <div class="pos-card-desc">إصدار تذاكر الدخول الفورية وطباعة الإيصال فوراً</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("دخول كاشير التذاكر", key="btn_nav_tickets"):
            st.session_state.current_screen = 'tickets'
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    col3, col4, col5, col6 = st.columns(4, gap="medium")
    
    with col3:
        st.markdown("""
        <div class="pos-card-container">
            <div class="card-icon-circle"><i class="fa-solid fa-chart-pie"></i></div>
            <div class="pos-card-title">التقارير</div>
            <div class="pos-card-desc">الحسابات والربحية</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("التقارير والميزانية", key="btn_nav_reports"):
            st.session_state.current_screen = 'reports'
            st.rerun()

    with col4:
        st.markdown("""
        <div class="pos-card-container">
            <div class="card-icon-circle"><i class="fa-solid fa-boxes-stacked"></i></div>
            <div class="pos-card-title">العهدة</div>
            <div class="pos-card-desc">المعدات والأجهزة</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("إدارة العهدة", key="btn_nav_equip"):
            st.session_state.current_screen = 'equip'
            st.rerun()

    with col5:
        st.markdown("""
        <div class="pos-card-container">
            <div class="card-icon-circle"><i class="fa-solid fa-file-invoice-dollar"></i></div>
            <div class="pos-card-title">المصروفات</div>
            <div class="pos-card-desc">النفقات الإدارية</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("تسجيل المصاريف", key="btn_nav_expenses"):
            st.session_state.current_screen = 'expenses'
            st.rerun()

    with col6:
        st.markdown("""
        <div class="pos-card-container">
            <div class="card-icon-circle"><i class="fa-solid fa-users-gear"></i></div>
            <div class="pos-card-title">العمالة</div>
            <div class="pos-card-desc">الحضور والسُلف</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("إدارة العمالة", key="btn_nav_staff"):
            st.session_state.current_screen = 'staff'
            st.rerun()

# ==========================================
# 5. شاشة تذاكر الأفراد
# ==========================================
elif st.session_state.current_screen == 'tickets':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>قطع تذاكر دخول الأفراد</h3>", unsafe_allow_html=True)
    col_in, col_print = st.columns([1.1, 1], gap="large")
    
    with col_in:
        count = st.number_input("عدد الأفراد", min_value=1, value=1, step=1, key="pos_t_count")
        price_per_ticket = st.number_input("سعر التذكرة للفرد (ج.م)", min_value=1, value=50, step=10, key="pos_t_price")
        total_price = count * price_per_ticket
        
        st.markdown(f"""
        <div style="background: #141824; border:1px solid #d4af37; padding:15px; border-radius:10px; text-align:center; margin: 15px 0;">
            <div style="font-size: 14px; color:#94a3b8;">الإجمالي المطلوب دفعه</div>
            <div style="font-size: 28px; font-weight:900; color:#d4af37;">{total_price:,.0f} ج.م</div>
        </div>
        """, unsafe_allow_html=True)
        
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button("تأكيد وحفظ وطباعة"):
                try:
                    supabase.table("tickets").insert({"count": count, "price_per_ticket": price_per_ticket, "total_price": total_price}).execute()
                    st.session_state.last_ticket = {"time": datetime.now().strftime('%Y-%m-%d %H:%M'), "count": count, "price": price_per_ticket, "total": total_price}
                    st.success("تم الحفظ بنجاح! جاري طلب الطباعة...")
                    st.markdown("<script>window.print();</script>", unsafe_allow_html=True)
                except Exception as ex:
                    st.error(f"خطأ في العملية: {ex}")
        with btn_c2:
            if st.button("إعادة الطباعة"):
                if st.session_state.last_ticket:
                    st.markdown("<script>window.print();</script>", unsafe_allow_html=True)
                else:
                    st.warning("لا توجد تذكرة سابقة.")

    with col_print:
        t_data = st.session_state.last_ticket if st.session_state.last_ticket else {"time": datetime.now().strftime('%Y-%m-%d %H:%M'), "count": count, "price": price_per_ticket, "total": total_price}
        st.markdown(f"""
        <div class="receipt-container">
            <div class="receipt-header">
                <div class="receipt-title">آتون لوكيشن</div>
                <div style="font-size: 11px; font-weight: 700; color: #333; margin-top:5px;">إيصال دخول أفراد</div>
            </div>
            <div class="receipt-row"><span>التاريخ والوقت:</span> <strong>{t_data['time']}</strong></div>
            <div class="receipt-row"><span>عدد الأفراد:</span> <strong>{t_data['count']} فرد</strong></div>
            <div class="receipt-row"><span>سعر الفرد:</span> <strong>{t_data['price']:,.0f} ج.م</strong></div>
            <div class="receipt-total receipt-row"><span>الإجمالي:</span> <span>{t_data['total']:,.0f} ج.م</span></div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 6. شاشة الحجوزات
# ==========================================
elif st.session_state.current_screen == 'bookings':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>حجز سيشن وتقويم المواعيد</h3>", unsafe_allow_html=True)
    tab_new, tab_cal, tab_list = st.tabs(["حجز جديد وإيصال", "تقويم الاستعلام", "سجل الحجوزات"])

    with tab_new:
        col_b_input, col_b_print = st.columns([1.2, 1], gap="large")
        with col_b_input:
            client_name = st.text_input("اسم العريس / العروسة", key="b_cname")
            phone = st.text_input("رقم الهاتف", key="b_phone")
            session_type = st.selectbox("نوع الجلسة / الباقة", ["سيشن عادي", "سيشن مميز", "باقة الفرح الكامل", "فوتوسيشن خارجي"], key="b_stype")
            c1, c2 = st.columns(2)
            with c1:
                session_date = st.date_input("تاريخ السيشن", value=date.today(), key="b_sdate")
                start_t = st.time_input("وقت البداية", value=time(15, 0), key="b_sstart")
                location_room = st.selectbox("اللوكيشن المطلوبة", ["اللوكيشن الكلاسيك", "اللوكيشن المودرن", "غرفة التجهيز", "الاستوديو بالكامل"], key="b_sloc")
            with c2:
                end_t = st.time_input("وقت النهاية", value=time(16, 0), key="b_send")
                total_agreed = st.number_input("إجمالي الاتفاق (ج.م)", min_value=0, value=600, step=50, key="b_stotal")
                paid_amount = st.number_input("العربون المدفوع (ج.م)", min_value=0, value=200, step=50, key="b_spaid")

            if st.button("تأكيد وطباعة الحجز"):
                if client_name:
                    payload = {"client_name": client_name, "phone": phone, "session_date": str(session_date), "session_type": session_type, "total_agreed": total_agreed, "paid_amount": paid_amount, "start_time": str(start_t), "end_time": str(end_t), "location_room": location_room}
                    try:
                        supabase.table("bookings").insert(payload).execute()
                        st.session_state.last_booking = payload
                        st.success("تم الحفظ بنجاح!")
                        st.markdown("<script>window.print();</script>", unsafe_allow_html=True)
                    except Exception as ex:
                        st.error(f"خطأ: {ex}")
                else:
                    st.warning("أدخل اسم العميل.")

        with col_b_print:
            b_curr = st.session_state.last_booking if st.session_state.last_booking else {"client_name": '...', "phone": '...', "session_type": session_type, "location_room": location_room, "session_date": str(session_date), "start_time": str(start_t), "end_time": str(end_t), "total_agreed": total_agreed, "paid_amount": paid_amount}
            rem_calc = float(b_curr.get("total_agreed", 0)) - float(b_curr.get("paid_amount", 0))
            st.markdown(f"""
            <div class="receipt-container">
                <div class="receipt-header"><div class="receipt-title">آتون لوكيشن</div></div>
                <div class="receipt-row"><span>العميل:</span> <strong>{b_curr.get('client_name')}</strong></div>
                <div class="receipt-row"><span>التاريخ:</span> <strong>{b_curr.get('session_date')}</strong></div>
                <div class="receipt-row"><span>المتبقي:</span> <strong style="color:red;">{rem_calc:,.0f} ج.م</strong></div>
            </div>
            """, unsafe_allow_html=True)

    with tab_cal:
        st.subheader("تقويم المواعيد")
        try:
            res_cal = supabase.table("bookings").select("*").execute()
            if res_cal.data:
                df_b = pd.DataFrame(res_cal.data)
                sel_cal_date = st.date_input("اختر تاريخاً", value=date.today(), key="cal_filter_date")
                df_b['session_date'] = pd.to_datetime(df_b['session_date']).dt.date
                day_bookings = df_b[df_b['session_date'] == sel_cal_date]
                if not day_bookings.empty:
                    st.dataframe(day_bookings, use_container_width=True)
                else:
                    st.info("لا توجد حجوزات في هذا اليوم.")
        except Exception as e:
            st.info("لا توجد بيانات كافية للتقويم.")

    with tab_list:
        try:
            st.dataframe(pd.DataFrame(supabase.table("bookings").select("*").execute().data), use_container_width=True)
        except Exception:
            st.info("لا توجد سجلات.")

# ==========================================
# 7, 8, 9, 10. التقارير، العهدة، المصروفات، والعمالة
# ==========================================
elif st.session_state.current_screen == 'reports':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>التقارير المالية</h3>", unsafe_allow_html=True)
    try:
        t_rev = sum([float(x.get('total_price', 0)) for x in supabase.table("tickets").select("total_price").execute().data])
        b_rev = sum([float(x.get('paid_amount', 0)) for x in supabase.table("bookings").select("paid_amount").execute().data])
        st.metric("إجمالي الإيرادات", f"{t_rev + b_rev:,.0f} ج.م")
    except Exception:
        st.metric("إجمالي الإيرادات", "0 ج.م")

elif st.session_state.current_screen == 'equip':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>إدارة العهدة</h3>", unsafe_allow_html=True)
    eq_name = st.text_input("اسم المعدة")
    if st.button("إضافة معدة"):
        if eq_name:
            supabase.table("equipment").insert({"name": eq_name, "status": "سليمة"}).execute()
            st.success("تمت الإضافة!")

elif st.session_state.current_screen == 'expenses':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>المصروفات</h3>", unsafe_allow_html=True)
    exp_title = st.text_input("بند المصروف")
    exp_amount = st.number_input("المبلغ", min_value=0.0)
    if st.button("حفظ المصروف"):
        if exp_title:
            supabase.table("expenses").insert({"title": exp_title, "amount": exp_amount}).execute()
            st.success("تم الحفظ!")

elif st.session_state.current_screen == 'staff':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>إدارة العمالة</h3>", unsafe_allow_html=True)
    st_name = st.text_input("اسم الموظف")
    if st.button("إضافة موظف"):
        if st_name:
            supabase.table("staff").insert({"name": st_name}).execute()
            st.success("تمت الإضافة!")