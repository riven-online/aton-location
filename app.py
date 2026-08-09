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
    
    .stApp {
        background-color: #0b0d12;
    }

    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    @keyframes goldNeonGlow {
        0% {
            text-shadow: 0 0 5px rgba(212, 175, 55, 0.4), 0 0 10px rgba(212, 175, 55, 0.2);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6), inset 0 0 15px rgba(212, 175, 55, 0.15);
        }
        50% {
            text-shadow: 0 0 15px rgba(212, 175, 55, 0.8), 0 0 25px rgba(212, 175, 55, 0.5), 0 0 35px rgba(212, 175, 55, 0.3);
            box-shadow: 0 8px 35px rgba(212, 175, 55, 0.3), inset 0 0 25px rgba(212, 175, 55, 0.3);
        }
        100% {
            text-shadow: 0 0 5px rgba(212, 175, 55, 0.4), 0 0 10px rgba(212, 175, 55, 0.2);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6), inset 0 0 15px rgba(212, 175, 55, 0.15);
        }
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
        text-align: center !important;
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
        transition: all 0.3s ease;
    }
    .pos-card-container:hover {
        border-color: #d4af37;
        box-shadow: 0 12px 35px rgba(212, 175, 55, 0.2);
        transform: translateY(-3px);
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
        box-shadow: 0 0 12px rgba(212, 175, 55, 0.3);
    }
    .card-icon-circle i {
        font-size: 20px;
        color: #fce181;
    }

    .pos-card-title {
        color: #ffffff;
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 6px;
    }
    .pos-card-desc {
        color: #94a3b8;
        font-size: 12px;
        margin: 0;
    }

    .stButton {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%) !important;
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 14px !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 15px !important;
        width: 100% !important;
        max-width: 200px !important;
        margin: 0 auto !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.25);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4);
    }

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

# ------------------------------------------
# أداة فحص وحفظ بيانات Supabase (للتأكد أن الاتصال سليم)
# ------------------------------------------
with st.expander("🛠️ فحص حالة اتصال سوبابيز (Supabase Connection Status)"):
    if st.button("فحص جداول البيانات الآن"):
        try:
            test_t = supabase.table("tickets").select("id", count="exact").limit(1).execute()
            test_b = supabase.table("bookings").select("id", count="exact").limit(1).execute()
            st.success(f"✅ الاتصال بقاعدة البيانات سليم 100%!")
            st.info(f"📊 عدد السجلات في جدول التذاكر: {test_t.count if hasattr(test_t, 'count') else 'متاح'}")
            st.info(f"📅 عدد السجلات في جدول الحجوزات: {test_b.count if hasattr(test_b, 'count') else 'متاح'}")
        except Exception as conn_err:
            st.error(f"❌ حدث خطأ أثناء الاتصال بالجداول، تأكد من إنشاء جدولين باسم `tickets` و `bookings` في سوبابيز: {conn_err}")

if st.session_state.current_screen != 'dashboard':
    c_back1, c_back2, c_back3 = st.columns([1, 2, 1])
    with c_back2:
        if st.button("العودة للشاشة الرئيسية", key="back_to_home"):
            st.session_state.current_screen = 'dashboard'
            st.rerun()

st.divider()

# # ==========================================
# 4. الشاشة الرئيسية (معدلة لاسترجاع جميع الأقسام)
# ==========================================
if st.session_state.current_screen == 'dashboard':
    st.markdown("<h3 style='text-align: center; color: #d4af37; margin-bottom: 30px;'>لوحة التحكم الرئيسية</h3>", unsafe_allow_html=True)
    
    # توزيع الأقسام في شبكة (Grid)
    col1, col2, col3 = st.columns(3, gap="medium")
    col4, col5 = st.columns(2, gap="medium")
    
    # 1. قسم الحجوزات (مربوط بالداتا)
    with col1:
        st.markdown("""
        <div class="pos-card-container">
            <div class="card-icon-circle"><i class="fa-solid fa-calendar-days"></i></div>
            <div class="pos-card-title">حجز السيشن</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("دخول الحجوزات", key="nav_bookings"):
            st.session_state.current_screen = 'bookings'
            st.rerun()

    # 2. قسم التذاكر (مربوط بالداتا)
    with col2:
        st.markdown("""
        <div class="pos-card-container">
            <div class="card-icon-circle"><i class="fa-solid fa-ticket"></i></div>
            <div class="pos-card-title">تذاكر الأفراد</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("دخول التذاكر", key="nav_tickets"):
            st.session_state.current_screen = 'tickets'
            st.rerun()

    # 3. قسم الموظفين (إداري - بدون داتا)
    with col3:
        st.markdown("""
        <div class="pos-card-container" style="border-color: #64748b;">
            <div class="card-icon-circle" style="border-color: #64748b;"><i class="fa-solid fa-users"></i></div>
            <div class="pos-card-title">شؤون الموظفين</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("دخول الموظفين", key="nav_staff"):
            st.info("قسم إداري غير مربوط بقاعدة البيانات حالياً.")

    # 4. قسم المصروفات (إداري - بدون داتا)
    with col4:
        st.markdown("""
        <div class="pos-card-container" style="border-color: #64748b;">
            <div class="card-icon-circle" style="border-color: #64748b;"><i class="fa-solid fa-wallet"></i></div>
            <div class="pos-card-title">المصروفات والخزينة</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("دخول المصروفات", key="nav_expenses"):
            st.info("قسم إداري غير مربوط بقاعدة البيانات حالياً.")

    # 5. قسم التقارير (إداري - بدون داتا)
    with col5:
        st.markdown("""
        <div class="pos-card-container" style="border-color: #64748b;">
            <div class="card-icon-circle" style="border-color: #64748b;"><i class="fa-solid fa-chart-line"></i></div>
            <div class="pos-card-title">التقارير والإحصائيات</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("دخول التقارير", key="nav_reports"):
            st.info("قسم إداري غير مربوط بقاعدة البيانات حالياً.")

# ==========================================
# 5. قسم كاشير تذاكر الأفراد
# ==========================================
elif st.session_state.current_screen == 'tickets':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>قطع تذاكر دخول الأفراد</h3>", unsafe_allow_html=True)
    
    col_in, col_print = st.columns([1.1, 1], gap="large")
    
    with col_in:
        st.subheader("بيانات التذكرة")
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
                    st.success("تم الحفظ في قاعدة البيانات بنجاح!")
                except Exception as ex:
                    st.error(f"خطأ في الحفظ بقاعدة البيانات: {ex}")

        with btn_c2:
            if st.button("إعادة الطباعة"):
                if st.session_state.last_ticket:
                    st.info("جاري إعادة طباعة آخر تذكرة...")
                else:
                    st.warning("لا توجد تذكرة سابقة.")

    with col_print:
        st.subheader("معاينة الإيصال للطباعة")
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
                <div style="font-size: 11px; font-weight: 700; color: #333; margin-top:5px;">إيصال دخول أفراد</div>
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
                شكراً لزيارتكم آتون لوكيشن
            </div>
        </div>
        """
        st.markdown(receipt_html, unsafe_allow_html=True)

# ==========================================
# 6. قسم حجوزات الأفراح والتقويم
# ==========================================
elif st.session_state.current_screen == 'bookings':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>حجز سيشن وتقويم المواعيد</h3>", unsafe_allow_html=True)
    
    tab_new, tab_cal, tab_list = st.tabs(["حجز جديد وإيصال", "تقويم الاستعلام", "سجل الحجوزات"])

    with tab_new:
        col_b_input, col_b_print = st.columns([1.2, 1], gap="large")
        
        with col_b_input:
            client_name = st.text_input("اسم العريس / العروسة", key="b_cname")
            phone = st.text_input("رقم الهاتف", key="b_phone")
            
            session_type = st.selectbox(
                "نوع الجلسة / الباقة", 
                ["سيشن عادي", "سيشن مميز", "باقة الفرح الكامل", "فوتوسيشن خارجي", "تخصيص يدوي"],
                key="b_stype"
            )
            
            c1, c2 = st.columns(2)
            with c1:
                session_date = st.date_input("تاريخ السيشن", value=date.today(), key="b_sdate")
                start_t = st.time_input("وقت البداية", value=time(15, 0), key="b_sstart")
                location_room = st.selectbox("اللوكيشن المطلوبة", ["اللوكيشن الكلاسيك", "اللوكيشن المودرن", "غرفة التجهيز", "الاستوديو بالكامل"], key="b_sloc")
            with c2:
                end_t = st.time_input("وقت النهاية", value=time(16, 0), key="b_send")
                total_agreed = st.number_input("إجمالي الاتفاق (ج.م)", min_value=0, value=600, step=50, key="b_stotal")
                paid_amount = st.number_input("العربون المدفوع (ج.م)", min_value=0, value=200, step=50, key="b_spaid")

            photographer_commission = st.number_input("عمولة المصور", min_value=0, value=0, step=50, key="b_scomm")
            notes = st.text_area("ملاحظات", key="b_snotes")

            b_btn1, b_btn2 = st.columns(2)
            with b_btn1:
                if st.button("تأكيد وطباعة"):
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
                            st.success("تم حفظ الحجز في سوبابيز بنجاح!")
                        except Exception as ex:
                            try:
                                payload["booking_date"] = payload.pop("session_date")
                                supabase.table("bookings").insert(payload).execute()
                                st.session_state.last_booking = payload
                                st.success("تم حفظ الحجز في سوبابيز بنجاح!")
                            except Exception as ex2:
                                st.error(f"خطأ في الحفظ بقاعدة البيانات: {ex2}")

            with b_btn2:
                if st.button("إعادة طباعة"):
                    if st.session_state.last_booking:
                        st.info("جاري إعادة طباعة العقد الأخير...")
                    else:
                        st.warning("لا يوجد عقد محجوز مؤخراً.")

        with col_b_print:
            st.subheader("معاينة عقد الحجز")
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
                    <div style="font-size: 11px; font-weight: bold; color: #333; margin-top:5px;">إيصال تأكيد موعد وحجز</div>
                </div>
                <div class="receipt-row"><span>العميل:</span> <strong>{b_curr.get('client_name')}</strong></div>
                <div class="receipt-row"><span>الهاتف:</span> <strong>{b_curr.get('phone')}</strong></div>
                <div class="receipt-row"><span>الباقة:</span> <strong>{b_curr.get('session_type')}</strong></div>
                <div class="receipt-row"><span>اللوكيشن:</span> <strong>{b_curr.get('location_room')}</strong></div>
                <div class="receipt-row"><span>التاريخ:</span> <strong>{b_curr.get('session_date')}</strong></div>
                <div class="receipt-row"><span>الموعد:</span> <strong>من {str(b_curr.get('start_time'))[:5]} إلى {str(b_curr.get('end_time'))[:5]}</strong></div>
                <hr style="border:0.5px dashed #444; margin:8px 0;">
                <div class="receipt-row"><span>الإجمالي:</span> <strong>{float(b_curr.get('total_agreed', 0)):,.0f} ج.م</strong></div>
                <div class="receipt-row"><span>العربون:</span> <strong style="color:green;">{float(b_curr.get('paid_amount', 0)):,.0f} ج.م</strong></div>
                <div class="receipt-total receipt-row">
                    <span>المتبقي عند الحضور:</span>
                    <span style="color:red;">{rem_calc:,.0f} ج.م</span>
                </div>
            </div>
            """
            st.markdown(receipt_html, unsafe_allow_html=True)

    with tab_cal:
        st.subheader("تقويم استعلام المواعيد اليومية (من قاعدة البيانات)")
        search_date = st.date_input("اختر اليوم للتحقق", value=date.today(), key="cal_search_date")
        try:
            all_b = supabase.table("bookings").select("*").execute().data
            day_bookings = []
            if all_b:
                for b in all_b:
                    b_d = str(b.get('session_date') or b.get('booking_date') or b.get('date') or '').split('T')[0]
                    if b_d == str(search_date):
                        day_bookings.append(b)

            if day_bookings:
                st.success(f"✅ تم جلب {len(day_bookings)} حجز لهذا التاريخ من سوبابيز بنجاح")
                df_day = pd.DataFrame(day_bookings)
                st.dataframe(df_day, use_container_width=True)
            else:
                st.info("ℹ️ يوم فاضي: لا توجد حجوزات مسجلة في هذا اليوم على قاعدة البيانات.")
        except Exception as ex:
            st.warning(f"تعذر جلب الحجوزات من سوبابيز: {ex}")

    with tab_list:
        st.subheader("سجل كافة الحجوزات المسجلة بقاعدة البيانات")
        try:
            res_all = supabase.table("bookings").select("*").execute().data
            if res_all:
                st.dataframe(pd.DataFrame(res_all), use_container_width=True)
            else:
                st.info("لا توجد حجوزات سابقة مسجلة في قاعدة البيانات حتى الآن.")
        except Exception as ex:
            st.error(f"خطأ في جلب السجل: {ex}")

# شاشات الأقسام الأخرى
elif st.session_state.current_screen == 'reports':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>التقارير والميزانية</h3>", unsafe_allow_html=True)
    st.info("قسم التقارير المالية والربحية...")

elif st.session_state.current_screen == 'equip':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>إدارة العهدة والمعدات</h3>", unsafe_allow_html=True)
    st.info("قسم تسجيل وتسليم المعدات والعهدة...")

elif st.session_state.current_screen == 'expenses':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>المصروفات والنفقات</h3>", unsafe_allow_html=True)
    st.info("قسم تسجيل النفقات والمصروفات الإدارية اليومية...")

elif st.session_state.current_screen == 'staff':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>العمالة والحضور والسُلف</h3>", unsafe_allow_html=True)
    st.info("قسم تتبع الحضور، الانصراف، وسُلف الموظفين...")
