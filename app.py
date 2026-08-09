import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, time, date

# ==========================================
# 1. تهيئة الصفحة والأنماط البصرية (بريميوم نظيف)
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
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        text-align: right;
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    
    .stApp {
        background-color: #0b0f19;
    }

    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* هيدر فاخر وهادئ */
    .app-header {
        background: linear-gradient(135deg, #131b2e 0%, #0d1322 100%);
        border: 1px solid rgba(212, 175, 55, 0.3);
        padding: 18px;
        border-radius: 12px;
        margin: 10px auto 25px auto;
        text-align: center;
        width: 100%;
        max-width: 700px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    .app-title {
        font-size: 26px;
        font-weight: 800;
        color: #e2c062;
        letter-spacing: 1px;
        margin: 0;
    }

    /* تصميم أزرار القائمة الرئيسية لتكون ككروت احترافية متناسقة */
    .stButton>button {
        background: linear-gradient(145deg, #161f33, #0f172a) !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        color: #f1f5f9 !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        border-radius: 12px !important;
        padding: 25px 15px !important;
        width: 100% !important;
        min-height: 130px !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        border-color: #e2c062 !important;
        background: linear-gradient(145deg, #1c2740, #131d33) !important;
        box-shadow: 0 10px 25px rgba(212, 175, 55, 0.2) !important;
        transform: translateY(-3px);
    }

    /* إيصالات الطباعة */
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
<div class="app-header">
    <div class="app-title">آتون لوكيشن | ATON LOCATION</div>
</div>
""", unsafe_allow_html=True)

if st.session_state.current_screen != 'dashboard':
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        if st.button("العودة للقائمة الرئيسية", key="back_home_btn", use_container_width=True):
            st.session_state.current_screen = 'dashboard'
            st.rerun()

st.divider()

# ==========================================
# 4. الشاشة الرئيسية (Dashboard)
# ==========================================
if st.session_state.current_screen == 'dashboard':
    st.markdown("<h4 style='text-align: center; color: #e2c062; margin-bottom: 25px;'>اختر القسم المطلوب للبدء</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        if st.button("حجز سيشن وتقويم المواعيد\nإضافة حجز جديد، طباعة العقد، وتتبع تقويم الأيام", key="btn_nav_bookings"):
            st.session_state.current_screen = 'bookings'
            st.rerun()

    with col2:
        if st.button("قطع تذاكر الأفراد\nإصدار تذاكر الدخول الفورية وطباعة الإيصال فوراً", key="btn_nav_tickets"):
            st.session_state.current_screen = 'tickets'
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    col3, col4, col5, col6 = st.columns(4, gap="medium")
    with col3:
        if st.button("التقارير والميزانية\nالحسابات ومتابعة الأرباح", key="btn_nav_reports"):
            st.session_state.current_screen = 'reports'
            st.rerun()

    with col4:
        if st.button("العهدة والمعدات\nإدارة الأجهزة والأرقام", key="btn_nav_equip"):
            st.session_state.current_screen = 'equip'
            st.rerun()

    with col5:
        if st.button("المصروفات والنفقات\nالنفقات والمصاريف اليومية", key="btn_nav_expenses"):
            st.session_state.current_screen = 'expenses'
            st.rerun()

    with col6:
        if st.button("العمالة والحضور والسُلف\nحضور الموظفين وطلب السُلف", key="btn_nav_staff"):
            st.session_state.current_screen = 'staff'
            st.rerun()

# ==========================================
# 5. قسم كاشير تذاكر الأفراد
# ==========================================
elif st.session_state.current_screen == 'tickets':
    st.markdown("<h4 style='color: #e2c062; text-align: center;'>قطع تذاكر دخول الأفراد</h4>", unsafe_allow_html=True)
    
    col_in, col_print = st.columns([1.1, 1], gap="large")
    
    with col_in:
        st.subheader("بيانات التذكرة")
        count = st.number_input("عدد الأفراد", min_value=1, value=1, step=1, key="pos_t_count")
        price_per_ticket = st.number_input("سعر التذكرة للفرد (ج.م)", min_value=1, value=50, step=10, key="pos_t_price")
        total_price = count * price_per_ticket
        
        st.markdown(f"""
        <div style="background: #131b2e; border:1px solid #e2c062; padding:15px; border-radius:10px; text-align:center; margin: 15px 0;">
            <div style="font-size: 13px; color:#94a3b8;">الإجمالي المطلوب دفعه</div>
            <div style="font-size: 26px; font-weight:800; color:#e2c062;">{total_price:,.0f} ج.م</div>
        </div>
        """, unsafe_allow_html=True)
        
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button("تأكيد وحفظ وطباعة", use_container_width=True):
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
            if st.button("إعادة الطباعة", use_container_width=True):
                if st.session_state.last_ticket:
                    st.info("جاري إعادة طباعة آخر تذكرة...")
                    st.markdown("<script>window.print();</script>", unsafe_allow_html=True)
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
    st.markdown("<h4 style='color: #e2c062; text-align: center;'>حجز سيشن وتقويم المواعيد</h4>", unsafe_allow_html=True)
    
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
                if st.button("تأكيد وطباعة", use_container_width=True):
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
                            st.success("تم الحفظ بنجاح! جاري فتح الطباعة...")
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
                if st.button("إعادة طباعة", use_container_width=True):
                    if st.session_state.last_booking:
                        st.info("جاري إعادة طباعة العقد الأخير...")
                        st.markdown("<script>window.print();</script>", unsafe_allow_html=True)
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
        st.subheader("تقويم استعلام المواعيد اليومية")
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
                st.success(f"تم العثور على {len(day_bookings)} حجز في هذا التاريخ")
                df_day = pd.DataFrame(day_bookings)
                st.dataframe(df_day, use_container_width=True)
            else:
                st.info("لا توجد حجوزات مسجلة في هذا اليوم")
        except Exception as ex:
            st.warning(f"تعذر جلب الحجوزات: {ex}")

    with tab_list:
        st.subheader("سجل كافة الحجوزات المسجلة")
        try:
            res_all = supabase.table("bookings").select("*").execute().data
            if res_all:
                st.dataframe(pd.DataFrame(res_all), use_container_width=True)
            else:
                st.info("لا توجد حجوزات سابقة مسجلة في قاعدة البيانات")
        except Exception as ex:
            st.error(f"خطأ في جلب السجل: {ex}")

# ==========================================
# 7. قسم التقارير والميزانية
# ==========================================
elif st.session_state.current_screen == 'reports':
    st.markdown("<h4 style='color: #e2c062; text-align: center;'>التقارير والميزانية</h4>", unsafe_allow_html=True)
    try:
        rep_data = supabase.table("reports").select("*").execute().data
        if rep_data:
            st.dataframe(pd.DataFrame(rep_data), use_container_width=True)
        else:
            st.info("لا توجد تقارير مسجلة حالياً في قاعدة البيانات.")
    except Exception as ex:
        st.warning(f"ملاحظة: جدول التقارير غير متاح أو فارغ ({ex})")

# ==========================================
# 8. قسم العهدة والمعدات
# ==========================================
elif st.session_state.current_screen == 'equip':
    st.markdown("<h4 style='color: #e2c062; text-align: center;'>إدارة العهدة والمعدات</h4>", unsafe_allow_html=True)
    
    with st.form("add_equip_form"):
        st.subheader("إضافة عهدة أو معدة جديدة")
        eq_name = st.text_input("اسم المعدة / الجهاز")
        eq_serial = st.text_input("الرقم التسلسلي (Serial Number)")
        eq_status = st.selectbox("الحالة", ["متاحة", "قيد الاستخدام", "تحت الصيانة"])
        eq_submit = st.form_submit_button("حفظ المعدة")
        if eq_submit:
            if eq_name:
                try:
                    supabase.table("equip").insert({"equipment_name": eq_name, "serial_number": eq_serial, "status": eq_status}).execute()
                    st.success("تم حفظ المعدة بنجاح!")
                except Exception as e:
                    st.error(f"خطأ في الحفظ: {e}")
            else:
                st.warning("يرجى إدخال اسم المعدة على الأقل.")

    st.markdown("---")
    st.subheader("سجل العهدة الحالية")
    try:
        eq_data = supabase.table("equip").select("*").execute().data
        if eq_data:
            st.dataframe(pd.DataFrame(eq_data), use_container_width=True)
        else:
            st.info("لا توجد معدات مسجلة في العهدة.")
    except Exception as ex:
        st.warning(f"ملاحظة: جدول العهدة غير متاح أو فارغ ({ex})")

# ==========================================
# 9. قسم المصروفات والنفقات
# ==========================================
elif st.session_state.current_screen == 'expenses':
    st.markdown("<h4 style='color: #e2c062; text-align: center;'>المصروفات والنفقات</h4>", unsafe_allow_html=True)
    
    with st.form("add_expense_form"):
        st.subheader("تسجيل مصروف جديد")
        exp_desc = st.text_input("بيان المصروف (السبب)")
        exp_amount = st.number_input("المبلغ (ج.م)", min_value=0.0, value=50.0, step=10.0)
        exp_submit = st.form_submit_button("حفظ المصروف")
        if exp_submit:
            if exp_desc:
                try:
                    supabase.table("expenses").insert({"description": exp_desc, "amount": exp_amount}).execute()
                    st.success("تم تسجيل المصروف بنجاح!")
                except Exception as e:
                    st.error(f"خطأ في حفظ المصروف: {e}")
            else:
                st.warning("يرجى كتابة بيان المصروف.")

    st.markdown("---")
    st.subheader("سجل المصروفات اليومية")
    try:
        exp_data = supabase.table("expenses").select("*").execute().data
        if exp_data:
            st.dataframe(pd.DataFrame(exp_data), use_container_width=True)
        else:
            st.info("لا توجد مصروفات مسجلة حتى الآن.")
    except Exception as ex:
        st.warning(f"ملاحظة: جدول المصروفات غير متاح أو فارغ ({ex})")

# ==========================================
# 10. قسم العمالة والحضور والسُلف
# ==========================================
elif st.session_state.current_screen == 'staff':
    st.markdown("<h4 style='color: #e2c062; text-align: center;'>العمالة والحضور والسُلف</h4>", unsafe_allow_html=True)
    
    with st.form("add_staff_form"):
        st.subheader("تسجيل موظف أو سُلفة جديدة")
        st_name = st.text_input("اسم الموظف")
        st_action = st.selectbox("نوع الحركة", ["حضور", "انصراف", "طلب سُلفة"])
        st_amount = st.number_input("قيمة السُلفة (إن وجدت)", min_value=0.0, value=0.0, step=50.0)
        st_submit = st.form_submit_button("حفظ حركة الموظف")
        if st_submit:
            if st_name:
                try:
                    supabase.table("staff").insert({"staff_name": st_name, "action": st_action, "amount": st_amount}).execute()
                    st.success("تم تسجيل الحركة بنجاح!")
                except Exception as e:
                    st.error(f"خطأ في الحفظ: {e}")
            else:
                st.warning("يرجى إدخال اسم الموظف.")

    st.markdown("---")
    st.subheader("سجل العمالة والحضور")
    try:
        st_data = supabase.table("staff").select("*").execute().data
        if st_data:
            st.dataframe(pd.DataFrame(st_data), use_container_width=True)
        else:
            st.info("لا توجد بيانات مسجلة للعمالة.")
    except Exception as ex:
        st.warning(f"ملاحظة: جدول العمالة غير متاح أو فارغ ({ex})")