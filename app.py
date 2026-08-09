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

# تهيئة متغيرات الجلسة (Session State)
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
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* شريط الرأس المعنون والموسع في منتصف الصفحة */
    .pos-header-center {
        background: linear-gradient(135deg, #141824 0%, #0d1017 100%);
        border: 2px solid #d4af37;
        padding: 20px;
        border-radius: 16px;
        margin: 0 auto 30px auto;
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

    /* بطاقات الأحصائيات */
    .stat-card {
        background: #141824;
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .stat-val {
        font-size: 24px;
        font-weight: 900;
        color: #d4af37;
    }
    .stat-lbl {
        font-size: 12px;
        color: #94a3b8;
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
# 3. الهيدر العلوي الموحد والمستهدف في منتصف الصفحة
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
            <div class="pos-card-title">حجز سيشن وتقويم المواعيد</div>
            <div class="pos-card-desc">إضافة حجز جديد، طباعة العقد، وتتبع تقويم الأيام</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("دخول قسم الحجوزات", key="btn_nav_bookings"):
            st.session_state.current_screen = 'bookings'
            st.rerun()

    with row1_2:
        st.markdown("""
        <div class="pos-card-button">
            <div class="pos-card-title">قطع تذاكر الأفراد</div>
            <div class="pos-card-desc">إصدار تذاكر الدخول الفورية وطباعة الإيصال فوراً</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("دخول كاشير التذاكر", key="btn_nav_tickets"):
            st.session_state.current_screen = 'tickets'
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    # الصف الثاني: باقي الخدمات والأقسام الفرعية
    row2_1, row2_2, row2_3, row2_4 = st.columns(4)
    
    with row2_1:
        st.markdown("""
        <div class="pos-card-button">
            <div class="pos-card-title">التقارير والميزانية</div>
            <div class="pos-card-desc">الحسابات والربحية</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("التقارير", key="btn_nav_reports"):
            st.session_state.current_screen = 'reports'
            st.rerun()

    with row2_2:
        st.markdown("""
        <div class="pos-card-button">
            <div class="pos-card-title">إدارة العهدة والمعدات</div>
            <div class="pos-card-desc">تسليم واستلام المعدات</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("العهدة", key="btn_nav_equip"):
            st.session_state.current_screen = 'equip'
            st.rerun()

    with row2_3:
        st.markdown("""
        <div class="pos-card-button">
            <div class="pos-card-title">المصروفات والنفقات</div>
            <div class="pos-card-desc">تسجيل المصاريف الإدارية</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("المصروفات", key="btn_nav_expenses"):
            st.session_state.current_screen = 'expenses'
            st.rerun()

    with row2_4:
        st.markdown("""
        <div class="pos-card-button">
            <div class="pos-card-title">العمالة والحضور والسُلف</div>
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
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>قطع تذاكر دخول الأفراد</h3>", unsafe_allow_html=True)
    
    col_in, col_print = st.columns([1.1, 1])
    
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
                    st.success("تم الحفظ بنجاح! جاري طلب الطباعة...")
                    st.markdown("<script>window.print();</script>", unsafe_allow_html=True)
                except Exception as ex:
                    st.error(f"خطأ في العملية: {ex}")

        with btn_c2:
            if st.button("إعادة طباعة آخر تذكرة"):
                if st.session_state.last_ticket:
                    st.info("جاري إعادة طباعة آخر تذكرة دون تسجيلها مجدداً...")
                    st.markdown("<script>window.print();</script>", unsafe_allow_html=True)
                else:
                    st.warning("لا توجد تذكرة سابقة مسجلة في الجلسة لإعادة طباعتها.")

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
        col_b_input, col_b_print = st.columns([1.2, 1])
        
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
                if st.button("تأكيد وحفظ العقد وطباعة"):
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
                if st.button("إعادة طباعة العقد الحالي"):
                    if st.session_state.last_booking:
                        st.info("جاري إعادة طباعة العقد الأخير...")
                        st.markdown("<script>window.print();</script>", unsafe_allow_html=True)
                    else:
                        st.warning("لا يوجد عقد محجوز مؤخراً لإعادة طباعته.")

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
                st.success(f"يوجد عدد ({len(day_bookings)}) سيشن محجوز يوم {search_date}:")
                for idx, b in enumerate(day_bookings, 1):
                    s_t = str(b.get('start_time', ''))[:5]
                    e_t = str(b.get('end_time', ''))[:5]
                    with st.expander(f"سيشن {idx}: {b.get('client_name')} | من {s_t} إلى {e_t} ({b.get('location_room')})"):
                        st.write(f"**الهاتف:** {b.get('phone', '-')}")
                        st.write(f"**الاتفاق:** {b.get('total_agreed', 0)} ج.م | **المدفوع:** {b.get('paid_amount', 0)} ج.م")
            else:
                st.info(f"يوم {search_date} لا توجد به أي حجوزات حتى الآن.")
        except Exception as ex:
            st.error(f"خطأ أثناء التحميل: {ex}")

    with tab_list:
        try:
            b_list = supabase.table("bookings").select("*").execute().data
            if b_list:
                st.dataframe(pd.DataFrame(b_list), use_container_width=True)
            else:
                st.info("لا توجد حجوزات.")
        except Exception as ex:
            st.error(f"خطأ: {ex}")

# ==========================================
# 7. قسم العمالة والحضور والغياب والسُلف (مُحدث بالكامل)
# ==========================================
elif st.session_state.current_screen == 'staff':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>إدارة طاقم العمل والسُلف والحضور</h3>", unsafe_allow_html=True)
    
    tab_att, tab_advance, tab_emp = st.tabs(["📝 الحضور والغياب اليومي", "💸 تسجيل السُلف والخصومات", "👥 إضافة وإدارة الموظفين"])

    # تبويب الحضور والغياب
    with tab_att:
        st.subheader("تسجيل الحضور والغياب اليومي")
        att_date = st.date_input("تاريخ اليوم", value=date.today(), key="att_date")
        
        try:
            emp_data = supabase.table("employees").select("*").execute().data
            if emp_data:
                emp_df = pd.DataFrame(emp_data)
                
                with st.form("attendance_form"):
                    st.write("حدد حالة كل موظف لهذا اليوم:")
                    attendance_records = {}
                    
                    for idx, row in emp_df.iterrows():
                        c_emp, c_status = st.columns([2, 2])
                        c_emp.write(f"**{row['name']}** ({row.get('role', 'موظف')})")
                        status = c_status.radio(
                            f"الحالة لـ {row['name']}",
                            ["حاضر", "غائب", "إجازة"],
                            horizontal=True,
                            key=f"att_{row['id']}"
                        )
                        attendance_records[row['id']] = status
                    
                    if st.form_submit_button("حفظ الحضور والغياب"):
                        for emp_id, st_val in attendance_records.items():
                            supabase.table("attendance").insert({
                                "employee_id": emp_id,
                                "date": str(att_date),
                                "status": st_val
                            }).execute()
                        st.success("تم تسجيل الحضور والغياب بنجاح!")
            else:
                st.info("يرجى إضافة موظفين أولاً في تبويب 'إضافة وإدارة الموظفين'.")
        except Exception as ex:
            st.error(f"خطأ أثناء تحميل بيانات الموظفين أو الحضور: {ex}")

    # تبويب السُلف والخصومات
    with tab_advance:
        st.subheader("تسجيل سُلفة أو خصم مالية")
        try:
            emp_data = supabase.table("employees").select("*").execute().data
            if emp_data:
                emp_df = pd.DataFrame(emp_data)
                selected_emp_id = st.selectbox("اختر الموظف", emp_df["id"].tolist(), format_func=lambda x: emp_df[emp_df['id']==x]['name'].values[0], key="adv_emp_select")
                
                adv_amount = st.number_input("المبلغ (ج.م)", min_value=1, value=100, step=50, key="adv_amt")
                adv_type = st.selectbox("النوع", ["سُلفة مقدماً", "خصم إداري", "مكافأة"], key="adv_type")
                adv_notes = st.text_area("سبب السُلفة / الخصم", key="adv_notes")
                
                if st.button("حفظ العملية المالـية"):
                    supabase.table("expenses").insert({
                        "category": f"سُلفة/خصم - موظف ID: {selected_emp_id}",
                        "amount": adv_amount if adv_type != "مكافأة" else -adv_amount,
                        "description": f"{adv_type}: {adv_notes}"
                    }).execute()
                    st.success("تم تسجيل المبلغ بنجاح!")
            else:
                st.info("لا يوجد موظفون مسجلون.")
        except Exception as ex:
            st.error(f"خطأ: {ex}")

    # تبويب إضافة الموظفين
    with tab_emp:
        st.subheader("إضافة موظف جديد")
        emp_n = st.text_input("اسم الموظف / المصور", key="add_emp_name")
        emp_r = st.text_input("الوظيفة", key="add_emp_role")
        daily_rate = st.number_input("الراتب / اليومية (ج.م)", min_value=0, value=150, key="add_emp_rate")
        
        if st.button("حفظ الموظف الجديد"):
            if emp_n:
                try:
                    supabase.table("employees").insert({"name": emp_n, "role": emp_r, "daily_rate": daily_rate}).execute()
                    st.success("تمت إضافة الموظف بنجاح!")
                    st.rerun()
                except Exception as ex:
                    st.error(f"خطأ: {ex}")

# ==========================================
# 8. قسم التقارير المالي والميزانية
# ==========================================
elif st.session_state.current_screen == 'reports':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>التقارير والميزانية المالية</h3>", unsafe_allow_html=True)
    try:
        b_res = supabase.table("bookings").select("*").execute().data
        t_res = supabase.table("tickets").select("*").execute().data
        e_res = supabase.table("expenses").select("*").execute().data

        b_df = pd.DataFrame(b_res) if b_res else pd.DataFrame()
        t_df = pd.DataFrame(t_res) if t_res else pd.DataFrame()
        e_df = pd.DataFrame(e_res) if e_res else pd.DataFrame()

        t_inc = t_df['total_price'].sum() if not t_df.empty and 'total_price' in t_df else 0
        b_inc = b_df['paid_amount'].sum() if not b_df.empty and 'paid_amount' in b_df else 0
        exp_val = e_df['amount'].sum() if not e_df.empty and 'amount' in e_df else 0
        net_profit = (t_inc + b_inc) - exp_val

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="stat-card"><div class="stat-val">{t_inc:,.0f}</div><div class="stat-lbl">إيراد التذاكر (ج.م)</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="stat-card"><div class="stat-val">{b_inc:,.0f}</div><div class="stat-lbl">مقبوضات الحجوزات (ج.م)</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#ef4444;">{exp_val:,.0f}</div><div class="stat-lbl">المصروفات (ج.م)</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#10b981;">{net_profit:,.0f}</div><div class="stat-lbl">صافي الربح (ج.م)</div></div>', unsafe_allow_html=True)
    except Exception as ex:
        st.error(f"خطأ في إعداد التقارير: {ex}")

# ==========================================
# 9. قسم العهدة والمصروفات
# ==========================================
elif st.session_state.current_screen == 'equip':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>إدارة عهدة ومعدات التصوير</h3>", unsafe_allow_html=True)
    with st.form("eq_add"):
        eq_name = st.text_input("اسم المعدة")
        eq_cat = st.selectbox("النوع", ["كاميرات", "عدسات", "إضاءات", "صوتيات", "إكسسوارات"])
        if st.form_submit_button("إضافة للعهدة"):
            if eq_name:
                supabase.table("equipment").insert({"name": eq_name, "category": eq_cat, "status": "متاحة"}).execute()
                st.success("تم الحفظ!")
                st.rerun()

elif st.session_state.current_screen == 'expenses':
    st.markdown("<h3 style='color: #d4af37; text-align: center;'>المصروفات والنفقات</h3>", unsafe_allow_html=True)
    with st.form("exp_add"):
        cat = st.selectbox("البند", ["إيجار", "مرافق", "مشتريات", "صيانة", "نثريات"])
        amt = st.number_input("المبلغ", min_value=1, value=50)
        desc = st.text_area("التفاصيل")
        if st.form_submit_button("تسجيل المصروف"):
            supabase.table("expenses").insert({"category": cat, "amount": amt, "description": desc}).execute()
            st.success("تم التسجيل!")
