import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, time

# ==========================================
# 1. تهيئة الصفحة والأنماط البصرية (Custom CSS)
# ==========================================
st.set_page_config(
    page_title="سيستم الاستوديو | Studio Management",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .stApp {
        background-color: #0f1117;
        color: #e0e6ed;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e2430 0%, #151922 100%);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 6px;
        font-weight: 600;
    }
    .metric-value {
        color: #d4af37;
        font-size: 1.7rem;
        font-weight: 800;
    }

    .stButton>button {
        background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%);
        color: #000000 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        width: 100%;
    }
    
    .invoice-box {
        max-width: 450px;
        margin: auto;
        padding: 20px;
        border: 2px dashed #d4af37;
        border-radius: 12px;
        background-color: #ffffff;
        color: #000000;
        font-family: 'Cairo', sans-serif;
    }
    .invoice-header {
        text-align: center;
        border-bottom: 2px solid #eee;
        padding-bottom: 8px;
        margin-bottom: 12px;
    }
    .invoice-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 6px;
        font-size: 13px;
    }
    .invoice-total {
        border-top: 2px solid #111;
        padding-top: 8px;
        margin-top: 8px;
        font-size: 16px;
        font-weight: bold;
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
# 3. القائمة الجانبية الهيكلية
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #d4af37;'>🎬 سيستم الاستوديو</h2>", unsafe_allow_html=True)
    st.divider()
    
    page = st.radio(
        "الانتقال السريع",
        [
            "📊 لوحة التحكم والتقارير",
            "💍 حجوزات الأفراح والمواعيد",
            "🎟️ حجز تذاكر أفراد",
            "📷 عهدة ومعدات التصوير",
            "💸 المصروفات والنفقات",
            "👥 العمالة والسُلف"
        ]
    )
    st.divider()
    st.caption("تاريخ اليوم: " + datetime.now().strftime("%Y-%m-%d"))

# ==========================================
# الصفحة 1: لوحة التحكم والتقارير المالية
# ==========================================
if page == "📊 لوحة التحكم والتقارير":
    st.markdown("<h2 style='color: #d4af37;'>📊 الميزانية والتقارير التحليلية</h2>", unsafe_allow_html=True)
    
    try:
        b_res = supabase.table("bookings").select("*").execute().data
        t_res = supabase.table("tickets").select("*").execute().data
        e_res = supabase.table("expenses").select("*").execute().data

        b_df = pd.DataFrame(b_res) if b_res else pd.DataFrame()
        t_df = pd.DataFrame(t_res) if t_res else pd.DataFrame()
        e_df = pd.DataFrame(e_res) if e_res else pd.DataFrame()

        total_bookings_income = b_df['paid_amount'].sum() if not b_df.empty and 'paid_amount' in b_df else 0
        total_tickets_income = t_df['total_price'].sum() if not t_df.empty and 'total_price' in t_df else 0
        
        # مجموع عمولات المصورين المسجلة في الحجوزات
        photographer_comm = b_df['photographer_commission'].sum() if not b_df.empty and 'photographer_commission' in b_df else 0
        
        total_income = total_bookings_income + total_tickets_income
        total_expenses = (e_df['amount'].sum() if not e_df.empty and 'amount' in e_df else 0) + photographer_comm
        net_profit = total_income - total_expenses

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="metric-card"><div class="metric-title">إيراد التذاكر</div><div class="metric-value">{total_tickets_income:,.0f} ج.م</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><div class="metric-title">مقبوضات الحجوزات</div><div class="metric-value">{total_bookings_income:,.0f} ج.م</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card"><div class="metric-title">إجمالي المصروفات + العمولة</div><div class="metric-value" style="color:#ef4444;">{total_expenses:,.0f} ج.م</div></div>', unsafe_allow_html=True)
        with c4:
            p_color = "#10b981" if net_profit >= 0 else "#ef4444"
            st.markdown(f'<div class="metric-card"><div class="metric-title">صافي الربح الفعلي</div><div class="metric-value" style="color:{p_color};">{net_profit:,.0f} ج.م</div></div>', unsafe_allow_html=True)

        st.divider()
        st.subheader("📈 الرسم البياني المالي")
        chart_df = pd.DataFrame({
            "البند": ["إيراد تذاكر", "إيراد حجوزات", "مصروفات وعمولات"],
            "المبلغ": [total_tickets_income, total_bookings_income, total_expenses]
        }).set_index("البند")
        st.bar_chart(chart_df)

    except Exception as ex:
        st.error(f"خطأ في إعداد التقارير: {ex}")

# ==========================================
# الصفحة 2: حجوزات الأفراح والمواعيد (مع فحص التضارب)
# ==========================================
elif page == "💍 حجوزات الأفراح والمواعيد":
    st.markdown("<h2 style='color: #d4af37;'>💍 إدارة الحجوزات والمواعيد واللوكيشنز</h2>", unsafe_allow_html=True)
    
    tab_new, tab_calendar = st.tabs(["📝 حجز جديد وتحديد اللوكيشن", "📋 جدول الحجوزات اليومية"])

    with tab_new:
        col_input, col_preview = st.columns([1.3, 1])
        
        with col_input:
            st.subheader("تفاصيل الحجز والوقت")
            
            client_name = st.text_input("اسم العريس / العروسة")
            phone = st.text_input("رقم الهاتف")
            
            # العروض والباقات
            session_type = st.selectbox(
                "اختر الباقة / نوع الجلسة", 
                ["سيشن عادي (300 ج.م)", "سيشن مميز (600 ج.م)", "باقة الفرح الكامل (1500 ج.م)", "فوتوسيشن خارجي (800 ج.م)", "تخصيص يدوي"]
            )
            
            c1, c2 = st.columns(2)
            with c1:
                session_date = st.date_input("تاريخ السيشن")
                start_t = st.time_input("وقت البداية", value=time(15, 0))
                location_room = st.selectbox("اللوكيشن / الغرفة المطلوبة", ["اللوكيشن الكلاسيك", "اللوكيشن المودرن", "غرفة الميك أب والتجهيز", "الاستوديو بالكامل"])
            with c2:
                end_t = st.time_input("وقت النهاية المتوقع", value=time(16, 0))
                total_agreed = st.number_input("إجمالي قيمة الاتفاق (ج.م)", min_value=0, value=600, step=50)
                paid_amount = st.number_input("العربون المدفوع (ج.م)", min_value=0, value=200, step=50)

            photographer_commission = st.number_input("عمولة / إكرامية المصور (إن وجد)", min_value=0, value=0, step=50, help="تكتب يدوياً في حال كان العريس جلب مصوراً أو تم تخصيص عمولة له")
            notes = st.text_area("ملاحظات إضافية")

            # --- فحص تضارب المواعيد (Slot Collision Check) ---
            collision_found = False
            try:
                # جلب حجوزات نفس اليوم والنفس اللوكيشن
                existing_b = supabase.table("bookings").select("*").eq("session_date", str(session_date)).eq("location_room", location_room).execute().data
                if existing_b:
                    for b in existing_b:
                        if b.get("start_time") and b.get("end_time"):
                            # تحويل النصوص إلى أوقات للمقارنة
                            b_start = datetime.strptime(b["start_time"], "%H:%M:%S").time() if len(b["start_time"])==8 else datetime.strptime(b["start_time"], "%H:%M").time()
                            b_end = datetime.strptime(b["end_time"], "%H:%M:%S").time() if len(b["end_time"])==8 else datetime.strptime(b["end_time"], "%H:%M").time()
                            
                            # شرط التداخل في الوقت
                            if (start_t < b_end) and (end_t > b_start):
                                collision_found = True
                                st.error(f"⚠️ تنبيه تضارب: {location_room} محجوز بالفعل في هذا الوقت للعميل ({b['client_name']}) من {b_start.strftime('%H:%M')} إلى {b_end.strftime('%H:%M')}!")
            except Exception as ex:
                pass

            if st.button("💾 تأكيد وحفظ الحجز"):
                if not client_name:
                    st.warning("يرجى إدخال اسم العميل.")
                elif collision_found:
                    st.error("لا يمكن الحفظ بسبب تضارب الموعد في نفس اللوكيشن!")
                else:
                    try:
                        supabase.table("bookings").insert({
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
                        }).execute()
                        st.success("تم تأكيد الحجز وحفظ الموعد بنجاح!")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"حدث خطأ أثناء الحفظ: {ex}")

        with col_preview:
            st.subheader("📄 معاينة العقد والإيصال")
            rem = total_agreed - paid_amount
            receipt_html = f"""
            <div class="invoice-box">
                <div class="invoice-header">
                    <div class="invoice-title">🎬 عقد وحجز استوديو</div>
                    <div style="font-size: 11px; color: #666;">إيصال حجز ولوكيشن</div>
                </div>
                <div class="invoice-row"><span>العميل:</span> <strong>{client_name if client_name else '---'}</strong></div>
                <div class="invoice-row"><span>الهاتف:</span> <strong>{phone if phone else '---'}</strong></div>
                <div class="invoice-row"><span>الباقة:</span> <strong>{session_type}</strong></div>
                <div class="invoice-row"><span>اللوكيشن:</span> <strong>{location_room}</strong></div>
                <div class="invoice-row"><span>التاريخ:</span> <strong>{session_date}</strong></div>
                <div class="invoice-row"><span>الوقت:</span> <strong>من {start_t.strftime('%H:%M')} إلى {end_t.strftime('%H:%M')}</strong></div>
                <hr style="border:0.5px solid #eee; margin:8px 0;">
                <div class="invoice-row"><span>إجمالي الاتفاق:</span> <strong>{total_agreed:,.0f} ج.م</strong></div>
                <div class="invoice-row"><span>المدفوع (العربون):</span> <strong style="color:green;">{paid_amount:,.0f} ج.م</strong></div>
                <div class="invoice-total invoice-row">
                    <span>المتبقي عند الحضور:</span>
                    <span style="color:red;">{rem:,.0f} ج.م</span>
                </div>
            </div>
            """
            st.markdown(receipt_html, unsafe_allow_html=True)

    with tab_calendar:
        st.subheader("📋 قائمة الحجوزات")
        try:
            b_list = supabase.table("bookings").select("*").order("id", desc=True).execute().data
            if b_list:
                df_b = pd.DataFrame(b_list)
                st.dataframe(df_b, use_container_width=True)
            else:
                st.info("لا توجد حجوزات مسجلة حالياً.")
        except Exception as ex:
            st.error(f"خطأ في التحميل: {ex}")

# ==========================================
# الصفحة 3: عهدة ومعدات التصوير
# ==========================================
elif page == "📷 عهدة ومعدات التصوير":
    st.markdown("<h2 style='color: #d4af37;'>📷 تتبع عهدة ومعدات التصوير</h2>", unsafe_allow_html=True)
    
    col_eq1, col_eq2 = st.columns([1, 1.2])

    with col_eq1:
        st.subheader("إضافة معدة جديدة")
        with st.form("eq_form", clear_on_submit=True):
            eq_name = st.text_input("اسم المعدة (مثال: كاميرا Sony A7III)")
            eq_cat = st.selectbox("النوع", ["كاميرات", "عدسات", "إضاءات وكشافات", "صوتيات وميكروفونات", "إكسسوارات وحوامل"])
            
            if st.form_submit_button("حفظ في العهدة"):
                if eq_name:
                    try:
                        supabase.table("equipment").insert({
                            "name": eq_name,
                            "category": eq_cat,
                            "status": "متاحة بالاستوديو"
                        }).execute()
                        st.success("تمت إضافة المعدة للعهدة!")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"خطأ أثناء الحفظ: {ex}")

    with col_eq2:
        st.subheader("تحديث حالة المعدة (خروج / عودة)")
        try:
            eq_data = supabase.table("equipment").select("*").execute().data
            if eq_data:
                eq_df = pd.DataFrame(eq_data)
                selected_eq_id = st.selectbox("اختر المعدة", eq_df["id"].tolist(), format_func=lambda x: eq_df[eq_df['id']==x]['name'].values[0])
                
                status_choice = st.radio("الحالة الحالية", ["متاحة بالاستوديو", "خارجة لسيشن خارجي", "تحت الصيانة"])
                assigned_to = st.text_input("اسم المصور المستلم (في حال الخروج)")
                expected_return = st.text_input("موعد العودة المتوقع")

                if st.button("تحديث حالة العهدة"):
                    supabase.table("equipment").update({
                        "status": status_choice,
                        "assigned_to": assigned_to if status_choice == "خارجة لسيشن خارجي" else "",
                        "expected_return": expected_return if status_choice == "خارجة لسيشن خارجي" else ""
                    }).eq("id", selected_eq_id).execute()
                    st.success("تم تحديث حالة المعدة بنجاح!")
                    st.rerun()

                st.divider()
                st.dataframe(eq_df[['name', 'category', 'status', 'assigned_to', 'expected_return']], use_container_width=True)
            else:
                st.info("لا توجد معدات مسجلة بعد.")
        except Exception as ex:
            st.error(f"خطأ أثناء التحميل: {ex}")

# ==========================================
# الصفحة 4: حجز تذاكر أفراد
# ==========================================
elif page == "🎟️ حجز تذاكر أفراد":
    st.markdown("<h2 style='color: #d4af37;'>🎟️ قطع تذاكر أفراد</h2>", unsafe_allow_html=True)
    count = st.number_input("عدد الأفراد", min_value=1, value=1)
    price_per_ticket = st.number_input("سعر التذكرة (ج.م)", min_value=1, value=50)
    total_price = count * price_per_ticket
    st.markdown(f"### الإجمالي: {total_price:,.0f} ج.م")
    
    if st.button("🎫 حفظ وقطع التذكرة"):
        try:
            supabase.table("tickets").insert({
                "count": count,
                "price_per_ticket": price_per_ticket,
                "total_price": total_price
            }).execute()
            st.success("تم تسجيل التذكرة بنجاح!")
        except Exception as ex:
            st.error(f"خطأ: {ex}")

# ==========================================
# الصفحة 5: المصروفات العامة
# ==========================================
elif page == "💸 المصروفات والنفقات":
    st.markdown("<h2 style='color: #d4af37;'>💸 تسجيل المصروفات والتكاليف</h2>", unsafe_allow_html=True)
    with st.form("exp_form", clear_on_submit=True):
        category = st.selectbox("بند المصروف", ["إيجار", "كهرباء ومرافق", "مشتريات كافيه وبضاعة", "صيانة", "نثريات"])
        amount = st.number_input("المبلغ (ج.م)", min_value=1, value=50)
        description = st.text_area("تفاصيل المصروف")
        if st.form_submit_button("تسجيل الصرف"):
            try:
                supabase.table("expenses").insert({
                    "category": category,
                    "amount": amount,
                    "description": description
                }).execute()
                st.success("تم تسجيل المصروف بنجاح!")
            except Exception as ex:
                st.error(f"خطأ: {ex}")

# ==========================================
# الصفحة 6: شؤون الموظفين والسُلف
# ==========================================
elif page == "👥 العمالة والسُلف":
    st.markdown("<h2 style='color: #d4af37;'>👥 إدارة طاقم العمل والسُلف</h2>", unsafe_allow_html=True)
    emp_name = st.text_input("اسم الموظف / المصور")
    emp_role = st.text_input("الوظيفة")
    daily_rate = st.number_input("الراتب / اليومية", min_value=0, value=150)
    if st.button("حفظ الموظف"):
        if emp_name:
            try:
                supabase.table("employees").insert({"name": emp_name, "role": emp_role, "daily_rate": daily_rate}).execute()
                st.success("تمت إضافة الموظف!")
            except Exception as ex:
                st.error(f"خطأ: {ex}")
