import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime

# ==========================================
# 1. تهيئة الصفحة والأنماط البصرية (Custom CSS)
# ==========================================
st.set_page_config(
    page_title="سيستم الاستوديو | Studio Management",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# حقن تصميم CSS فاخر يعكس هوية الاستوديو
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    /* الخلفية والبطاقات */
    .stApp {
        background-color: #0f1117;
        color: #e0e6ed;
    }
    
    /* بطاقات الإحصائيات المخصصة */
    .metric-card {
        background: linear-gradient(135deg, #1e2430 0%, #151922 100%);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: #d4af37;
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-bottom: 8px;
        font-weight: 600;
    }
    .metric-value {
        color: #d4af37;
        font-size: 1.8rem;
        font-weight: 800;
    }
    .metric-subtitle {
        color: #10b981;
        font-size: 0.8rem;
        margin-top: 5px;
    }

    /* أزرار النظام */
    .stButton>button {
        background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%);
        color: #000000 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        width: 100%;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(212, 175, 55, 0.2);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #f3e5ab 0%, #d4af37 100%);
        box-shadow: 0 6px 18px rgba(212, 175, 55, 0.4);
        transform: translateY(-1px);
    }

    /* الجداول */
    .stDataFrame {
        border: 1px solid #2e3646;
        border-radius: 10px;
        overflow: hidden;
    }

    /* تصميم الفاتورة للطباعة */
    .invoice-box {
        max-width: 450px;
        margin: auto;
        padding: 25px;
        border: 2px dashed #d4af37;
        border-radius: 12px;
        background-color: #ffffff;
        color: #000000;
        font-family: 'Cairo', sans-serif;
    }
    .invoice-header {
        text-align: center;
        border-bottom: 2px solid #eee;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    .invoice-title {
        font-size: 20px;
        font-weight: bold;
        color: #111;
    }
    .invoice-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        font-size: 14px;
    }
    .invoice-total {
        border-top: 2px solid #111;
        padding-top: 10px;
        margin-top: 10px;
        font-size: 18px;
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
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.85rem;'>نظام إدارة الحجوزات والحسابات</p>", unsafe_allow_html=True)
    st.divider()
    
    page = st.radio(
        "الانتقال السريع",
        [
            "📊 لوحة التحكم والتقارير",
            "🎟️ حجز تذاكر أفراد",
            "💍 حجوزات الأفراح والسيشن",
            "💸 المصروفات والنفقات",
            "👥 العمالة والسُلف"
        ]
    )
    st.divider()
    st.caption("التاريخ اليوم: " + datetime.now().strftime("%Y-%m-%d"))

# ==========================================
# الصفحة 1: لوحة التحكم والتقارير المالية
# ==========================================
if page == "📊 لوحة التحكم والتقارير":
    st.markdown("<h2 style='color: #d4af37;'>📊 الميزانية والتقارير التحليلية</h2>", unsafe_allow_html=True)
    st.markdown("متابعة تدفقات الإيرادات، المصروفات، وصافي الأرباح في مكان واحد.")
    st.write("")

    try:
        b_res = supabase.table("bookings").select("*").execute().data
        t_res = supabase.table("tickets").select("*").execute().data
        e_res = supabase.table("expenses").select("*").execute().data

        b_df = pd.DataFrame(b_res) if b_res else pd.DataFrame(columns=['paid_amount', 'total_agreed'])
        t_df = pd.DataFrame(t_res) if t_res else pd.DataFrame(columns=['total_price'])
        e_df = pd.DataFrame(e_res) if e_res else pd.DataFrame(columns=['amount', 'category'])

        total_bookings_income = b_df['paid_amount'].sum() if 'paid_amount' in b_df else 0
        total_tickets_income = t_df['total_price'].sum() if 'total_price' in t_df else 0
        total_income = total_bookings_income + total_tickets_income
        total_expenses = e_df['amount'].sum() if 'amount' in e_df else 0
        net_profit = total_income - total_expenses

        # عرض الكروت الإحصائية
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">إجمالي إيراد التذاكر</div>
                <div class="metric-value">{total_tickets_income:,.0f} ج.م</div>
                <div class="metric-subtitle">مبيعات الأفراد</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">إجمالي المقبوضات (حجوزات)</div>
                <div class="metric-value">{total_bookings_income:,.0f} ج.م</div>
                <div class="metric-subtitle">عربونات وعقود</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">إجمالي المصروفات</div>
                <div class="metric-value" style="color: #ef4444;">{total_expenses:,.0f} ج.م</div>
                <div class="metric-subtitle">تشغيل وسُلف</div>
            </div>
            """, unsafe_allow_html=True)
        with c4:
            profit_color = "#10b981" if net_profit >= 0 else "#ef4444"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">صافي الأرباح</div>
                <div class="metric-value" style="color: {profit_color};">{net_profit:,.0f} ج.م</div>
                <div class="metric-subtitle">الرصيد الفعلي</div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # رسم بياني وملخص
        col_chart, col_details = st.columns([1.5, 1])
        
        with col_chart:
            st.subheader("📈 توزيع التدفقات المالية")
            summary_data = pd.DataFrame({
                "البند": ["إيراد التذاكر", "إيراد الحجوزات", "المصروفات العامة"],
                "المبلغ (ج.م)": [total_tickets_income, total_bookings_income, total_expenses]
            }).set_index("البند")
            st.bar_chart(summary_data)

        with col_details:
            st.subheader("📋 ملخص سريع")
            st.write(f"• **عدد الحجوزات المسجلة:** {len(b_df)}")
            st.write(f"• **عدد عمليات قطع التذاكر:** {len(t_df)}")
            st.write(f"• **عدد عمليات الصرف:** {len(e_df)}")

    except Exception as ex:
        st.error(f"حدث خطأ أثناء إعداد التقارير: {ex}")

# ==========================================
# الصفحة 2: قطع تذاكر أفراد + طباعة
# ==========================================
elif page == "🎟️ حجز تذاكر أفراد":
    st.markdown("<h2 style='color: #d4af37;'>🎟️ قطع تذاكر أفراد واصدار إيصال</h2>", unsafe_allow_html=True)
    
    col_form, col_ticket = st.columns([1.2, 1])

    with col_form:
        st.subheader("بيانات التذكرة")
        with st.form("ticket_form", clear_on_submit=False):
            count = st.number_input("عدد الأفراد / التذاكر", min_value=1, value=1, step=1)
            price_per_ticket = st.number_input("سعر التذكرة للفرد (ج.م)", min_value=1, value=50, step=5)
            total_price = count * price_per_ticket
            
            st.markdown(f"### الإجمالي: <span style='color:#d4af37;'>{total_price:,.0f} ج.م</span>", unsafe_allow_html=True)
            
            submit_ticket = st.form_submit_button("🎫 قطع وتأكيد الحفظ")

            if submit_ticket:
                try:
                    supabase.table("tickets").insert({
                        "count": count,
                        "price_per_ticket": price_per_ticket,
                        "total_price": total_price
                    }).execute()
                    st.success("تم تسجيل التذكرة بنجاح في قاعدة البيانات!")
                except Exception as ex:
                    st.error(f"حدث خطأ أثناء الحفظ: {ex}")

    with col_ticket:
        st.subheader("👁️ معاينة كارت التذكرة للطباعة")
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # تصميم التذكرة المطبوعة
        ticket_html = f"""
        <div class="invoice-box">
            <div class="invoice-header">
                <div class="invoice-title">🎬 استوديو التصوير</div>
                <div style="font-size: 12px; color: #666;">تذكرة دخول / سيشن أفراد</div>
            </div>
            <div class="invoice-row"><span>التاريخ والوقت:</span> <strong>{now_str}</strong></div>
            <div class="invoice-row"><span>عدد الأفراد:</span> <strong>{count}</strong></div>
            <div class="invoice-row"><span>سعر الفرد:</span> <strong>{price_per_ticket} ج.م</strong></div>
            <div class="invoice-total invoice-row">
                <span>الإجمالي المدفوع:</span>
                <span>{total_price:,.0f} ج.م</span>
            </div>
            <div style="text-align: center; margin-top: 15px; font-size: 11px; color: #888;">
                أهلاً بكم في الاستوديو - نتمنى لكم جلسة تصوير ممتعة!
            </div>
        </div>
        """
        st.markdown(ticket_html, unsafe_allow_html=True)

    st.divider()
    st.subheader("📋 سجل التذاكر الأخيرة")
    try:
        t_data = supabase.table("tickets").select("*").order("id", desc=True).limit(10).execute().data
        if t_data:
            st.dataframe(pd.DataFrame(t_data), use_container_width=True)
    except Exception as ex:
        st.error(f"خطأ في عرض السجل: {ex}")

# ==========================================
# الصفحة 3: حجوزات الأفراح والسيشن + الطباعة
# ==========================================
elif page == "💍 حجوزات الأفراح والسيشن":
    st.markdown("<h2 style='color: #d4af37;'>💍 إدارة حجوزات السيشن والأفراح</h2>", unsafe_allow_html=True)
    
    tab_new, tab_list = st.tabs(["📝 إضافة حجز جديد وطباعة عقد", "📋 قائمة الحجوزات المسجلة"])

    with tab_new:
        col_input, col_preview = st.columns([1.3, 1])
        
        with col_input:
            with st.form("booking_form", clear_on_submit=False):
                st.subheader("بيانات العريس / العروسة")
                c1, c2 = st.columns(2)
                with c1:
                    client_name = st.text_input("اسم العريس / العروسة")
                    phone = st.text_input("رقم الهاتف")
                    session_type = st.selectbox("نوع الجلسة / القاعة", ["سيشن عادي", "سيشن مميز", "فرح كامل", "فوتوسيشن خارجي"])
                with c2:
                    session_date = st.date_input("تاريخ السيشن")
                    total_agreed = st.number_input("إجمالي قيمة الاتفاق (ج.م)", min_value=0, value=1000, step=100)
                    paid_amount = st.number_input("العربون / المدفوع (ج.م)", min_value=0, value=200, step=50)

                remaining_amount = total_agreed - paid_amount
                st.markdown(f"**المتبقي للتحصيل:** <span style='color:#ef4444; font-weight:bold;'>{remaining_amount:,.0f} ج.م</span>", unsafe_allow_html=True)
                
                notes = st.text_area("ملاحظات إضافية (تفاصيل العرض / المواعيد)")
                save_booking = st.form_submit_button("💾 حفظ الحجز وتأكيد العقد")

                if save_booking:
                    if not client_name:
                        st.warning("يرجى كتابة اسم العميل.")
                    else:
                        try:
                            supabase.table("bookings").insert({
                                "client_name": client_name,
                                "phone": phone,
                                "session_date": str(session_date),
                                "session_type": session_type,
                                "total_agreed": total_agreed,
                                "paid_amount": paid_amount,
                                "notes": notes
                            }).execute()
                            st.success("تم تسجيل الحجز بنجاح!")
                        except Exception as ex:
                            st.error(f"فشل الحفظ: {ex}")

        with col_preview:
            st.subheader("📄 معاينة إيصال الحجز (للطباعة)")
            rem = total_agreed - paid_amount
            receipt_html = f"""
            <div class="invoice-box">
                <div class="invoice-header">
                    <div class="invoice-title">🎬 عقد وحجز سيشن تصوير</div>
                    <div style="font-size: 12px; color: #666;">إيصال استلام عربون</div>
                </div>
                <div class="invoice-row"><span>اسم العميل:</span> <strong>{client_name if client_name else '---'}</strong></div>
                <div class="invoice-row"><span>رقم الهاتف:</span> <strong>{phone if phone else '---'}</strong></div>
                <div class="invoice-row"><span>نوع السيشن:</span> <strong>{session_type}</strong></div>
                <div class="invoice-row"><span>تاريخ السيشن:</span> <strong>{session_date}</strong></div>
                <hr style="border:0.5px solid #eee; margin:10px 0;">
                <div class="invoice-row"><span>إجمالي الاتفاق:</span> <strong>{total_agreed:,.0f} ج.م</strong></div>
                <div class="invoice-row"><span>العربون المدفوع:</span> <strong style="color:green;">{paid_amount:,.0f} ج.م</strong></div>
                <div class="invoice-total invoice-row">
                    <span>المتبقي عند التسليم:</span>
                    <span style="color:red;">{rem:,.0f} ج.م</span>
                </div>
                <div style="text-align: center; margin-top: 15px; font-size: 10px; color: #777;">
                    * الملاحظات: {notes if notes else 'لا يوجد'}
                </div>
            </div>
            """
            st.markdown(receipt_html, unsafe_allow_html=True)

    with tab_list:
        try:
            b_list = supabase.table("bookings").select("*").order("id", desc=True).execute().data
            if b_list:
                df_b = pd.DataFrame(b_list)
                if 'total_agreed' in df_b and 'paid_amount' in df_b:
                    df_b['المتبقي'] = df_b['total_agreed'] - df_b['paid_amount']
                st.dataframe(df_b, use_container_width=True)
            else:
                st.info("لا توجد حجوزات مسجلة حالياً.")
        except Exception as ex:
            st.error(f"خطأ في التحميل: {ex}")

# ==========================================
# الصفحة 4: المصروفات العامة
# ==========================================
elif page == "💸 المصروفات والنفقات":
    st.markdown("<h2 style='color: #d4af37;'>💸 تسجيل المصروفات والتكاليف</h2>", unsafe_allow_html=True)
    
    col_exp_form, col_exp_list = st.columns([1, 1.3])

    with col_exp_form:
        st.subheader("إضافة إيصال صرف")
        with st.form("expense_form", clear_on_submit=True):
            category = st.selectbox("نوع بند المصروف", ["إيجار القاعة/الاستوديو", "كهرباء ومرافق", "صيانة ومعدات تصوير", "بوفيه وضيافة", "دعاية وتسويق", "مصروفات نثرية"])
            amount = st.number_input("المبلغ (ج.م)", min_value=1, value=50, step=10)
            description = st.text_area("تفاصيل المصروف")
            
            submit_exp = st.form_submit_button("💸 تسجيل الصرف")
            if submit_exp:
                try:
                    supabase.table("expenses").insert({
                        "category": category,
                        "amount": amount,
                        "description": description
                    }).execute()
                    st.success("تم تسجيل المصروف بنجاح!")
                    st.rerun()
                except Exception as ex:
                    st.error(f"حدث خطأ أثناء حفظ المصروف: {ex}")

    with col_exp_list:
        st.subheader("📋 سجل النفقات والمصروفات")
        try:
            e_list = supabase.table("expenses").select("*").order("id", desc=True).execute().data
            if e_list:
                st.dataframe(pd.DataFrame(e_list), use_container_width=True)
            else:
                st.info("لم يتم تسجيل أي مصروفات بعد.")
        except Exception as ex:
            st.error(f"خطأ أثناء التحميل: {ex}")

# ==========================================
# الصفحة 5: شؤون الموظفين والسُلف
# ==========================================
elif page == "👥 العمالة والسُلف":
    st.markdown("<h2 style='color: #d4af37;'>👥 إدارة طاقم العمل والسُلف</h2>", unsafe_allow_html=True)
    
    tab_emp1, tab_emp2 = st.tabs(["➕ إضافة موظف جديد", "💵 تسجيل سُلفة مالية"])

    with tab_emp1:
        col1, col2 = st.columns(2)
        with col1:
            emp_name = st.text_input("اسم الموظف / المصور")
            emp_role = st.text_input("الوظيفة (مثال: مصور، مساعد، ميك أب أرتست)")
            daily_rate = st.number_input("الراتب / اليومية (ج.م)", min_value=0, value=150)
            
            if st.button("حفظ بيانات الموظف"):
                if emp_name:
                    try:
                        supabase.table("employees").insert({
                            "name": emp_name,
                            "role": emp_role,
                            "daily_rate": daily_rate
                        }).execute()
                        st.success("تمت إضافة الموظف بنجاح!")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"فشل الحفظ: {ex}")

    with tab_emp2:
        try:
            employees = supabase.table("employees").select("*").execute().data
            if employees:
                emp_names = [e["name"] for e in employees]
                selected_emp = st.selectbox("اختر الموظف", emp_names)
                advance_amount = st.number_input("مبلغ السُلفة (ج.م)", min_value=10, value=100, step=50)
                
                if st.button("تسجيل وخصم السُلفة"):
                    # تسجل كبند مصروفات أيضاً لتؤثر في الخزينة
                    supabase.table("expenses").insert({
                        "category": f"سُلفة - {selected_emp}",
                        "amount": advance_amount,
                        "description": f"سُلفة شخصية للموظف {selected_emp}"
                    }).execute()
                    st.success(f"تم تسجيل سُلفة بقيمة {advance_amount} ج.م للموظف {selected_emp}")
            else:
                st.info("يرجى إضافة موظفين أولاً قبل تسجيل السُلف.")
        except Exception as ex:
            st.error(f"خطأ أثناء تحميل الموظفين: {ex}")
